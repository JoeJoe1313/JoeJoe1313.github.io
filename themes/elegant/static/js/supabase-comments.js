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

  function getSavedName() {
    try {
      return localStorage.getItem("sb-comments-name") || "";
    } catch (err) {
      return "";
    }
  }

  function saveName(value) {
    try {
      localStorage.setItem("sb-comments-name", value);
    } catch (err) {
      // ignore
    }
  }

  function validateInputs(container, authorName, body) {
    if (!authorName || !body) {
      setStatus(container, "Name and comment are required.", "error");
      return false;
    }
    if (authorName.length > 80) {
      setStatus(container, "Name is too long (max 80 characters).", "error");
      return false;
    }
    if (body.length > 5000) {
      setStatus(container, "Comment is too long (max 5000 characters).", "error");
      return false;
    }
    return true;
  }

  function buildCommentTree(comments) {
    const byId = new Map();
    const roots = [];

    for (const comment of comments) {
      comment.children = [];
      byId.set(String(comment.id), comment);
    }

    for (const comment of comments) {
      const parentId = comment.parent_id;
      const parentKey = parentId === null || parentId === undefined
        ? ""
        : String(parentId);
      if (parentKey && byId.has(parentKey)) {
        byId.get(parentKey).children.push(comment);
      } else {
        roots.push(comment);
      }
    }

    return roots;
  }

  function renderComment(comment, level) {
    const wrapper = el("div", {
      class: "sb-comment",
      "data-comment-id": String(comment.id),
      style: `--sb-level: ${level}`
    });
    const meta = el("div", { class: "sb-comment__meta" });
    const name = comment?.author_name?.trim() || "Anonymous";
    const when = formatDate(comment?.created_at);
    meta.textContent = when ? `${name} · ${when}` : name;

    const body = el("div", { class: "sb-comment__body" });
    body.textContent = comment?.body || "";

    const actions = el("div", { class: "sb-comment__actions" });
    const replyButton = el(
      "button",
      { type: "button", class: "sb-comment__reply" },
      "Reply"
    );
    actions.appendChild(replyButton);

    wrapper.appendChild(meta);
    wrapper.appendChild(body);
    wrapper.appendChild(actions);
    return wrapper;
  }

  function renderCommentTree(list, comments, level) {
    for (const comment of comments) {
      const node = renderComment(comment, level);
      list.appendChild(node);
      if (comment.children && comment.children.length > 0) {
        renderCommentTree(list, comment.children, level + 1);
      }
    }
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
    url.searchParams.set("select", "id,parent_id,author_name,body,created_at");
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
      const tree = buildCommentTree(comments);
      renderCommentTree(list, tree, 0);
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
    parentId,
    requireApproval
  }) {
    setStatus(container, "Submitting…", "info");

    const entry = {
      thread_id: threadId,
      author_name: authorName,
      body
    };

    if (parentId !== undefined && parentId !== null && parentId !== "") {
      const numericParent = Number(parentId);
      entry.parent_id = Number.isNaN(numericParent) ? parentId : numericParent;
    }

    const payload = [entry];

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

    const list = container.querySelector("[data-sb-comments-list]");
    const form = container.querySelector("form[data-sb-comments-form]");
    const nameInput = container.querySelector("input[name='sb-name']");
    const bodyInput = container.querySelector("textarea[name='sb-body']");
    const submitButton = container.querySelector("button[type='submit']");

    const savedName = getSavedName();
    if (savedName && nameInput && !nameInput.value) nameInput.value = savedName;

    let replyForm = null;
    let replyNameInput = null;
    let replyBodyInput = null;
    let replySubmitButton = null;
    let replyCancelButton = null;
    let activeReplyParentId = null;

    function closeReplyForm() {
      if (replyForm && replyForm.parentNode) replyForm.parentNode.removeChild(replyForm);
      activeReplyParentId = null;
    }

    function ensureReplyForm() {
      if (replyForm) return;

      replyForm = el("form", { class: "sb-comments__reply-form" });

      const nameLabel = el("label", {}, "Name");
      replyNameInput = el("input", {
        type: "text",
        name: "sb-reply-name",
        maxlength: "80",
        required: "required"
      });
      nameLabel.appendChild(replyNameInput);

      const bodyLabel = el("label", {}, "Reply");
      replyBodyInput = el("textarea", {
        name: "sb-reply-body",
        maxlength: "5000",
        required: "required"
      });
      bodyLabel.appendChild(replyBodyInput);

      const actions = el("div", { class: "sb-comments__reply-actions" });
      replySubmitButton = el(
        "button",
        { type: "submit", class: "btn btn-primary" },
        "Post reply"
      );
      replyCancelButton = el(
        "button",
        { type: "button", class: "btn" },
        "Cancel"
      );

      actions.appendChild(replySubmitButton);
      actions.appendChild(replyCancelButton);

      replyForm.appendChild(nameLabel);
      replyForm.appendChild(bodyLabel);
      replyForm.appendChild(actions);

      replyCancelButton.addEventListener("click", () => {
        closeReplyForm();
      });

      replyForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        if (!replyNameInput || !replyBodyInput) return;

        const authorName = replyNameInput.value.trim();
        const body = replyBodyInput.value.trim();
        if (!validateInputs(container, authorName, body)) return;

        if (replySubmitButton) replySubmitButton.disabled = true;
        try {
          saveName(authorName);

          await submitComment({
            container,
            endpoint,
            headers,
            threadId,
            authorName,
            body,
            parentId: activeReplyParentId,
            requireApproval: requireApprovalBool
          });
          replyBodyInput.value = "";
          closeReplyForm();
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
              ? `Couldn’t submit your reply: ${detail}`
              : "Couldn’t submit your reply. Please try again.",
            "error"
          );
          console.error("[supabase-comments] reply failed", err);
        } finally {
          if (replySubmitButton) replySubmitButton.disabled = false;
        }
      });
    }

    function openReplyForm(commentEl, parentId) {
      if (!commentEl) return;

      ensureReplyForm();
      if (replyForm && replyForm.parentNode === commentEl) {
        closeReplyForm();
        return;
      }

      activeReplyParentId = parentId;
      const savedReplyName = getSavedName();
      if (savedReplyName && replyNameInput && !replyNameInput.value) {
        replyNameInput.value = savedReplyName;
      }
      commentEl.appendChild(replyForm);
      if (replyBodyInput) replyBodyInput.focus();
    }

    if (list) {
      list.addEventListener("click", (event) => {
        const button = event.target.closest(".sb-comment__reply");
        if (!button) return;
        event.preventDefault();
        const commentEl = button.closest(".sb-comment");
        if (!commentEl) return;
        const parentId = commentEl.getAttribute("data-comment-id");
        openReplyForm(commentEl, parentId);
      });
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
      if (!validateInputs(container, authorName, body)) return;

      if (submitButton) submitButton.disabled = true;
      try {
        saveName(authorName);

        await submitComment({
          container,
          endpoint,
          headers,
          threadId,
          authorName,
          body,
          parentId: null,
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
