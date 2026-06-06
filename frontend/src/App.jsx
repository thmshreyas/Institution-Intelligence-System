import { Route, Routes } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import InstitutionDetails from "./pages/InstitutionDetails";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Dashboard />} />
      <Route path="/institutions/:name" element={<InstitutionDetails />} />
    </Routes>
  );
}
