import { Worker } from "@react-pdf-viewer/core";

import Reader from "./Reader";

import "./App.css";

function App({ source, search, page }) {
  return (
    <div className="pdf-reader">
      <Worker workerUrl="https://unpkg.com/pdfjs-dist@3.4.120/build/pdf.worker.min.js">
        <Reader source={source} search={search} page={page} />
      </Worker>
    </div>
  );
}

export default App;
