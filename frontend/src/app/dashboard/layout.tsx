import { Sidebar } from "@/components/dashboard/sidebar"
import { Header } from "@/components/dashboard/header"

export default function DashboardLayout({
    children,
}: {
    children: React.ReactNode
}) {
    return (
        <div className="h-screen overflow-hidden relative bg-linear-to-br from-[#0A1628] via-[#0F172A] to-[#1E293B] text-white">
            <div className="hidden h-full md:flex md:w-72 md:flex-col md:fixed md:inset-y-0 z-[80]">
                <Sidebar />
            </div>
            <main className="md:pl-72 h-full overflow-y-auto">
                <Header />
                {children}
            </main>
        </div >
    )
}
