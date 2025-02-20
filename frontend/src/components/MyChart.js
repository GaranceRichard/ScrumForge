import React from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts";

// Données du graphique
const data = [
  { mois: "Jan", valeur: 400 },
  { mois: "Fév", valeur: 700 },
  { mois: "Mar", valeur: 200 },
  { mois: "Avr", valeur: 500 },
  { mois: "Mai", valeur: 900 },
];

// Composant personnalisé pour l'étiquette du Tooltip
const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <div style={{
        background: "#222",
        color: "white",
        padding: "10px",
        borderRadius: "5px",
        boxShadow: "0px 0px 10px rgba(255, 255, 255, 0.2)"
      }}>
        <p style={{ margin: 0, fontWeight: "bold" }}>{label}</p>
        <p style={{ margin: 0 }}>{`Valeur : ${payload[0].value}`}</p>
      </div>
    );
  }
  return null;
};

const MyChart = () => {
  return (
    <div style={{ width: "60%", height: 400, margin: "auto" }}>
      <h3 style={{ textAlign: "center", color: "white" }}>Évolution des valeurs</h3>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#555" />
          <XAxis dataKey="mois" stroke="white" />
          <YAxis stroke="white" />
          <Tooltip content={<CustomTooltip />} />  {/* 🟢 Ici on remplace le Tooltip par le CustomTooltip */}
          <Legend />
          <Line type="monotone" dataKey="valeur" stroke="#8884d8" strokeWidth={3} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default MyChart;
