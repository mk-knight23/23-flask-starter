import { motion } from 'framer-motion';
import { BookOpen, FileText, BarChart2, Search, Quote, Link2, Download, Users, Award, Globe, ArrowRight, ExternalLink, Database, Calculator, Scale, Calendar } from 'lucide-react';

const REFERENCES = [
    { id: 1, authors: "Smith, J., & Johnson, K.", title: "Scalable API Architecture Patterns", journal: "Journal of Systems Architecture", year: "2024", volume: "142", pages: "102889" },
    { id: 2, authors: "Chen, L., et al.", title: "Async Performance Benchmarks in Python", journal: "Proceedings of the 2024 Python Conference", year: "2024", pages: "234-251" },
    { id: 3, authors: "Williams, R., & Davis, M.", title: "Microservices Communication Patterns", journal: "IEEE Software", year: "2023", volume: "40", issue: "3", pages: "45-58" },
];

const KEY_FINDINGS = [
    { metric: "Response Latency", value: "42%", description: "Reduction in median response time compared to traditional WSGI implementations", source: "[2]" },
    { metric: "Throughput", value: "3.2x", description: "Higher request throughput under concurrent load conditions", source: "[2]" },
    { metric: "Memory Usage", value: "28%", description: "Lower memory footprint during sustained operation", source: "[1]" },
];

const AUTHORS = [
    { name: "Dr. Sarah Mitchell", affiliation: "Department of Computer Science, Stanford University" },
    { name: "Prof. James Chen", affiliation: "Software Systems Laboratory, MIT" },
    { name: "Dr. Emily Watson", affiliation: "Data Science Institute, Oxford University" },
];

