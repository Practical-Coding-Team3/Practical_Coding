"use client"

import type React from "react"
import axios from "axios"
import { useState, useRef } from "react"
import { Search, Loader2, ArrowRight, Clock, TrendingUp } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { motion, AnimatePresence } from "framer-motion"


export default function SearchBrowser() {
  const [query, setQuery] = useState("")
  const inputRef = useRef<HTMLInputElement>(null) // React에서는 이렇게!
  const [hasSearched, setHasSearched] = useState(false)
  const [results, setResults] = useState<any[]>([])
  const [isSearching, setIsSearching] = useState(false)
  const [recentSearches] = useState(["인공지능", "웹 개발", "React", "Next.js"])
  const [trendingSearches] = useState(["최신 기술", "프로그래밍 언어", "디자인 트렌드", "AI 개발"])

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!query.trim()) return

    setIsSearching(true)
   
    const response = await axios.post("http://localhost:8000/text", { text: query });
  


    // 검색 효과를 위한 타임아웃
    setTimeout(() => {
      // 가상 검색 결과
      const mockResults = [
        {
          id: 1,
         
          description: "이것은 첫 번째 검색 결과입니다. 여기에는 검색어와 관련된 자세한 정보가 표시됩니다.",
          url: "https://example.com/result1",
          category: "웹사이트",
        },
        {
          id: 2,
    
          description:
            "두 번째 검색 결과에는 더 많은 정보와 관련 링크가 포함되어 있습니다. 사용자가 원하는 정보를 쉽게 찾을 수 있도록 도와줍니다.",
          url: "https://example.com/result2",
          category: "블로그",
        },
        {
          id: 3,
          description:
            "세 번째 검색 결과는 사용자의 검색어와 가장 관련성이 높은 정보를 제공합니다. 여기에는 자세한 설명과 함께 유용한 링크가 포함되어 있습니다.",
          url: "https://example.com/result3",
          category: "뉴스",
        },
        {
          id: 4,
          description:
            "네 번째 검색 결과는 사용자가 찾고 있는 정보에 대한 추가적인 내용을 제공합니다. 이 결과는 검색어와 관련된 다양한 측면을 다룹니다.",
          url: "https://example.com/result4",
          category: "포럼",
        },
        {
          id: 5,
          description:
            "다섯 번째 검색 결과는 사용자의 검색어와 관련된 최신 정보를 제공합니다. 이 결과는 최근에 업데이트된 내용을 포함하고 있습니다.",
          url: "https://example.com/result5",
          category: "학술자료",
        },
        {
          id: 6,
          description:
            "여섯 번째 검색 결과는 사용자의 검색어와 관련된 심층적인 분석을 제공합니다. 이 결과는 주제에 대한 깊이 있는 이해를 원하는 사용자에게 유용합니다.",
          url: "https://example.com/result6",
          category: "비디오",
        },
      ]

      setResults(mockResults)
      setHasSearched(true)
      setIsSearching(false)
    }, 800) // 검색 효과를 위한 지연 시간
  }




  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800 p-4 transition-all duration-300">
      <div className="max-w-5xl mx-auto">
        <div
          className={`w-full max-w-3xl mx-auto transition-all duration-500 ease-in-out ${
            hasSearched ? "pt-4" : "pt-[25vh]"
          }`}
        >
          {!hasSearched && (
            <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }} className="text-center mb-8">
              <h1 className="text-4xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent mb-2">
                웹 검색
              </h1>
              <p className="text-slate-600 dark:text-slate-300">원하는 정보를 빠르게 찾아보세요</p>
            </motion.div>
          )}

          <form onSubmit={handleSearch} className="w-full">
            <div className="relative flex gap-2 group">
              <div className="relative flex-1">
                <div className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400">
                  {isSearching ? <Loader2 className="h-5 w-5 animate-spin" /> : <Search className="h-5 w-5" />}
                </div>
                <Input
                  type="text"
                  placeholder="검색어를 입력하세요"
                  className="w-full pl-10 h-12 bg-white dark:bg-slate-800 border-slate-200 dark:border-slate-700 rounded-xl shadow-sm focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                />
              </div>
              <Button
                type="submit"
                className="h-12 px-6 rounded-xl bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white shadow-md hover:shadow-lg transition-all"
                disabled={isSearching}
              >
                {isSearching ? "검색 중..." : "검색"}
              </Button>
            </div>
          </form>

          {!hasSearched && (
            <div className="mt-8">
              <div className="mb-6">
                <div className="flex items-center text-sm text-slate-500 dark:text-slate-400 mb-2">
                  <Clock className="h-4 w-4 mr-2" />
                  <span>최근 검색어</span>
                </div>
                <div className="flex flex-wrap gap-2">
                  {recentSearches.map((term, index) => (
                    <button
                      key={index}
                      className="px-3 py-1.5 bg-white dark:bg-slate-800 rounded-full text-sm border border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors"
                      onClick={() => {
                        setQuery(term)
                        handleSearch(new Event("submit") as any)
                      }}
                    >
                      {term}
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <div className="flex items-center text-sm text-slate-500 dark:text-slate-400 mb-2">
                  <TrendingUp className="h-4 w-4 mr-2" />
                  <span>인기 검색어</span>
                </div>
                <div className="flex flex-wrap gap-2">
                  {trendingSearches.map((term, index) => (
                    <button
                      key={index}
                      className="px-3 py-1.5 bg-white dark:bg-slate-800 rounded-full text-sm border border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors"
                      onClick={() => {
                        setQuery(term)
                        handleSearch(new Event("submit") as any)
                      }}
                    >
                      {term}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          )}

          <AnimatePresence>
            {hasSearched && (
              <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="mt-8 space-y-4">
                <p className="text-sm text-slate-500 dark:text-slate-400 mb-4">
                  "{query}"에 대한 검색 결과 {results.length}개
                </p>

                {results.map((result, index) => (
                  <motion.div
                    key={result.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.1 }}
                    className="bg-white dark:bg-slate-800 rounded-xl p-5 shadow-sm hover:shadow-md transition-all border border-slate-100 dark:border-slate-700"
                  >
                    <div className="flex items-start">
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-1">
                          <span className="text-xs px-2 py-0.5 bg-purple-100 dark:bg-purple-900 text-purple-800 dark:text-purple-100 rounded-full">
                            {result.category}
                          </span>
                          <span className="text-xs text-slate-500 dark:text-slate-400 truncate">{result.url}</span>
                        </div>
                        <h2 className="text-xl font-semibold mb-2 text-slate-900 dark:text-white">{result.title}</h2>
                        <p className="text-slate-600 dark:text-slate-300 text-sm">{result.description}</p>
                      </div>
                      <Button
                        variant="ghost"
                        size="icon"
                        className="ml-2 text-slate-400 hover:text-purple-600 dark:text-slate-500 dark:hover:text-purple-400"
                      >
                        <ArrowRight className="h-5 w-5" />
                        <span className="sr-only">방문하기</span>
                      </Button>
                    </div>
                  </motion.div>
                ))}
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </main>
  )
}
