import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";

function startApp({ rootEl, pk, source, search = false, page = 1, isVector = true }) {
  rootEl = HTMLElement.prototype.isPrototypeOf(rootEl)
    ? rootEl
    : document.querySelector(rootEl);
  const root = ReactDOM.createRoot(rootEl);
  const props = { pk, source, search, page, isVector };
  root.render(
    <React.StrictMode>
      <App {...props} />
    </React.StrictMode>
  );
}

window.renderPdf = startApp;
if (process.env.NODE_ENV === "development") {
  const query = new URLSearchParams(window.location.search);

  startApp({
    rootEl: "#root",
    pk: 0,
    source: "/static/hemeroteca/uploads/documents/AVVallvidrera000.pdf",
    search: query.get("search") || "",
    page: query.get("page") || "",
    isVector: false,
  });
}