export default function App() {
    return (
        <div className="min-h-screen bg-[#fdfbf7]">
            {/* Header */}
            <header className="bg-white border-b border-slate-200 sticky top-0 z-50">
                <div className="max-w-5xl mx-auto px-8 py-4 flex items-center justify-between">
                    <div className="flex items-center gap-4">
                        <div className="p-2 bg-slate-100 rounded">
                            <BookOpen className="w-5 h-5 text-slate-700" />
                        </div>
                        <span className="font-semibold text-slate-900">ScholarStack</span>
                    </div>
                    <div className="flex items-center gap-6 text-sm">
                        <a href="#" className="text-slate-600 hover:text-slate-900">Abstract</a>
                        <a href="#" className="text-slate-600 hover:text-slate-900">Introduction</a>
                        <a href="#" className="text-slate-600 hover:text-slate-900">Methods</a>
                        <a href="#" className="text-slate-600 hover:text-slate-900">Results</a>
                        <a href="#" className="text-slate-600 hover:text-slate-900">Discussion</a>
                        <button className="flex items-center gap-2 px-3 py-1.5 bg-slate-900 text-white rounded hover:bg-slate-800 transition-colors">
                            <Download className="w-4 h-4" /> PDF
                        </button>
                    </div>
                </div>
            </header>

            <main className="max-w-5xl mx-auto px-8 py-12">
                {/* Paper Header */}
                <motion.article
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6 }}
                >
                    <div className="text-center mb-12">
                        <span className="inline-block px-3 py-1 text-xs font-semibold text-blue-700 bg-blue-50 rounded-full mb-6">
                            Peer-Reviewed Research Article
                        </span>

                        <h1 className="text-3xl md:text-4xl font-bold text-slate-900 mb-6 leading-tight">
                            Optimizing Python Web APIs: A Comparative Analysis of Synchronous and Asynchronous Architectures
                        </h1>

                        <div className="author-block">
                            <p className="author-name">{AUTHORS.map(a => a.name).join(", ")}</p>
                            <p className="author-affiliation">
                                {AUTHORS.map(a => a.affiliation).join("; ")}
                            </p>
                        </div>

                        <div className="flex items-center justify-center gap-6 text-sm text-slate-500 mt-6">
                            <span className="flex items-center gap-1">
                                <Calendar className="w-4 h-4" /> Published: January 15, 2026
                            </span>
                            <span className="flex items-center gap-1">
                                <FileText className="w-4 h-4" /> DOI: 10.1234/ss.2026.001
                            </span>
                            <span className="flex items-center gap-1">
                                <Globe className="w-4 h-4" /> Views: 12,847
                            </span>
                        </div>
                    </div>

                    {/* Abstract */}
                    <section className="paper-card mb-8">
                        <h2 className="abstract-heading">Abstract</h2>
                        <p className="abstract-text">
                            This study presents a comprehensive evaluation of FlaskStack, a novel architectural pattern for building high-performance Python web APIs. We conduct empirical benchmarks comparing synchronous WSGI implementations against asynchronous ASGI-based solutions across multiple metrics including response latency, throughput scalability, and resource utilization. Our findings indicate that FlaskStack achieves a 42% reduction in median response latency and 3.2x higher throughput under concurrent load conditions<span className="citation">[1]</span>. These results have significant implications for organizations seeking to optimize their Python-based web infrastructure for high-concurrency scenarios.
                        </p>
                        <div className="footnote">
                            <strong>Keywords:</strong> Python, Web APIs, Asynchronous Programming, Performance Optimization, Flask, ASGI, Microservices
                        </div>
                    </section>

                    {/* Introduction */}
                    <section className="mb-12">
                        <h2 className="section-heading">1. Introduction</h2>
                        <p className="text-slate-700 leading-relaxed mb-6">
                            The demand for high-performance web APIs has grown substantially with the proliferation of distributed systems and microservices architectures<span className="citation">[3]</span>. Python, despite its widespread adoption for web development, has historically faced criticism for its synchronous execution model in traditional WSGI deployments.
                        </p>
                        <p className="text-slate-700 leading-relaxed mb-6">
                            FlaskStack addresses these limitations by introducing a hybrid architecture that leverages the strengths of both synchronous and asynchronous programming paradigms. This approach enables developers to maintain the simplicity and familiarity of Flask while achieving performance characteristics comparable to purpose-built async frameworks.
                        </p>
                        <div className="paper-card my-8 bg-slate-50">
                            <div className="flex items-start gap-3">
                                <Quote className="w-6 h-6 text-slate-400 flex-shrink-0 mt-1" />
                                <blockquote className="text-slate-700 italic">
                                    "The key innovation of FlaskStack lies in its ability to seamlessly transition between synchronous and asynchronous execution contexts based on workload characteristics, without requiring significant changes to application code."
                                </blockquote>
                            </div>
                        </div>
                    </section>

                    {/* Methods */}
                    <section className="mb-12">
                        <h2 className="section-heading">2. Methodology</h2>
                        <p className="text-slate-700 leading-relaxed mb-8">
                            Our experimental methodology employed a controlled benchmarking environment with standardized hardware and network conditions. We utilized wrk2 as our primary load generation tool, configured to produce consistent request rates across all test scenarios.
                        </p>

                        <div className="grid md:grid-cols-3 gap-6 mb-8">
                            <div className="methodology-step flex-col">
                                <div className="methodology-number mb-3">1</div>
                                <h4 className="font-semibold text-slate-900 mb-2">Environment Setup</h4>
                                <p className="text-sm text-slate-600">Python 3.12, 16GB RAM, 8-core CPU</p>
                            </div>
                            <div className="methodology-step flex-col">
                                <div className="methodology-number mb-3">2</div>
                                <h4 className="font-semibold text-slate-900 mb-2">Load Generation</h4>
                                <p className="text-sm text-slate-600">wrk2 with consistent request rates</p>
                            </div>
                            <div className="methodology-step flex-col">
                                <div className="methodology-number mb-3">3</div>
                                <h4 className="font-semibold text-slate-900 mb-2">Metrics Collection</h4>
                                <p className="text-sm text-slate-600">Latency, throughput, memory profiles</p>
                            </div>
                        </div>
                    </section>

                    {/* Results */}
                    <section className="mb-12">
                        <h2 className="section-heading">3. Results</h2>
                        <p className="text-slate-700 leading-relaxed mb-8">
                            The benchmarking results demonstrate significant performance improvements across all measured metrics. Below we present the key findings from our empirical evaluation.
                        </p>

                        <div className="grid md:grid-cols-3 gap-6 mb-8">
                            {KEY_FINDINGS.map((finding, idx) => (
                                <motion.div
                                    key={idx}
                                    initial={{ opacity: 0, y: 20 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    transition={{ delay: idx * 0.1 }}
                                    className="paper-card text-center"
                                >
                                    <div className="text-4xl font-bold text-slate-900 mb-2">{finding.value}</div>
                                    <div className="text-sm font-semibold text-slate-700 mb-3">{finding.metric}</div>
                                    <p className="text-xs text-slate-500 leading-relaxed">{finding.description}</p>
                                    <span className="citation mt-2 inline-block">{finding.source}</span>
                                </motion.div>
                            ))}
                        </div>

                        <div className="paper-card">
                            <h3 className="font-semibold text-slate-900 mb-4">Table 1: Performance Comparison Under Concurrent Load</h3>
                            <table className="data-table">
                                <thead>
                                    <tr>
                                        <th>Metric</th>
                                        <th>Traditional WSGI</th>
                                        <th>FlaskStack (Async)</th>
                                        <th>Improvement</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td>Median Latency (p50)</td>
                                        <td>45ms</td>
                                        <td>26ms</td>
                                        <td className="text-green-600 font-medium">42%</td>
                                    </tr>
                                    <tr>
                                        <td>99th Percentile (p99)</td>
                                        <td>128ms</td>
                                        <td>67ms</td>
                                        <td className="text-green-600 font-medium">48%</td>
                                    </tr>
                                    <tr>
                                        <td>Requests/Second</td>
                                        <td>2,450</td>
                                        <td>7,840</td>
                                        <td className="text-green-600 font-medium">3.2x</td>
                                    </tr>
                                    <tr>
                                        <td>Memory (steady state)</td>
                                        <td>256MB</td>
                                        <td>184MB</td>
                                        <td className="text-green-600 font-medium">28%</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </section>

                    {/* Discussion */}
                    <section className="mb-12">
                        <h2 className="section-heading">4. Discussion</h2>
                        <p className="text-slate-700 leading-relaxed mb-6">
                            The results presented in Section 3 have several important implications for practitioners and researchers in the field of web API development. First, the substantial latency improvements demonstrated by FlaskStack suggest that async architectures can be practically adopted without sacrificing the developer experience that Flask provides<span className="citation">[2]</span>.
                        </p>
                        <p className="text-slate-700 leading-relaxed mb-6">
                            Second, the memory efficiency gains observed under sustained load conditions indicate that FlaskStack is particularly well-suited for containerized deployments where resource constraints are a primary concern. This finding aligns with emerging industry trends toward lean, cloud-native application architectures.
                        </p>
                    </section>

                    {/* References */}
                    <section className="mb-12">
                        <h2 className="section-heading">References</h2>
                        <div className="paper-card">
                            {REFERENCES.map((ref) => (
                                <div key={ref.id} className="reference-item">
                                    <span className="citation-number mr-2">[{ref.id}]</span>
                                    <span className="text-slate-700">
                                        {ref.authors}. ({ref.year}). <em>{ref.title}</em>. {ref.journal}{ref.volume ? `, ${ref.volume}` : ''}{ref.issue ? `(${ref.issue})` : ''}{ref.pages ? `, ${ref.pages}` : ''}.
                                    </span>
                                </div>
                            ))}
                        </div>
                    </section>

                    {/* Footer */}
                    <footer className="text-center pt-8 border-t border-slate-200">
                        <div className="flex items-center justify-center gap-6 mb-4">
                            <span className="flex items-center gap-1 text-sm text-slate-500">
                                <Award className="w-4 h-4" /> This paper received the Best Paper Award at PyCon 2026
                            </span>
                            <span className="flex items-center gap-1 text-sm text-slate-500">
                                <Users className="w-4 h-4" /> 847 citations
                            </span>
                        </div>
                        <p className="text-xs text-slate-400">
                            © 2026 ScholarStack Research Foundation. All rights reserved.
                        </p>
                    </footer>
                </motion.article>
            </main>
        </div>
    );
}
