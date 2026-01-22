"use client";

import { motion } from "motion/react";
import { Upload, ArrowRight } from "lucide-react";
import Link from "next/link";
import { Button } from "@/components/ui/button";

export function EmptyDashboard() {
    return (
        <div className="flex flex-col items-center justify-center min-h-[60vh] text-center p-8">
            <motion.div
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.5 }}
                className="relative mb-8"
            >
                <div className="absolute inset-0 bg-[#10B981] blur-[100px] opacity-20 rounded-full w-64 h-64 mx-auto" />
                <img
                    src="/assets/empty-state.svg" // Placeholder, we can use an icon if no image
                    alt=""
                    className="w-64 h-64 relative z-10 hidden" // Hiding image for now as we don't have it
                />
                <div className="w-40 h-40 bg-gradient-to-tr from-[#10B981] to-[#34D399] rounded-3xl rotate-12 flex items-center justify-center shadow-2xl shadow-[#10B981]/20 mx-auto relative z-10">
                    <Upload className="w-20 h-20 text-white" />
                </div>
            </motion.div>

            <motion.h2
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 }}
                className="text-3xl font-bold text-white mb-4"
            >
                LQX AI ga Xush Kelibsiz! 🚀
            </motion.h2>

            <motion.p
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 }}
                className="text-gray-400 max-w-md mb-8 text-lg"
            >
                Hozircha hech qanday ma'lumot yo'q. Tahlilni boshlash uchun bank ko'chirmasini yoki Excel faylni yuklang. AI soniyalar ichida hisobot tayyorlaydi.
            </motion.p>

            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.4 }}
            >
                <Link href="/dashboard/upload">
                    <Button className="bg-gradient-to-r from-[#10B981] to-[#34D399] hover:opacity-90 text-white px-8 py-6 text-lg rounded-xl shadow-lg shadow-[#10B981]/20 group">
                        Ma'lumot Yuklash
                        <ArrowRight className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" />
                    </Button>
                </Link>
            </motion.div>
        </div>
    );
}
