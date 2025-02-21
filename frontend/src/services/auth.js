import api from "./api";

// 🔐 Fonction de connexion (Login)
export const login = async (username, password) => {
  try {
    const response = await api.post("/authentication/token/", { username, password });

    console.log("🔍 Réponse API:", response.data); // Debugging

    if (response.data.access) {
      localStorage.setItem("access_token", response.data.access);
      localStorage.setItem("refresh_token", response.data.refresh);
      
      console.log("✅ Token stocké :", localStorage.getItem("access_token")); // Vérifier si le stockage fonctionne
    } else {
      throw new Error("Aucun token reçu");
    }

    return response.data;
  } catch (error) {
    console.error("❌ Erreur de connexion:", error.response ? error.response.data : error.message);
    throw error;
  }
};

// 🚪 Fonction de déconnexion (Logout)
export const logout = async () => {
  try {
    await api.post("/authentication/logout/");
  } catch (error) {
    console.error("❌ Erreur lors de la déconnexion:", error);
  } finally {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    console.log("🚪 Déconnexion réussie, tokens supprimés.");
    window.location.href = "/login";
  }
};

// 🔍 Vérifier si l'utilisateur est authentifié
export const isAuthenticated = () => {
  const token = localStorage.getItem("access_token");

  console.log("🔍 Vérification Auth - Token récupéré :", token); // Vérifier si le token est présent
  console.log("🔎 Condition de validation :", !!token, token !== "undefined", token !== "null");


  return token && token !== "undefined" && token !== "null";
};

// 🔄 Rafraîchir le token (Optionnel mais utile)
export const refreshAccessToken = async () => {
  try {
    const refreshToken = localStorage.getItem("refresh_token");

    if (!refreshToken) {
      console.warn("⚠️ Aucun refresh token disponible.");
      return false;
    }

    const response = await api.post("/authentication/token/refresh/", {
      refresh: refreshToken,
    });

    console.log("🔄 Nouveau token reçu :", response.data.access);

    localStorage.setItem("access_token", response.data.access);
    return true;
  } catch (error) {
    console.error("❌ Erreur lors du rafraîchissement du token:", error.response ? error.response.data : error.message);
    logout(); // Déconnexion automatique si le refresh échoue
    return false;
  }
};
