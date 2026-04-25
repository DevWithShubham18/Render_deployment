"use client";

import { useEffect, useRef } from "react";
import { Message } from "../types";
import ChartRenderer from "./ChartRenderer";

export default function ChatMessages({
  messages,
  loading,
}: {
  messages: Message[];
  loading: boolean;
}) {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="h-full overflow-y-auto px-4 py-6">
      {/* Center wrapper */}
      <div className="max-w-2xl mx-auto space-y-6">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`flex ${
              msg.role === "user" ? "justify-end" : "justify-start"
            }`}
          >
            <div
              className={`max-w-[75%] px-4 py-3 rounded-2xl text-sm leading-relaxed ${
                msg.role === "user"
                  ? "bg-black text-white"
                  : "bg-gray-100 text-gray-900 border border-gray-200"
              }`}
            >
              {msg.content}

              {msg.config && (
                <div className="mt-4 w-full">
                  <ChartRenderer config={msg.config} />
                </div>
              )}
            </div>
          </div>
        ))}

        {loading && <div className="text-sm text-gray-400">Thinking...</div>}

        <div ref={bottomRef} />
      </div>
    </div>
  );
}
