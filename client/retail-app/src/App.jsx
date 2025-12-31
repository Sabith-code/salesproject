import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Sales from "./pages/Sales";
import Inventory from "./pages/Inventory";
import Workforce from "./pages/Workforce";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Redirect root to sales */}
        <Route path="/" element={<Navigate to="/sales" replace />} />

        <Route path="/sales" element={<Sales />} />
        <Route path="/inventory" element={<Inventory />} />
        <Route path="/workforce" element={<Workforce />} />
      </Routes>
    </BrowserRouter>
  );
}
