// src/App.jsx
import { BrowserRouter, Routes, Route } from "react-router-dom";
import LoginPage from "./pages/LoginPage";
import Dashboard from "./pages/Dashboard";
import HomePage from "./pages/HomePage"
import LoginAdmin from "./pages/LoginAdmin";
import Monitoreo from "./pages/Monitoreo";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/login-admin" element={<LoginAdmin />} />
        <Route path="/monitoreo" element={<Monitoreo/>} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
