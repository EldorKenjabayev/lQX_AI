import { AIAdvantage } from "@/components/AIAdvantage";
import { Features } from "@/components/Features";
import { FinalCTA } from "@/components/FinalCTA";
import { Hero } from "@/components/Hero";
import { HowItWorks } from "@/components/HowItWorks";
import { Navigation } from "@/components/Navigation";
import { Pricing } from "@/components/Pricing";

export default function App() {
  return (
    <div className="min-h-screen bg-linear-to-br from-[#0A1628] via-[#0F172A] to-[#1E293B] text-white overflow-x-hidden">
      <Navigation />
      <Hero />
      <HowItWorks />
      <Features />
      <Pricing />
      <AIAdvantage />
      <FinalCTA />
    </div>
  );
}
