"use client";

import { useState } from "react";
import ChatHeader from "./ChatHeader";
import ChatMessages from "./ChatMessages";
import ChatInput from "./ChatInput";
import { Message } from "../types";

export default function ChatLayout() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);

  function cleanText(text: string) {
  return text.replace(/```json[\s\S]*?```/g, "").trim();
}

  const handleSend = async (query: string) => {
    if (!query.trim()) return;

    const userMsg: Message = {
      role: "user",
      content: query,
    };

    setMessages((prev) => [...prev, userMsg]);
    setLoading(true);

    try {
      const res = await fetch("http://localhost:8000/v1/conversation/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });

      const data = await res.json();

      if (!data.success) throw new Error(data.error);

      const payload = data.data;

      let botMsg: Message = {
        role: "assistant",
      };

      if (payload.type === "text") {
        botMsg.content = payload.text;
      }

      if (payload.type === "chart") {
        botMsg.config = payload.chart;
      }

      if (payload.type === "both") {
        botMsg.content = cleanText(payload.text); 
        botMsg.config = payload.chart;
      }

      setMessages((prev) => [...prev, botMsg]);
    } catch (err: any) {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: err.message },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="h-screen flex flex-col bg-white text-black">
      <ChatHeader />

      <div className="flex-1 overflow-hidden">
        <ChatMessages messages={messages} loading={loading} />
      </div>

      <ChatInput onSend={handleSend} loading={loading} />
    </div>
  );
}
