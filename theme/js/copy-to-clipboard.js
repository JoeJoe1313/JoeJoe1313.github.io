const copyToClipboardDefaultText = {
  innerText: "Copy",
  ariaLabel: "Copy to clipboard",
};
const copyToClipboardSuccessText = {
  innerText: "Copied!",
  ariaLabel: "Copied to clipboard",
};

// Get all pre. But ignore line numbers section
document.querySelectorAll("div.highlight pre").forEach((snippet) => {
  // create div.codecopy
  const wrapper = document.createElement("div");
  wrapper.classList.add("codecopy");

  // Wrap code inside div.codecopy
  const parent = snippet.parentNode;
  parent.replaceChild(wrapper, snippet);
  wrapper.appendChild(snippet);

  // Create button
  const button = `
            <button
                type="button"
                class="codecopy-btn"
                title="${copyToClipboardDefaultText.ariaLabel}"
                aria-label="${copyToClipboardDefaultText.ariaLabel}"
            >
                <span class="codecopy-icon" aria-hidden="true">
                    <svg class="codecopy-icon-copy" width="16" height="16" viewBox="0 0 16 16" focusable="false" aria-hidden="true">
                        <rect x="5" y="1" width="9" height="11" rx="1" ry="1" fill="none" stroke="currentColor" stroke-width="1.5" />
                        <rect x="2" y="4" width="9" height="11" rx="1" ry="1" fill="none" stroke="currentColor" stroke-width="1.5" />
                    </svg>
                    <svg class="codecopy-icon-success" width="16" height="16" viewBox="0 0 16 16" focusable="false" aria-hidden="true">
                        <polyline points="3.5 8.5 6.5 11.5 12.5 4.5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" />
                    </svg>
                </span>
                <span class="sr-only">${copyToClipboardDefaultText.innerText}</span>
            </button>`;

  // Add button to div.codecopy
  wrapper.insertAdjacentHTML("afterbegin", button);
});

// Add copy to clipboard functionality
const clipboard = new ClipboardJS(".codecopy-btn", {
  text: (trigger) => {
    const wrapper = trigger.closest(".codecopy");

    if (!wrapper) {
      return "";
    }

    const preElement = wrapper.querySelector("pre");

    if (!preElement) {
      return "";
    }

    const codeElement = preElement.querySelector("code");

    // Ensure we only copy the code contents, never the button label
    return (codeElement || preElement).textContent;
  },
});

// Show message on success
clipboard.on("success", (e) => {
  const screenReaderText = e.trigger.querySelector(".sr-only");

  e.trigger.classList.add("is-copied");
  e.trigger.setAttribute("aria-label", copyToClipboardSuccessText.ariaLabel);
  e.trigger.setAttribute("title", copyToClipboardSuccessText.ariaLabel);

  if (screenReaderText) {
    screenReaderText.textContent = copyToClipboardSuccessText.innerText;
  }

  e.clearSelection();

  // Reset button text
  setTimeout(() => {
    e.trigger.classList.remove("is-copied");
    e.trigger.setAttribute("aria-label", copyToClipboardDefaultText.ariaLabel);
    e.trigger.setAttribute("title", copyToClipboardDefaultText.ariaLabel);

    if (screenReaderText) {
      screenReaderText.textContent = copyToClipboardDefaultText.innerText;
    }
  }, 1000);
});
