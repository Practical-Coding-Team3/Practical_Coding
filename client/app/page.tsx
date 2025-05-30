"use client"

import type React from "react"
import { useState, useRef, useEffect } from "react"
import { Search, Loader2, ArrowRight, Clock, X } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { motion, AnimatePresence } from "framer-motion"

const RECENT_SEARCHES_KEY = "recentSearches"
const MAX_RECENT_SEARCHES = 5 // 저장할 최대 최근 검색어 개수

export default function SearchBrowser() {
  const [query, setQuery] = useState("")
  const inputRef = useRef<HTMLInputElement>(null) // React에서는 이렇게!
  const [hasSearched, setHasSearched] = useState(false)
  const [results, setResults] = useState<{ main?: any; sub?: any[] }>({})
  const [isSearching, setIsSearching] = useState(false)
  const [recentSearches, setRecentSearches] = useState<string[]>([])
  const [selectedResult, setSelectedResult] = useState<any>(null)

  // 스택 형태로 모달 상태 관리
  const [resultStack, setResultStack] = useState<any[]>([])

  // 모달 닫기 (스택 pop)
  const handleCloseModal = () => {
    setResultStack((prev) => prev.slice(0, -1))
  }

  // 현재 모달에 표시할 내용
  const currentResult = resultStack[resultStack.length - 1]


  useEffect(() => {
    const storedSearches = localStorage.getItem(RECENT_SEARCHES_KEY)
    if (storedSearches) {
      setRecentSearches(JSON.parse(storedSearches))
    }
  }, [query])

  // 링크를 적용할 단어 목록(모의)
  const keywordLinks: Record<string, string> = {
    분야: "https://example.com/definition/분야",
    출처: "https://example.com/definition/출처",
    동향: "https://example.com/definition/동향",
  }

  // 어려운 단어 설명 페이지(모의)
  const keywordDetails: Record<string, any> = {
    분야: {
      id: "분야",
      title: `"분야"의 의미`,
      description: "분야는 지식이나 활동이 나누어진 특정 영역을 의미합니다.",
      fullDescription:
        "‘분야’는 특정한 전문 영역이나 주제를 지칭합니다. 예: 의료 분야, 교육 분야 등으로 나뉘며, 이 용어는 조직화된 주제나 활동 범위를 나타냅니다.",
      url: "https://example.com/definition/분야",
      category: "어려운 단어",
      image: "/placeholder.svg?height=200&width=300",
      publishDate: "2024년 1월 20일",
      readTime: "1분 읽기",
    },
    출처: {
      id: "출처",
      title: `"출처"의 의미`,
      description: "출처는 어떤 정보나 자료가 나온 곳을 의미합니다.",
      fullDescription:
        "‘출처’는 정보나 인용이 어디에서 유래했는지를 나타냅니다. 신뢰할 수 있는 출처는 콘텐츠의 신뢰도를 높여줍니다.",
      url: "https://example.com/definition/출처",
      category: "어려운 단어",
      image: "/placeholder.svg?height=200&width=300",
      publishDate: "2024년 1월 21일",
      readTime: "1분 읽기",
    },
    동향: {
      id: "동향",
      title: `"동향"의 의미`,
      description: "동향은 어떤 주제나 현상의 변화나 움직임을 말합니다.",
      fullDescription:
        "‘동향’은 사회, 산업, 기술 등의 분야에서 나타나는 변화의 흐름을 의미합니다. 예를 들어 ‘기술 동향’은 기술이 어떤 방향으로 발전하고 있는지를 설명합니다.",
      url: "https://example.com/definition/동향",
      category: "어려운 단어",
      image: "/placeholder.svg?height=200&width=300",
      publishDate: "2024년 1월 22일",
      readTime: "1분 읽기",
    },
  }


  // 단어 강조 및 클릭 시 모달 스택에 push
  function highlightKeywords(text: string): React.ReactNode[] {
    const parts = text.split(new RegExp(`(${Object.keys(keywordDetails).join("|")})`, "g"))
    return parts.map((part, index) => {
      if (keywordDetails[part]) {
        return (
          <button
            key={index}
            className="text-purple-600 underline hover:opacity-80"
            onClick={(e) => {
              e.stopPropagation()
              setResultStack((prev) => [...prev, keywordDetails[part]])
            }}
          >
            {part}
          </button>
        )
      }
      return <span key={index}>{part}</span>
    })
  }

  const saveRecentSearch = (newQuery: string) => {
    if (newQuery.trim() === "") return
    // 기존 검색어 목록 불러오기
    const storedSearches = localStorage.getItem(RECENT_SEARCHES_KEY)
    const recentSearches = storedSearches ? JSON.parse(storedSearches) : []
    // 중복된 검색어 제거 후 새로운 검색어 추가
    const updatedSearches = [newQuery, ...recentSearches.filter((q: string) => q !== newQuery)].slice(
      0,
      MAX_RECENT_SEARCHES,
    )
    // 업데이트된 목록 로컬 스토리지에 저장
    localStorage.setItem(RECENT_SEARCHES_KEY, JSON.stringify(updatedSearches))
  }

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!query.trim()) return
    setIsSearching(true)
    console.log(inputRef.current?.value)
    saveRecentSearch(query)

    // const response = await axios.post("http://localhost:8000/text", { text: query });
    // 검색 효과를 위한 타임아웃
    setTimeout(() => {
      const mainResult = {
        id: "main",
        title: `"${query}"에 대한 주요 정보`,
        description: `${query}에 대한 가장 관련성 높은 정보입니다. 이 결과는 사용자가 찾고 있는 핵심 내용을 포함하고 있으며, 신뢰할 수 있는 출처에서 제공됩니다. 여기에는 상세한 설명과 함께 관련 링크, 이미지, 그리고 추가 정보가 포함되어 있습니다.`,
        fullDescription: `${query}에 대한 상세한 정보입니다. 이 주제는 현재 많은 관심을 받고 있으며, 다양한 분야에서 활용되고 있습니다. 전문가들은 이 분야의 발전 가능성을 높게 평가하고 있으며, 앞으로도 지속적인 연구와 개발이 이루어질 것으로 예상됩니다. 이 정보는 신뢰할 수 있는 출처에서 수집되었으며, 최신 동향과 연구 결과를 반영하고 있습니다.`,
        url: "https://main-source.com",
        category: "주요 결과",
        image: "/placeholder.svg?height=200&width=300",
        publishDate: "2024년 1월 15일",
        readTime: "5분 읽기",
      }

      // 가상 검색 결과
      const mockResults = [
        {
          id: 1,
          title: `"${query}"에 대한 검색 결과 1`,
          description: "이것은 첫 번째 검색 결과입니다. 여기에는 검색어와 관련된 자세한 정보가 표시됩니다.",
          fullDescription: `${query}에 대한 첫 번째 상세 정보입니다. 이 내용은 기본적인 개념부터 고급 응용까지 포괄적으로 다루고 있으며, 실무에서 바로 활용할 수 있는 실용적인 정보를 제공합니다. 또한 최신 트렌드와 업계 동향을 반영하여 독자들이 현재 상황을 정확히 파악할 수 있도록 도와줍니다.`,
          url: "https://example.com/result1",
          category: "웹사이트",
          image: "/placeholder.svg?height=200&width=300",
          publishDate: "2024년 1월 12일",
          readTime: "3분 읽기",
        },
        {
          id: 2,
          title: `"${query}"에 대한 검색 결과 2`,
          description:
            "두 번째 검색 결과에는 더 많은 정보와 관련 링크가 포함되어 있습니다. 사용자가 원하는 정보를 쉽게 찾을 수 있도록 도와줍니다.",
          fullDescription: `${query}에 대한 두 번째 상세 정보로, 다양한 관점에서의 분석과 해석을 제공합니다. 이 자료는 여러 전문가들의 의견을 종합하여 작성되었으며, 객관적이고 균형 잡힌 시각을 제시합니다. 독자들이 주제에 대해 깊이 있게 이해할 수 있도록 구체적인 사례와 데이터를 포함하고 있습니다.`,
          url: "https://example.com/result2",
          category: "블로그",
          image: "/placeholder.svg?height=200&width=300",
          publishDate: "2024년 1월 10일",
          readTime: "4분 읽기",
        },
        {
          id: 3,
          title: `"${query}"에 대한 검색 결과 3`,
          description:
            "세 번째 검색 결과는 사용자의 검색어와 가장 관련성이 높은 정보를 제공합니다. 여기에는 자세한 설명과 함께 유용한 링크가 포함되어 있습니다.",
          fullDescription: `${query}에 대한 세 번째 상세 정보로, 실용적인 가이드와 단계별 설명을 제공합니다. 이 콘텐츠는 초보자도 쉽게 따라할 수 있도록 구성되었으며, 각 단계마다 상세한 설명과 주의사항을 포함하고 있습니다. 또한 자주 발생하는 문제들과 해결 방법도 함께 제시하여 실용성을 높였습니다.`,
          url: "https://example.com/result3",
          category: "뉴스",
          image: "/placeholder.svg?height=200&width=300",
          publishDate: "2024년 1월 8일",
          readTime: "6분 읽기",
        },
        {
          id: 4,
          title: `"${query}"에 대한 검색 결과 4`,
          description:
            "네 번째 검색 결과는 사용자가 찾고 있는 정보에 대한 추가적인 내용을 제공합니다. 이 결과는 검색어와 관련된 다양한 측면을 다룹니다.",
          fullDescription: `${query}에 대한 네 번째 상세 정보로, 최신 연구 결과와 업계 동향을 중심으로 작성되었습니다. 이 자료는 미래 전망과 발전 가능성을 다루며, 전문가들의 예측과 분석을 포함하고 있습니다. 독자들이 변화하는 환경에 대비할 수 있도록 실용적인 조언과 전략을 제시합니다.`,
          url: "https://example.com/result4",
          category: "포럼",
          image: "/placeholder.svg?height=200&width=300",
          publishDate: "2024년 1월 5일",
          readTime: "5분 읽기",
        },
        {
          id: 5,
          title: `"${query}"에 대한 검색 결과 5`,
          description:
            "다섯 번째 검색 결과는 사용자의 검색어와 관련된 최신 정보를 제공합니다. 이 결과는 최근에 업데이트된 내용을 포함하고 있습니다.",
          fullDescription: `${query}에 대한 다섯 번째 상세 정보로, 심화 학습을 원하는 사용자를 위한 고급 내용을 다룹니다. 이 자료는 이론적 배경부터 실제 적용 사례까지 포괄적으로 설명하며, 학술적 근거와 실증적 데이터를 바탕으로 작성되었습니다. 전문가 수준의 지식을 원하는 독자들에게 깊이 있는 통찰을 제공합니다.`,
          url: "https://example.com/result5",
          category: "학술자료",
          image: "/placeholder.svg?height=200&width=300",
          publishDate: "2024년 1월 3일",
          readTime: "8분 읽기",
        },
        {
          id: 6,
          title: `"${query}"에 대한 검색 결과 6`,
          description:
            "여섯 번째 검색 결과는 사용자의 검색어와 관련된 심층적인 분석을 제공합니다. 이 결과는 주제에 대한 깊이 있는 이해를 원하는 사용자에게 유용합니다.",
          fullDescription: `${query}에 대한 여섯 번째 상세 정보로, 다양한 시각과 접근 방법을 제시합니다. 이 콘텐츠는 국내외 사례를 비교 분석하여 작성되었으며, 문화적, 사회적 맥락을 고려한 해석을 제공합니다. 독자들이 글로벌 관점에서 주제를 이해할 수 있도록 폭넓은 정보와 인사이트를 담고 있습니다.`,
          url: "https://example.com/result6",
          category: "비디오",
          image: "/placeholder.svg?height=200&width=300",
          publishDate: "2024년 1월 1일",
          readTime: "7분 읽기",
        },
      ]

      setResults({ main: mainResult, sub: mockResults })
      setHasSearched(true)
      setIsSearching(false)
    }, 800) // 검색 효과를 위한 지연 시간
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800 p-4 transition-all duration-300">
      <div className="max-w-5xl mx-auto">
        <div
          className={`w-full max-w-3xl mx-auto transition-all duration-500 ease-in-out ${hasSearched ? "pt-4" : "pt-[25vh]"
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
                  ref={inputRef}
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
            </div>
          )}

          <AnimatePresence>
            {hasSearched && (
              <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="mt-8">
                <p className="text-sm text-slate-500 dark:text-slate-400 mb-6">"{query}"에 대한 검색 결과</p>

                {/* 메인 결과 */}
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.1 }}
                  className="bg-white dark:bg-slate-800 rounded-2xl p-6 shadow-lg hover:shadow-xl transition-all border border-slate-100 dark:border-slate-700 mb-8 cursor-pointer"
                  // onClick={() => setSelectedResult(results.main)}
                  onClick={() => setResultStack((prev) => [...prev, results.main])}
                >
                  <div className="flex items-start gap-4">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-2">
                        <span className="text-xs px-3 py-1 bg-gradient-to-r from-purple-100 to-pink-100 dark:from-purple-900 dark:to-pink-900 text-purple-800 dark:text-purple-100 rounded-full font-medium">
                          {results.main?.category}
                        </span>
                        <span className="text-xs text-slate-500 dark:text-slate-400">{results.main?.publishDate}</span>
                        <span className="text-xs text-slate-500 dark:text-slate-400">•</span>
                        <span className="text-xs text-slate-500 dark:text-slate-400">{results.main?.readTime}</span>
                      </div>
                      <h2 className="text-2xl font-bold mb-3 text-slate-900 dark:text-white leading-tight">
                        {results.main?.title}
                      </h2>
                      <p className="text-slate-600 dark:text-slate-300 mb-4 leading-relaxed">
                        {results.main?.description}
                      </p>
                      <div className="flex items-center justify-between">
                        <span className="text-sm text-slate-500 dark:text-slate-400 truncate">{results.main?.url}</span>
                      </div>
                    </div>
                    <div className="hidden md:block">
                      <img
                        src={results.main?.image || "/placeholder.svg"}
                        alt="메인 결과 이미지"
                        className="w-48 h-32 object-cover rounded-xl"
                      />
                    </div>
                  </div>
                </motion.div>

                {/* 부가 결과들 */}
                <div className="space-y-3">
                  <h3 className="text-lg font-semibold text-slate-900 dark:text-white mb-4">관련 결과</h3>
                  {results.sub?.map((result, index) => (
                    <motion.div
                      key={result.id}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: 0.2 + index * 0.1 }}
                      className="bg-white dark:bg-slate-800 rounded-xl p-4 shadow-sm hover:shadow-md transition-all border border-slate-100 dark:border-slate-700 group cursor-pointer"
                      // onClick={() => setSelectedResult(result)}
                      onClick={() => setResultStack((prev) => [...prev, result])}
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <div className="flex items-center gap-2 mb-1">
                            <span className="text-xs px-2 py-0.5 bg-slate-100 dark:bg-slate-700 text-slate-700 dark:text-slate-300 rounded-full">
                              {result.category}
                            </span>
                            <span className="text-xs text-slate-500 dark:text-slate-400 truncate">{result.url}</span>
                          </div>
                          <h4 className="text-lg font-medium mb-1 text-slate-900 dark:text-white group-hover:text-purple-600 dark:group-hover:text-purple-400 transition-colors">
                            {result.title}
                          </h4>
                          <p className="text-sm text-slate-600 dark:text-slate-300 line-clamp-2">
                            {result.description}
                          </p>
                        </div>
                        <Button
                          variant="ghost"
                          size="icon"
                          className="ml-3 text-slate-400 hover:text-purple-600 dark:text-slate-500 dark:hover:text-purple-400 opacity-0 group-hover:opacity-100 transition-all"
                        >
                          <ArrowRight className="h-4 w-4" />
                          <span className="sr-only">방문하기</span>
                        </Button>
                      </div>
                    </motion.div>
                  ))}
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>

      {/* 모달 */}
      {/* {selectedResult && ( */}
      {currentResult && (
        <div
          className="fixed inset-0 backdrop-blur-sm bg-white/5 bg-opacity-50 flex items-center justify-center p-4 z-50"
          // onClick={() => setSelectedResult(null)}
          onClick={handleCloseModal}
        >
          <div
            className="bg-white dark:bg-slate-800 rounded-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="p-6">
              <div className="flex justify-between items-start mb-4">
                <div className="flex items-center gap-2">
                  <span className="text-xs px-3 py-1 bg-gradient-to-r from-purple-100 to-pink-100 dark:from-purple-900 dark:to-pink-900 text-purple-800 dark:text-purple-100 rounded-full font-medium">
                    {/* {selectedResult.category} */}
                    {currentResult.category}
                  </span>
                  {/* <span className="text-xs text-slate-500 dark:text-slate-400">{selectedResult.publishDate}</span> */}
                  <span className="text-xs text-slate-500 dark:text-slate-400">{currentResult.publishDate}</span>
                  <span className="text-xs text-slate-500 dark:text-slate-400">•</span>
                  {/* <span className="text-xs text-slate-500 dark:text-slate-400">{selectedResult.readTime}</span> */}
                  <span className="text-xs text-slate-500 dark:text-slate-400">{currentResult.readTime}</span>
                </div>
                <button
                  // onClick={() => setSelectedResult(null)}
                  onClick={handleCloseModal}
                  className="text-slate-400 hover:text-slate-600 dark:hover:text-slate-300"
                >
                  <X className="h-6 w-6" />
                </button>
              </div>

              <h2 className="text-3xl font-bold mb-4 text-slate-900 dark:text-white leading-tight">
                {/* {selectedResult.title} */}
                {currentResult.title}
              </h2>

              {/* {selectedResult.image && ( */}
              {currentResult.image && (
                <img
                  // src={selectedResult.image || "/placeholder.svg"}
                  src={currentResult.image || "/placeholder.svg"}
                  alt="상세 이미지"
                  className="w-full h-64 object-cover rounded-xl mb-4"
                />
              )}

              {/* <p className="text-slate-600 dark:text-slate-300 mb-6 leading-relaxed text-lg">
                {selectedResult.fullDescription || selectedResult.description}
              </p> */}
              <p className="text-slate-600 dark:text-slate-300 mb-6 leading-relaxed text-lg">
                {/* {highlightKeywords(selectedResult.fullDescription || selectedResult.description)} */}
                {highlightKeywords(currentResult.fullDescription || currentResult.description)}
              </p>

              <div className="border-t border-slate-200 dark:border-slate-700 pt-4">
                <div className="flex items-center justify-between">
                  {/* <span className="text-sm text-slate-500 dark:text-slate-400">{selectedResult.url}</span> */}
                  <span className="text-sm text-slate-500 dark:text-slate-400">{currentResult.url}</span>
                  <Button
                    // onClick={() => window.open(selectedResult.url, "_blank")}
                    onClick={() => window.open(currentResult.url, "_blank")}
                    className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white"
                  >
                    사이트 방문하기
                    <ArrowRight className="h-4 w-4 ml-2" />
                  </Button>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </main>
  )
}
