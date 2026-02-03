import { useState } from "react";
import axios from "axios";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend);

function App() {
  const [summary, setSummary] = useState(null);
  const [error, setError] = useState("");

  const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post("/api/upload/", formData);
      setSummary(res.data.summary);
      setError("");
    } catch (err) {
      setError("Upload failed. Is backend running?");
      setSummary(null);
    }
  };

  const typeDist = summary?.equipment_type_distribution || {};

  return (
    <div style={{ padding: "40px" }}>
      <h1>Chemical Equipment Parameter Visualizer</h1>

      <input type="file" accept=".csv" onChange={handleUpload} />

      {error && <p style={{ color: "red" }}>{error}</p>}

      {summary && (
        <>
          <h2>Summary</h2>
          <p>Total Equipment: {summary.total_equipment}</p>
          <p>Avg Flowrate: {summary.average_flowrate}</p>
          <p>Avg Pressure: {summary.average_pressure}</p>
          <p>Avg Temperature: {summary.average_temperature}</p>

          <h2>Equipment Type Distribution</h2>
          {Object.keys(typeDist).length > 0 && (
            <Bar
              data={{
                labels: Object.keys(typeDist),
                datasets: [
                  {
                    label: "Count",
                    data: Object.values(typeDist),
                    backgroundColor: "rgba(75, 192, 192, 0.6)",
                  },
                ],
              }}
            />
          )}
        </>
      )}
    </div>
  );
}

export default App;
