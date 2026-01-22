"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { getCookie } from "cookies-next";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { TrendingUp, Building2, GraduationCap, Factory } from "lucide-react";

const businessTypes = [
    {
        id: "savdo",
        label: "Savdo",
        description: "Do'kon, market, chakana savdo",
        icon: Building2,
        color: "from-blue-500 to-cyan-500",
    },
    {
        id: "oquv_markazi",
        label: "O'quv Markazi",
        description: "Maktab, kurs, ta'lim muassasasi",
        icon: GraduationCap,
        color: "from-purple-500 to-pink-500",
    },
    {
        id: "ishlab_chiqarish",
        label: "Ishlab Chiqarish",
        description: "Zavod, fabrika, sanoat",
        icon: Factory,
        color: "from-orange-500 to-red-500",
    },
];

export default function OnboardingPage() {
    const router = useRouter();
    const [selected, setSelected] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);

    const handleSubmit = async () => {
        if (!selected) return;

        setLoading(true);
        const token = getCookie("access_token");

        try {
            const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/me`, {
                method: "PATCH",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
                body: JSON.stringify({ business_type: selected }),
            });

            if (response.ok) {
                router.push("/dashboard");
            } else {
                throw new Error("Update failed");
            }
        } catch (error) {
            console.error("Onboarding failed:", error);
            alert("Xatolik yuz berdi. Iltimos qayta urinib ko'ring.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-[#0A1628] to-[#1A2642] p-6">
            <div className="max-w-4xl w-full">
                {/* Header */}
                <div className="text-center mb-10">
                    <div className="inline-flex items-center gap-3 mb-4">
                        <div className="w-12 h-12 bg-gradient-to-tr from-[#10B981] to-[#34D399] rounded-xl flex items-center justify-center">
                            <TrendingUp className="w-7 h-7 text-white" />
                        </div>
                        <h1 className="text-3xl font-bold">LQX AI</h1>
                    </div>
                    <h2 className="text-2xl font-semibold text-white mb-2">
                        Biznesingiz turini tanlang
                    </h2>
                    <p className="text-gray-400">
                        Bu sizga maxsus tahlil va tavsiyalar olishga yordam beradi
                    </p>
                </div>

                {/* Business Type Cards */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                    {businessTypes.map((type) => {
                        const Icon = type.icon;
                        const isSelected = selected === type.id;

                        return (
                            <Card
                                key={type.id}
                                onClick={() => setSelected(type.id)}
                                className={`p-6 cursor-pointer transition-all hover:scale-105 ${isSelected
                                        ? "border-2 border-[#10B981] bg-[#10B981]/10"
                                        : "border border-white/10 hover:border-white/30"
                                    }`}
                            >
                                <div
                                    className={`w-14 h-14 rounded-xl mb-4 flex items-center justify-center bg-gradient-to-br ${type.color}`}
                                >
                                    <Icon className="w-8 h-8 text-white" />
                                </div>
                                <h3 className="text-xl font-semibold text-white mb-2">
                                    {type.label}
                                </h3>
                                <p className="text-gray-400 text-sm">{type.description}</p>
                            </Card>
                        );
                    })}
                </div>

                {/* Submit Button */}
                <div className="text-center">
                    <Button
                        onClick={handleSubmit}
                        disabled={!selected || loading}
                        className="px-8 py-3 bg-gradient-to-r from-[#10B981] to-[#34D399] hover:shadow-lg hover:shadow-[#10B981]/50 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        {loading ? "Yuklanmoqda..." : "Davom etish"}
                    </Button>
                </div>
            </div>
        </div>
    );
}
