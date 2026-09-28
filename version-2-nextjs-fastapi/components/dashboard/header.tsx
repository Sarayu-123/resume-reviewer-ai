"use client"

import { Sparkles, Bell, Settings } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"

export function DashboardHeader() {
  return (
    <header className="border-b border-blue-100 bg-white/70 backdrop-blur-xl sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex items-center gap-3">
            <div className="flex items-center justify-center w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-cyan-500 shadow-lg shadow-blue-500/25">
              <Sparkles className="w-5 h-5 text-white" />
            </div>
            <div>
              <h1 className="text-lg font-bold text-blue-900 tracking-tight">
                ResumeAI
              </h1>
              <p className="text-xs text-muted-foreground">AI-Powered Analysis</p>
            </div>
          </div>

          {/* Right Side */}
          <div className="flex items-center gap-2">
            <Button variant="ghost" size="icon" className="relative hover:bg-blue-50">
              <Bell className="w-5 h-5 text-muted-foreground" />
              <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-blue-500 rounded-full animate-pulse" />
            </Button>
            
            <Button variant="ghost" size="icon" className="hover:bg-blue-50">
              <Settings className="w-5 h-5 text-muted-foreground" />
            </Button>

            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" className="relative h-9 w-9 rounded-full ml-2 ring-2 ring-blue-100 hover:ring-blue-200 transition-all">
                  <Avatar className="h-9 w-9">
                    <AvatarImage src="/avatar.png" alt="User" />
                    <AvatarFallback className="bg-gradient-to-br from-blue-500 to-cyan-500 text-white font-medium">JD</AvatarFallback>
                  </Avatar>
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent className="w-56 bg-white/95 backdrop-blur-xl border-blue-100" align="end" forceMount>
                <DropdownMenuLabel className="font-normal">
                  <div className="flex flex-col space-y-1">
                    <p className="text-sm font-medium leading-none">John Doe</p>
                    <p className="text-xs leading-none text-muted-foreground">
                      john@example.com
                    </p>
                  </div>
                </DropdownMenuLabel>
                <DropdownMenuSeparator className="bg-blue-100" />
                <DropdownMenuItem className="hover:bg-blue-50 cursor-pointer">
                  <span className="mr-2">&#x1F464;</span> Profile
                </DropdownMenuItem>
                <DropdownMenuItem className="hover:bg-blue-50 cursor-pointer">
                  <span className="mr-2">&#x1F4B3;</span> Billing
                </DropdownMenuItem>
                <DropdownMenuItem className="hover:bg-blue-50 cursor-pointer">
                  <span className="mr-2">&#x2699;&#xFE0F;</span> Settings
                </DropdownMenuItem>
                <DropdownMenuSeparator className="bg-blue-100" />
                <DropdownMenuItem className="hover:bg-red-50 text-red-600 cursor-pointer">
                  <span className="mr-2">&#x1F6AA;</span> Log out
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
        </div>
      </div>
    </header>
  )
}
