"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { cn } from "@/lib/utils"
import { LayoutDashboard, Receipt, MessageSquare, PieChart, Upload, LogOut, Settings } from "lucide-react"
import { useAuth } from "@/components/providers/auth-provider"
import { Button } from "@/components/ui/button"

const routes = [
    {
        label: "Bosh Sahifa",
        icon: LayoutDashboard,
        href: "/dashboard",
        color: "text-sky-500",
    },
    {
        label: "Ma'lumot Yuklash",
        icon: Upload,
        href: "/dashboard/upload",
        color: "text-violet-500",
    },
    {
        label: "Tranzaksiyalar",
        icon: Receipt,
        href: "/dashboard/transactions",
        color: "text-green-500",
    },
    {
        label: "Bashorat",
        icon: PieChart,
        href: "/dashboard/forecast",
        color: "text-pink-700",
    },
    {
        label: "Maslahatchi",
        icon: MessageSquare,
        href: "/dashboard/chat",
        color: "text-orange-700",
    },
]

export function Sidebar() {
    const { user, logout } = useAuth()
    const pathname = usePathname()

    return (
        <div className="space-y-4 py-4 flex flex-col h-full bg-[#0A1628]/50 backdrop-blur-xl border-r border-white/10 text-white">
            <div className="px-3 py-2 flex-1">
                <Link href="/dashboard" className="flex items-center pl-3 mb-14">
                    <h1 className="text-2xl font-bold bg-gradient-to-r from-[#10B981] to-[#34D399] bg-clip-text text-transparent">
                        LQX AI
                    </h1>
                </Link>
                <div className="space-y-1">
                    {routes.map((route) => (
                        <Link
                            key={route.href}
                            href={route.href}
                            className={cn(
                                "text-sm group flex p-3 w-full justify-start font-medium cursor-pointer hover:text-white hover:bg-white/10 rounded-lg transition",
                                pathname === route.href ? "text-white bg-[#10B981]/10 border border-[#10B981]/20" : "text-zinc-400"
                            )}
                        >
                            <div className="flex items-center flex-1">
                                <route.icon className={cn("h-5 w-5 mr-3", pathname === route.href ? "text-[#34D399]" : route.color)} />
                                {route.label}
                            </div>
                        </Link>
                    ))}
                </div>
            </div>

            {/* User Profile Section */}
            <div className="px-3 py-2 border-t border-white/10">
                <div className="flex items-center gap-3 px-3 py-3 mb-2">
                    <div className="w-10 h-10 rounded-full bg-[#10B981]/20 flex items-center justify-center text-[#10B981] font-bold">
                        {user?.email?.[0].toUpperCase() || "U"}
                    </div>
                    <div className="flex-1 overflow-hidden">
                        <p className="text-sm font-medium text-white truncate">{user?.email}</p>
                        <p className="text-xs text-gray-400 truncate capitalize">{user?.business_type || "User"}</p>
                    </div>
                </div>

                <Link href="/dashboard/profile">
                    <Button variant="ghost" className="w-full justify-start text-zinc-400 hover:text-white hover:bg-white/10">
                        <Settings className="h-5 w-5 mr-3 text-gray-400" />
                        Sozlamalar
                    </Button>
                </Link>

                <Button
                    variant="ghost"
                    className="w-full justify-start text-red-400 hover:text-red-300 hover:bg-red-500/10"
                    onClick={logout}
                >
                    <LogOut className="h-5 w-5 mr-3" />
                    Chiqish
                </Button>
            </div>
        </div>
    )
}
