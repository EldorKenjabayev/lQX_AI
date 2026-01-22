"use client";

import { motion } from "motion/react";
import { TrendingUp } from "lucide-react";
import Link from "next/link";
import { Button } from "./ui/button";

export function Navigation() {
    return (
        <motion.nav
            initial={{ y: -100, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ duration: 0.6 }}
            className="fixed top-0 left-0 right-0 z-50 backdrop-blur-md bg-[#0A1628]/80 border-b border-white/10"
        >
            <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
                {/* Logo */}
                <div className="flex items-center gap-3">
                    <div className="relative w-10 h-10 bg-gradient-to-tr from-[#10B981] to-[#34D399] rounded-xl flex items-center justify-center">
                        <TrendingUp className="w-6 h-6 text-white" />
                    </div>
                    <span className="text-xl font-semibold">LQX</span>
                </div>

                {/* Navigation Links */}
                <div className="hidden md:flex items-center gap-8">
                    <a href="#features" className="text-gray-300 hover:text-white transition-colors">
                        Imkoniyatlar
                    </a>
                    <a href="#pricing" className="text-gray-300 hover:text-white transition-colors">
                        Narxlar
                    </a>
                    <a href="#how-it-works" className="text-gray-300 hover:text-white transition-colors">
                        Qanday ishlaydi
                    </a>
                </div>

                {/* CTA Buttons */}
                <div className="flex items-center gap-4">
                    <Link href="/login">
                        <Button
                            variant="ghost"
                            className="hidden md:block px-4 py-2 text-gray-300 hover:text-white transition-colors"
                        >
                            Kirish
                        </Button>
                    </Link>
                    <Link href="/register">
                        <Button
                            className="px-6 py-2.5 bg-gradient-to-r from-[#10B981] to-[#34D399] rounded-lg hover:shadow-lg hover:shadow-[#10B981]/50 transition-all"
                        >
                            Bepul sinab ko'rish
                        </Button>
                    </Link>
                </div>
            </div>
        </motion.nav>
    );
}
