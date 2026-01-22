"use client";

import { useState, useCallback } from "react";
import { useDropzone } from "react-dropzone";
import { motion, AnimatePresence } from "motion/react";
import { Upload, FileText, CheckCircle2, AlertCircle, X } from "lucide-react";
import { cn } from "@/lib/utils";
import api from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Textarea } from "@/components/ui/textarea"

export function UploadZone() {
    const [activeTab, setActiveTab] = useState("file");
    const [file, setFile] = useState<File | null>(null);
    const [text, setText] = useState("");
    const [isUploading, setIsUploading] = useState(false);
    const [status, setStatus] = useState<{ type: "success" | "error"; message: string } | null>(null);

    // File Dropzone Logic
    const onDrop = useCallback((acceptedFiles: File[]) => {
        if (acceptedFiles.length > 0) {
            setFile(acceptedFiles[0]);
            setStatus(null);
        }
    }, []);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: {
            "application/pdf": [".pdf"],
            "text/csv": [".csv"],
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": [".xlsx"],
            "application/msword": [".doc"],
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document": [".docx"],
        },
        maxFiles: 1,
    });

    const [progress, setProgress] = useState(0);
    const [processMessage, setProcessMessage] = useState("");

    // Handle Upload
    const handleUpload = async () => {
        setIsUploading(true);
        setStatus(null);
        setProgress(0);
        setProcessMessage("Yuklanmoqda...");

        try {
            let taskId;

            if (activeTab === "file" && file) {
                const formData = new FormData();
                formData.append("file", file);
                // 1. Start Upload Task
                const res = await api.post("/data/upload/file", formData, {
                    headers: { "Content-Type": "multipart/form-data" },
                });
                taskId = res.data.task_id;

            } else if (activeTab === "text" && text) {
                // Text upload is fast, but we can wrap it if needed. 
                // For now, assume text is instant or modify backend if needed.
                // Current backend implementation for /upload/text is sync.
                const response = await api.post("/data/upload/text", { text });
                setStatus({
                    type: "success",
                    message: `${response.data.transactions_count || 0} ta tranzaksiya muvaffaqiyatli yuklandi!`,
                });
                setText("");
                setIsUploading(false);
                return;
            } else {
                return; // Nothing to upload
            }

            if (taskId) {
                // 2. Poll Status
                const interval = setInterval(async () => {
                    try {
                        const statusRes = await api.get(`/data/upload/status/${taskId}`);
                        const data = statusRes.data;

                        setProgress(data.progress || 0);
                        setProcessMessage(data.message || "Jarayon ketmoqda...");

                        if (data.status === "completed") {
                            clearInterval(interval);
                            setStatus({
                                type: "success",
                                message: data.message || "Muvaffaqiyatli yakunlandi!"
                            });
                            setFile(null);
                            setIsUploading(false);
                        } else if (data.status === "failed") {
                            clearInterval(interval);
                            setStatus({
                                type: "error",
                                message: data.error || "Xatolik yuz berdi"
                            });
                            setIsUploading(false);
                        }
                    } catch (e) {
                        console.error("Polling error", e);
                        // Don't stop polling on single error, maybe network hiccup
                    }
                }, 1000);
            }

        } catch (error: any) {
            console.error("Upload error:", error);
            setStatus({
                type: "error",
                message: error.response?.data?.detail || "Yuklashda xatolik yuz berdi.",
            });
            setIsUploading(false);
        }
    };

    return (
        <div className="w-full max-w-3xl mx-auto p-6 bg-[#0A1628]/50 backdrop-blur-xl border border-white/10 rounded-2xl">
            <h2 className="text-2xl font-bold text-white mb-6 text-center">Ma'lumot Yuklash</h2>

            <Tabs defaultValue="file" value={activeTab} onValueChange={setActiveTab} className="w-full">
                <TabsList className="grid w-full grid-cols-2 bg-[#1A2642] mb-6">
                    <TabsTrigger value="file">Fayl (PDF, Excel)</TabsTrigger>
                    <TabsTrigger value="text">Matn (SMS, Telegram)</TabsTrigger>
                </TabsList>

                <TabsContent value="file">
                    <div
                        {...getRootProps()}
                        className={cn(
                            "border-2 border-dashed rounded-xl p-10 flex flex-col items-center justify-center cursor-pointer transition-all duration-300 min-h-[300px]",
                            isDragActive
                                ? "border-[#10B981] bg-[#10B981]/10"
                                : "border-white/20 hover:border-white/40 hover:bg-white/5"
                        )}
                    >
                        <input {...getInputProps()} />
                        <AnimatePresence mode="wait">
                            {file ? (
                                <motion.div
                                    key="file-selected"
                                    initial={{ opacity: 0, scale: 0.9 }}
                                    animate={{ opacity: 1, scale: 1 }}
                                    exit={{ opacity: 0, scale: 0.9 }}
                                    className="flex flex-col items-center"
                                >
                                    <FileText className="w-16 h-16 text-[#10B981] mb-4" />
                                    <p className="text-white font-medium text-lg">{file.name}</p>
                                    <p className="text-gray-400 text-sm mb-4">{(file.size / 1024).toFixed(1)} KB</p>
                                    <Button
                                        variant="ghost"
                                        size="sm"
                                        className="text-red-400 hover:text-red-300 hover:bg-red-900/20"
                                        onClick={(e) => {
                                            e.stopPropagation();
                                            setFile(null);
                                        }}
                                    >
                                        <X className="w-4 h-4 mr-2" /> Bekor qilish
                                    </Button>
                                </motion.div>
                            ) : (
                                <motion.div
                                    key="drop-prompt"
                                    initial={{ opacity: 0 }}
                                    animate={{ opacity: 1 }}
                                    exit={{ opacity: 0 }}
                                    className="flex flex-col items-center text-center"
                                >
                                    <div className="w-20 h-20 bg-[#1A2642] rounded-full flex items-center justify-center mb-6">
                                        <Upload className="w-10 h-10 text-gray-400" />
                                    </div>
                                    <p className="text-white text-lg font-medium mb-2">
                                        Faylni shu yerga tashlang yoki tanlash uchun bosing
                                    </p>
                                    <p className="text-gray-400 text-sm max-w-sm">
                                        PDF (Bank ko'chirmalari), Excel, CSV formatlarini qo'llab-quvvatlaymiz
                                    </p>
                                </motion.div>
                            )}
                        </AnimatePresence>
                    </div>
                </TabsContent>

                <TabsContent value="text">
                    <div className="space-y-4">
                        <label className="text-sm text-gray-400">
                            SMS yoki Telegram xabarlarni nusxalab qo'ying (AI o'zi tushunadi)
                        </label>
                        <Textarea
                            value={text}
                            onChange={(e) => setText(e.target.value)}
                            placeholder="Masalan: Kecha bozorga 450000 so'm, tushlikka 60000 so'm ishlatdim."
                            className="min-h-[300px] bg-[#1A2642] border-white/10 text-white placeholder:text-gray-500 focus-visible:ring-[#10B981] text-lg p-6"
                        />
                    </div>
                </TabsContent>
            </Tabs>

            {/* Status Message */}
            <AnimatePresence>
                {status && (
                    <motion.div
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0 }}
                        className={cn(
                            "mt-6 p-4 rounded-lg flex items-center gap-3",
                            status.type === "success" ? "bg-[#10B981]/10 text-[#10B981] border border-[#10B981]/20" : "bg-red-500/10 text-red-500 border border-red-500/20"
                        )}
                    >
                        {status.type === "success" ? <CheckCircle2 className="w-5 h-5" /> : <AlertCircle className="w-5 h-5" />}
                        <p className="font-medium">{status.message}</p>
                    </motion.div>
                )}
            </AnimatePresence>


            {isUploading && (
                <div className="mt-6 mb-2">
                    <div className="flex justify-between text-sm text-gray-400 mb-2">
                        <span>{processMessage}</span>
                        <span>{progress}%</span>
                    </div>
                    <div className="w-full bg-white/10 rounded-full h-2 overflow-hidden">
                        <motion.div
                            className="bg-[#10B981] h-2 rounded-full"
                            initial={{ width: 0 }}
                            animate={{ width: `${progress}%` }}
                            transition={{ duration: 0.5 }}
                        />
                    </div>
                </div>
            )}

            <div className="mt-8 flex justify-end">
                <Button
                    onClick={handleUpload}
                    disabled={isUploading || (!file && !text)}
                    className="bg-gradient-to-r from-[#10B981] to-[#34D399] hover:opacity-90 min-w-[150px] py-6 text-lg"
                >
                    {isUploading ? "Yuklanmoqda..." : "Tahlil qilish"}
                </Button>
            </div>
        </div>
    );
}
