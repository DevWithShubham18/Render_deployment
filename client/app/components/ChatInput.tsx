"use client";

import { useRef, useState } from "react";
import { ArrowUp, Paperclip, X } from "lucide-react";
import TextareaAutosize from "react-textarea-autosize";

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
    // Prevent sending empty messages
    if (!value.trim() && !file) return;

    onSend(value, file);
    setValue("");
    setFile(null);

    // Reset the hidden file input
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

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    // Send message on Enter, but allow new lines with Shift + Enter
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault(); 
      handleSubmit();
    }
  };

  return (
    <div className="pb-3 bg-white">
      <div className="max-w-5xl mx-auto">
        
        {/* File preview attachment bubble */}
        {file && (
          <div className="mb-2 flex items-center justify-between px-3 py-2 rounded-lg border border-gray-200 bg-gray-50 text-xs text-gray-600">
            <span className="truncate">📎 {file.name}</span>
            <button
              onClick={handleRemoveFile}
              className="ml-2 p-1 rounded hover:bg-gray-200 transition-colors"
            >
              <X size={14} />
            </button>
          </div>
        )}

        {/* Main Input Area */}
        {/* Switched to items-end and rounded-3xl so it looks natural when expanding */}
        <div className="flex items-end gap-2 px-3 py-2 rounded-3xl border border-gray-200 bg-white shadow-sm">
          
          {/* Paperclip Button */}
          <label className="cursor-pointer p-2 hover:bg-gray-100 rounded-full mb-0.5 transition-colors">
            <Paperclip size={16} />
            <input
              ref={fileInputRef}
              type="file"
              className="hidden"
              onChange={(e) => setFile(e.target.files?.[0] || null)}
            />
          </label>

          {/* Expanding Text Area */}
          <TextareaAutosize
            value={value}
            onChange={(e) => setValue(e.target.value)}
            placeholder="Ask something..."
            onKeyDown={handleKeyDown}
            minRows={1}
            maxRows={6}
            className="flex-1 px-2 py-2 bg-transparent outline-none text-sm resize-none overflow-hidden"
          />

          {/* Send Button */}
          <button
            onClick={handleSubmit}
            disabled={loading || (!value.trim() && !file)}
            className="flex items-center justify-center h-9 w-9 rounded-full bg-black text-white disabled:opacity-50 mb-0.5 shrink-0 transition-opacity"
          >
            <ArrowUp size={16} />
          </button>
          
        </div>
      </div>
    </div>
  );
}
