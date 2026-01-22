"use client";

import { useState, useEffect } from "react";
import { format } from "date-fns";
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow
} from "@/components/ui/table";
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuLabel,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
} from "@/components/ui/dialog";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge"; // You might need to add badge component or use custom styles
import {
    MoreHorizontal,
    ArrowUpDown,
    Search,
    Filter,
    Download,
    Trash2,
    Edit,
    Plus
} from "lucide-react";
import api from "@/lib/api";
import { toast } from "sonner"; // Assuming sonner is used, or replace with your toast lib

// Interface
interface Transaction {
    id: string;
    date: string;
    amount: number;
    description: string;
    category: string;
    is_expense: boolean;
    is_fixed: boolean;
}

export default function TransactionsPage() {
    const [transactions, setTransactions] = useState<Transaction[]>([]);
    const [filteredData, setFilteredData] = useState<Transaction[]>([]);
    const [loading, setLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState("");
    const [categoryFilter, setCategoryFilter] = useState("all");
    const [typeFilter, setTypeFilter] = useState("all");

    // Edit/Delete State
    const [isEditOpen, setIsEditOpen] = useState(false);
    const [currentTxn, setCurrentTxn] = useState<Transaction | null>(null);
    const [isDeleteAlertOpen, setIsDeleteAlertOpen] = useState(false);
    const [deleteId, setDeleteId] = useState<string | null>(null);
    const [isClearAlertOpen, setIsClearAlertOpen] = useState(false);

    // Fetch Data
    const fetchTransactions = async () => {
        try {
            setLoading(true);
            const res = await api.get("/data/transactions");
            setTransactions(res.data);
            setFilteredData(res.data);
        } catch (error) {
            console.error("Failed to fetch transactions", error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchTransactions();
    }, []);

    // Helper: Unique Categories for Filter
    const categories = Array.from(new Set(transactions.map((t) => t.category))).filter(Boolean);

    // Filter Logic
    useEffect(() => {
        let data = transactions;

        if (searchTerm) {
            data = data.filter(t =>
                t.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
                t.category.toLowerCase().includes(searchTerm.toLowerCase())
            );
        }

        if (categoryFilter !== "all") {
            data = data.filter(t => t.category === categoryFilter);
        }

        if (typeFilter !== "all") {
            const isExpense = typeFilter === "expense";
            data = data.filter(t => t.is_expense === isExpense);
        }

        setFilteredData(data);
    }, [searchTerm, categoryFilter, typeFilter, transactions]);

    // Format Currency
    const formatCurrency = (amount: number) => {
        return new Intl.NumberFormat("uz-UZ", {
            style: "currency",
            currency: "UZS",
            minimumFractionDigits: 0,
        }).format(amount);
    };

    // Actions
    const handleDelete = async () => {
        if (!deleteId) return;
        try {
            await api.delete(`/data/transaction/${deleteId}`);
            setTransactions(prev => prev.filter(t => t.id !== deleteId));
            toast.success("Tranzaksiya o'chirildi");
        } catch (error) {
            toast.error("O'chirishda xatolik yuz berdi");
        } finally {
            setIsDeleteAlertOpen(false);
            setDeleteId(null);
        }
    };

    const handleClearAll = async () => {
        try {
            await api.delete("/data/analytics/clear");
            setTransactions([]);
            setFilteredData([]);
            toast.success("Barcha ma'lumotlar o'chirildi");
        } catch (error) {
            toast.error("Tozalashda xatolik yuz berdi");
        } finally {
            setIsClearAlertOpen(false);
        }
    };

    const handleEditSave = async (e: React.FormEvent) => {
        // ... (Edit logic stays same)
        e.preventDefault();
        if (!currentTxn) return;

        try {
            const payload = {
                date: currentTxn.date.split("T")[0],
                amount: Number(currentTxn.amount),
                description: currentTxn.description,
                category: currentTxn.category,
                is_expense: currentTxn.is_expense,
                is_fixed: currentTxn.is_fixed
            };

            const res = await api.patch(`/data/transaction/${currentTxn.id}`, payload);

            setTransactions(prev => prev.map(t => t.id === currentTxn.id ? res.data : t));
            toast.success("Muvaffaqiyatli saqlandi");
            setIsEditOpen(false);
        } catch (error) {
            console.error(error);
            toast.error("Saqlashda xatolik");
        }
    };

    return (
        <div className="p-8 space-y-8">
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                <div>
                    <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-gray-400">
                        Tranzaksiyalar
                    </h1>
                    <p className="text-gray-400 mt-1">Barcha kirim va chiqimlar tarixi</p>
                </div>
                <div className="flex gap-2">
                    <Button
                        variant="destructive"
                        className="gap-2 bg-red-500/10 text-red-400 hover:bg-red-500/20 border border-red-500/20"
                        onClick={() => setIsClearAlertOpen(true)}
                    >
                        <Trash2 className="w-4 h-4" /> Tozalash
                    </Button>
                    <Button variant="outline" className="gap-2 border-white/10 hover:bg-white/5">
                        <Download className="w-4 h-4" /> Eksport (Excel)
                    </Button>
                </div>
            </div>

            {/* Filters Bar */}
            <div className="flex flex-col md:flex-row gap-4 bg-white/5 p-4 rounded-xl border border-white/10">
                <div className="relative flex-1">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
                    <Input
                        placeholder="Izlash..."
                        className="pl-9 bg-black/20 border-white/10"
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                    />
                </div>

                <Select value={typeFilter} onValueChange={setTypeFilter}>
                    <SelectTrigger className="w-[180px] bg-black/20 border-white/10">
                        <SelectValue placeholder="Turi" />
                    </SelectTrigger>
                    <SelectContent>
                        <SelectItem value="all">Barchasi</SelectItem>
                        <SelectItem value="expense">Xarajat</SelectItem>
                        <SelectItem value="income">Daromad</SelectItem>
                    </SelectContent>
                </Select>

                <Select value={categoryFilter} onValueChange={setCategoryFilter}>
                    <SelectTrigger className="w-[180px] bg-black/20 border-white/10">
                        <SelectValue placeholder="Kategoriya" />
                    </SelectTrigger>
                    <SelectContent>
                        <SelectItem value="all">Barchasi</SelectItem>
                        {categories.map(cat => (
                            <SelectItem key={cat} value={cat}>{cat}</SelectItem>
                        ))}
                    </SelectContent>
                </Select>
            </div>

            {/* Data Table */}
            <div className="rounded-xl border border-white/10 bg-white/5 overflow-hidden">
                <Table>
                    <TableHeader className="bg-white/5">
                        <TableRow className="border-white/10 hover:bg-white/5">
                            <TableHead className="text-gray-400">Sana</TableHead>
                            <TableHead className="text-gray-400">Tavsif</TableHead>
                            <TableHead className="text-gray-400">Kategoriya</TableHead>
                            <TableHead className="text-gray-400">Summa</TableHead>
                            <TableHead className="text-gray-400">Turi</TableHead>
                            <TableHead className="text-right text-gray-400">Amallar</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {loading ? (
                            <TableRow>
                                <TableCell colSpan={6} className="h-24 text-center text-gray-400">
                                    Yuklanmoqda...
                                </TableCell>
                            </TableRow>
                        ) : filteredData.length === 0 ? (
                            <TableRow>
                                <TableCell colSpan={6} className="h-24 text-center text-gray-400">
                                    Ma'lumot topilmadi
                                </TableCell>
                            </TableRow>
                        ) : (
                            filteredData.map((txn) => (
                                <TableRow key={txn.id} className="border-white/10 hover:bg-white/5 transition-colors">
                                    <TableCell className="font-medium text-gray-300">
                                        {format(new Date(txn.date), "dd.MM.yyyy")}
                                    </TableCell>
                                    <TableCell className="text-gray-300">{txn.description}</TableCell>
                                    <TableCell>
                                        <span className="px-2 py-1 rounded-full text-xs bg-white/10 text-gray-300 border border-white/10">
                                            {txn.category}
                                        </span>
                                    </TableCell>
                                    <TableCell className={`font-semibold ${txn.is_expense ? 'text-red-400' : 'text-emerald-400'}`}>
                                        {txn.is_expense ? '-' : '+'}{formatCurrency(Math.abs(txn.amount))}
                                    </TableCell>
                                    <TableCell>
                                        <span className={`px-2 py-1 rounded-md text-xs font-medium ${txn.is_expense
                                            ? 'bg-red-500/10 text-red-400 border border-red-500/20'
                                            : 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                                            }`}>
                                            {txn.is_expense ? "Xarajat" : "Daromad"}
                                        </span>
                                    </TableCell>
                                    <TableCell className="text-right">
                                        <div className="flex justify-end gap-2">
                                            <Button
                                                variant="ghost"
                                                size="icon"
                                                className="h-8 w-8 text-gray-400 hover:text-white hover:bg-white/10"
                                                onClick={() => {
                                                    setCurrentTxn(txn);
                                                    setIsEditOpen(true);
                                                }}
                                            >
                                                <Edit className="h-4 w-4" />
                                            </Button>
                                            <Button
                                                variant="ghost"
                                                size="icon"
                                                className="h-8 w-8 text-gray-400 hover:text-red-400 hover:bg-red-500/10"
                                                onClick={() => {
                                                    setDeleteId(txn.id);
                                                    setIsDeleteAlertOpen(true);
                                                }}
                                            >
                                                <Trash2 className="h-4 w-4" />
                                            </Button>
                                        </div>
                                    </TableCell>
                                </TableRow>
                            ))
                        )}
                    </TableBody>
                </Table>
            </div>

            {/* Edit Dialog */}
            <Dialog open={isEditOpen} onOpenChange={setIsEditOpen}>
                <DialogContent className="bg-[#1A2642] border-white/10 text-white sm:max-w-[425px]">
                    <DialogHeader>
                        <DialogTitle>Tahrirlash</DialogTitle>
                        <DialogDescription className="text-gray-400">
                            Tranzaksiya ma'lumotlarini o'zgartirish.
                        </DialogDescription>
                    </DialogHeader>
                    {currentTxn && (
                        <form onSubmit={handleEditSave} className="grid gap-4 py-4">
                            <div className="grid gap-2">
                                <Label htmlFor="date">Sana</Label>
                                <Input
                                    id="date"
                                    type="date"
                                    value={currentTxn.date.split('T')[0]}
                                    onChange={(e) => setCurrentTxn({ ...currentTxn, date: e.target.value })}
                                    className="bg-black/20 border-white/10"
                                />
                            </div>
                            <div className="grid gap-2">
                                <Label htmlFor="amount">Summa</Label>
                                <Input
                                    id="amount"
                                    type="number"
                                    value={currentTxn.amount}
                                    onChange={(e) => setCurrentTxn({ ...currentTxn, amount: Number(e.target.value) })}
                                    className="bg-black/20 border-white/10"
                                />
                            </div>
                            <div className="grid gap-2">
                                <Label htmlFor="description">Tavsif</Label>
                                <Input
                                    id="description"
                                    value={currentTxn.description}
                                    onChange={(e) => setCurrentTxn({ ...currentTxn, description: e.target.value })}
                                    className="bg-black/20 border-white/10"
                                />
                            </div>
                            <div className="grid gap-2">
                                <Label htmlFor="category">Kategoriya</Label>
                                <Input
                                    id="category"
                                    value={currentTxn.category}
                                    onChange={(e) => setCurrentTxn({ ...currentTxn, category: e.target.value })}
                                    className="bg-black/20 border-white/10"
                                />
                            </div>
                            <div className="flex items-center gap-4">
                                <div className="flex items-center gap-2">
                                    <input
                                        type="checkbox"
                                        id="is_expense"
                                        checked={currentTxn.is_expense}
                                        onChange={(e) => setCurrentTxn({ ...currentTxn, is_expense: e.target.checked })}
                                        className="rounded border-gray-600 bg-black/20"
                                    />
                                    <Label htmlFor="is_expense">Xarajat</Label>
                                </div>
                                <div className="flex items-center gap-2">
                                    <input
                                        type="checkbox"
                                        id="is_fixed"
                                        checked={currentTxn.is_fixed}
                                        onChange={(e) => setCurrentTxn({ ...currentTxn, is_fixed: e.target.checked })}
                                        className="rounded border-gray-600 bg-black/20"
                                    />
                                    <Label htmlFor="is_fixed">Doimiy</Label>
                                </div>
                            </div>
                            <DialogFooter>
                                <Button type="submit" className="bg-[#10B981] hover:bg-[#059669]">Saqlash</Button>
                            </DialogFooter>
                        </form>
                    )}
                </DialogContent>
            </Dialog>

            {/* Delete Confirmation Dialog */}
            <Dialog open={isDeleteAlertOpen} onOpenChange={setIsDeleteAlertOpen}>
                <DialogContent className="bg-[#1A2642] border-white/10 text-white">
                    <DialogHeader>
                        <DialogTitle>Haqiqatan ham o'chirmoqchimisiz?</DialogTitle>
                        <DialogDescription className="text-gray-400">
                            Bu amalni ortga qaytarib bo'lmaydi.
                        </DialogDescription>
                    </DialogHeader>
                    <DialogFooter>
                        <Button variant="ghost" onClick={() => setIsDeleteAlertOpen(false)}>Bekor qilish</Button>
                        <Button variant="destructive" onClick={handleDelete}>O'chirish</Button>
                    </DialogFooter>
                </DialogContent>
            </Dialog>

            {/* Clear All Confirmation Dialog */}
            <Dialog open={isClearAlertOpen} onOpenChange={setIsClearAlertOpen}>
                <DialogContent className="bg-[#1A2642] border-white/10 text-white border-red-500/50">
                    <DialogHeader>
                        <DialogTitle className="text-red-500">DIQQAT: Barcha ma'lumotlar o'chadi!</DialogTitle>
                        <DialogDescription className="text-gray-400">
                            Siz hamma tranzaksiyalarni o'chirmoqchisiz. Bu amalni umuman ortga qaytarib bo'lmaydi. Tasdiqlaysizmi?
                        </DialogDescription>
                    </DialogHeader>
                    <DialogFooter>
                        <Button variant="ghost" onClick={() => setIsClearAlertOpen(false)}>Bekor qilish</Button>
                        <Button variant="destructive" onClick={handleClearAll} className="bg-red-600 hover:bg-red-700">Hammasini O'chirish</Button>
                    </DialogFooter>
                </DialogContent>
            </Dialog>
        </div>
    );
}
