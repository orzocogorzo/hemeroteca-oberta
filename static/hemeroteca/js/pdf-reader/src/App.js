import * as core from "@react-pdf-viewer/core";

import Reader from "./Reader";

import "./App.css";

function App(props) {
  return (
    <div className="pdf-reader">
      <core.Worker workerUrl="https://unpkg.com/pdfjs-dist@3.4.120/build/pdf.worker.min.js">
        <Reader {...props} />
      </core.Worker>
    </div>
  );
}

export default App;
