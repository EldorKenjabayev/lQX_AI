"use client";

import {
    AreaChart,
    Area,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer,
    Legend,
    ReferenceLine
} from "recharts";
import { format } from "date-fns";
import { uz } from "date-fns/locale";

interface ChartPoint {
    date: string;
    income: number;
    expense: number;
    net_change: number;
}

interface TrendChartProps {
    data: ChartPoint[];
    avgStats?: {
        daily_income: number;
        daily_expense: number;
    };
}

export function TrendChart({ data, avgStats }: TrendChartProps) {
    if (!data || data.length === 0) {
        return (
            <div className="h-[300px] flex items-center justify-center text-gray-400 bg-[#0A1628]/30 rounded-xl border border-white/5">
                Ma'lumot yo'q
            </div>
        );
    }

    // Format date for tooltip and axis
    const formatDate = (dateStr: string) => {
        try {
            // If date is already Month name (Jan, Feb) from backend, return as is (translated)
            // But usually backend returns English short names or localized.
            // Let's rely on date-fns if it looks like ISO date.
            if (dateStr.includes('-')) {
                const date = new Date(dateStr);
                return format(date, "d MMM", { locale: uz });
            }
            // Assume it's Month name (Jan, Feb, etc) - simple translation map or return as is
            const monthMap: { [key: string]: string } = {
                'Jan': 'Yan', 'Feb': 'Fev', 'Mar': 'Mar', 'Apr': 'Apr', 'May': 'May', 'Jun': 'Iyun',
                'Jul': 'Iyul', 'Aug': 'Avg', 'Sep': 'Sen', 'Oct': 'Okt', 'Nov': 'Noy', 'Dec': 'Dek'
            };
            return monthMap[dateStr] || dateStr;
        } catch {
            return dateStr;
        }
    };

    const CustomTooltip = ({ active, payload, label }: any) => {
        if (active && payload && payload.length) {
            return (
                <div className="bg-[#1A2642] border border-white/10 p-4 rounded-lg shadow-xl z-50">
                    <p className="text-gray-300 text-sm mb-2">{formatDate(label)}</p>
                    {payload.map((entry: any, index: number) => {
                        if (entry.dataKey === 'income' || entry.dataKey === 'expense') {
                            return (
                                <div key={index} className="flex items-center gap-2 mb-1">
                                    <div
                                        className="w-3 h-3 rounded-full"
                                        style={{ backgroundColor: entry.color }}
                                    />
                                    <span className="text-gray-300 text-sm capitalize">
                                        {entry.name === "income" ? "Kirim" : "Chiqim"}:
                                    </span>
                                    <span className="text-white font-medium text-sm">
                                        {entry.value.toLocaleString()} so'm
                                    </span>
                                </div>
                            )
                        }
                        return null;
                    })}
                </div>
            );
        }
        return null;
    };

    return (
        <div className="w-full h-[350px]">
            <ResponsiveContainer width="100%" height="100%">
                <AreaChart
                    data={data}
                    margin={{ top: 10, right: 10, left: 0, bottom: 0 }}
                >
                    <defs>
                        <linearGradient id="colorIncome" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="#10B981" stopOpacity={0.3} />
                            <stop offset="95%" stopColor="#10B981" stopOpacity={0} />
                        </linearGradient>
                        <linearGradient id="colorExpense" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="#EF4444" stopOpacity={0.3} />
                            <stop offset="95%" stopColor="#EF4444" stopOpacity={0} />
                        </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="#ffffff10" vertical={false} />
                    <XAxis
                        dataKey="date"
                        stroke="#6B7280"
                        tickFormatter={formatDate}
                        tick={{ fontSize: 11, fill: '#6B7280' }}
                        tickLine={false}
                        axisLine={false}
                        minTickGap={30}
                    />
                    <YAxis
                        stroke="#6B7280"
                        tickFormatter={(value) => `${(value / 1000000).toFixed(1)}m`}
                        tick={{ fontSize: 11, fill: '#6B7280' }}
                        tickLine={false}
                        axisLine={false}
                    />
                    <Tooltip content={<CustomTooltip />} cursor={{ stroke: 'rgba(255,255,255,0.1)', strokeWidth: 1 }} />
                    <Legend
                        verticalAlign="top"
                        height={36}
                        iconType="circle"
                        formatter={(value) => (
                            <span className="text-gray-400 text-xs ml-1 font-medium capitalize">{value === "income" ? "Kirim" : "Chiqim"}</span>
                        )}
                    />

                    {/* Average Reference Lines */}
                    {avgStats && avgStats.daily_income > 0 && (
                        <ReferenceLine
                            y={avgStats.daily_income}
                            stroke="#10B981"
                            strokeDasharray="3 3"
                            strokeOpacity={0.5}
                            label={{ position: 'right', value: 'Avg Inc', fill: '#10B981', fontSize: 10 }}
                        />
                    )}
                    {avgStats && avgStats.daily_expense > 0 && (
                        <ReferenceLine
                            y={avgStats.daily_expense}
                            stroke="#EF4444"
                            strokeDasharray="3 3"
                            strokeOpacity={0.5}
                            label={{ position: 'right', value: 'Avg Exp', fill: '#EF4444', fontSize: 10 }}
                        />
                    )}

                    <Area
                        type="monotone"
                        dataKey="income"
                        name="income"
                        stroke="#10B981"
                        strokeWidth={3}
                        fillOpacity={1}
                        fill="url(#colorIncome)"
                        activeDot={{ r: 6, strokeWidth: 0 }}
                    />
                    <Area
                        type="monotone"
                        dataKey="expense"
                        name="expense"
                        stroke="#EF4444"
                        strokeWidth={3}
                        fillOpacity={1}
                        fill="url(#colorExpense)"
                        activeDot={{ r: 6, strokeWidth: 0 }}
                    />
                </AreaChart>
            </ResponsiveContainer>
        </div>
    );
}
