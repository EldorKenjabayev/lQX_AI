"use client"

import { Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis, CartesianGrid } from "recharts"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { ChartPoint } from "@/lib/api"

interface OverviewChartProps {
    data: ChartPoint[]
}

export function OverviewChart({ data }: OverviewChartProps) {
    return (
        <Card className="col-span-4 bg-white/5 border-white/10 backdrop-blur-xl">
            <CardHeader>
                <CardTitle className="text-white">Overview</CardTitle>
            </CardHeader>
            <CardContent className="pl-2">
                <ResponsiveContainer width="100%" height={350}>
                    <LineChart data={data}>
                        <CartesianGrid strokeDasharray="3 3" opacity={0.1} stroke="#ffffff" />
                        <XAxis
                            dataKey="date"
                            stroke="#9ca3af" // gray-400
                            fontSize={12}
                            tickLine={false}
                            axisLine={false}
                        />
                        <YAxis
                            stroke="#9ca3af" // gray-400
                            fontSize={12}
                            tickLine={false}
                            axisLine={false}
                            tickFormatter={(value) => `${value}`}
                        />
                        <Tooltip
                            contentStyle={{
                                backgroundColor: 'rgba(15, 23, 42, 0.9)',
                                borderRadius: '12px',
                                border: '1px solid rgba(255,255,255,0.1)',
                                boxShadow: '0 4px 20px rgba(0,0,0,0.5)',
                                color: '#fff'
                            }}
                            itemStyle={{ color: '#fff' }}
                        />
                        <Line
                            type="monotone"
                            dataKey="income"
                            stroke="#10b981" // emerald-500
                            strokeWidth={3}
                            dot={{ fill: '#10b981', strokeWidth: 2, r: 4, stroke: '#fff' }}
                            activeDot={{ r: 6, strokeWidth: 0 }}
                            name="Income"
                        />
                        <Line
                            type="monotone"
                            dataKey="expense"
                            stroke="#ef4444" // red-500
                            strokeWidth={3}
                            dot={{ fill: '#ef4444', strokeWidth: 2, r: 4, stroke: '#fff' }}
                            activeDot={{ r: 6, strokeWidth: 0 }}
                            name="Expense"
                        />
                    </LineChart>
                </ResponsiveContainer>
            </CardContent>
        </Card>
    )
}
