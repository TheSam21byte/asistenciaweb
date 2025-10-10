// src/main.jsx
import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./index.css"; // si tienes Tailwind o estilos
import { StrictMode } from "react";

ReactDOM.createRoot(document.getElementById("root")).render(
  <StrictMode>
    <App />
  </StrictMode>
);
