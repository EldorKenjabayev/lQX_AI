"use client";

import { useState, useRef, useEffect } from "react";
import { Send, User, Bot, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";
import api from "@/lib/api";

interface Message {
    role: "user" | "assistant";
    content: string;
}

export default function ChatPage() {
    const [messages, setMessages] = useState<Message[]>([
        { role: "assistant", content: "Assalomu alaykum! Men sizning moliyaviy maslahatchingizman. Bugun sizga qanday yordam bera olaman?" }
    ]);
    const [input, setInput] = useState("");
    const [loading, setLoading] = useState(false);
    const scrollRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollIntoView({ behavior: "smooth" });
        }
    }, [messages]);

    const handleSend = async () => {
        if (!input.trim() || loading) return;

        const userMessage = input.trim();
        setInput("");
        setMessages(prev => [...prev, { role: "user", content: userMessage }]);
        setLoading(true);

        try {
            // 1. Get current balance for context (optional but helpful)
            const dashRes = await api.get("/analytics/dashboard?filter_type=this_month");
            const currentBal = dashRes.data.data.current_balance || 0;

            // 2. Call Chat endpoint
            const res = await api.post("/chat/ask", {
                message: userMessage,
                initial_balance: currentBal
            });

            const aiResponse = res.data.response;

            // 3. Add AI message
            setMessages(prev => [...prev, {
                role: "assistant",
                content: aiResponse
            }]);

        } catch (error) {
            console.error("Chat error:", error);
            setMessages(prev => [...prev, {
                role: "assistant",
                content: "Uzr, tizimda xatolik yuz berdi. Iltimos keyinroq urinib ko'ring."
            }]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex flex-col h-[calc(100vh-64px)] bg-[#0A1628]">
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
                {messages.map((m, i) => (
                    <div
                        key={i}
                        className={cn(
                            "flex items-start gap-4 max-w-3xl mx-auto",
                            m.role === "user" ? "flex-row-reverse" : "flex-row"
                        )}
                    >
                        <div className={cn(
                            "w-8 h-8 rounded-full flex items-center justify-center shrink-0",
                            m.role === "user" ? "bg-violet-600" : "bg-[#10B981]"
                        )}>
                            {m.role === "user" ? <User className="w-5 h-5 text-white" /> : <Bot className="w-5 h-5 text-white" />}
                        </div>
                        <div className={cn(
                            "p-4 rounded-2xl max-w-[80%] text-white",
                            m.role === "user" ? "bg-violet-600 rounded-tr-none" : "bg-[#1A2642] rounded-tl-none border border-white/10"
                        )}>
                            {m.content}
                        </div>
                    </div>
                ))}
                {loading && (
                    <div className="flex items-start gap-4 max-w-3xl mx-auto">
                        <div className="w-8 h-8 rounded-full bg-[#10B981] flex items-center justify-center shrink-0">
                            <Bot className="w-5 h-5 text-white" />
                        </div>
                        <div className="bg-[#1A2642] p-4 rounded-2xl rounded-tl-none border border-white/10 flex items-center gap-2">
                            <Loader2 className="w-4 h-4 text-[#10B981] animate-spin" />
                            <span className="text-gray-400 text-sm">O'ylamoqda...</span>
                        </div>
                    </div>
                )}
                <div ref={scrollRef} />
            </div>

            <div className="p-4 bg-[#1A2642] border-t border-white/10">
                <div className="max-w-3xl mx-auto flex gap-4">
                    <Input
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={(e) => e.key === "Enter" && handleSend()}
                        placeholder="Savolingizni yozing..."
                        className="bg-[#0A1628] border-white/10 text-white focus-visible:ring-violet-600"
                    />
                    <Button onClick={handleSend} disabled={loading || !input.trim()} className="bg-violet-600 hover:bg-violet-700">
                        <Send className="w-5 h-5" />
                    </Button>
                </div>
            </div>
        </div>
    );
}
