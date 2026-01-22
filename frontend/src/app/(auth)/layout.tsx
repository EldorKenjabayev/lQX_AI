export default function AuthLayout({
    children,
}: {
    children: React.ReactNode
}) {
    return (
        <div className="flex min-h-screen items-center justify-center bg-linear-to-br from-[#0A1628] via-[#0F172A] to-[#1E293B] p-4 text-white">
            <div className="w-full max-w-md space-y-8">
                <div className="text-center">
                    <h2 className="mt-6 text-3xl font-bold tracking-tight bg-gradient-to-r from-[#10B981] to-[#34D399] bg-clip-text text-transparent">
                        LQX AI
                    </h2>
                </div>
                {children}
            </div>
        </div>
    )
}
