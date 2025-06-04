"use client"

import type React from "react"
import { useState, useRef, useEffect } from "react"
import { Search, Loader2, ArrowRight, Clock, X } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { motion, AnimatePresence } from "framer-motion"
import axios from 'axios';
import { title } from "process"

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

  type Concept = {
    title: string;
    summary: string;
    keywords: string[];
  };

  const [conceptStack, setConceptStack] = useState<Concept[]>([]);
  const [allDifficultWords, setAllDifficultWords] = useState<string[][]>([]);

  // 클릭된 단어를 모달 스택에 추가, 키워드 추출과 단어 의미 요청
  const openConcept = async (word: string) => {
    try {
      const res = await axios.post("http://localhost:8000/keyword/explain", { word: word });

      const summary = res.data.summary;

      const keywordRes = await axios.post("http://localhost:8000/keyword", {
        text: summary,
      });

      let raw = keywordRes.data.received_text.trim();
      const match = raw.match(/```(?:json)?\s*([\s\S]*?)\s*```/i);
      if (match && match[1]) raw = match[1].trim();

      let keywords: string[] = [];
      try {
        keywords = JSON.parse(raw);
      } catch (err) {
        console.error("키워드 파싱 실패:", err);
      }

      setConceptStack(prev => [...prev, {
        title: word,
        summary,
        keywords
      }]);
    } catch (err) {
      console.error("openConcept 에러:", err);
    }
  };

  // 맨 위 모달 닫기
  const closeLastConcept = () => {
    setConceptStack(prev => prev.slice(0, -1));
  };

  // 주어진 텍스트에서 특정 키워드에 해당하는 단어를 찾아
  // 클릭 가능한 <span> 요소로 하이라이트
  function highlightConcepts(text: string, keywords: string[], onClick: (word: string) => void) {
    const regex = new RegExp(`(${keywords.join('|')})`, 'gi');
    const parts = text.split(regex);
    return parts.map((part, i) =>
      keywords.includes(part)
        ? <span key={i} className="text-purple-600 underline cursor-pointer" onClick={() => onClick(part)}>{part}</span>
        : part
    );
  }

  useEffect(() => {
    const storedSearches = localStorage.getItem(RECENT_SEARCHES_KEY)
    if (storedSearches) {
      setRecentSearches(JSON.parse(storedSearches))
    }
  }, [query])

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

  // URL 문자열을 파싱하는 함수
  function parseUrls(main: string, sub: string): string[] {
    const combinedText = `${main} | ${sub}`;
    const urlRegex = /https:\/\/[^\s|)\]]+/g;
    const urls = new Set<string>();

    let match;
    while ((match = urlRegex.exec(combinedText)) !== null) {
      let url = match[0];

      // 중복된 마크다운 링크 처리: https://...](https://...) 구조에서 앞부분만 남김
      const markdownDupMatch = url.match(/(https:\/\/[^\]]+)\]\(https:\/\/[^\)]+\)/);
      if (markdownDupMatch) {
        url = markdownDupMatch[1];
      }

      // 괄호, 대괄호, 따옴표, 마침표 제거
      url = url.replace(/[\])]+$/, '');
      urls.add(url);
    }

    return Array.from(urls);
  }

  // 날짜를 문자열로 반환하는 함수
  function formatDateString(dateStr?: string): string {
    if (!dateStr || dateStr.length !== 14) {
      return "날짜 정보 없음";
    }

    const year = dateStr.slice(0, 4);
    const month = dateStr.slice(4, 6);
    const day = dateStr.slice(6, 8);

    return `${year}년 ${parseInt(month)}월 ${parseInt(day)}일`;
  }

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!query.trim()) return
    setIsSearching(true)
    console.log(inputRef.current?.value)
    saveRecentSearch(query)

    const response = await axios.post("http://localhost:8000/text/core_word", { text: query });

    console.log(response.data);

    const parsed_urls = parseUrls(response.data.main, response.data.sub);
    console.log(parsed_urls);


    type CrawlData = {
      content: string;
      image_url: string;
      metadata: any; // 어떤 구조든 허용
    };

    const raw_crawl_datas: CrawlData[] = []; // 결과 저장용 배열

    for (const url of parsed_urls) {
      const res = await axios.post("http://localhost:8000/summary/crawl", { url });
      raw_crawl_datas.push(res.data);
    }

    console.log(raw_crawl_datas);

    // 크롤링 불가 페이지, metadata가 없는 페이지 제거한 배열
    const crawl_datas: CrawlData[] = raw_crawl_datas.filter(data => {
      const isValidMetadata =
        data.metadata &&
        typeof data.metadata === 'object' &&
        !Array.isArray(data.metadata) &&
        Object.keys(data.metadata).length > 0;

      return data.content !== "Cannot Crawling page" && isValidMetadata;
    });

    console.log(crawl_datas);

    // 요약 결과 저장용 배열
    const descriptions: string[] = [];
    const fullDescriptions: string[] = [];

    // 모든 crawl_datas에 대해 요약 요청
    for (const data of crawl_datas) {
      if (data.content === "No meaningful content found.") { // content가 없으면 빈 문자열 넣기
        descriptions.push("");
        fullDescriptions.push("");
        continue;
      }

      try {
        const [descRes, fullDescRes] = await Promise.all([
          axios.post("http://localhost:8000/summary/summarize", {
            text: data.content,
            detail: false
          }),
          axios.post("http://localhost:8000/summary/summarize", {
            text: data.content,
            detail: true
          })
        ]);

        descriptions.push(descRes.data.summary);
        fullDescriptions.push(fullDescRes.data.summary);
      } catch (error) {
        console.error("요약 실패:", error);
        descriptions.push("요약 실패");
        fullDescriptions.push("요약 실패");
      }
    }

    // 검색 효과를 위한 타임아웃
    setTimeout(() => {
      if (crawl_datas.length === 0) {
        console.warn("유효한 크롤링 결과가 없습니다.");
        setResults({ main: undefined, sub: [] });
        setHasSearched(true);
        setIsSearching(false);
        return;
      }

      const mainResult = {
        id: "main",
        title: crawl_datas[0].metadata.title,
        description: descriptions[0],
        fullDescription: fullDescriptions[0],
        url: crawl_datas[0].metadata.url,
        category: crawl_datas[0].metadata.type,
        image: crawl_datas[0].image_url,
        publishDate: formatDateString(crawl_datas[0].metadata.regDate),
        readTime: "5분 읽기"
      }

      const subResults = crawl_datas.slice(1).map((item, index) => ({
        id: index + 1,
        title: item.metadata.title,
        description: descriptions[index + 1],
        fullDescription: fullDescriptions[index + 1],
        url: item.metadata.url,
        category: item.metadata.type,
        image: item.image_url,
        publishDate: formatDateString(item.metadata.regDate),
        readTime: "5분 읽기"
      }));


      setResults({ main: mainResult, sub: subResults })
      setHasSearched(true)
      setIsSearching(false)
    }, 800) // 검색 효과를 위한 지연 시간

    const allDifficultWords: string[][] = [];

    for (const fullDesc of fullDescriptions) {
      try {
        const keywordRes = await axios.post("http://localhost:8000/keyword", {
          text: fullDesc,
        });

        let raw = keywordRes.data.received_text.trim();
        const match = raw.match(/```(?:json)?\s*([\s\S]*?)\s*```/i);
        if (match && match[1]) raw = match[1].trim();

        const keywords = JSON.parse(raw);
        allDifficultWords.push(keywords);
      } catch (e) {
        allDifficultWords.push([]);
      }
    }

    setAllDifficultWords(allDifficultWords)
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
                  onClick={() => setSelectedResult(results.main)}
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
                      onClick={() => setSelectedResult(result)}
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
      {selectedResult && (
        <div
          className="fixed inset-0 backdrop-blur-sm bg-white/5 bg-opacity-50 flex items-center justify-center p-4 z-50"
          onClick={() => setSelectedResult(null)}
        >
          <div
            className="bg-white dark:bg-slate-800 rounded-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="p-6">
              <div className="flex justify-between items-start mb-4">
                <div className="flex items-center gap-2">
                  <span className="text-xs px-3 py-1 bg-gradient-to-r from-purple-100 to-pink-100 dark:from-purple-900 dark:to-pink-900 text-purple-800 dark:text-purple-100 rounded-full font-medium">
                    {selectedResult.category}
                  </span>
                  <span className="text-xs text-slate-500 dark:text-slate-400">{selectedResult.publishDate}</span>
                  <span className="text-xs text-slate-500 dark:text-slate-400">•</span>
                  <span className="text-xs text-slate-500 dark:text-slate-400">{selectedResult.readTime}</span>
                </div>
                <button
                  onClick={() => setSelectedResult(null)}
                  className="text-slate-400 hover:text-slate-600 dark:hover:text-slate-300"
                >
                  <X className="h-6 w-6" />
                </button>
              </div>

              <h2 className="text-3xl font-bold mb-4 text-slate-900 dark:text-white leading-tight">
                {selectedResult.title}
              </h2>

              {selectedResult.image && (
                <img
                  src={selectedResult.image || "/placeholder.svg"}
                  alt="상세 이미지"
                  className="w-full h-64 object-cover rounded-xl mb-4"
                />
              )}

              <p className="text-slate-600 dark:text-slate-300 mb-6 leading-relaxed text-lg">
                {highlightConcepts(
                  selectedResult.fullDescription || selectedResult.description,
                  allDifficultWords[selectedResult.id === "main" ? 0 : selectedResult.id] || [],
                  openConcept
                )}
              </p>

              <div className="border-t border-slate-200 dark:border-slate-700 pt-4">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-slate-500 dark:text-slate-400">{selectedResult.url}</span>
                  <Button
                    onClick={() => window.open(selectedResult.url, "_blank")}
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

      {/* conceptStack 배열에 담긴 단어 요약들을 순서대로 렌더링 */}
      {conceptStack.map((concept, idx) => (
        <div key={idx} className="fixed inset-0 z-[1000] bg-black/30 flex items-center justify-center">
          <div className="bg-white dark:bg-slate-800 rounded-xl max-w-xl p-6 relative" onClick={(e) => e.stopPropagation()}>
            <h2 className="text-xl font-bold mb-4">{concept.title}</h2>
            <p className="text-slate-600 dark:text-slate-300">
              {highlightConcepts(concept.summary, concept.keywords || [], openConcept)}
            </p>
            <button onClick={closeLastConcept} className="absolute top-4 right-4 text-slate-400 hover:text-slate-600">
              <X className="h-5 w-5" />
            </button>
          </div>
        </div>
      ))}
    </main>
  )
}
