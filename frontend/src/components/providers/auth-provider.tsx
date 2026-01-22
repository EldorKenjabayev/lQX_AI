"use client";

import { createContext, useContext, useEffect, useState } from "react";
import { useRouter, usePathname } from "next/navigation";
import { getCookie, deleteCookie } from "cookies-next";
import api from "@/lib/api";

type User = {
    id: string;
    email: string;
    business_type?: string | null;
    auth_provider: string;
};

type AuthContextType = {
    user: User | null;
    isLoading: boolean;
    logout: () => void;
};

const AuthContext = createContext<AuthContextType>({
    user: null,
    isLoading: true,
    logout: () => { },
});

export function AuthProvider({ children }: { children: React.ReactNode }) {
    const router = useRouter();
    const pathname = usePathname();
    const [user, setUser] = useState<User | null>(null);
    const [isLoading, setIsLoading] = useState(true);

    const logout = () => {
        deleteCookie("access_token");
        deleteCookie("user_id");
        setUser(null);
        router.push("/");
    };

    useEffect(() => {
        const checkAuth = async () => {
            const token = getCookie("access_token");
            const isPublicRoute = ["/", "/login", "/register", "/auth/callback"].includes(pathname);

            if (!token) {
                if (!isPublicRoute) {
                    router.push("/login");
                }
                setIsLoading(false);
                return;
            }

            try {
                const { data } = await api.get("/auth/me");
                setUser(data);

                // Onboarding check
                if (!data.business_type && pathname.startsWith("/dashboard")) {
                    router.push("/onboarding");
                } else if (data.business_type && pathname === "/onboarding") {
                    // Agar business_type bo'lsa, onboardingga kirish shart emas
                    router.push("/dashboard");
                }

            } catch (error) {
                console.error("Auth check failed:", error);
                // Token valid emas
                deleteCookie("access_token");
                if (!isPublicRoute) {
                    router.push("/login");
                }
            } finally {
                setIsLoading(false);
            }
        };

        checkAuth();
    }, [pathname, router]);

    return (
        <AuthContext.Provider value={{ user, isLoading, logout }}>
            {children}
        </AuthContext.Provider>
    );
}

export const useAuth = () => useContext(AuthContext);
