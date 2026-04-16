import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.jsx";

ReactDOM.createRoot(document.getElementById("root")).render(
  // React.StrictMode is a tool for highlighting potential problems in an application.
  // But don't use this in production
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
