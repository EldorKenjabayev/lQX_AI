"use client";

import { motion } from "framer-motion";
import {
    ArrowRight,
    Sparkles,
    TrendingUp,
    CheckCircle,
} from "lucide-react";

import { Button } from "./ui/button";
import Link from "next/link";
import { Badge } from "./ui/badge";

export function FinalCTA() {
    return (
        <section className="relative py-32 px-6 overflow-hidden">
            {/* Background */}
            <div className="absolute inset-0">
                <motion.div
                    animate={{ scale: [1, 1.2, 1], opacity: [0.2, 0.4, 0.2] }}
                    transition={{ duration: 8, repeat: Infinity, ease: "easeInOut" }}
                    className="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[800px] bg-emerald-500/20 rounded-full blur-3xl"
                />
            </div>

            <div className="max-w-5xl mx-auto relative">
                <motion.div
                    initial={{ opacity: 0, y: 30 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ duration: 0.6 }}
                    className="p-12 md:p-16 bg-gradient-to-br from-emerald-500/20 to-emerald-400/20 backdrop-blur-xl border border-emerald-500/30 rounded-3xl text-center relative"
                >
                    <div className="relative z-10">
                        {/* Badge */}
                        <motion.div
                            initial={{ scale: 0 }}
                            whileInView={{ scale: 1 }}
                            viewport={{ once: true }}
                            transition={{ duration: 0.5, delay: 0.2 }}
                        >
                            <Badge className="inline-flex items-center gap-2 px-4 py-2 mb-6 bg-emerald-500/20 border border-emerald-500/40 text-emerald-400">
                                <Sparkles className="w-4 h-4" />
                                14 kunlik bepul sinov
                            </Badge>
                        </motion.div>

                        {/* Title */}
                        <motion.h2
                            initial={{ opacity: 0, y: 20 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            viewport={{ once: true }}
                            transition={{ duration: 0.6, delay: 0.3 }}
                            className="text-4xl md:text-6xl font-bold mb-6"
                        >
                            Moliyaviy Kelajagingizni Bugun Boshqaring
                        </motion.h2>

                        {/* Subtitle */}
                        <motion.p
                            initial={{ opacity: 0, y: 20 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            viewport={{ once: true }}
                            transition={{ duration: 0.6, delay: 0.4 }}
                            className="text-xl text-gray-300 mb-10 max-w-2xl mx-auto"
                        >
                            Individual foydalanuvchilar, tadbirkorlar va yirik kompaniyalar uchun yagona yechim.
                            To'g'ri moliyaviy qarorlar qabul qilishni hozirdan boshlang.
                        </motion.p>

                        {/* Buttons */}
                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            viewport={{ once: true }}
                            transition={{ duration: 0.6, delay: 0.5 }}
                            className="flex flex-col sm:flex-row gap-4 justify-center"
                        >
                            <Link href="/register">
                                <Button
                                    size="lg"
                                    className="group px-8 py-4 h-auto bg-gradient-to-r from-emerald-500 to-emerald-400"
                                >
                                    Bepul sinab ko'rish
                                    <ArrowRight className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" />
                                </Button>
                            </Link>

                            <Link href="/register">
                                <Button
                                    size="lg"
                                    variant="outline"
                                    className="px-8 py-4 h-auto bg-white/10 border-white/20"
                                >
                                    Demo ko'rish
                                </Button>
                            </Link>
                        </motion.div>

                        {/* Trust */}
                        <motion.div
                            initial={{ opacity: 0 }}
                            whileInView={{ opacity: 1 }}
                            viewport={{ once: true }}
                            transition={{ duration: 0.6, delay: 0.6 }}
                            className="flex flex-col sm:flex-row justify-center gap-6 mt-10 text-sm text-gray-400"
                        >
                            {[
                                "Kredit karta talab qilinmaydi",
                                "Istalgan vaqtda bekor qilish",
                                "5 daqiqada sozlash",
                            ].map((text) => (
                                <div key={text} className="flex items-center gap-2">
                                    <CheckCircle className="w-5 h-5 text-emerald-400" />
                                    {text}
                                </div>
                            ))}
                        </motion.div>
                    </div>
                </motion.div>
            </div>
        </section>
    );
}
