import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { motion } from "motion/react"
import { DashboardSummary } from "@/lib/api"
import { TrendingUp, TrendingDown, DollarSign, Wallet } from "lucide-react"

interface StatsCardsProps {
    summary: DashboardSummary
}

export function StatsCards({ summary }: StatsCardsProps) {
    const formatter = new Intl.NumberFormat('uz-UZ', { style: 'currency', currency: 'UZS' });

    return (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            <motion.div whileHover={{ scale: 1.02 }} transition={{ type: "spring", stiffness: 300 }}>
                <Card className="bg-white/5 border-white/10 backdrop-blur-xl transition-colors hover:bg-white/10">
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium text-gray-200">Jami Daromad</CardTitle>
                        <DollarSign className="h-4 w-4 text-[#10B981]" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold text-white">{formatter.format(summary.total_income)}</div>
                        <p className="text-xs text-gray-400">
                            Tanlangan davrdagi jami kirim
                        </p>
                    </CardContent>
                </Card>
            </motion.div>
            <motion.div whileHover={{ scale: 1.02 }} transition={{ type: "spring", stiffness: 300 }}>
                <Card className="bg-white/5 border-white/10 backdrop-blur-xl transition-colors hover:bg-white/10">
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium text-gray-200">Jami Xarajat</CardTitle>
                        <TrendingDown className="h-4 w-4 text-red-500" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold text-white">{formatter.format(summary.total_expense)}</div>
                        <p className="text-xs text-gray-400">
                            Tanlangan davrdagi jami chiqim
                        </p>
                    </CardContent>
                </Card>
            </motion.div>
            <motion.div whileHover={{ scale: 1.02 }} transition={{ type: "spring", stiffness: 300 }}>
                <Card className="bg-white/5 border-white/10 backdrop-blur-xl transition-colors hover:bg-white/10">
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium text-gray-200">Joriy Balans</CardTitle>
                        <TrendingUp className="h-4 w-4 text-blue-500" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold text-white">{formatter.format(summary.net_profit || 0)}</div>
                        <p className="text-xs text-gray-400">
                            Kassadagi qolgan pul
                        </p>
                    </CardContent>
                </Card>
            </motion.div>
            <motion.div whileHover={{ scale: 1.02 }} transition={{ type: "spring", stiffness: 300 }}>
                <Card className="bg-white/5 border-white/10 backdrop-blur-xl transition-colors hover:bg-white/10">
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium text-gray-200">Tejash Foizi</CardTitle>
                        <Wallet className="h-4 w-4 text-[#34D399]" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold text-white">{summary.savings_rate?.toFixed(1)}%</div>
                        <p className="text-xs text-gray-400">
                            Tejab qolish foizi
                        </p>
                    </CardContent>
                </Card>
            </motion.div>
        </div>
    )
}
