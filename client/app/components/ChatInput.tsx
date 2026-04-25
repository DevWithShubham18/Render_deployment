"use client";

import { useState } from "react";
import { Send } from "lucide-react";

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
      <div className="max-w-2xl mx-auto">
        <div className="flex items-center gap-2 px-4 py-3 rounded-2xl border border-gray-200 bg-white shadow-sm focus-within:shadow-md transition-all">
          <input
            value={value}
            onChange={(e) => setValue(e.target.value)}
            placeholder="Ask something..."
            onKeyDown={(e) => e.key === "Enter" && handleSubmit()}
            className="flex-1 bg-transparent outline-none text-sm placeholder:text-gray-400"
          />

          <button
            onClick={handleSubmit}
            disabled={loading}
            className="flex items-center justify-center h-9 w-9 rounded-xl bg-black text-white hover:opacity-90 transition disabled:opacity-50"
          >
            <Send size={16} />
          </button>
        </div>
      </div>
    </div>
  );
}
