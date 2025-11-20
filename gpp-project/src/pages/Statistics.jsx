import React, { useEffect, useState } from "react";
import { Bar, Line, Pie } from "react-chartjs-2";
import * as XLSX from "xlsx";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

function computeStats(values) {
  const mean = values.reduce((a, b) => a + b, 0) / values.length;
  const sorted = [...values].sort((a, b) => a - b);
  const mid = Math.floor(values.length / 2);
  const median = values.length % 2 !== 0 ? sorted[mid] : (sorted[mid - 1] + sorted[mid]) / 2;
  const min = Math.min(...values);
  const max = Math.max(...values);
  const std = Math.sqrt(values.map(v => Math.pow(v - mean, 2)).reduce((a, b) => a + b, 0) / values.length);

  return {
    mean: mean.toFixed(2),
    median: median.toFixed(2),
    min: min.toFixed(2),
    max: max.toFixed(2),
    std: std.toFixed(2)
  };
}

export default function Statistics() {

  useEffect(() => {
    document.title = "Radarix | Statistics";
  }, []);

  const [stats, setStats] = useState(null);
  const [barData, setBarData] = useState(null);
  const [lineData, setLineData] = useState(null);
  const [pieData, setPieData] = useState(null);

  useEffect(() => {
    fetch("/Dataset_Vital_Signs.xlsx")
      .then(res => res.arrayBuffer())
      .then(data => {
        const workbook = XLSX.read(data, { type: "array" });
        const sheetName = workbook.SheetNames[0];
        const sheet = workbook.Sheets[sheetName];
        const jsonData = XLSX.utils.sheet_to_json(sheet);
        processDataset(jsonData);
      });
  }, []);

  const processDataset = (dataset) => {
    const categories = [...new Set(dataset.map(d => d.category))];
    const numericFields = ["respiration_rate", "chest_displacement", "signal_strength"];

    const statsObj = {};
    categories.forEach(cat => {
      const items = dataset.filter(d => d.category === cat);
      statsObj[cat] = {};

      numericFields.forEach(field => {
        const values = items.map(d => parseFloat(d[field]));
        statsObj[cat][field] = computeStats(values);
      });
    });

    setStats(statsObj);

    setBarData({
      labels: categories,
      datasets: [
        {
          label: "Mean Respiration Rate",
          data: categories.map(cat => statsObj[cat].respiration_rate.mean),
          backgroundColor: ["#36A2EB", "#FF6384", "#FFCE56"]
        }
      ]
    });

    setLineData({
      labels: categories,
      datasets: numericFields.map((field, i) => ({
        label: field.replace("_", " "),
        data: categories.map(cat => statsObj[cat][field].mean),
        borderColor: ["#36A2EB", "#FF6384", "#FFCE56"][i],
        backgroundColor: "transparent",
        fill: false,
        tension: 0.3
      }))
    });

    setPieData({
      labels: categories,
      datasets: [
        {
          label: "Mean Signal Strength",
          data: categories.map(cat => statsObj[cat].signal_strength.mean),
          backgroundColor: ["#36A2EB", "#FF6384", "#FFCE56"]
        }
      ]
    });
  };

  const renderSummaryBoxes = (category) => (
    <div key={category} style={{ margin: "20px 0" }}>
      <h2 style={{ marginBottom: "15px", textAlign: "center", color: "white", fontSize: "32px", fontWeight: "bold" }}>
        {category} Statistics
      </h2>

      <div style={{ display: "flex", flexWrap: "wrap", gap: "20px", justifyContent: "center" }}>
        {Object.keys(stats[category]).map(field => (
          <div
            key={field}
            style={{
              border: "1px solid #444",
              borderRadius: "10px",
              padding: "15px",
              minWidth: "200px",
              backgroundColor: "#1e1e1e",
              color: "white",
              boxShadow: "2px 2px 8px rgba(0,0,0,0.5)"
            }}
          >
            <h3 style={{ textTransform: "capitalize", marginBottom: "10px", fontSize: "22px", fontWeight: "bold" }}>
              {field.replace("_", " ")}
            </h3>

            <p><strong>Mean:</strong> {stats[category][field].mean}</p>
            <p><strong>Median:</strong> {stats[category][field].median}</p>
            <p><strong>Min:</strong> {stats[category][field].min}</p>
            <p><strong>Max:</strong> {stats[category][field].max}</p>
            <p><strong>Std Dev:</strong> {stats[category][field].std}</p>
          </div>
        ))}
      </div>
    </div>
  );

  if (!stats) {
    return (
      <div
        style={{
          width: "100vw",
          height: "100vh",
          backgroundColor: "#121212",
          color: "white",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          fontSize: "32px",
          fontWeight: "bold",
          overflowX: "hidden"
        }}
      >
        Loading...
      </div>
    );
  }

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: { labels: { color: "white", font: { size: 16, weight: "bold" } } },
      title: { display: false }
    },
    scales: {
      x: { ticks: { color: "white" }, grid: { color: "#444" } },
      y: { ticks: { color: "white" }, grid: { color: "#444" } }
    }
  };

  const chartBoxStyle = {
    backgroundColor: "#1e1e1e",
    borderRadius: "10px",
    padding: "20px",
    margin: "20px auto",
    maxWidth: "700px",
    width: "90%",
    boxShadow: "2px 2px 10px rgba(0,0,0,0.5)"
  };

  return (
    <div
      style={{
        width: "100vw",
        minHeight: "100vh",
        textAlign: "center",
        backgroundColor: "#121212",
        padding: "20px",
        overflowX: "hidden"
      }}
    >
      <h1 style={{ color: "white", fontSize: "48px", marginBottom: "40px", fontWeight: "bold" }}>
        Respiration Health Data Analysis
      </h1>

      <div style={chartBoxStyle}>
        <h2 style={{ color: "white", fontSize: "28px", marginBottom: "20px", fontWeight: "bold" }}>
          Bar Chart: Mean Respiration Rate
        </h2>
        <Bar data={barData} options={chartOptions} />
      </div>

      <div style={chartBoxStyle}>
        <h2 style={{ color: "white", fontSize: "28px", marginBottom: "20px", fontWeight: "bold" }}>
          Line Chart: Mean Values of Fields
        </h2>
        <Line data={lineData} options={chartOptions} />
      </div>

      <div style={chartBoxStyle}>
        <h2 style={{ color: "white", fontSize: "28px", marginBottom: "20px", fontWeight: "bold" }}>
          Pie Chart: Mean Signal Strength
        </h2>
        <Pie data={pieData} />
      </div>

      {Object.keys(stats).map(cat => renderSummaryBoxes(cat))}
    </div>
  );
}
