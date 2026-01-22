"use client";

import { motion } from "motion/react";
import { X, Check, Zap } from "lucide-react";

const comparisonData = [
    {
        feature: "Sozlash vaqti",
        traditional: "Soatlab qo'lda sozlash",
        ai: "AI avtomatlashtirish bilan daqiqalar",
    },
    {
        feature: "Kategoriyalash",
        traditional: "Qo'lda belgilash kerak",
        ai: "99.9% avtomatik kategoriyalash",
    },
    {
        feature: "Tahlillar",
        traditional: "Oddiy grafik va jadvallar",
        ai: "Chuqur AI-quvvatli tahlil",
    },
    {
        feature: "Prognoz",
        traditional: "Mavjud emas",
        ai: "Bashoratlovchi AI modellari",
    },
    {
        feature: "Tavsiyalar",
        traditional: "Yo'q",
        ai: "Shaxsiylashtirilgan AI maslahatlari",
    },
    {
        feature: "Xatolarni aniqlash",
        traditional: "Qo'lda tekshirish kerak",
        ai: "Real vaqtda AI monitoring",
    },
];

export function AIAdvantage() {
    return (
        <section className="relative py-32 px-6">
            <div className="max-w-7xl mx-auto">
                {/* Section Header */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ duration: 0.6 }}
                    className="text-center mb-20"
                >
                    <div className="inline-block px-4 py-2 bg-[#10B981]/10 border border-[#10B981]/30 rounded-full mb-4">
                        <span className="text-sm text-[#34D399]">AI va an'anaviy usullar</span>
                    </div>
                    <h2 className="text-4xl md:text-5xl font-bold mb-4">
                        AI nima uchun Exceldan ustun
                    </h2>
                    <p className="text-xl text-gray-400 max-w-2xl mx-auto">
                        Qo'lda buxgalteriya bilan vaqt sarflamang. Og'ir ishni AI ga qoldiring.
                    </p>
                </motion.div>

                {/* Comparison Table */}
                <motion.div
                    initial={{ opacity: 0, y: 30 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ duration: 0.6, delay: 0.2 }}
                    className="max-w-5xl mx-auto"
                >
                    <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-3xl overflow-hidden">
                        {/* Table Header */}
                        <div className="grid grid-cols-3 gap-4 p-6 md:p-8 border-b border-white/10">
                            <div className="text-gray-400">Xususiyat</div>
                            <div className="text-center">
                                <div className="inline-flex items-center gap-2 text-gray-400">
                                    <X className="w-4 h-4" />
                                    An'anaviy vositalar
                                </div>
                            </div>
                            <div className="text-center">
                                <div className="inline-flex items-center gap-2 px-3 py-1.5 bg-gradient-to-r from-[#10B981] to-[#34D399] rounded-full">
                                    <Zap className="w-4 h-4 text-white fill-white" />
                                    <span className="font-semibold text-white">LQX AI</span>
                                </div>
                            </div>
                        </div>

                        {/* Table Rows */}
                        {comparisonData.map((row, index) => (
                            <motion.div
                                key={index}
                                initial={{ opacity: 0, x: -20 }}
                                whileInView={{ opacity: 1, x: 0 }}
                                viewport={{ once: true }}
                                transition={{ duration: 0.4, delay: index * 0.1 }}
                                className={`grid grid-cols-3 gap-4 p-6 md:p-8 ${index !== comparisonData.length - 1 ? 'border-b border-white/10' : ''
                                    } hover:bg-white/5 transition-colors`}
                            >
                                <div className="font-semibold">{row.feature}</div>
                                <div className="text-center text-gray-400 text-sm flex items-center justify-center gap-2">
                                    <X className="w-4 h-4 text-red-400 flex-shrink-0" />
                                    <span>{row.traditional}</span>
                                </div>
                                <div className="text-center text-[#34D399] text-sm flex items-center justify-center gap-2">
                                    <Check className="w-4 h-4 flex-shrink-0" />
                                    <span className="font-semibold">{row.ai}</span>
                                </div>
                            </motion.div>
                        ))}
                    </div>
                </motion.div>

                {/* Stats Grid */}
                <motion.div
                    initial={{ opacity: 0, y: 30 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ duration: 0.6, delay: 0.6 }}
                    className="grid md:grid-cols-3 gap-6 mt-16"
                >
                    <div className="p-8 bg-gradient-to-br from-[#10B981]/10 to-[#34D399]/10 backdrop-blur-xl border border-[#10B981]/30 rounded-3xl text-center">
                        <div className="text-5xl font-bold text-[#34D399] mb-2">10x</div>
                        <div className="text-gray-300">Tezroq moliyaviy tahlillar</div>
                    </div>
                    <div className="p-8 bg-gradient-to-br from-[#10B981]/10 to-[#34D399]/10 backdrop-blur-xl border border-[#10B981]/30 rounded-3xl text-center">
                        <div className="text-5xl font-bold text-[#34D399] mb-2">+32%</div>
                        <div className="text-gray-300">O'rtacha foyda optimizatsiyasi</div>
                    </div>
                    <div className="p-8 bg-gradient-to-br from-[#10B981]/10 to-[#34D399]/10 backdrop-blur-xl border border-[#10B981]/30 rounded-3xl text-center">
                        <div className="text-5xl font-bold text-[#34D399] mb-2">95%</div>
                        <div className="text-gray-300">Buxgalteriyada tejalgan vaqt</div>
                    </div>
                </motion.div>
            </div>
        </section>
    );
}
