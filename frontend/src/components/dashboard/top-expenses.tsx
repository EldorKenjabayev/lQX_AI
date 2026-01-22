import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { TopExpense } from "@/lib/api"

interface TopExpensesProps {
    expenses: TopExpense[]
}

export function TopExpenses({ expenses }: TopExpensesProps) {
    const formatter = new Intl.NumberFormat('uz-UZ', { style: 'currency', currency: 'UZS' });

    return (
        <Card className="col-span-3 bg-white/5 border-white/10 backdrop-blur-xl">
            <CardHeader>
                <CardTitle className="text-white">Top Expenses</CardTitle>
            </CardHeader>
            <CardContent>
                <div className="space-y-8">
                    {expenses.map((expense, index) => (
                        <div key={index} className="flex items-center">
                            <div className="space-y-1">
                                <p className="text-sm font-medium leading-none text-white">{expense.category}</p>
                                <p className="text-xs text-gray-400">
                                    {expense.percentage}% of total expenses
                                </p>
                            </div>
                            <div className="ml-auto font-medium text-white">
                                {formatter.format(expense.amount)}
                            </div>
                        </div>
                    ))}
                    {expenses.length === 0 && (
                        <p className="text-sm text-gray-400">No expenses found.</p>
                    )}
                </div>
            </CardContent>
        </Card>
    )
}
