"use client"

import { useState, useRef, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Mic, MicOff, Activity } from "lucide-react"


export default function AudioRecorder() {
  const [isRecording, setIsRecording] = useState(false)
  const [audioLevel, setAudioLevel] = useState(0)
  const [status, setStatus] = useState("Ready")
  const [countdown, setCountdown] = useState<number | null>(null)

  const mediaRecorderRef = useRef<MediaRecorder | null>(null)
  const audioChunksRef = useRef<Blob[]>([])
  const silenceTimerRef = useRef<NodeJS.Timeout | null>(null)
  const socketRef = useRef<WebSocket | null>(null)
  const analyserRef = useRef<AnalyserNode | null>(null)
  const streamRef = useRef<MediaStream | null>(null)
  const animationFrameRef = useRef<number | null>(null)

  // Function to update audio visualization
  const updateAudioVisualization = () => {
    if (analyserRef.current && isRecording) {
      const bufferLength = analyserRef.current.frequencyBinCount
      const dataArray = new Uint8Array(bufferLength)
      analyserRef.current.getByteFrequencyData(dataArray)

      // Calculate average volume
      const averageVolume = dataArray.reduce((sum, value) => sum + value, 0) / bufferLength
      // Scale to 0-100 for progress bar
      const scaledVolume = Math.min(100, Math.max(0, averageVolume * 2))
      setAudioLevel(scaledVolume)

      animationFrameRef.current = requestAnimationFrame(updateAudioVisualization)
    }
  }

  // Clean up animation frame on unmount
  useEffect(() => {
    return () => {
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current)
      }
    }
  }, [])

  const startRecording = async () => {
    try {
      setStatus("Connecting...")

      // WebSocket connection
      const socket = new WebSocket("ws://localhost:8000/media-stream")
      socketRef.current = socket

      socket.onopen = () => {
        setStatus("Connected")
        console.log("✅ WebSocket Connected")
      }
      socket.onclose = () => {
        setStatus("Disconnected")
        console.log("❌ WebSocket Disconnected")
      }
      socket.onerror = (error) => {
        setStatus("Error")
        console.log("⚠️ WebSocket Error:", error)
      }

      // Get audio stream
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      streamRef.current = stream

      // Set up AudioContext
      const audioContext = new AudioContext()
      const analyser = audioContext.createAnalyser()
      const microphone = audioContext.createMediaStreamSource(stream)

      microphone.connect(analyser)
      analyser.fftSize = 256
      analyserRef.current = analyser

      // Set up MediaRecorder
      const mediaRecorder = new MediaRecorder(stream, {
        mimeType: "audio/webm",
        audioBitsPerSecond: 128000,
      })

      mediaRecorderRef.current = mediaRecorder
      audioChunksRef.current = []
      
      // Set recording state first before starting visualization
      setIsRecording(true)
      setStatus("Recording")

      // Start audio visualization - calling this function here explicitly
      animationFrameRef.current = requestAnimationFrame(updateAudioVisualization)

      // Collect audio chunks
      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data)
        }
      }

      // Voice detection logic
      const bufferLength = analyser.frequencyBinCount
      const dataArray = new Uint8Array(bufferLength)
      let isSpeaking = false

      const checkSilence = () => {
        analyser.getByteFrequencyData(dataArray)

        // Calculate average volume
        const averageVolume = dataArray.reduce((sum, value) => sum + value, 0) / bufferLength

        if (averageVolume < 10) {
          // No sound
          if (isSpeaking) {
            // Speech stopped
            setStatus("Silence detected")
            silenceTimerRef.current = setTimeout(() => {
              setStatus("Processing")
              mediaRecorder.stop()
              isSpeaking = false
            }, 1500) // Changed to 1.5 seconds as per requirement

            // Start countdown
            setCountdown(1.5)
            const startTime = Date.now()

            const updateCountdown = () => {
              const elapsed = (Date.now() - startTime) / 1000
              const remaining = Math.max(0, 1.5 - elapsed)
              setCountdown(remaining)

              if (remaining > 0 && isSpeaking) {
                requestAnimationFrame(updateCountdown)
              }
            }

            requestAnimationFrame(updateCountdown)
          }
        } else {
          // Speaking
          isSpeaking = true
          setStatus("Recording")
          setCountdown(null)
          if (silenceTimerRef.current) {
            clearTimeout(silenceTimerRef.current)
            silenceTimerRef.current = null
          }
        }
      }

      // Start recording
      mediaRecorder.start(100)

      // Check voice periodically (every 100ms)
      const silenceCheckInterval = setInterval(checkSilence, 100)

      // Handle recording stop
      mediaRecorder.onstop = async () => {
        if (animationFrameRef.current) {
          cancelAnimationFrame(animationFrameRef.current)
          animationFrameRef.current = null
        }

        clearInterval(silenceCheckInterval)
        setCountdown(null)

        if (audioChunksRef.current.length > 0) {
          setStatus("Sending to server")
          const audioBlob = new Blob(audioChunksRef.current, { type: "audio/webm" })
          const arrayBuffer = await audioBlob.arrayBuffer()

          console.log(`📤 Sending ${arrayBuffer.byteLength} bytes to server`)
          socket.send(arrayBuffer)

          // Explicitly close socket after data transmission
          socket.close()
        }

        // Clean up resources
        stream.getTracks().forEach((track) => track.stop())
        audioContext.close()

        setIsRecording(false)
        setAudioLevel(0)
        setStatus("Ready")
      }
    } catch (error) {
      console.error("Error starting recording:", error)
      setIsRecording(false)
      setStatus("Error")
    }
  }

  return (
    <div className="flex items-center justify-center min-h-screen bg-gradient-to-b from-gray-50 to-gray-100 p-4">
      <Card className="w-full max-w-md shadow-lg">
        <CardHeader className="text-center">
          <CardTitle className="text-2xl">Voice Recorder</CardTitle>
          <CardDescription>
            Press the button and speak. Recording will be sent after 1.5 seconds of silence.
          </CardDescription>
        </CardHeader>

        <CardContent className="flex flex-col items-center gap-2">
          <div className="relative w-32 h-32 flex items-center justify-center">
            <div
              className={`absolute inset-0 rounded-full ${isRecording ? "bg-red-100 animate-pulse" : "bg-gray-100"}`}
            ></div>
            <Button
              onClick={startRecording}
              disabled={isRecording}
              className={`relative z-10 w-24 h-24 rounded-full ${isRecording ? "bg-red-500 hover:bg-red-600" : "bg-emerald-500 hover:bg-emerald-600"}`}
            >
              {isRecording ? <MicOff className="h-10 w-10 text-white" /> : <Mic className="h-10 w-10 text-white" />}
            </Button>
          </div>
        </CardContent>

        <CardFooter className="flex justify-center border-t pt-4">
          <p className="text-xs text-gray-500 text-center">
            {isRecording
              ? "Speak now. Recording will automatically stop after silence."
              : "Click the button to start recording"}
          </p>
        </CardFooter>
      </Card>
    </div>
  )
}