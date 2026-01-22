"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import api, { DashboardData } from "@/lib/api";
import {
    BarChart3,
    TrendingUp,
    DollarSign,
    ArrowUpRight,
    ArrowDownRight,
    LogOut,
    Calendar,
    Filter,
    Clock,
    PieChart,
    Activity
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { useAuth } from "@/components/providers/auth-provider";
import { TrendChart } from "@/components/dashboard/charts/trend-chart";
import { CategoryPieChart } from "@/components/dashboard/charts/category-pie-chart";
import { EmptyDashboard } from "@/components/dashboard/empty-dashboard";
import { StatsCards } from "@/components/dashboard/stats-cards";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";
import { motion } from "motion/react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

// Simple Recent Transactions Component
function RecentTransactions({ limit = 5 }: { limit?: number }) {
    const [transactions, setTransactions] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        async function fetchTransactions() {
            try {
                const response = await api.getTransactions();
                // Backend returns array directly, not wrapped
                const items = Array.isArray(response) ? response : (response.items || []);
                setTransactions(items.slice(0, limit));
            } catch (error) {
                console.error('Failed to fetch transactions:', error);
            } finally {
                setLoading(false);
            }
        }
        fetchTransactions();
    }, [limit]);

    if (loading) {
        return <p className="text-gray-500 text-center py-4">Yuklanmoqda...</p>;
    }

    if (transactions.length === 0) {
        return <p className="text-gray-500 text-center py-4">Tranzaksiyalar yo'q</p>;
    }

    return (
        <div className="space-y-2">
            {transactions.map((txn, i) => (
                <div key={i} className="flex items-center justify-between p-3 rounded-lg bg-white/5 hover:bg-white/10 transition-colors">
                    <div className="flex items-center gap-3">
                        <div className={`w-2 h-2 rounded-full ${txn.is_expense ? 'bg-red-500' : 'bg-green-500'}`} />
                        <div>
                            <p className="text-sm font-medium text-gray-200">{txn.description}</p>
                            <p className="text-xs text-gray-500">{new Date(txn.date).toLocaleDateString('uz-UZ')}</p>
                        </div>
                    </div>
                    <p className={`text-sm font-semibold font-mono ${txn.is_expense ? 'text-red-400' : 'text-green-400'}`}>
                        {txn.is_expense ? '-' : '+'}{new Intl.NumberFormat('uz-UZ').format(txn.amount)}
                    </p>
                </div>
            ))}
        </div>
    );
}

