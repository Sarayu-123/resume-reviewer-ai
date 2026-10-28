import { NextResponse } from "next/server"

export async function POST(request: Request) {
  try {
    const body = await request.json()

    if (!body.resumeText || !body.jdText) {
      return NextResponse.json(
        {
          error: "Both resumeText and jdText are required",
        },
        { status: 400 }
      )
    }

    const backendUrl =
      process.env.BACKEND_API_URL || "http://127.0.0.1:8000"

    const response = await fetch(`${backendUrl}/analyze-jd`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
      cache: "no-store",
    })

    const result = await response.json()

    if (!response.ok) {
      return NextResponse.json(
        {
          error:
            result.detail ||
            result.error ||
            "Job Description analysis failed",
        },
        { status: response.status }
      )
    }

    return NextResponse.json(result)
  } catch (error) {
    console.error("JD analysis request failed:", error)

    return NextResponse.json(
      {
        error: "Could not connect to the JD analysis backend",
      },
      { status: 502 }
    )
  }
}

