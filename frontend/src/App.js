import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import Home from "./pages/Home"; // ← Page après connexion
import PrivateRoute from "./routes/PrivateRoute"; // ← Route protégée

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Page de connexion */}
        <Route path="/login" element={<Login />} />

        {/* Routes protégées */}
        <Route path="/" element={<PrivateRoute />}>
          <Route index element={<Home />} /> {/* Page affichée après connexion */}
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
