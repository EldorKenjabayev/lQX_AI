"use client";

import React from "react";

import { motion } from "framer-motion";
import { Check, Zap, Star } from "lucide-react";
import { Button } from "./ui/button";
import { Badge } from "./ui/badge";


const plans = [
    {
        id: "individual",
        name: "Individual",
        description: "Shaxsiy moliyaviy nazorat",
        price: { lite: "$3", pro: "$5" },
        period: "/oy",
        features: {
            lite: [
                "Faqat matnli kiritish",
                "Oddiy hisobotlar",
                "Cheklovli tranzaksiyalar",
            ],
            pro: [
                "Fayl yuklash (.pdf, .xls)",
                "Shaxsiy byudjet prognozi",
                "Cheklarni scan qilish",
                "Kengaytirilgan hisobotlar",
            ]
        },
        cta: "Boshlash",
        popular: false,
    },
    {
        id: "small_business",
        name: "Kichik Biznes",
        description: "Kafelar va do'konlar",
        price: { lite: "$10", pro: "$15" },
        period: "/oy",
        features: {
            lite: [
                "Cheklangan tranzaksiyalar",
                "Matnli kiritish",
                "Oddiy statistika",
            ],
            pro: [
                "Fayl yuklash va Integratsiya",
                "Savdo prognozlari (AI)",
                "3-10 kishilik jamoa",
                "Daromad/Xarajat chuqur tahlili",
            ]
        },
        cta: "Sinab ko'rish",
        popular: true,
    },
    {
        id: "medium_business",
        name: "O'rta Biznes",
        description: "O'quv markazlari, Ishlab chiqarish",
        price: { lite: "$25", pro: "$30" },
        period: "/oy",
        features: {
            lite: [
                "Bazaviy ma'lumotlar tahlili",
                "Cheklangan foydalanuvchilar",
                "Standart yordam",
            ],
            pro: [
                "Text-to-Speech (Ovozli kiritish)",
                "Katta ma'lumotlar ($100M+)",
                "Kunlik batafsil AI hisobot",
                "Cheksiz jamoa a'zolari",
            ]
        },
        cta: "Tanlash",
        popular: false,
    },
    {
        id: "enterprise",
        name: "Enterprise",
        description: "Banklar va Venchur Fondlar",
        price: { lite: "Kelishuv", pro: "Kelishuv" },
        period: "",
        features: {
            lite: [
                "API Kirish",
                "Risk Tahlili",
                "Shaxsiy menejer",
            ],
            pro: [
                "To'liq API va Integratsiya",
                "Biznes Sog'lig'i Scoring",
                "Chuqur Likvidlik Tahlili",
                "Maxsus Serverlar",
            ]
        },
        cta: "Bog'lanish",
        popular: false,
    },
];

