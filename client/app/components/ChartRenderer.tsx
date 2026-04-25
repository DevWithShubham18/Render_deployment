"use client";

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
import { useMemo, useRef } from "react";
import { Download } from "lucide-react";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  Tooltip,
  Legend,
);

const chartMap: Record<string, any> = {
  bar: Bar,
  line: Line,
  pie: Pie,
  doughnut: Doughnut,
};

export default function ChartRenderer({ config }: any) {
  const chartRef = useRef<any>(null);
  const safeConfig = useMemo(() => sanitize(config), [config]);

  const ChartComponent = chartMap[safeConfig.type];

  if (!ChartComponent) return null;

  const handleDownload = () => {
    const chart = chartRef.current;
    if (!chart) return;

    const url = chart.toBase64Image("image/png", 1);
    const link = document.createElement("a");
    link.href = url;
    link.download = "chart.png";
    link.click();
  };

  return (
    <div className="max-w-3xl relative group border border-gray-200 bg-white rounded-2xl p-4 shadow-sm hover:shadow-md transition-all">
      {/* Download button */}
      <button
        onClick={handleDownload}
        className="absolute top-3 right-3 flex items-center justify-center h-8 w-8 rounded-lg bg-white/80 backdrop-blur border border-gray-200 opacity-0 group-hover:opacity-100 transition cursor-pointer hover:scale-105 active:scale-95"
      >
        <Download size={16} className="text-gray-700" />
      </button>

      {/* Chart */}
      <div className="h-80  w-full cursor-pointer">
        <ChartComponent
          ref={chartRef}
          data={safeConfig.data}
          options={safeConfig.options}
        />
      </div>
    </div>
  );
}

function sanitize(config: any) {
  return {
    type: config?.type || "bar",
    data: {
      labels: config?.data?.labels || [],
      datasets:
        config?.data?.datasets?.map((d: any) => ({
          label: d.label || "Dataset",
          data: Array.isArray(d.data) ? d.data : [],
          backgroundColor: d.backgroundColor || "rgba(0,0,0,0.7)",
          borderColor: d.borderColor || "rgba(0,0,0,1)",
          borderWidth: d.borderWidth ?? 1,
        })) || [],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          labels: { color: "#374151" },
        },
      },
      ...config?.options,
    },
  };
}
