"use client";

import { UploadZone } from "@/components/dashboard/upload-zone";

export default function UploadPage() {
    return (
        <div className="min-h-screen bg-gradient-to-br from-[#0A1628] to-[#1A2642] p-6">
            <div className="max-w-7xl mx-auto">
                {/* Header */}
                <div className="mb-8">
                    <h1 className="text-3xl font-bold text-white mb-2">Ma'lumot Yuklash</h1>
                    <p className="text-gray-400">
                        Bank ko'chirmalari (PDF), Excel jadvallar yoki shunchaki SMS xabarlarni yuklang.
                        AI avtomatik tahlil qiladi.
                    </p>
                </div>

                {/* Upload Zone */}
                <div className="mt-10">
                    <UploadZone />
                </div>
            </div>
        </div>
    );
}