export function Pricing() {
    const [isPro, setIsPro] = React.useState(true);

    return (
        <section id="pricing" className="relative py-32 px-6">
            {/* Background glow */}
            <div className="absolute inset-0 overflow-hidden">
                <motion.div
                    animate={{ scale: [1, 1.2, 1], opacity: [0.1, 0.2, 0.1] }}
                    transition={{ duration: 10, repeat: Infinity, ease: "easeInOut" }}
                    className="absolute top-1/4 left-1/2 w-96 h-96 -translate-x-1/2 bg-emerald-500/20 rounded-full blur-3xl"
                />
            </div>

            <div className="relative max-w-7xl mx-auto">
                {/* Header */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ duration: 0.6 }}
                    className="text-center mb-24"
                >
                    <div className="inline-block mb-4">
                        <Badge className="bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
                            Moslashuvchan narxlar
                        </Badge>
                    </div>

                    <h2 className="text-4xl md:text-5xl font-bold mb-4">
                        Tarifingizni tanlang
                    </h2>
                    <p className="text-xl text-gray-400 max-w-2xl mx-auto mb-8">
                        Biznesingiz ehtiyojiga mos rejani tanlang
                    </p>

                    {/* Toggle Switch */}
                    <div className="flex items-center justify-center gap-4 bg-white/5 p-1 rounded-xl w-fit mx-auto border border-white/10">
                        <button
                            onClick={() => setIsPro(false)}
                            className={`px-6 py-2 rounded-lg text-sm font-medium transition-all ${!isPro
                                ? "bg-emerald-500 text-white shadow-lg"
                                : "text-gray-400 hover:text-white"
                                }`}
                        >
                            Bazaviy (Lite)
                        </button>
                        <button
                            onClick={() => setIsPro(true)}
                            className={`px-6 py-2 rounded-lg text-sm font-medium transition-all ${isPro
                                ? "bg-emerald-500 text-white shadow-lg"
                                : "text-gray-400 hover:text-white"
                                }`}
                        >
                            To'liq (Pro)
                        </button>
                    </div>
                </motion.div>

                {/* Cards */}
                <div className="grid md:grid-cols-2 xl:grid-cols-4 gap-8">
                    {plans.map((plan, index) => (
                        <motion.div
                            key={plan.id}
                            initial={{ opacity: 0, y: 30 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            viewport={{ once: true }}
                            transition={{ duration: 0.5, delay: index * 0.1 }}
                            className={`relative ${plan.popular ? "md:-mt-8" : ""}`}
                        >
                            {plan.popular && (
                                <Badge className="absolute -top-5 left-1/2 -translate-x-1/2 z-10 flex gap-2 px-4 py-2 bg-gradient-to-r from-emerald-500 to-emerald-400 text-white border-0 shadow-lg">
                                    <Star className="w-4 h-4 fill-white" />
                                    Eng mashhur
                                </Badge>
                            )}

                            <div
                                className={`h-full p-8 rounded-3xl transition-all ${plan.popular
                                    ? "bg-gradient-to-br from-emerald-500/20 to-emerald-400/20 border-2 border-emerald-500 shadow-2xl shadow-emerald-500/30"
                                    : "bg-white/5 backdrop-blur-xl border border-white/10 hover:bg-white/10"
                                    }`}
                            >
                                {/* Title */}
                                <div className="mb-8">
                                    <h3 className="text-2xl font-bold mb-2">{plan.name}</h3>
                                    <p className="text-gray-400 text-sm h-10">{plan.description}</p>
                                </div>

                                {/* Price */}
                                <div className="mb-8">
                                    <div className="flex items-baseline gap-2 mb-1">
                                        <span className="text-4xl font-bold">
                                            {isPro ? plan.price.pro : plan.price.lite}
                                        </span>
                                        <span className="text-gray-400">{plan.period}</span>
                                    </div>
                                    <p className="text-sm text-gray-400">
                                        {isPro ? "To'liq imkoniyatlar" : "Bazaviy imkoniyatlar"}
                                    </p>
                                </div>

                                {/* CTA */}
                                <Button
                                    size="lg"
                                    className={`w-full mb-8 h-auto py-4 rounded-xl ${plan.popular
                                        ? "bg-gradient-to-r from-emerald-500 to-emerald-400 text-white hover:shadow-xl hover:shadow-emerald-500/50"
                                        : "bg-white/10 border border-white/20 text-white hover:bg-white/20"
                                        }`}
                                >
                                    {plan.cta}
                                </Button>

                                {/* Features */}
                                <div className="space-y-4">
                                    {(isPro ? plan.features.pro : plan.features.lite).map((feature) => (
                                        <div key={feature} className="flex gap-3">
                                            <div
                                                className={`w-5 h-5 mt-0.5 flex items-center justify-center rounded-full ${plan.popular ? "bg-emerald-500" : "bg-white/10"
                                                    }`}
                                            >
                                                <Check className="w-3 h-3 text-white" />
                                            </div>
                                            <span className="text-sm text-gray-300">{feature}</span>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </motion.div>
                    ))}
                </div>

                {/* Footer note */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ duration: 0.6, delay: 0.6 }}
                    className="text-center mt-16"
                >
                    <p className="text-gray-400">
                        14 kunlik bepul sinov • Kredit karta talab qilinmaydi • Istalgan vaqtda bekor qilish
                    </p>
                </motion.div>
            </div>
        </section>
    );
}
