"use client";

import {
    PieChart,
    Pie,
    Cell,
    Tooltip,
    ResponsiveContainer,
    Legend,
} from "recharts";

interface CategoryDetail {
    category: string;
    amount: number;
    percentage: number;
}

interface CategoryPieChartProps {
    data: CategoryDetail[];
}

const COLORS = [
    "#10B981", "#3B82F6", "#F59E0B", "#EF4444", "#8B5CF6",
    "#EC4899", "#6366F1", "#14B8A6", "#F97316", "#06B6D4"
];

export function CategoryPieChart({ data }: CategoryPieChartProps) {
    if (!data || data.length === 0) {
        return (
            <div className="h-[300px] flex items-center justify-center text-gray-400 bg-[#0A1628]/30 rounded-xl border border-white/5">
                Ma'lumot yo'q
            </div>
        );
    }

    const CustomTooltip = ({ active, payload }: any) => {
        if (active && payload && payload.length) {
            const item = payload[0].payload;
            return (
                <div className="bg-[#1A2642] border border-white/10 p-4 rounded-lg shadow-xl">
                    <p className="text-gray-200 font-medium mb-1">{item.category}</p>
                    <p className="text-white font-bold text-lg">
                        {item.amount.toLocaleString()} so'm
                    </p>
                    <p className="text-gray-400 text-sm">
                        {item.percentage}% of total
                    </p>
                </div>
            );
        }
        return null;
    };

    return (
        <div className="w-full h-full">
            <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                    <Pie
                        data={data}
                        cx="50%"
                        cy="50%"
                        innerRadius={60}
                        outerRadius={90}
                        paddingAngle={2}
                        dataKey="amount"
                        nameKey="category"
                    >
                        {data.map((entry, index) => (
                            <Cell
                                key={`cell-${index}`}
                                fill={COLORS[index % COLORS.length]}
                                stroke="rgba(255,255,255,0.1)"
                            />
                        ))}
                    </Pie>
                    <Tooltip content={<CustomTooltip />} />
                    <Legend
                        verticalAlign="bottom"
                        height={36}
                        iconType="circle"
                        formatter={(value) => <span className="text-gray-300 ml-1">{value}</span>}
                    />
                </PieChart>
            </ResponsiveContainer>
        </div>
    );
}
