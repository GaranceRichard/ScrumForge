import React from "react";
import MyChart from "./components/MyChart"; // Import du graphique
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Tableau de Bord</h1>
        <MyChart /> {/* Affichage du graphique */}
      </header>
    </div>
  );
}

export default App;
