const { createProxyMiddleware } = require("http-proxy-middleware");

module.exports = function (app) {
  app.use(
    "/static/hemeroteca",
    createProxyMiddleware({
      target: "http://127.0.0.1:8000",
      changeOrigin: true,
      pathRewrite: async (path, req) => {
        return path;
      },
    })
  );
};
