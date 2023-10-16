function OhPdfViewer({ url, container, search }) {
  this.container = container;
  this.eventBus = new pdfjsViewer.EventBus();
  this.linkService = new pdfjsViewer.PDFLinkService({ eventBus: this.eventBus });
  this.findController = new pdfjsViewer.PDFFindController({
    eventBus: this.eventBus,
    linkService: this.linkService,
  });

  this.eventBus.on("pagesinit", () => {
    if (search) this.search(search);
  });

  this.viewer = new pdfjsViewer.PDFViewer({
    container: this.container,
    eventBus: this.eventBus,
    linkService: this.linkService,
    findController: this.findController,
    textLayerMode: 2,
  });

  this.linkService.setViewer(this.viewer);

  pdfjsLib.getDocument(url).promise.then((doc) => {
    this.viewer.setDocument(doc);
    this.linkService.setDocument(doc, null);
    this.doc = doc;
  });

  this.textMatches = [];
  this.eventBus.on("updatetextlayermatches", this.onMatchText.bind(this));

  this.textSearcher = new OhPdfTextSearcher(search);
  this.textSearcher.on("change", () => {
    if (this.textSearcher.value) this.search(this.textSearcher.value);
  });
  this.textSearcher.on("keydown", () => {
    this.textMatches.push(this.textMatches.shift());
    this.search(this.textSearcher.value, this.textMatches[0]);
  });
  this.container.parentElement.appendChild(this.textSearcher.el);
}

OhPdfViewer.prototype.search = function (query, match) {
  if (match) {
    // this.findController._offset.pageIdx = match.pageIdx;
    // this.findController._offset.matchIdx = match.matchIdx;
    this.findController.selected.pageIdx = match.pageIdx;
    this.findController.selected.matchIdx = match.matchIdx;
    // this.linkService.page = match.pageIdx;
    this.eventBus.dispatch("updatetextlayermatches", {
      pageIndex: match.pageIdx,
    });
  } else {
    this.eventBus.dispatch("find", {
      caseSensitive: false,
      phraseSearch: true,
      findPrevious: false,
      query,
    });
  }
};

OhPdfViewer.prototype.onMatchText = function () {
  this.textMatches = this.findController.pageMatches.flatMap((pm, i) => {
    if (pm.length) {
      return pm.map((x, j) => ({
        pageIdx: i + 1,
        matchIdx: j,
        matchLocation: x,
      }));
    }

    return [];
  });
};

function OhPdfTextSearcher(pattern) {
  this.listeners = new Proxy(
    {},
    {
      get: (target, key) => {
        return target[key] || [];
      },
      set: (target, key, value) => {
        target[key] = target[key] || [];
        if (Array.isArray(value)) target[key] = target[key].concat(value);
        else target[key].push(value);
      },
    }
  );

  this.el = document.createElement("input");
  this.el.type = "text";
  this.el.value = pattern;
  this.el.style.position = "absolute";
  this.el.style.zIndex = 1000;

  this.el.addEventListener("change", () => {
    this.listeners["change"].forEach((l) => l(this.value));
  });
  this.el.addEventListener("keydown", (ev) => {
    if (ev.keyCode !== 13) return;
    this.listeners["keydown"].forEach((l) => l(this.value));
  });

  Object.defineProperty(this, "value", {
    get: () => {
      return this.el.value;
    },
    set: (pattern) => {
      this.el.value = pattern;
      this.el.dispatchEvent(new Event("change"));
    },
  });
}

OhPdfTextSearcher.prototype.on = function (event, listener) {
  this.listeners[event] = listener;
};

OhPdfTextSearcher.prototype.off = function (event, listener) {
  this.listeners[event] = this.listeners[event].filter((l) => l !== listener);
};
