"use client";

import { useEffect, Suspense } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { setCookie } from "cookies-next";

function CallbackContent() {
    const router = useRouter();
    const searchParams = useSearchParams();

    useEffect(() => {
        const access_token = searchParams.get("access_token");
        const user_id = searchParams.get("user_id");

        if (access_token && user_id) {
            // Token va user_id ni saqlash
            setCookie("access_token", access_token, { maxAge: 60 * 60 * 24 * 7 }); // 7 kun
            setCookie("user_id", user_id, { maxAge: 60 * 60 * 24 * 7 });

            // Backend ga user ma'lumotlarini tekshirish
            fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/me`, {
                headers: {
                    Authorization: `Bearer ${access_token}`,
                },
            })
                .then((res) => res.json())
                .then((user) => {
                    if (!user.business_type) {
                        // Onboardingga yo'naltirish
                        router.push("/onboarding");
                    } else {
                        // Dashboardga yo'naltirish
                        router.push("/dashboard");
                    }
                })
                .catch((err) => {
                    console.error("Auth check failed:", err);
                    router.push("/login");
                });
        } else {
            // Token yo'q bo'lsa loginга qaytarish
            router.push("/login");
        }
    }, [searchParams, router]);

    return (
        <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-[#0A1628] to-[#1A2642]">
            <div className="text-center">
                <div className="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-[#10B981]"></div>
                <p className="mt-4 text-gray-300">Tizimga kirilmoqda...</p>
            </div>
        </div>
    );
}

export default function AuthCallbackPage() {
    return (
        <Suspense
            fallback={
                <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-[#0A1628] to-[#1A2642]">
                    <div className="text-center">
                        <div className="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-[#10B981]"></div>
                        <p className="mt-4 text-gray-300">Yuklanmoqda...</p>
                    </div>
                </div>
            }
        >
            <CallbackContent />
        </Suspense>
    );
}
