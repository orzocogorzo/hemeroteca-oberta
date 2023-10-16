import "./style.css";

function ReaderToolbar({ Toolbar }) {
  return (
    <Toolbar>
      {({
        CurrentPageInput,
        Download,
        EnterFullScreen,
        GoToNextPage,
        GoToPreviousPage,
        NumberOfPages,
        Print,
        Zoom,
        ZoomIn,
        ZoomOut,
      }) => (
        <div className="rpv-toolbar" data-testid="toolbar" role="toolbar">
          <div className="rpv-toolbar__left">
            <div className="rpv-toolbar__item">
              <ZoomOut />
            </div>
            <div className="rpv-toolbar__item">
              <Zoom />
            </div>
            <div className="rpv-toolbar__item">
              <ZoomIn />
            </div>
          </div>
          <div className="rpv-toolbar__center">
            <div className="rpv-toolbar__item">
              <GoToPreviousPage />
            </div>
            <div className="rpv-toolbar__item">
              <CurrentPageInput /> / <NumberOfPages />
            </div>
            <div className="rpv-toolbar__item">
              <GoToNextPage />
            </div>
          </div>
          <div className="rpv-toolbar__right">
            <div className="rpv-toolbar__item">
              <EnterFullScreen />
            </div>
            <div className="rpv-toolbar__item">
              <Download />
            </div>
            <div className="rpv-toolbar__item">
              <Print />
            </div>
          </div>
        </div>
      )}
    </Toolbar>
  );
}

export default ReaderToolbar;
