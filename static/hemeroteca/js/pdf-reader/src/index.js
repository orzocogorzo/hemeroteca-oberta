import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";

function startApp({ rootEl, source, search = false, page = 1 }) {
  rootEl = HTMLElement.prototype.isPrototypeOf(rootEl)
    ? rootEl
    : document.querySelector(rootEl);
  const root = ReactDOM.createRoot(rootEl);
  root.render(
    <React.StrictMode>
      <App source={source} search={search} page={page} />
    </React.StrictMode>
  );
}

window.renderPdf = startApp;
if (process.env.NODE_ENV === "development") {
  const search = window.location.hash.match(/(?<=search=)[^&]+/);
  const page = window.location.hash.match(/(?<=page=)[^&]+/);

  startApp({
    rootEl: "#root",
    source: "/static/hemeroteca/uploads/documents/195VDVNov2011pmedium.pdf",
    search: search ? search[0] : "",
    page: page ? page[0] : "",
  });
}
