"use client";

import { useSession } from "next-auth/react";
import { useState } from "react";
import ChatHeader from "./ChatHeader";
import ChatMessages from "./ChatMessages";
import ChatInput from "./ChatInput";
import { Message } from "../types";

export default function ChatLayout() {
  const { data: session } = useSession();
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);

  function cleanText(text: string) {
  return text.replace(/```json[\s\S]*?```/g, "").trim();
}

  const handleSend = async (query: string, file?: File | null) => {
  if (!query.trim() && !file) return;

  const userMsg: Message = {
    role: "user",
    content: file ? `${query}\n📎 ${file.name}` : query,
  };

  setMessages((prev) => [...prev, userMsg]);
  setLoading(true);

  try {
    const formData = new FormData();
    formData.append("query", query);
    formData.append("userId", session?.user?.id || "");

    if (file) {
      formData.append("file", file);
    }

    const res = await fetch(
      `${process.env.NEXT_PUBLIC_API_URL}/v1/conversation/query`,
      {
        method: "POST",
        body: formData, 
      }
    );

    const data = await res.json();
    if (!data.success) throw new Error(data.error);

    const payload = data.data;

    let botMsg: Message = { role: "assistant" };

    if (payload.type === "text") botMsg.content = payload.text;
    if (payload.type === "chart") botMsg.configs = payload.charts;
    if (payload.type === "both") {
      botMsg.content = cleanText(payload.text);
      botMsg.configs = payload.charts;
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
