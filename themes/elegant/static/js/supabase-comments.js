(() => {
  function el(tagName, attrs = {}, text) {
    const node = document.createElement(tagName);
    for (const [key, value] of Object.entries(attrs)) {
      if (value === undefined || value === null) continue;
      if (key === "class") node.className = value;
      else if (key.startsWith("data-")) node.setAttribute(key, value);
      else if (key === "text") node.textContent = value;
      else node.setAttribute(key, value);
    }
    if (text !== undefined) node.textContent = text;
    return node;
  }

  function formatDate(value) {
    try {
      const date = new Date(value);
      if (Number.isNaN(date.getTime())) return "";
      return new Intl.DateTimeFormat(undefined, {
        year: "numeric",
        month: "short",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit"
      }).format(date);
    } catch (err) {
      return "";
    }
  }

  function setStatus(container, message, kind = "info") {
    const status = container.querySelector("[data-sb-comments-status]");
    if (!status) return;
    status.textContent = message || "";
    status.dataset.kind = kind;
  }

  function renderComment(comment) {
    const wrapper = el("div", { class: "sb-comment" });
    const meta = el("div", { class: "sb-comment__meta" });
    const name = comment?.author_name?.trim() || "Anonymous";
    const when = formatDate(comment?.created_at);
    meta.textContent = when ? `${name} · ${when}` : name;

    const body = el("div", { class: "sb-comment__body" });
    body.textContent = comment?.body || "";

    wrapper.appendChild(meta);
    wrapper.appendChild(body);
    return wrapper;
  }

  async function loadComments({
    container,
    endpoint,
    headers,
    threadId,
    requireApproval
  }) {
    const list = container.querySelector("[data-sb-comments-list]");
    const count = container.querySelector("[data-sb-comments-count]");
    if (!list) return;

    setStatus(container, "Loading comments…", "info");

    const url = new URL(endpoint);
    url.searchParams.set("select", "id,author_name,body,created_at");
    url.searchParams.set("thread_id", `eq.${threadId}`);
    url.searchParams.set("is_approved", "eq.true");
    url.searchParams.set("order", "created_at.asc");
    url.searchParams.set("limit", "100");

    try {
      const res = await fetch(url.toString(), { headers });
      if (!res.ok) {
        const text = await res.text().catch(() => "");
        throw new Error(`Supabase error ${res.status}${text ? `: ${text}` : ""}`);
      }
      const comments = await res.json();
      list.innerHTML = "";

      if (!Array.isArray(comments) || comments.length === 0) {
        if (count) count.textContent = "0";
        list.appendChild(el("p", { class: "sb-comments__empty" }, "No comments yet."));
        setStatus(
          container,
          requireApproval
            ? "Comments appear after approval."
            : "Be the first to comment.",
          "muted"
        );
        return;
      }

      if (count) count.textContent = String(comments.length);
      for (const comment of comments) list.appendChild(renderComment(comment));
      setStatus(container, "", "muted");
    } catch (err) {
      setStatus(
        container,
        "Couldn’t load comments. Please try again later.",
        "error"
      );
      console.error("[supabase-comments] load failed", err);
      if (count) count.textContent = "—";
      list.innerHTML = "";
    }
  }

  async function submitComment({
    container,
    endpoint,
    headers,
    threadId,
    authorName,
    body,
    requireApproval
  }) {
    setStatus(container, "Submitting…", "info");

    const payload = [
      {
        thread_id: threadId,
        author_name: authorName,
        body
      },
    ];

    const res = await fetch(endpoint, {
      method: "POST",
      headers: {
        ...headers,
        "Content-Type": "application/json",
        Prefer: "return=minimal"
      },
      body: JSON.stringify(payload)
    });

    if (!res.ok) {
      const text = await res.text().catch(() => "");
      throw new Error(`Supabase error ${res.status}${text ? `: ${text}` : ""}`);
    }

    setStatus(
      container,
      requireApproval
        ? "Thanks! Your comment is awaiting approval."
        : "Thanks! Your comment was posted.",
      "success"
    );
  }

  function initOne(container) {
    const supabaseUrl = (container.dataset.supabaseUrl || "").trim();
    const supabaseAnonKey = (container.dataset.supabaseAnonKey || "").trim();
    const table = (container.dataset.supabaseTable || "comments").trim();
    const threadId = (container.dataset.threadId || "").trim();
    const requireApproval = (container.dataset.requireApproval || "true")
      .toLowerCase()
      .trim();

    const requireApprovalBool = !["0", "false", "no", "off"].includes(
      requireApproval
    );

    if (!supabaseUrl || !supabaseAnonKey || !threadId) return;

    const base = supabaseUrl.replace(/\/+$/, "");
    const endpoint = `${base}/rest/v1/${encodeURIComponent(table)}`;

    const headers = {
      apikey: supabaseAnonKey,
      Authorization: `Bearer ${supabaseAnonKey}`,
      Accept: "application/json"
    };

    const form = container.querySelector("form[data-sb-comments-form]");
    const nameInput = container.querySelector("input[name='sb-name']");
    const bodyInput = container.querySelector("textarea[name='sb-body']");
    const submitButton = container.querySelector("button[type='submit']");

    try {
      const savedName = localStorage.getItem("sb-comments-name");
      if (savedName && nameInput && !nameInput.value) nameInput.value = savedName;
    } catch (err) {
      // ignore
    }

    void loadComments({
      container,
      endpoint,
      headers,
      threadId,
      requireApproval: requireApprovalBool
    });

    if (!form || !nameInput || !bodyInput) return;

    form.addEventListener("submit", async (e) => {
      e.preventDefault();

      const authorName = nameInput.value.trim();
      const body = bodyInput.value.trim();
      if (!authorName || !body) {
        setStatus(container, "Name and comment are required.", "error");
        return;
      }
      if (authorName.length > 80) {
        setStatus(container, "Name is too long (max 80 characters).", "error");
        return;
      }
      if (body.length > 5000) {
        setStatus(container, "Comment is too long (max 5000 characters).", "error");
        return;
      }

      if (submitButton) submitButton.disabled = true;
      try {
        try {
          localStorage.setItem("sb-comments-name", authorName);
        } catch (err) {
          // ignore
        }

        await submitComment({
          container,
          endpoint,
          headers,
          threadId,
          authorName,
          body,
          requireApproval: requireApprovalBool
        });
        bodyInput.value = "";
        if (!requireApprovalBool) {
          await loadComments({
            container,
            endpoint,
            headers,
            threadId,
            requireApproval: requireApprovalBool
          });
        }
      } catch (err) {
        const detail =
          err && typeof err.message === "string" ? err.message.trim() : "";
        setStatus(
          container,
          detail
            ? `Couldn’t submit your comment: ${detail}`
            : "Couldn’t submit your comment. Please try again.",
          "error"
        );
        console.error("[supabase-comments] submit failed", err);
      } finally {
        if (submitButton) submitButton.disabled = false;
      }
    });
  }

  function initAll() {
    const containers = document.querySelectorAll("[data-supabase-comments]");
    for (const container of containers) initOne(container);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initAll);
  } else {
    initAll();
  }
})();
