import { useState } from "react";
import { Viewer, SpecialZoomLevel } from "@react-pdf-viewer/core";
import { toolbarPlugin } from "@react-pdf-viewer/toolbar";

import SearchControl from "../SearchControl";
import ReaderToolbar from "../Toolbar";

import "@react-pdf-viewer/core/lib/styles/index.css";
import "@react-pdf-viewer/toolbar/lib/styles/index.css";
import "./style.css";

function Reader({ source, search = false, page = 1 }) {
  const [ready, setReady] = useState(false);

  const toolbarInstance = toolbarPlugin({
    searchPlugin: {
      keyword: search,
      matchCase: false,
    },
  });

  const { searchPluginInstance, Toolbar } = toolbarInstance;

  return (
    <div className="reader">
      {search !== false && (
        <aside className="reader-sidebar">
          <SearchControl ready={ready} searcher={searchPluginInstance} keyword={search} />
        </aside>
      )}
      <div className="reader-content">
        <ReaderToolbar Toolbar={Toolbar} />
        <Viewer
          fileUrl={source}
          plugins={[toolbarInstance]}
          onDocumentLoad={() => setReady(true)}
          initialPage={page - 1}
          defaultScale={SpecialZoomLevel.PageFit}
        />
      </div>
    </div>
  );
}

export default Reader;
