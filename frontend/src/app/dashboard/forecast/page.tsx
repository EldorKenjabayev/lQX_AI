"use client";

import { useState, useEffect } from "react";
import { DollarSign, TrendingUp, AlertTriangle, CheckCircle2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from "@/components/ui/card";
import {
    AreaChart,
    Area,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer
} from "recharts";
import api from "@/lib/api";

export default function ForecastPage() {
    const [balance, setBalance] = useState<number>(0);
    const [days, setDays] = useState<number>(90);
    const [forecast, setForecast] = useState<any>(null);
    const [loading, setLoading] = useState(false);
    const [initializing, setInitializing] = useState(true);

    // Fetch current balance and run forecast automatically
    useEffect(() => {
        const initForecast = async () => {
            try {
                // 1. Get current balance from dashboard analytics
                const dashRes = await api.get("/analytics/dashboard?filter_type=this_year");
                const dashData = dashRes.data.data;
                // Current balance = Total Income - Total Expense (from summary)
                const currentBal = dashData.summary.total_income - dashData.summary.total_expense;
                setBalance(currentBal);

                // No auto-run for forecast as per user request
            } catch (error) {
                console.error("Auto-fetch balance error:", error);
            } finally {
                setLoading(false);
                setInitializing(false);
            }
        };

        if (initializing) {
            initForecast();
        }
    }, [initializing]);

    const handleForecast = async () => {
        setLoading(true);
        try {
            const res = await api.post("/forecast/run", {
                initial_balance: balance,
                forecast_days: days
            });
            setForecast(res.data);
        } catch (error) {
            console.error(error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-[#0A1628] to-[#1A2642] p-6">
            <div className="max-w-7xl mx-auto">
                <div className="mb-8">
                    <h1 className="text-3xl font-bold text-white mb-2">Moliyaviy Bashorat (AI)</h1>
                    <p className="text-gray-400">
                        Sun'iy intellekt yordamida kelgusi {days} kunlik moliyaviy holatingizni prognoz qiling.
                    </p>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                    {/* Controls */}
                    <Card className="bg-[#1A2642] border-white/10 text-white lg:col-span-1 h-fit">
                        <CardHeader>
                            <CardTitle>Parametrlar</CardTitle>
                            <CardDescription className="text-gray-400">
                                Joriy balans va muddatni kiriting
                            </CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <div className="space-y-2">
                                <label className="text-sm font-medium text-gray-300">Joriy Balans (so'm)</label>
                                <div className="relative">
                                    <DollarSign className="absolute left-3 top-2.5 h-4 w-4 text-gray-400" />
                                    <Input
                                        type="number"
                                        value={balance}
                                        onChange={(e) => setBalance(Number(e.target.value))}
                                        className="bg-[#0A1628] border-white/10 pl-9 text-white"
                                    />
                                </div>
                            </div>

                            <div className="space-y-2">
                                <label className="text-sm font-medium text-gray-300">Prognoz muddati (kun)</label>
                                <Input
                                    type="number"
                                    value={days}
                                    onChange={(e) => setDays(Number(e.target.value))}
                                    min={30}
                                    max={365}
                                    className="bg-[#0A1628] border-white/10 text-white"
                                />
                            </div>

                            <Button
                                onClick={handleForecast}
                                disabled={loading}
                                className="w-full bg-gradient-to-r from-violet-600 to-indigo-600 hover:opacity-90 mt-4"
                            >
                                {loading ? "Hisoblanmoqda..." : "Bashorat qilish"}
                            </Button>
                        </CardContent>
                    </Card>

                    {/* Results */}
                    <div className="lg:col-span-2 space-y-6">
                        {forecast ? (
                            <>
                                {/* Summary Cards */}
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                    <Card className="bg-[#1A2642] border-white/10 text-white">
                                        <CardHeader className="pb-2">
                                            <CardTitle className="text-sm font-medium text-gray-400">Xavf Darajasi</CardTitle>
                                        </CardHeader>
                                        <CardContent>
                                            <div className="flex items-center gap-2">
                                                {forecast.risk_level === "High" ? (
                                                    <AlertTriangle className="text-red-500 w-6 h-6" />
                                                ) : forecast.risk_level === "Medium" ? (
                                                    <AlertTriangle className="text-yellow-500 w-6 h-6" />
                                                ) : (
                                                    <CheckCircle2 className="text-green-500 w-6 h-6" />
                                                )}
                                                <span className={`text-2xl font-bold ${forecast.risk_level === "High" ? "text-red-500" :
                                                    forecast.risk_level === "Medium" ? "text-yellow-500" : "text-green-500"
                                                    }`}>
                                                    {forecast.risk_level}
                                                </span>
                                            </div>
                                        </CardContent>
                                    </Card>

                                    <Card className="bg-[#1A2642] border-white/10 text-white">
                                        <CardHeader className="pb-2">
                                            <CardTitle className="text-sm font-medium text-gray-400">Tavsiya</CardTitle>
                                        </CardHeader>
                                        <CardContent>
                                            <p className="text-sm text-gray-300 leading-relaxed">
                                                {forecast.recommendation}
                                            </p>
                                        </CardContent>
                                    </Card>
                                </div>

                                {/* Chart */}
                                <Card className="bg-[#1A2642] border-white/10 text-white p-6">
                                    <h3 className="text-lg font-semibold mb-6">Balans Prognozi</h3>
                                    <div className="h-[300px] w-full">
                                        <ResponsiveContainer width="100%" height="100%">
                                            <AreaChart data={forecast.forecast}>
                                                <defs>
                                                    <linearGradient id="colorBalance" x1="0" y1="0" x2="0" y2="1">
                                                        <stop offset="5%" stopColor="#8884d8" stopOpacity={0.8} />
                                                        <stop offset="95%" stopColor="#8884d8" stopOpacity={0} />
                                                    </linearGradient>
                                                </defs>
                                                <CartesianGrid strokeDasharray="3 3" stroke="#ffffff10" />
                                                <XAxis dataKey="date" stroke="#6B7280" fontSize={12} tickLine={false} axisLine={false} />
                                                <YAxis stroke="#6B7280" fontSize={12} tickLine={false} axisLine={false} tickFormatter={(value) => `${(value / 1000000).toFixed(1)}m`} />
                                                <Tooltip
                                                    contentStyle={{ backgroundColor: '#1F2937', border: 'none', color: '#fff' }}
                                                    formatter={(value: any) => [`${value.toLocaleString()} so'm`, "Balans"]}
                                                />
                                                <Area type="monotone" dataKey="predicted_balance" stroke="#8884d8" fillOpacity={1} fill="url(#colorBalance)" />
                                                <Area type="monotone" dataKey="lower_bound" stroke="transparent" fill="transparent" />
                                                <Area type="monotone" dataKey="upper_bound" stroke="transparent" fill="transparent" />
                                            </AreaChart>
                                        </ResponsiveContainer>
                                    </div>
                                </Card>
                            </>
                        ) : (
                            <Card className="bg-[#1A2642] border-white/10 text-center py-12 flex flex-col items-center justify-center min-h-[400px]">
                                <TrendingUp className="w-16 h-16 text-gray-600 mb-4" />
                                <h3 className="text-xl font-medium text-white mb-2">Prognoz Ishga Tushirilmagan</h3>
                                <p className="text-gray-400 max-w-sm">
                                    Parametrlarni kiriting va "Bashorat qilish" tugmasini bosing.
                                </p>
                            </Card>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}
