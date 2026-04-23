'use client'
import React, { useEffect, useMemo, useRef, useState } from "react";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  Tooltip,
  Legend,
} from "chart.js";
import { Bar, Line, Pie, Doughnut } from "react-chartjs-2";

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  Tooltip,
  Legend
);

// Map chart types
const chartMap: Record<string, any> = {
  bar: Bar,
  line: Line,
  pie: Pie,
  doughnut: Doughnut,
};

type LLMConfig = {
  type: string;
  data: any;
  options?: any;
};

export default function App() {
  const [config, setConfig] = useState<LLMConfig | null>(null);
  const chartRef = useRef<any>(null);

  // Simulated LLM response
  useEffect(() => {
    const fakeLLMResponse: LLMConfig = {
      type: "bar",
      data: {
        labels: ["Mon", "Tue", "Wed", "Thu", "Fri"],
        datasets: [
          {
            label: "Visitors",
            data: [120, 190, 300, 250, 220],
            backgroundColor: "rgba(54, 162, 235, 0.6)",
          },
        ],
      },
      options: {
        responsive: true,
        devicePixelRatio: 3, // sharper export
        plugins: {
          legend: { position: "top" },
        },
      },
    };

    setTimeout(() => setConfig(fakeLLMResponse), 800);
  }, []);

  const safeConfig = useMemo(() => sanitize(config), [config]);

  const handleDownload = () => {
    const chart = chartRef.current;
    if (!chart) return;

    const url = chart.toBase64Image("image/png", 1);

    const link = document.createElement("a");
    link.href = url;
    link.download = "llm-chart.png";
    link.click();
  };

  if (!safeConfig) return <div>Loading chart from LLM...</div>;

  const ChartComponent = chartMap[safeConfig.type];
  if (!ChartComponent) return <div>Unsupported chart type</div>;

  return (
    <div style={{ width: 650, height: 420, margin: "40px auto" }}>
      <ChartComponent
        ref={chartRef}
        data={safeConfig.data}
        options={safeConfig.options}
      />

      <div style={{ marginTop: 16 }}>
        <button onClick={handleDownload}>
          Save as Image
        </button>
      </div>
    </div>
  );
}

// Sanitize LLM output
function sanitize(config: LLMConfig | null): LLMConfig | null {
  if (!config) return null;

  return {
    type: config.type || "bar",
    data: {
      labels: config?.data?.labels || [],
      datasets:
        config?.data?.datasets?.map((d: any) => ({
          label: d.label || "Dataset",
          data: Array.isArray(d.data) ? d.data : [],
          backgroundColor:
            d.backgroundColor || "rgba(75, 192, 192, 0.5)",
          borderColor: d.borderColor || "rgba(75,192,192,1)",
          borderWidth: d.borderWidth ?? 1,
        })) || [],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      devicePixelRatio: 2,
      ...config.options,
    },
  };
}