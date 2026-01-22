"use client";

import { motion } from "motion/react";
import { Tags, TrendingUp, MessageSquare, AlertTriangle, BarChart3, Sparkles } from "lucide-react";

const features = [
    {
        icon: Tags,
        title: "Aqlli kategoriyalash",
        description: "AI har bir xarajat va daromad manbalarini 99.9% aniqlik bilan avtomatik kategoriyalaydi.",
        gradient: "from-[#10B981] to-[#34D399]",
    },
    {
        icon: TrendingUp,
        title: "Foyda tahlili",
        description: "Daromad oqimlari, foyda marjasi va o'sish imkoniyatlari bo'yicha chuqur tahlillar.",
        gradient: "from-[#34D399] to-[#10B981]",
    },
    {
        icon: MessageSquare,
        title: "AI tavsiyanomalar",
        description: "AI maslahatchimizdandan shaxsiylashtirilgan moliyaviy maslahatlar va optimallashtirish strategiyalarini oling.",
        gradient: "from-[#10B981] to-[#34D399]",
    },
    {
        icon: AlertTriangle,
        title: "Xavfni aniqlash",
        description: "G'ayrioddiy xarajatlar, pul oqimi muammolari va moliyaviy xavflar haqida real vaqtdagi ogohlantirishlar.",
        gradient: "from-[#34D399] to-[#10B981]",
    },
    {
        icon: BarChart3,
        title: "Prognoz va statistika",
        description: "AI modellari yordamida kelajakdagi pul oqimi, daromad tendensiyalari va moliyaviy natijalarni bashorat qiling.",
        gradient: "from-[#10B981] to-[#34D399]",
    },
    {
        icon: Sparkles,
        title: "Avtomatik hisobotlar",
        description: "Har hafta, oy yoki chorakda avtomatik ravishda chiroyli moliyaviy hisobotlar yaratiladi.",
        gradient: "from-[#34D399] to-[#10B981]",
    },
];

export function Features() {
    return (
        <section id="features" className="relative py-32 px-6">
            {/* Background Decoration */}
            <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(16,185,129,0.05),transparent_70%)]" />

            <div className="max-w-7xl mx-auto relative">
                {/* Section Header */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ duration: 0.6 }}
                    className="text-center mb-20"
                >
                    <div className="inline-block px-4 py-2 bg-[#10B981]/10 border border-[#10B981]/30 rounded-full mb-4">
                        <span className="text-sm text-[#34D399]">Kuchli imkoniyatlar</span>
                    </div>
                    <h2 className="text-4xl md:text-5xl font-bold mb-4">Sizga kerak bo'lgan hamma narsa</h2>
                    <p className="text-xl text-gray-400 max-w-2xl mx-auto">
                        Zamonaviy bizneslar uchun mo'ljallangan AI-quvvatli moliyaviy vositalar
                    </p>
                </motion.div>

                {/* Features Grid */}
                <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {features.map((feature, index) => (
                        <motion.div
                            key={index}
                            initial={{ opacity: 0, y: 30 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            viewport={{ once: true }}
                            transition={{ duration: 0.5, delay: index * 0.1 }}
                            className="group"
                        >
                            {/* Feature Card with Glassmorphism */}
                            <div className="h-full p-8 bg-white/5 backdrop-blur-xl border border-white/10 rounded-3xl hover:bg-white/10 transition-all duration-500 hover:border-[#10B981]/50 hover:shadow-2xl hover:shadow-[#10B981]/20 hover:-translate-y-2">
                                {/* Icon */}
                                <div className={`inline-flex w-14 h-14 bg-gradient-to-br ${feature.gradient} rounded-2xl items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-500`}>
                                    <feature.icon className="w-7 h-7 text-white" />
                                </div>

                                {/* Content */}
                                <h3 className="text-xl font-bold mb-3">{feature.title}</h3>
                                <p className="text-gray-400 leading-relaxed">{feature.description}</p>

                                {/* Hover Effect - Learn More */}
                                <div className="mt-4 flex items-center gap-2 text-[#34D399] opacity-0 group-hover:opacity-100 transition-opacity duration-500">
                                    <span className="text-sm font-semibold">Batafsil</span>
                                    <svg width="16" height="16" viewBox="0 0 16 16" fill="none" className="group-hover:translate-x-1 transition-transform">
                                        <path d="M6 12L10 8L6 4" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                                    </svg>
                                </div>
                            </div>
                        </motion.div>
                    ))}
                </div>

                {/* Bottom Feature Highlight */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ duration: 0.6, delay: 0.8 }}
                    className="mt-16 p-8 md:p-12 bg-gradient-to-r from-[#10B981]/10 to-[#34D399]/10 backdrop-blur-xl border border-[#10B981]/30 rounded-3xl"
                >
                    <div className="grid md:grid-cols-2 gap-8 items-center">
                        <div>
                            <h3 className="text-3xl font-bold mb-4">Real vaqtda AI tahlili</h3>
                            <p className="text-gray-300 text-lg leading-relaxed mb-6">
                                Bizning AI tizimimiz har soniyada millionlab ma'lumot nuqtalarini qayta ishlaydi, biznesingiz andozalaridan o'rganib, tobora aniq tahlillar va tavsiyalar taqdim etadi.
                            </p>
                            <div className="flex flex-wrap gap-4">
                                <div className="px-4 py-2 bg-white/5 border border-white/10 rounded-lg">
                                    <div className="text-2xl font-bold text-[#34D399]">&lt; 1s</div>
                                    <div className="text-sm text-gray-400">Tahlil vaqti</div>
                                </div>
                                <div className="px-4 py-2 bg-white/5 border border-white/10 rounded-lg">
                                    <div className="text-2xl font-bold text-[#34D399]">24/7</div>
                                    <div className="text-sm text-gray-400">Monitoring</div>
                                </div>
                                <div className="px-4 py-2 bg-white/5 border border-white/10 rounded-lg">
                                    <div className="text-2xl font-bold text-[#34D399]">100%</div>
                                    <div className="text-sm text-gray-400">Avtomatlashtirilgan</div>
                                </div>
                            </div>
                        </div>
                        <div className="relative h-64 md:h-auto">
                            <div className="absolute inset-0 bg-gradient-to-br from-[#10B981]/20 to-[#34D399]/20 rounded-2xl flex items-center justify-center">
                                <div className="text-center">
                                    <div className="text-6xl font-bold text-[#34D399] mb-2">AI</div>
                                    <div className="text-gray-300">Quvvatli tahlil</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </motion.div>
            </div>
        </section>
    );
}