"use client";

import { motion } from "motion/react";
import { Upload, Brain, Lightbulb, ArrowRight } from "lucide-react";

const steps = [
    {
        icon: Upload,
        title: "Ma'lumotlarni yuklang yoki ulang",
        description: "Bank, buxgalteriya dasturi yoki jadvallardan daromad va xarajat ma'lumotlarini osonlik bilan import qiling.",
        color: "from-[#10B981] to-[#34D399]",
    },
    {
        icon: Brain,
        title: "AI pul oqimini tahlil qiladi",
        description: "Bizning ilg'or AI tizimimiz moliyaviy ma'lumotlaringizni qayta ishlaydi, tendensiyalar va anomaliyalarni real vaqtda aniqlaydi.",
        color: "from-[#34D399] to-[#10B981]",
    },
    {
        icon: Lightbulb,
        title: "Aqlli tavsiyalar oling",
        description: "Biznesingiz moliyasini optimallashtirish uchun amaliy maslahatlar, prognozlar va tavsiyalar oling.",
        color: "from-[#10B981] to-[#34D399]",
    },
];

export function HowItWorks() {
    return (
        <section id="how-it-works" className="relative py-32 px-6">
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
                        <span className="text-sm text-[#34D399]">Oddiy va kuchli</span>
                    </div>
                    <h2 className="text-4xl md:text-5xl font-bold mb-4">Qanday ishlaydi</h2>
                    <p className="text-xl text-gray-400 max-w-2xl mx-auto">
                        AI yordamida moliyaviy boshqaruvingizni o'zgartirish uchun uchta oddiy qadam
                    </p>
                </motion.div>

                {/* Steps */}
                <div className="relative">
                    {/* Connection Lines */}
                    <div className="hidden lg:block absolute top-1/2 left-0 right-0 h-0.5 bg-gradient-to-r from-[#10B981]/20 via-[#34D399]/20 to-[#10B981]/20" />

                    <div className="grid md:grid-cols-3 gap-8 lg:gap-12 relative">
                        {steps.map((step, index) => (
                            <motion.div
                                key={index}
                                initial={{ opacity: 0, y: 30 }}
                                whileInView={{ opacity: 1, y: 0 }}
                                viewport={{ once: true }}
                                transition={{ duration: 0.6, delay: index * 0.2 }}
                                className="relative"
                            >
                                {/* Card */}
                                <div className="group p-8 bg-white/5 backdrop-blur-xl border border-white/10 rounded-3xl hover:bg-white/10 transition-all duration-500 hover:border-[#10B981]/50 hover:shadow-2xl hover:shadow-[#10B981]/20">
                                    {/* Icon */}
                                    <div className="relative mb-6">
                                        <div className={`w-16 h-16 bg-gradient-to-br ${step.color} rounded-2xl flex items-center justify-center group-hover:scale-110 transition-transform duration-500`}>
                                            <step.icon className="w-8 h-8 text-white" />
                                        </div>
                                        {/* Step Number */}
                                        <div className="absolute -top-2 -right-2 w-8 h-8 bg-[#0F172A] border-2 border-[#10B981] rounded-full flex items-center justify-center text-sm font-bold text-[#34D399]">
                                            {index + 1}
                                        </div>
                                    </div>

                                    {/* Content */}
                                    <h3 className="text-xl font-bold mb-3">{step.title}</h3>
                                    <p className="text-gray-400 leading-relaxed">{step.description}</p>

                                    {/* Arrow for desktop */}
                                    {index < steps.length - 1 && (
                                        <motion.div
                                            animate={{ x: [0, 10, 0] }}
                                            transition={{ duration: 2, repeat: Infinity }}
                                            className="hidden lg:block absolute -right-6 top-1/2 -translate-y-1/2"
                                        >
                                            <ArrowRight className="w-6 h-6 text-[#34D399]/50" />
                                        </motion.div>
                                    )}
                                </div>
                            </motion.div>
                        ))}
                    </div>
                </div>

                {/* Bottom CTA */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ duration: 0.6, delay: 0.8 }}
                    className="text-center mt-16"
                >
                    <button className="group px-8 py-4 bg-gradient-to-r from-[#10B981] to-[#34D399] rounded-xl font-semibold hover:shadow-2xl hover:shadow-[#10B981]/50 transition-all flex items-center justify-center gap-2 mx-auto">
                        Hoziroq boshlang
                        <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                    </button>
                </motion.div>
            </div>
        </section>
    );
}
