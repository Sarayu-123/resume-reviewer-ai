"use client"

import { Card, CardContent } from "@/components/ui/card"

export function EmptyState() {
  const features = [
    {
      icon: "\u{1F3AF}",
      title: "Skill Matching",
      description: "See how your skills align with job requirements",
      gradient: "from-blue-500 to-cyan-500",
      bg: "from-blue-50 to-cyan-50",
    },
    {
      icon: "\u{1F4CA}",
      title: "Score Analysis",
      description: "Get an overall compatibility score for your resume",
      gradient: "from-cyan-500 to-sky-500",
      bg: "from-cyan-50 to-sky-50",
    },
    {
      icon: "\u{1F4A1}",
      title: "AI Suggestions",
      description: "Receive personalized improvement recommendations",
      gradient: "from-sky-500 to-blue-500",
      bg: "from-sky-50 to-blue-50",
    },
    {
      icon: "\u{1F916}",
      title: "ATS Optimization",
      description: "Ensure your resume passes tracking systems",
      gradient: "from-blue-600 to-cyan-500",
      bg: "from-blue-50 to-cyan-50",
    },
  ]

  return (
    <div className="col-span-2 flex flex-col items-center justify-center py-8">
      <Card className="border-blue-100 bg-white/80 backdrop-blur-sm shadow-xl shadow-blue-500/5 max-w-2xl w-full overflow-hidden">
        <div className="h-1 w-full bg-gradient-to-r from-blue-500 via-cyan-500 to-sky-500" />
        <CardContent className="pt-10 pb-12 px-8 text-center">
          {/* Animated Icon */}
          <div className="flex justify-center mb-6">
            <div className="relative">
              <div className="w-24 h-24 rounded-3xl bg-gradient-to-br from-blue-500 via-cyan-500 to-sky-500 shadow-2xl shadow-blue-500/30 flex items-center justify-center animate-pulse">
                <span className="text-5xl">{"\u{1F4C4}"}</span>
              </div>
              <div className="absolute -right-2 -top-2 w-8 h-8 rounded-full bg-gradient-to-br from-cyan-400 to-blue-400 flex items-center justify-center shadow-lg animate-bounce">
                <span className="text-sm">{"\u2728"}</span>
              </div>
            </div>
          </div>
          
          <h2 className="text-2xl font-bold text-blue-900 mb-3">
            Upload Your Resume to Get Started
          </h2>
          <p className="text-muted-foreground mb-8 max-w-md mx-auto">
            Our AI will analyze your resume against your target role and provide actionable insights to improve your chances {"\u{1F680}"}
          </p>

          <div className="grid grid-cols-2 gap-4">
            {features.map((feature) => (
              <div
                key={feature.title}
                className={`p-5 rounded-2xl bg-gradient-to-br ${feature.bg} border-2 border-transparent hover:border-blue-200 transition-all duration-300 hover:scale-[1.02] hover:shadow-lg text-left cursor-default`}
              >
                <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${feature.gradient} flex items-center justify-center mb-3 shadow-lg`}>
                  <span className="text-2xl">{feature.icon}</span>
                </div>
                <h3 className="text-sm font-bold text-foreground mb-1">
                  {feature.title}
                </h3>
                <p className="text-xs text-muted-foreground leading-relaxed">
                  {feature.description}
                </p>
              </div>
            ))}
          </div>

          {/* Trust badges */}
          <div className="flex items-center justify-center gap-6 mt-8 pt-6 border-t border-blue-100">
            <div className="flex items-center gap-2 text-xs text-muted-foreground">
              <span>{"\u{1F512}"}</span>
              <span>Secure & Private</span>
            </div>
            <div className="flex items-center gap-2 text-xs text-muted-foreground">
              <span>{"\u26A1"}</span>
              <span>Instant Results</span>
            </div>
            <div className="flex items-center gap-2 text-xs text-muted-foreground">
              <span>{"\u{1F4AF}"}</span>
              <span>AI-Powered</span>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
