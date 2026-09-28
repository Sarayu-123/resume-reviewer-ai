"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import type { Suggestion } from "@/lib/types"

interface SuggestionsPanelProps {
  suggestions: Suggestion[]
  isLoading: boolean
  onRefresh: () => void
}

export function SuggestionsPanel({
  suggestions,
  isLoading,
  onRefresh,
}: SuggestionsPanelProps) {

  return (
    <Card className="border-blue-100 bg-white/80 backdrop-blur-sm shadow-lg">
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle className="text-lg text-foreground">
          AI Suggestions
        </CardTitle>

        <Button
          size="sm"
          variant="outline"
          onClick={onRefresh}
        >
          Refresh
        </Button>
      </CardHeader>

      <CardContent className="space-y-3">

        {isLoading && (
          <p className="text-sm text-muted-foreground">
            Generating AI suggestions...
          </p>
        )}

        {!isLoading && suggestions.length === 0 && (
          <p className="text-sm text-muted-foreground">
            No suggestions available yet.
          </p>
        )}

        {!isLoading && suggestions.map((suggestion, index) => (
          <div
            key={index}
            className="rounded-xl p-4 bg-blue-50 border border-blue-100"
          >
            <h4 className="font-semibold text-blue-700">
              {suggestion.title}
            </h4>

            <p className="text-sm text-muted-foreground mt-1">
              {suggestion.description}
            </p>
          </div>
        ))}

      </CardContent>
    </Card>
  )
}