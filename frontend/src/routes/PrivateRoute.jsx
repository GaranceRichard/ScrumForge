import { useState, useEffect } from "react";
import { Navigate, Outlet } from "react-router-dom";
import { isAuthenticated } from "../services/auth";

export default function PrivateRoute() {
  console.log("🔄 `PrivateRoute.jsx` exécuté");

  const [loading, setLoading] = useState(true);
  const [authenticated, setAuthenticated] = useState(false);

  useEffect(() => {
    console.log("🔄 Vérification d'authentification en cours...");
    const authStatus = isAuthenticated();
    console.log("🔍 PrivateRoute - Authenticated :", authStatus);
    setAuthenticated(authStatus);
    setLoading(false);
  }, []);

  if (loading) return <div>Chargement...</div>;

  console.log("🚀 Rendu de PrivateRoute - Authenticated :", authenticated);
  
  return authenticated ? <Outlet /> : <Navigate to="/login" />;
}
