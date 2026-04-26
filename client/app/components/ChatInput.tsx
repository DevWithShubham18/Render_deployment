"use client";

import { useRef, useState } from "react";
import { ArrowUp, Paperclip, X } from "lucide-react";

export default function ChatInput({
  onSend,
  loading,
}: {
  onSend: (msg: string, file?: File | null) => void;
  loading: boolean;
}) {
  const [value, setValue] = useState("");
  const [file, setFile] = useState<File | null>(null);

  const fileInputRef = useRef<HTMLInputElement | null>(null);

  const handleSubmit = () => {
    if (!value.trim() && !file) return;

    onSend(value, file);
    setValue("");
    setFile(null);

    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  const handleRemoveFile = () => {
    setFile(null);


    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  return (
    <div className="pb-3 bg-white">
      <div className="max-w-5xl mx-auto">

        {/* File preview */}
        {file && (
          <div className="mb-2 flex items-center justify-between px-3 py-2 rounded-lg border border-gray-200 bg-gray-50 text-xs text-gray-600">
            <span className="truncate">📎 {file.name}</span>
            <button
              onClick={handleRemoveFile}
              className="ml-2 p-1 rounded hover:bg-gray-200"
            >
              <X size={14} />
            </button>
          </div>
        )}

        {/* Input */}
        <div className="flex items-center gap-2 px-3 py-2 rounded-full border border-gray-200 bg-white shadow-sm">

          <label className="cursor-pointer p-2 hover:bg-gray-100 rounded-full">
            <Paperclip size={16} />
            <input
              ref={fileInputRef}
              type="file"
              className="hidden"
              onChange={(e) => setFile(e.target.files?.[0] || null)}
            />
          </label>

          <input
            value={value}
            onChange={(e) => setValue(e.target.value)}
            placeholder="Ask something..."
            onKeyDown={(e) => e.key === "Enter" && handleSubmit()}
            className="flex-1 px-2 bg-transparent outline-none text-sm"
          />

          <button
            onClick={handleSubmit}
            disabled={loading}
            className="flex items-center justify-center h-9 w-9 rounded-full bg-black text-white disabled:opacity-50"
          >
            <ArrowUp size={16} />
          </button>
        </div>
      </div>
    </div>
  );
}