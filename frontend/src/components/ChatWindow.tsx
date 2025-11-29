"use client";

import { useState, useRef, useEffect } from "react";
import { Send, Bot, User, MoreHorizontal, Smile, Paperclip, Plus } from "lucide-react";
import axios from "axios";

interface Message {
    role: "user" | "assistant";
    content: string;
}

export default function ChatWindow() {
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState("");
    const [loading, setLoading] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages, loading]);

    const sendMessage = async () => {
        if (!input.trim()) return;

        const userMessage = input.trim();
        setInput("");
        setMessages((prev) => [...prev, { role: "user", content: userMessage }]);
        setLoading(true);

        try {
            const response = await axios.post("http://localhost:8000/api/v1/chat/", {
                message: userMessage,
                project_id: 1
            });

            setMessages((prev) => [...prev, { role: "assistant", content: response.data.response }]);
        } catch (error) {
            console.error("Error sending message:", error);
            setMessages((prev) => [...prev, { role: "assistant", content: "Sorry, I encountered an error." }]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex flex-col h-full bg-[rgb(var(--background))]">
            {/* Notion Header */}
            <div className="h-12 flex items-center justify-between px-4 border-b border-[rgb(var(--border-color))] sticky top-0 bg-[rgb(var(--background))] z-10">
                <div className="flex items-center gap-2">
                    <div className="text-xl">🤖</div>
                    <h1 className="font-semibold text-[14px] truncate">AI Assistant</h1>
                </div>
                <div className="flex items-center gap-1 text-gray-500">
                    <div className="p-1 hover:bg-[rgb(var(--hover-bg))] rounded cursor-pointer">
                        <span className="text-xs">Share</span>
                    </div>
                    <div className="p-1 hover:bg-[rgb(var(--hover-bg))] rounded cursor-pointer">
                        <MoreHorizontal size={18} />
                    </div>
                </div>
            </div>

            {/* Messages Area */}
            <div className="flex-1 overflow-y-auto px-[15%] py-8 space-y-8">
                {messages.length === 0 && (
                    <div className="flex flex-col items-center justify-center h-full opacity-40">
                        <div className="text-6xl mb-4">✨</div>
                        <h2 className="text-xl font-medium mb-2">How can I help you today?</h2>
                        <p className="text-sm text-center max-w-md">Ask me to research a topic, summarize a document, or draft some content for you.</p>
                    </div>
                )}

                {messages.map((msg, idx) => (
                    <div key={idx} className="flex gap-4 group">
                        <div className="flex-shrink-0 mt-1">
                            {msg.role === "user" ? (
                                <div className="w-6 h-6 bg-orange-500 rounded-[3px] flex items-center justify-center text-white text-xs font-bold">U</div>
                            ) : (
                                <div className="w-6 h-6 bg-blue-500 rounded-[3px] flex items-center justify-center text-white text-xs font-bold">AI</div>
                            )}
                        </div>
                        <div className="flex-1 min-w-0">
                            <div className="flex items-center gap-2 mb-1">
                                <span className="font-semibold text-sm">{msg.role === "user" ? "You" : "Assistant"}</span>
                                <span className="text-xs text-gray-400 opacity-0 group-hover:opacity-100 transition-opacity">12:34 PM</span>
                            </div>
                            <div className="text-[15px] leading-7 whitespace-pre-wrap text-[rgb(var(--foreground))]">
                                {msg.content}
                            </div>
                        </div>
                    </div>
                ))}

                {loading && (
                    <div className="flex gap-4">
                        <div className="w-6 h-6 bg-blue-500 rounded-[3px] flex items-center justify-center text-white text-xs font-bold mt-1">AI</div>
                        <div className="flex items-center gap-1 h-6">
                            <div className="w-1.5 h-1.5 bg-gray-300 rounded-full animate-bounce" />
                            <div className="w-1.5 h-1.5 bg-gray-300 rounded-full animate-bounce delay-75" />
                            <div className="w-1.5 h-1.5 bg-gray-300 rounded-full animate-bounce delay-150" />
                        </div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>

            {/* Input Area */}
            <div className="px-[15%] pb-8 pt-2">
                <div className="relative group">
                    <div className="absolute inset-0 bg-gray-100 rounded-lg -z-10 group-focus-within:bg-white group-focus-within:shadow-[0_0_0_1px_rgba(35,131,226,0.5),0_1px_3px_rgba(0,0,0,0.05)] transition-all border border-transparent group-focus-within:border-blue-200" />
                    <div className="flex items-end p-3 gap-2 border border-gray-200 rounded-lg bg-white shadow-sm focus-within:border-transparent focus-within:shadow-none transition-all">
                        <div className="p-1 text-gray-400 hover:text-gray-600 cursor-pointer">
                            <Plus size={20} />
                        </div>
                        <textarea
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyDown={(e) => {
                                if (e.key === "Enter" && !e.shiftKey) {
                                    e.preventDefault();
                                    sendMessage();
                                }
                            }}
                            placeholder="Type a message..."
                            className="flex-1 bg-transparent border-none focus:ring-0 p-0 text-[15px] resize-none max-h-40 min-h-[24px] py-1"
                            rows={1}
                            style={{ height: 'auto' }}
                        />
                        <div className="flex gap-1">
                            <div className="p-1 text-gray-400 hover:text-gray-600 cursor-pointer">
                                <Smile size={20} />
                            </div>
                            <button
                                onClick={sendMessage}
                                disabled={loading || !input.trim()}
                                className="p-1 text-blue-500 hover:bg-blue-50 rounded disabled:opacity-30 disabled:hover:bg-transparent cursor-pointer"
                            >
                                <Send size={18} />
                            </button>
                        </div>
                    </div>
                    <div className="text-[11px] text-gray-400 mt-2 text-center">
                        AI can make mistakes. Please review generated responses.
                    </div>
                </div>
            </div>
        </div>
    );
}