export default function DashboardPage() {
    const { user, logout } = useAuth();
    const router = useRouter();

    // State
    const [dashboardData, setDashboardData] = useState<DashboardData | null>(null);
    const [loading, setLoading] = useState(true);
    const [filterType, setFilterType] = useState("this_year"); // Default to 2026 support
    const [categories, setCategories] = useState<string[]>([]);
    const [selectedCategory, setSelectedCategory] = useState<string | null>(null);

    // Fetch Filter Options (Categories)
    useEffect(() => {
        const fetchCategories = async () => {
            try {
                const options = await api.getFilterOptions();
                if (options && options.categories) {
                    setCategories(options.categories);
                }
            } catch (error) {
                console.error("Categories fetch error:", error);
            }
        };

        if (user) {
            fetchCategories();
        }
    }, [user]);

    // Fetch Dashboard Data
    useEffect(() => {
        const fetchDashboardData = async () => {
            try {
                setLoading(true);
                // Construct query with category if selected
                const query = new URLSearchParams({
                    filter_type: filterType,
                    ...(selectedCategory && selectedCategory !== "all" && { category: selectedCategory })
                }).toString();

                // Using generic get for flexibility as we updated api.ts but want to be sure
                const response = await api.get<{ success: boolean, data: DashboardData }>(`/analytics/dashboard?${query}`);

                if (response.data.success) {
                    setDashboardData(response.data.data);
                }
            } catch (error) {
                console.error("Dashboard data fetch error:", error);
            } finally {
                setLoading(false);
            }
        };

        if (user) {
            fetchDashboardData();
        }
    }, [user, filterType, selectedCategory]);

    const handleLogout = () => {
        logout();
        router.push("/login");
    };

    // Loading State
    if (loading) {
        return (
            <div className="flex flex-col items-center justify-center min-h-screen bg-[#020817]">
                <div className="flex items-center gap-3">
                    <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-500"></div>
                    <span className="text-gray-400 animate-pulse font-medium">Yuklanmoqda...</span>
                </div>
            </div>
        );
    }

    // Error State
    if (!dashboardData) {
        return (
            <div className="flex flex-col items-center justify-center min-h-screen bg-[#020817] text-white space-y-4">
                <div className="bg-red-500/10 p-4 rounded-full">
                    <LogOut className="w-8 h-8 text-red-500" />
                </div>
                <p className="text-xl font-medium">Ma'lumotlarni yuklashda xatolik yuz berdi.</p>
                <Button onClick={() => window.location.reload()} variant="outline" className="border-white/10 hover:bg-white/5">
                    Sahifani yangilash
                </Button>
            </div>
        );
    }

    // Check if empty
    const isEmpty =
        dashboardData.summary.total_income === 0 &&
        dashboardData.summary.total_expense === 0;

    return (
        <div className="p-4 md:p-8 space-y-8 text-white font-sans">
            {/* Header Section */}
            <motion.div
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                className="flex flex-col md:flex-row justify-between items-start md:items-center gap-6"
            >
                <div>
                    <h1 className="text-3xl font-bold tracking-tight bg-gradient-to-r from-blue-400 to-indigo-400 bg-clip-text text-transparent">
                        Moliya Holati
                    </h1>
                    <p className="text-gray-400 mt-1 flex items-center gap-2 text-sm">
                        <Calendar className="w-4 h-4" />
                        {new Date().getFullYear()}-yil hisoboti
                    </p>
                </div>

                <div className="flex flex-wrap items-center gap-3 w-full md:w-auto">
                    {/* Time Filter */}
                    <div className="flex items-center gap-2 bg-[#0F172A] p-1 rounded-lg border border-white/5 shadow-sm">
                        <Filter className="w-4 h-4 text-gray-400 ml-2" />
                        <Select value={filterType} onValueChange={setFilterType}>
                            <SelectTrigger className="w-[140px] md:w-[160px] bg-transparent border-none text-white focus:ring-0 text-sm">
                                <SelectValue placeholder="Vaqt oralig'i" />
                            </SelectTrigger>
                            <SelectContent className="bg-[#1A2642] border-white/10 text-white">
                                <SelectItem value="last_7_days">Oxirgi 7 kun</SelectItem>
                                <SelectItem value="this_month">Bu oy</SelectItem>
                                <SelectItem value="last_month">O'tgan oy</SelectItem>
                                <SelectItem value="this_year">Bu yil (2026)</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>

                    {/* Category Filter */}
                    <div className="flex items-center gap-2 bg-[#0F172A] p-1 rounded-lg border border-white/5 shadow-sm">
                        <PieChart className="w-4 h-4 text-gray-400 ml-2" />
                        <Select value={selectedCategory || "all"} onValueChange={(val) => setSelectedCategory(val === "all" ? null : val)}>
                            <SelectTrigger className="w-[140px] md:w-[160px] bg-transparent border-none text-white focus:ring-0 text-sm">
                                <SelectValue placeholder="Kategoriya" />
                            </SelectTrigger>
                            <SelectContent className="bg-[#1A2642] border-white/10 text-white max-h-[300px]">
                                <SelectItem value="all">Barcha Kategoriyalar</SelectItem>
                                {categories.map((cat) => (
                                    <SelectItem key={cat} value={cat}>{cat}</SelectItem>
                                ))}
                            </SelectContent>
                        </Select>
                    </div>

                    <Button onClick={handleLogout} variant="ghost" size="icon" className="text-gray-400 hover:text-white hover:bg-white/10 ml-auto md:ml-2">
                        <LogOut className="w-5 h-5" />
                    </Button>
                </div>
            </motion.div>

            {isEmpty ? (
                <EmptyDashboard />
            ) : (
                <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
                    <StatsCards summary={dashboardData.summary} />

                    {/* Trend Chart - Full Width */}
                    <motion.div
                        initial={{ opacity: 0, scale: 0.98 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ delay: 0.1 }}
                    >
                        <Card className="bg-[#0F172A]/50 border-white/5 backdrop-blur-xl shadow-xl">
                            <CardHeader className="pb-2">
                                <div className="flex items-center justify-between">
                                    <div>
                                        <CardTitle className="text-lg font-semibold text-gray-100 flex items-center gap-2">
                                            <Activity className="w-5 h-5 text-blue-500" />
                                            Kirim va Chiqim Dinamikasi
                                        </CardTitle>
                                        <p className="text-sm text-gray-500 mt-1">Vaqt bo'yicha moliyaviy oqimlar</p>
                                    </div>
                                </div>
                            </CardHeader>
                            <CardContent>
                                <div className="h-[350px] w-full mt-4">
                                    <TrendChart data={dashboardData.charts || []} avgStats={dashboardData.details?.avg_stats} />
                                </div>
                            </CardContent>
                        </Card>
                    </motion.div>

                    {/* Pie Chart & Top Expenses - Side by Side */}
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                        {/* Pie Chart */}
                        <motion.div
                            initial={{ opacity: 0, scale: 0.98 }}
                            animate={{ opacity: 1, scale: 1 }}
                            transition={{ delay: 0.2 }}
                        >
                            <Card className="bg-[#0F172A]/50 border-white/5 backdrop-blur-xl shadow-xl h-full">
                                <CardHeader className="pb-2">
                                    <CardTitle className="text-lg font-semibold text-gray-100 flex items-center gap-2">
                                        <PieChart className="w-5 h-5 text-purple-500" />
                                        Xarajatlar Taqsimoti
                                    </CardTitle>
                                </CardHeader>
                                <CardContent>
                                    <div className="h-[280px] w-full">
                                        <CategoryPieChart data={dashboardData.details?.expense_by_category || []} />
                                    </div>
                                </CardContent>
                            </Card>
                        </motion.div>

                        {/* Top Expenses List */}
                        <motion.div
                            initial={{ opacity: 0, scale: 0.98 }}
                            animate={{ opacity: 1, scale: 1 }}
                            transition={{ delay: 0.3 }}
                        >
                            <Card className="bg-[#0F172A]/50 border-white/5 backdrop-blur-xl shadow-xl h-full">
                                <CardHeader className="pb-4">
                                    <CardTitle className="text-lg font-semibold text-gray-100">
                                        Eng Ko'p Xarajatlar
                                    </CardTitle>
                                </CardHeader>
                                <CardContent className="space-y-3">
                                    {dashboardData.top_expenses && dashboardData.top_expenses.length > 0 ? (
                                        dashboardData.top_expenses.slice(0, 5).map((expense, i) => (
                                            <div key={i} className="flex items-center justify-between p-2 rounded-lg hover:bg-white/5 transition-colors group">
                                                <div className="flex items-center gap-3">
                                                    <div className="w-6 h-6 rounded-md bg-red-500/10 flex items-center justify-center text-xs font-bold text-red-500 group-hover:bg-red-500/20 transition-colors">
                                                        {i + 1}
                                                    </div>
                                                    <div>
                                                        <p className="text-sm font-medium text-gray-200">{expense.category}</p>
                                                    </div>
                                                </div>
                                                <div className="text-right">
                                                    <p className="text-sm font-semibold text-white font-mono">
                                                        {new Intl.NumberFormat('uz-UZ').format(expense.amount)}
                                                    </p>
                                                    <p className="text-[10px] text-gray-500">{expense.percentage}%</p>
                                                </div>
                                            </div>
                                        ))
                                    ) : (
                                        <p className="text-sm text-gray-500 text-center py-4">Xarajatlar mavjud emas</p>
                                    )}
                                </CardContent>
                            </Card>
                        </motion.div>
                    </div>

                    {/* Recent Transactions - New Section */}
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.4 }}
                    >
                        <Card className="bg-[#0F172A]/50 border-white/5 backdrop-blur-xl shadow-xl">
                            <CardHeader>
                                <CardTitle className="text-lg font-semibold text-gray-100 flex items-center gap-2">
                                    <Clock className="w-5 h-5 text-green-500" />
                                    Oxirgi Tranzaksiyalar
                                </CardTitle>
                            </CardHeader>
                            <CardContent>
                                <RecentTransactions limit={5} />
                            </CardContent>
                        </Card>
                    </motion.div>
                </div>
            )}
        </div>
    );
}
