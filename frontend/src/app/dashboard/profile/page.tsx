"use client";

import { useState, useEffect } from "react";
import { User, Mail, Briefcase, Save, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useAuth } from "@/components/providers/auth-provider";
import api from "@/lib/api";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";
import { cn } from "@/lib/utils";

export default function ProfilePage() {
    const { user } = useAuth();
    const [isLoading, setIsLoading] = useState(false);
    const [businessType, setBusinessType] = useState(user?.business_type || "");
    const [message, setMessage] = useState<{ type: "success" | "error", text: string } | null>(null);

    // Sync user data when it loads
    useEffect(() => {
        if (user?.business_type) {
            setBusinessType(user.business_type);
        }
    }, [user]);

    const handleUpdate = async () => {
        setIsLoading(true);
        setMessage(null);
        try {
            await api.patch("/auth/me", { business_type: businessType });
            setMessage({ type: "success", text: "Ma'lumotlar muvaffaqiyatli yangilandi!" });
        } catch (error) {
            console.error(error);
            setMessage({ type: "error", text: "Xatolik yuz berdi. Qaytadan urinib ko'ring." });
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-[#0A1628] to-[#1A2642] p-6">
            <div className="max-w-2xl mx-auto">
                <div className="mb-8">
                    <h1 className="text-3xl font-bold text-white mb-2">Profil Sozlamalari</h1>
                    <p className="text-gray-400">Shaxsiy ma'lumotlaringizni boshqaring</p>
                </div>

                <div className="bg-[#1A2642] border border-white/10 rounded-xl p-8 space-y-6">
                    {/* User Info Read-only */}
                    <div className="space-y-4">
                        <div className="flex flex-col space-y-2">
                            <label className="text-sm font-medium text-gray-300">Email</label>
                            <div className="relative">
                                <Mail className="absolute left-3 top-2.5 h-4 w-4 text-gray-400" />
                                <Input disabled value={user?.email || ""} className="pl-9 bg-[#0A1628] border-white/10 text-white cursor-not-allowed opacity-70" />
                            </div>
                        </div>

                        <div className="flex flex-col space-y-2">
                            <label className="text-sm font-medium text-gray-300">ID</label>
                            <div className="relative">
                                <User className="absolute left-3 top-2.5 h-4 w-4 text-gray-400" />
                                <Input disabled value={user?.id || ""} className="pl-9 bg-[#0A1628] border-white/10 text-white cursor-not-allowed opacity-70" />
                            </div>
                        </div>
                    </div>

                    <div className="h-px bg-white/10 my-6" />

                    {/* Editable Fields */}
                    <div className="space-y-4">
                        <div className="flex flex-col space-y-2">
                            <label className="text-sm font-medium text-white">Biznes Turi</label>
                            <Select value={businessType} onValueChange={setBusinessType}>
                                <SelectTrigger className="bg-[#0A1628] border-white/10 text-white">
                                    <SelectValue placeholder="Biznes turini tanlang" />
                                </SelectTrigger>
                                <SelectContent className="bg-[#1A2642] border-white/10 text-white">
                                    <SelectItem value="savdo">Savdo (Do'kon, Market)</SelectItem>
                                    <SelectItem value="oquv_markazi">O'quv Markazi</SelectItem>
                                    <SelectItem value="ishlab_chiqarish">Ishlab Chiqarish</SelectItem>
                                </SelectContent>
                            </Select>
                            <p className="text-xs text-gray-400">
                                Bu ma'lumot AI bashoratlari aniqligini oshirish uchun ishlatiladi.
                            </p>
                        </div>
                    </div>

                    {message && (
                        <div className={cn("p-3 rounded-lg text-sm", message.type === "success" ? "bg-green-500/10 text-green-500" : "bg-red-500/10 text-red-500")}>
                            {message.text}
                        </div>
                    )}

                    <Button
                        onClick={handleUpdate}
                        disabled={isLoading}
                        className="w-full bg-gradient-to-r from-violet-600 to-indigo-600 hover:opacity-90"
                    >
                        {isLoading ? <Loader2 className="w-4 h-4 animate-spin mr-2" /> : <Save className="w-4 h-4 mr-2" />}
                        Saqlash
                    </Button>
                </div>
            </div>
        </div>
    );
}
