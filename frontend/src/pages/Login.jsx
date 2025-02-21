import React, { useState } from "react";
import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";
import logo from "../assets/ScrumForge.webp";
import { login } from "../services/auth";

const Login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError(null);

    try {
      await login(username, password);
      navigate("/"); // Redirige vers la page d'accueil après connexion
    } catch (err) {
      setError("Nom d'utilisateur ou mot de passe incorrect.");
    }
  };

  // Fonction pour détecter la touche "Entrée"
  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      handleLogin(e);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gradient-to-b from-gray-100 to-gray-200">
      <div className="relative bg-gray-100 p-8 rounded-2xl shadow-2xl w-96 text-center border border-gray-300">
        
        {/* Effet de lumière pulsante derrière le logo */}
        <motion.div
          className="absolute top-15 left-1/2 transform -translate-x-1/2 w-40 h-40 bg-orange-500 rounded-full filter blur-2xl opacity-30"
          initial={{ scale: 0.8, opacity: 0.2 }}
          animate={{ scale: 1, opacity: 0.5 }}
          transition={{ duration: 1.5, repeat: Infinity, repeatType: "reverse" }}
        />

        {/* Logo ScrumForge */}
        <motion.div
          className="flex justify-center mb-6 relative"
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5 }}
        >
          <img
            src={logo}
            alt="ScrumForge Logo"
            className="relative w-132 h-132 rounded-full bg-gray-100 shadow-inner border border-gray-300"
          />
        </motion.div>

        {/* Affichage des erreurs */}
        {error && <p className="text-red-500 text-sm mb-4">{error}</p>}

        {/* Champs Nom d'utilisateur */}
        <div className="mb-4">
          <input
            type="text"
            placeholder="Nom d'utilisateur"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            onKeyDown={handleKeyDown} // Détecte "Entrée"
            className="w-full p-3 rounded-lg bg-gray-200 shadow-inner border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        {/* Champs Mot de passe */}
        <div className="mb-6">
          <input
            type="password"
            placeholder="Mot de passe"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            onKeyDown={handleKeyDown} // Détecte "Entrée"
            className="w-full p-3 rounded-lg bg-gray-200 shadow-inner border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        {/* Bouton Connexion */}
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={handleLogin}
          className="w-full bg-blue-500 text-white font-bold py-3 px-6 rounded-lg shadow-md hover:shadow-lg transition-all border border-blue-700"
        >
          Connexion
        </motion.button>

        {/* Lien Mot de passe oublié */}
        <div className="mt-4 text-gray-500">
          <button className="text-blue-500 hover:underline">Mot de passe oublié ?</button>
        </div>
      </div>
    </div>
  );
};

export default Login;
