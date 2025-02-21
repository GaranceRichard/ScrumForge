import React from "react";
import { useNavigate } from "react-router-dom";
import { logout } from "../services/auth";

export default function Home() {
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login"); // Redirige vers la page de connexion après déconnexion
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <h1 className="text-2xl font-bold mb-4">Bienvenue sur la page d'accueil !</h1>
      
      {/* Bouton de déconnexion */}
      <button
        onClick={handleLogout}
        className="bg-red-500 text-white px-4 py-2 rounded-lg shadow-md hover:bg-red-600 transition"
      >
        Déconnexion
      </button>
    </div>
  );
}
