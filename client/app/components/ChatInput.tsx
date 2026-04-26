"use client";

import { useState } from "react";
import { ArrowUp } from "lucide-react";

export default function ChatInput({
  onSend,
  loading,
}: {
  onSend: (msg: string) => void;
  loading: boolean;
}) {
  const [value, setValue] = useState("");

  const handleSubmit = () => {
    if (!value.trim()) return;
    onSend(value);
    setValue("");
  };

  return (
    <div className="pb-3 bg-white">
      <div className="max-w-5xl mx-auto">
        <div className="flex items-center gap-2 px-3 py-2 rounded-full border border-gray-200 bg-white shadow-sm focus-within:shadow-md transition-all">
          <input
            value={value}
            onChange={(e) => setValue(e.target.value)}
            placeholder="Ask something..."
            onKeyDown={(e) => e.key === "Enter" && handleSubmit()}
            className="flex-1 px-2 bg-transparent outline-none text-sm placeholder:text-gray-400"
          />

          <button
            onClick={handleSubmit}
            disabled={loading}
            className="flex items-center justify-center h-9 w-9 rounded-full bg-black text-white hover:opacity-90 transition disabled:opacity-50"
          >
            <ArrowUp size={16} />
          </button>
        </div>
      </div>
    </div>
  );
}
