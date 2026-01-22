"use client";

import { motion } from "motion/react";
import { ArrowRight, Sparkles, TrendingUp } from "lucide-react";
import { AreaChart, Area, ResponsiveContainer } from "recharts";
import { Button } from "./ui/button";
import Link from "next/link";

const chartData = [
    { value: 20 },
    { value: 35 },
    { value: 28 },
    { value: 45 },
    { value: 38 },
    { value: 58 },
    { value: 52 },
    { value: 72 },
    { value: 65 },
    { value: 85 },
];

export function Hero() {
    return (
        <section className="relative min-h-screen flex items-center justify-center pt-20 overflow-hidden">
            {/* Animated Background Elements */}
            <div className="absolute inset-0">
                {/* Gradient Orbs */}
                <motion.div
                    animate={{
                        scale: [1, 1.2, 1],
                        opacity: [0.3, 0.5, 0.3],
                    }}
                    transition={{
                        duration: 8,
                        repeat: Infinity,
                        ease: "easeInOut",
                    }}
                    className="absolute top-1/4 right-1/4 w-96 h-96 bg-[#10B981]/30 rounded-full blur-3xl"
                />
                <motion.div
                    animate={{
                        scale: [1, 1.3, 1],
                        opacity: [0.2, 0.4, 0.2],
                    }}
                    transition={{
                        duration: 10,
                        repeat: Infinity,
                        ease: "easeInOut",
                    }}
                    className="absolute bottom-1/4 left-1/4 w-[500px] h-[500px] bg-[#34D399]/20 rounded-full blur-3xl"
                />

                {/* Grid Pattern */}
                <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.02)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.02)_1px,transparent_1px)] bg-[size:100px_100px]" />
            </div>

            <div className="relative max-w-7xl mx-auto px-6 py-20">
                <div className="grid lg:grid-cols-2 gap-12 items-center">
                    {/* Left Content */}
                    <div className="space-y-8">
                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.6, delay: 0.2 }}
                            className="inline-flex items-center gap-2 px-4 py-2 bg-[#10B981]/10 border border-[#10B981]/30 rounded-full"
                        >
                            <Sparkles className="w-4 h-4 text-[#34D399]" />
                            <span className="text-sm text-[#34D399]">Universal AI Moliyaviy Tizim</span>
                        </motion.div>

                        <motion.h1
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.6, delay: 0.3 }}
                            className="text-5xl md:text-6xl lg:text-7xl font-bold leading-tight"
                        >
                            Moliya Boshqaruvining{" "}
                            <span className="bg-gradient-to-r from-[#10B981] to-[#34D399] bg-clip-text text-transparent">
                                Yangi Darajasi
                            </span>
                        </motion.h1>

                        <motion.p
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.6, delay: 0.4 }}
                            className="text-xl text-gray-300 leading-relaxed"
                        >
                            Shaxsiy byudjet, kichik biznes yoki yirik korporatsiya bo'lishidan qat'i nazar —
                            LQX AI sizning ishonchli moliyaviy maslahatchingiz.
                        </motion.p>

                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.6, delay: 0.5 }}
                            className="flex flex-col sm:flex-row gap-4"
                        >
                            <Link href="/register">
                                <Button
                                    size="lg"
                                    className="group px-8 py-4 bg-gradient-to-r from-[#10B981] to-[#34D399] hover:shadow-2xl hover:shadow-[#10B981]/50 transition-all h-auto"
                                >
                                    Bepul sinab ko'rish
                                    <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                                </Button>
                            </Link>
                            <Link href="#pricing">
                                <Button
                                    size="lg"
                                    variant="outline"
                                    className="px-8 py-4 bg-white/5 border border-white/10 hover:bg-white/10 transition-all backdrop-blur-sm h-auto"
                                >
                                    Narxlarni ko'rish
                                </Button>
                            </Link>
                        </motion.div>

                        {/* Trust Indicators */}
                        <motion.div
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            transition={{ duration: 0.6, delay: 0.6 }}
                            className="flex items-center gap-8 pt-4"
                        >
                            <div>
                                <div className="text-2xl font-bold text-[#34D399]">10,000+</div>
                                <div className="text-sm text-gray-400">Foydalanuvchilar</div>
                            </div>
                            <div className="h-12 w-px bg-white/10" />
                            <div>
                                <div className="text-2xl font-bold text-[#34D399]">$2.4B+</div>
                                <div className="text-sm text-gray-400">Tahlil qilingan</div>
                            </div>
                            <div className="h-12 w-px bg-white/10" />
                            <div>
                                <div className="text-2xl font-bold text-[#34D399]">99.9%</div>
                                <div className="text-sm text-gray-400">Aniqlik</div>
                            </div>
                        </motion.div>
                    </div>

                    {/* Right Content - Animated Chart */}
                    <motion.div
                        initial={{ opacity: 0, scale: 0.9 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ duration: 0.8, delay: 0.4 }}
                        className="relative"
                    >
                        {/* Glassmorphism Card */}
                        <div className="relative p-8 bg-white/5 backdrop-blur-xl border border-white/10 rounded-3xl shadow-2xl">
                            {/* Card Header */}
                            <div className="flex items-center justify-between mb-6">
                                <div>
                                    <h3 className="text-sm text-gray-400 mb-1">Jami daromad</h3>
                                    <div className="flex items-baseline gap-2">
                                        <span className="text-3xl font-bold">$847,392</span>
                                        <span className="text-[#34D399] text-sm font-semibold flex items-center gap-1">
                                            <TrendingUp className="w-4 h-4" />
                                            +32.4%
                                        </span>
                                    </div>
                                </div>
                                <div className="px-3 py-1.5 bg-[#10B981]/20 border border-[#10B981]/30 rounded-lg text-xs text-[#34D399]">
                                    AI optimallashtirilgan
                                </div>
                            </div>

                            {/* Chart */}
                            <div className="h-48">
                                <ResponsiveContainer width="100%" height="100%">
                                    <AreaChart data={chartData}>
                                        <defs>
                                            <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
                                                <stop offset="5%" stopColor="#10B981" stopOpacity={0.3} />
                                                <stop offset="95%" stopColor="#10B981" stopOpacity={0} />
                                            </linearGradient>
                                        </defs>
                                        <Area
                                            type="monotone"
                                            dataKey="value"
                                            stroke="#10B981"
                                            strokeWidth={2}
                                            fill="url(#colorValue)"
                                        />
                                    </AreaChart>
                                </ResponsiveContainer>
                            </div>

                            {/* Floating Stats */}
                            <motion.div
                                animate={{ y: [0, -10, 0] }}
                                transition={{ duration: 3, repeat: Infinity }}
                                className="absolute -top-4 -right-4 px-4 py-3 bg-gradient-to-br from-[#10B981] to-[#34D399] rounded-xl shadow-lg"
                            >
                                <div className="text-xs text-white/80">Oylik o'sish</div>
                                <div className="text-lg font-bold">+28%</div>
                            </motion.div>

                            <motion.div
                                animate={{ y: [0, 10, 0] }}
                                transition={{ duration: 4, repeat: Infinity }}
                                className="absolute -bottom-4 -left-4 px-4 py-3 bg-white/10 backdrop-blur-xl border border-white/20 rounded-xl"
                            >
                                <div className="text-xs text-gray-400">Tejash imkoniyati</div>
                                <div className="text-lg font-bold text-[#34D399]">$12,450</div>
                            </motion.div>
                        </div>
                    </motion.div>
                </div>
            </div>

            {/* Scroll Indicator */}
            <motion.div
                animate={{ y: [0, 10, 0] }}
                transition={{ duration: 2, repeat: Infinity }}
                className="absolute bottom-8 left-1/2 -translate-x-1/2"
            >
                <div className="w-6 h-10 border-2 border-white/20 rounded-full flex justify-center pt-2">
                    <motion.div
                        animate={{ y: [0, 12, 0] }}
                        transition={{ duration: 2, repeat: Infinity }}
                        className="w-1 h-2 bg-[#34D399] rounded-full"
                    />
                </div>
            </motion.div>
        </section>
    );
}