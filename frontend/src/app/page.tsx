"use client";
import { useState, useEffect } from "react";
import api from "@/lib/api";

// Eye Icon SVG Components
const EyeOpen = () => (
  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5">
    <path strokeLinecap="round" strokeLinejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z" />
    <path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
  </svg>
);
const EyeClosed = () => (
  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5">
    <path strokeLinecap="round" strokeLinejoin="round" d="M3.98 8.223A10.477 10.477 0 001.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.45 10.45 0 0112 4.5c4.756 0 8.773 3.162 10.065 7.498a10.523 10.523 0 01-4.293 5.774M6.228 6.228L3 3m3.228 3.228l3.65 3.65m7.894 7.894L21 21m-3.228-3.228l-3.65-3.65m0 0a3 3 0 10-4.243-4.243m4.242 4.242L9.88 9.88" />
  </svg>
);

export default function Dashboard() {
  const [token, setToken] = useState<string | null>(null);
  
  // Data States
  const [entries, setEntries] = useState<any[]>([]);
  const [commitments, setCommitments] = useState<any[]>([]);
  const [metrics, setMetrics] = useState<any[]>([]);
  
  // Auth States
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");

  // UI States
  const [isCheckInOpen, setIsCheckInOpen] = useState(false);
  const [isNewCommitmentOpen, setIsNewCommitmentOpen] = useState(false);
  
  const getLocalDateString = () => {
    const d = new Date();
    d.setMinutes(d.getMinutes() - d.getTimezoneOffset());
    return d.toISOString().split('T')[0];
  };

  // Reflection Form States
  const [formDate, setFormDate] = useState(getLocalDateString());
  const [sleep, setSleep] = useState<number | "">("");
  const [deepWork, setDeepWork] = useState<number | "">("");
  const [distraction, setDistraction] = useState<number | "">("");
  const [mood, setMood] = useState<number | "">("");
  const [energy, setEnergy] = useState<number | "">("");
  const [journal, setJournal] = useState("");
  const [whatAvoided, setWhatAvoided] = useState("");
  const [biggestWin, setBiggestWin] = useState("");
  const [biggestFailure, setBiggestFailure] = useState("");
  const [whatCanBeDifferent, setWhatCanBeDifferent] = useState("");
  const [quickMetricValues, setQuickMetricValues] = useState<Record<string, number>>({});

  // New Commitment Form States
  const [commTitle, setCommTitle] = useState("");
  const [commDescription, setCommDescription] = useState("");
  const [commDuration, setCommDuration] = useState<number | "">("");
  const [commStartDate, setCommStartDate] = useState(getLocalDateString());
  const [metricType, setMetricType] = useState("boolean");
  const [metricOperator, setMetricOperator] = useState(">=");
  const [metricTarget, setMetricTarget] = useState<number | "">("");

  useEffect(() => {
    const savedToken = localStorage.getItem("token");
    if (savedToken) {
      setToken(savedToken);
      fetchDashboardData();
    }
  }, []);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const formData = new URLSearchParams();
      formData.append("username", email);
      formData.append("password", password);

      const res = await api.post("/auth/login", formData, {
        headers: { "Content-Type": "application/x-www-form-urlencoded" }
      });
      
      const newToken = res.data.access_token;
      localStorage.setItem("token", newToken);
      setToken(newToken);
      setError("");
      fetchDashboardData();
    } catch (err) {
      setError("Invalid credentials.");
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    setToken(null);
    setEntries([]); setCommitments([]); setMetrics([]);
  };

  const fetchDashboardData = async () => {
    try {
      const entriesRes = await api.get("/daily-entries/");
      setEntries(entriesRes.data);

      const commsRes = await api.get("/commitments/");
      setCommitments(commsRes.data);

      const allMetrics = [];
      for (const comm of commsRes.data) {
        const metricsRes = await api.get(`/commitments/${comm.id}/metrics/`);
        allMetrics.push(...metricsRes.data);
      }
      setMetrics(allMetrics);
    } catch (err) {
      handleLogout();
    }
  };

  const autoSaveMetric = async (metricId: string, value: number) => {
    setQuickMetricValues(prev => ({ ...prev, [metricId]: value }));
    try {
      await api.post("/daily-entries/", {
        date: getLocalDateString(),
        custom_metrics: [{ metric_id: metricId, value: value }]
      });
      fetchDashboardData();
    } catch (err) {
      alert("Failed to auto-save metric.");
    }
  };

  const submitCheckIn = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.post("/daily-entries/", {
        date: formDate,
        sleep_hours: sleep === "" ? null : Number(sleep),
        deep_work_hours: deepWork === "" ? null : Number(deepWork),
        distraction_hours: distraction === "" ? null : Number(distraction),
        mood_score: mood === "" ? null : Number(mood),
        energy_score: energy === "" ? null : Number(energy),
        journal_entry: journal || null,
        what_avoided: whatAvoided || null,
        biggest_win: biggestWin || null,
        biggest_failure: biggestFailure || null,
        what_can_be_different: whatCanBeDifferent || null,
        custom_metrics: []
      });
      setIsCheckInOpen(false);
      setJournal(""); setWhatAvoided(""); setBiggestWin(""); setBiggestFailure(""); setWhatCanBeDifferent("");
      setSleep(""); setDeepWork(""); setDistraction(""); setMood(""); setEnergy("");
      fetchDashboardData();
    } catch (err) {
      alert("Failed to save entry.");
    }
  };

  const submitNewCommitment = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const commRes = await api.post("/commitments/", {
        title: commTitle,
        description: commDescription || null,
        duration_days: Number(commDuration),
        start_date: commStartDate
      });
      
      const newCommId = commRes.data.id;
      const isBoolean = metricType === "boolean";

      await api.post(`/commitments/${newCommId}/metrics/`, {
        name: commTitle, // Auto-assign metric name from commitment title
        metric_type: metricType,
        operator: isBoolean ? ">=" : metricOperator,
        target_value: isBoolean ? 1 : Number(metricTarget)
      });

      setIsNewCommitmentOpen(false);
      setCommTitle(""); setCommDescription(""); setCommDuration(""); 
      setMetricType("boolean"); setMetricOperator(">="); setMetricTarget("");
      fetchDashboardData();
    } catch (err) {
      alert("Failed to create commitment.");
      console.error(err);
    }
  };

  if (!token) {
    return (
      <div className="min-h-screen bg-black flex flex-col items-center justify-center text-neutral-100 selection:bg-blue-500/30">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-blue-900/20 via-black to-black"></div>
        <div className="relative z-10 mb-10 text-center">
          <h1 className="text-5xl font-black tracking-tighter text-transparent bg-clip-text bg-gradient-to-br from-white to-neutral-500 mb-3">Mentor</h1>
          <p className="text-neutral-400 font-medium tracking-wide">Behavioral Accountability Engine</p>
        </div>

        <form onSubmit={handleLogin} className="relative z-10 bg-neutral-900/40 p-8 rounded-3xl border border-neutral-800/60 w-[400px] flex flex-col gap-5 backdrop-blur-xl shadow-2xl">
          {error && <p className="text-red-400 text-sm font-medium bg-red-950/30 p-3 rounded-xl border border-red-900/50">{error}</p>}
          <div>
            <label className="text-xs font-bold text-neutral-500 uppercase tracking-wider mb-1.5 block">Email</label>
            <input type="email" className="w-full bg-black/50 p-4 rounded-xl border border-neutral-800/80 outline-none focus:border-blue-500/50 focus:ring-4 focus:ring-blue-500/10 transition-all text-white" value={email} onChange={e => setEmail(e.target.value)} />
          </div>
          <div>
            <label className="text-xs font-bold text-neutral-500 uppercase tracking-wider mb-1.5 block">Password</label>
            <div className="relative">
              <input type={showPassword ? "text" : "password"} className="w-full bg-black/50 p-4 pr-12 rounded-xl border border-neutral-800/80 outline-none focus:border-blue-500/50 focus:ring-4 focus:ring-blue-500/10 transition-all text-white" value={password} onChange={e => setPassword(e.target.value)} />
              <button type="button" onClick={() => setShowPassword(!showPassword)} className="absolute right-4 top-1/2 -translate-y-1/2 text-neutral-500 hover:text-white transition-colors">
                {showPassword ? <EyeClosed /> : <EyeOpen />}
              </button>
            </div>
          </div>
          <button type="submit" className="w-full bg-white text-black hover:bg-neutral-200 p-4 rounded-xl font-bold mt-2 transition-transform active:scale-[0.98]">Authenticate</button>
        </form>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-black text-neutral-100 font-sans selection:bg-blue-500/30 flex flex-col md:flex-row">
      
      {/* ---------------------------------------------------------
          LEFT PANEL: EXECUTION (25%)
      --------------------------------------------------------- */}
      <div className="w-full md:w-[320px] border-b md:border-b-0 md:border-r border-neutral-800/60 bg-neutral-950/50 p-6 flex flex-col h-auto md:h-screen sticky top-0 overflow-y-auto">
        <div className="flex justify-between items-center mb-8 shrink-0">
          <h2 className="text-xl font-black tracking-tight">Mentor</h2>
          <button onClick={handleLogout} className="text-xs font-bold text-neutral-500 hover:text-white transition-colors bg-neutral-900 px-3 py-1.5 rounded-md border border-neutral-800">Sign Out</button>
        </div>

        <div className="flex-1 pb-6">
          <h3 className="text-[10px] uppercase tracking-widest font-bold text-neutral-500 mb-6">Active Commitments</h3>
          {commitments.length === 0 ? (
            <p className="text-xs text-neutral-600 italic">No active commitments.</p>
          ) : (
            <div className="flex flex-col gap-8">
              {commitments.map(comm => {
                const commMetrics = metrics.filter(m => m.commitment_id === comm.id);
                const isFuture = comm.start_date > getLocalDateString();
                
                return (
                  <div key={comm.id} className={`relative ${isFuture ? 'opacity-50 grayscale' : ''}`}>
                    <div className="mb-3 flex justify-between items-start">
                      <div>
                        <h4 className="text-lg font-bold text-white tracking-tight">{comm.title}</h4>
                        {comm.description && <p className="text-xs text-neutral-500 mt-0.5">{comm.description}</p>}
                      </div>
                      {isFuture && (
                        <span className="text-[9px] font-black tracking-widest text-neutral-900 bg-yellow-500 px-2 py-1 rounded uppercase">Starts {new Date(comm.start_date).toLocaleDateString()}</span>
                      )}
                    </div>
                    <div className="flex flex-col gap-2">
                      {commMetrics.length === 0 ? (
                        <p className="text-[10px] text-neutral-600 italic px-2">No tracking metrics set.</p>
                      ) : (
                        commMetrics.map(metric => (
                          <div key={metric.id} className="bg-neutral-900/40 border border-neutral-800/50 p-3.5 rounded-xl flex justify-between items-center group hover:border-neutral-700 transition-colors">
                            <div>
                              <p className="font-semibold text-blue-400 text-sm">{metric.name}</p>
                              <p className="text-[10px] text-neutral-500 mt-0.5">Target: {metric.operator} {metric.target_value}</p>
                            </div>
                            {metric.metric_type === "boolean" ? (
                              <label className={`relative inline-flex items-center ${isFuture ? 'cursor-not-allowed' : 'cursor-pointer'}`}>
                                <input type="checkbox" disabled={isFuture} className="sr-only peer" checked={quickMetricValues[metric.id] >= 1} onChange={(e) => autoSaveMetric(metric.id, e.target.checked ? 1 : 0)} />
                                <div className="w-12 h-6 bg-neutral-800 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                              </label>
                            ) : (
                              <input type="number" disabled={isFuture} placeholder="0" className={`w-16 bg-black border border-neutral-800 p-2 rounded-lg text-white text-center text-sm outline-none focus:border-blue-500 transition-colors ${isFuture ? 'cursor-not-allowed opacity-50' : ''}`} value={quickMetricValues[metric.id] || ""} onBlur={(e) => { if (e.target.value !== "") autoSaveMetric(metric.id, Number(e.target.value)) }} onChange={(e) => setQuickMetricValues({...quickMetricValues, [metric.id]: Number(e.target.value)})} />
                            )}
                          </div>
                        ))
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>

        <div className="shrink-0 flex flex-col gap-3 mt-4 pt-4 border-t border-neutral-800/50">
          <button onClick={() => setIsNewCommitmentOpen(true)} className="w-full bg-neutral-900 hover:bg-neutral-800 border border-neutral-800 text-white font-bold py-3.5 rounded-xl transition-all active:scale-95 text-sm">
            + New Commitment
          </button>
          <button onClick={() => setIsCheckInOpen(true)} className="w-full bg-blue-600 hover:bg-blue-500 text-white font-bold py-3.5 rounded-xl transition-all shadow-[0_0_20px_rgba(37,99,235,0.2)] active:scale-95 text-sm">
            + Evening Reflection
          </button>
        </div>
      </div>

      {/* ---------------------------------------------------------
          RIGHT PANEL: HISTORY (75%)
      --------------------------------------------------------- */}
      <div className="flex-1 p-6 md:p-12 overflow-y-auto h-screen bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-neutral-900/20 via-black to-black">
        <div className="max-w-4xl mx-auto">
          <div className="mb-10">
            <h1 className="text-4xl font-black tracking-tighter text-white">Execution Log</h1>
            <p className="text-neutral-500 font-medium mt-1">Your historical behavioral data</p>
          </div>

          {entries.length === 0 ? (
            <div className="text-center py-24 border border-dashed border-neutral-800/80 rounded-3xl bg-neutral-900/10">
              <span className="text-3xl mb-4 block opacity-50">📝</span>
              <h3 className="text-lg font-bold text-white mb-1">No history found</h3>
              <p className="text-neutral-500 text-sm">Start executing your commitments today.</p>
            </div>
          ) : (
            <div className="grid gap-6">
              {entries.map((entry) => (
                <div key={entry.id} className="group bg-neutral-900/30 border border-neutral-800/50 p-6 sm:p-8 rounded-3xl flex flex-col gap-6 hover:border-neutral-700/80 transition-all">
                  <div className="flex justify-between items-center border-b border-neutral-800/50 pb-4">
                    <h2 className="text-2xl font-bold text-white tracking-tight">{new Date(entry.date).toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric' })}</h2>
                    {entry.energy_score !== null && (
                      <div className="bg-black border border-neutral-800 px-4 py-2 rounded-xl flex items-center gap-2">
                        <span className="text-[10px] text-neutral-500 font-bold uppercase tracking-widest">Energy</span>
                        <span className="text-lg font-black text-blue-400">{entry.energy_score}</span>
                      </div>
                    )}
                  </div>
                  
                  {(entry.journal_entry || entry.biggest_win || entry.biggest_failure || entry.what_avoided || entry.what_can_be_different) && (
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {entry.biggest_win && <div className="bg-black/30 p-4 rounded-2xl border border-green-900/20"><p className="text-[10px] font-bold text-green-500/70 uppercase tracking-widest mb-1">Biggest Win</p><p className="text-sm text-neutral-300">{entry.biggest_win}</p></div>}
                      {entry.biggest_failure && <div className="bg-black/30 p-4 rounded-2xl border border-red-900/20"><p className="text-[10px] font-bold text-red-500/70 uppercase tracking-widest mb-1">Failure / Friction</p><p className="text-sm text-neutral-300">{entry.biggest_failure}</p></div>}
                      {entry.what_avoided && <div className="bg-black/30 p-4 rounded-2xl border border-neutral-800/50"><p className="text-[10px] font-bold text-purple-500/70 uppercase tracking-widest mb-1">Avoided</p><p className="text-sm text-neutral-300">{entry.what_avoided}</p></div>}
                      {entry.what_can_be_different && <div className="bg-black/30 p-4 rounded-2xl border border-neutral-800/50 md:col-span-2"><p className="text-[10px] font-bold text-yellow-500/70 uppercase tracking-widest mb-1">Strategy for Tomorrow</p><p className="text-sm text-neutral-300">{entry.what_can_be_different}</p></div>}
                      {entry.journal_entry && <div className="bg-black/30 p-4 rounded-2xl border border-neutral-800/50 md:col-span-2"><p className="text-[10px] font-bold text-blue-500/70 uppercase tracking-widest mb-1">Journal</p><p className="text-sm text-neutral-300 font-serif italic">"{entry.journal_entry}"</p></div>}
                    </div>
                  )}

                  <div className="flex flex-wrap gap-4 mt-2">
                    <div className="flex items-center gap-2"><span className="text-[10px] font-bold text-neutral-600 uppercase">Sleep</span><span className="font-mono text-sm text-white bg-neutral-900 px-2 py-1 rounded">{entry.sleep_hours ?? '-'}h</span></div>
                    <div className="flex items-center gap-2"><span className="text-[10px] font-bold text-neutral-600 uppercase">Deep Work</span><span className="font-mono text-sm text-white bg-neutral-900 px-2 py-1 rounded">{entry.deep_work_hours ?? '-'}h</span></div>
                    <div className="flex items-center gap-2"><span className="text-[10px] font-bold text-neutral-600 uppercase">Mood</span><span className="font-mono text-sm text-white bg-neutral-900 px-2 py-1 rounded">{entry.mood_score ?? '-'}</span></div>
                    {entry.metric_logs && entry.metric_logs.length > 0 && (
                      <><div className="w-px h-6 bg-neutral-800 mx-2 hidden sm:block"></div>
                        {entry.metric_logs.map((log: any) => {
                          const mDef = metrics.find(m => m.id === log.metric_id);
                          return <div key={log.id} className="flex items-center gap-1.5 border border-blue-900/30 bg-blue-900/10 px-2.5 py-1 rounded-md"><span className="text-[10px] font-bold text-blue-400 uppercase">{mDef?.name || 'Metric'}</span><span className="font-mono text-xs text-blue-200">{log.value}</span></div>;
                        })}
                      </>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* ---------------------------------------------------------
          NEW COMMITMENT MODAL
      --------------------------------------------------------- */}
      {isNewCommitmentOpen && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-md z-50 flex items-center justify-center p-4 sm:p-6" onClick={(e) => { if (e.target === e.currentTarget) setIsNewCommitmentOpen(false); }}>
          <div className="bg-neutral-950 border border-neutral-800 w-full max-w-4xl max-h-[90vh] rounded-3xl shadow-2xl flex flex-col overflow-hidden">
            
            <div className="bg-neutral-900/50 p-5 sm:px-8 sm:py-6 border-b border-neutral-800 flex justify-between items-center shrink-0">
              <div>
                <h2 className="text-xl sm:text-2xl font-black text-white">Create Protocol</h2>
                <p className="text-neutral-500 text-xs sm:text-sm mt-0.5">Define your rules of engagement.</p>
              </div>
              <button type="button" onClick={() => setIsNewCommitmentOpen(false)} className="w-8 h-8 sm:w-10 sm:h-10 bg-neutral-800 hover:bg-neutral-700 rounded-full flex items-center justify-center text-neutral-400 hover:text-white transition-colors">✕</button>
            </div>

            <form onSubmit={submitNewCommitment} className="p-5 sm:p-8 flex flex-col gap-8 overflow-y-auto">
              
              <div>
                <h3 className="text-sm font-bold text-white mb-4 border-b border-neutral-800 pb-2">Core Commitment</h3>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label className="text-xs font-bold text-neutral-500 uppercase tracking-wider mb-1.5 block">Title</label>
                    <input type="text" required placeholder="e.g. 75 Hard" className="w-full bg-black border border-neutral-800 p-3 rounded-xl text-white outline-none focus:border-blue-500 text-sm" value={commTitle} onChange={e => setCommTitle(e.target.value)} />
                  </div>
                  <div>
                    <label className="text-xs font-bold text-neutral-500 uppercase tracking-wider mb-1.5 block">Description</label>
                    <input type="text" placeholder="Optional" className="w-full bg-black border border-neutral-800 p-3 rounded-xl text-white outline-none focus:border-blue-500 text-sm" value={commDescription} onChange={e => setCommDescription(e.target.value)} />
                  </div>
                  <div>
                    <label className="text-xs font-bold text-neutral-500 uppercase tracking-wider mb-1.5 block">Duration (Days)</label>
                    <input type="number" required min="1" placeholder="30" className="w-full bg-black border border-neutral-800 p-3 rounded-xl text-white outline-none focus:border-blue-500 text-sm" value={commDuration} onChange={e => setCommDuration(e.target.value ? Number(e.target.value) : "")} />
                  </div>
                  <div>
                    <label className="text-xs font-bold text-neutral-500 uppercase tracking-wider mb-1.5 block">Start Date</label>
                    <input type="date" required className="w-full bg-black border border-neutral-800 p-3 rounded-xl text-white outline-none focus:border-blue-500 text-sm" value={commStartDate} onChange={e => setCommStartDate(e.target.value)} />
                  </div>
                </div>
              </div>

              <div>
                <h3 className="text-sm font-bold text-white mb-4 border-b border-neutral-800 pb-2">Tracking Rule</h3>
                <div className="bg-neutral-900/40 p-5 rounded-xl border border-neutral-800/50 flex flex-wrap gap-4 items-end">
                  <div className="flex-1 min-w-[150px]">
                    <label className="text-[10px] text-neutral-500 uppercase font-bold mb-1.5 block">How will you track this?</label>
                    <select className="w-full bg-black border border-neutral-800 p-3 rounded-xl text-white text-sm outline-none focus:border-blue-500 transition-colors" value={metricType} onChange={e => setMetricType(e.target.value)}>
                      <option value="boolean">Yes/No (Check-off)</option>
                      <option value="hours">Hours</option>
                      <option value="count">Count (Numbers)</option>
                    </select>
                  </div>
                  
                  {metricType !== "boolean" && (
                    <>
                      <div className="w-24">
                        <label className="text-[10px] text-neutral-500 uppercase font-bold mb-1.5 block">Logic</label>
                        <select className="w-full bg-black border border-neutral-800 p-3 rounded-xl text-white text-sm outline-none focus:border-blue-500 transition-colors" value={metricOperator} onChange={e => setMetricOperator(e.target.value)}>
                          <option value=">=">{'>='}</option>
                          <option value="<=">{'<='}</option>
                          <option value="==">==</option>
                        </select>
                      </div>
                      <div className="w-32">
                        <label className="text-[10px] text-neutral-500 uppercase font-bold mb-1.5 block">Daily Target</label>
                        <input type="number" step="0.5" required className="w-full bg-black border border-neutral-800 p-3 rounded-xl text-white text-sm outline-none focus:border-blue-500 transition-colors" value={metricTarget} onChange={e => setMetricTarget(e.target.value ? Number(e.target.value) : "")} />
                      </div>
                    </>
                  )}
                </div>
              </div>

              <div className="flex gap-3 pt-4 mt-auto">
                <button type="button" onClick={() => setIsNewCommitmentOpen(false)} className="w-1/3 bg-neutral-900 hover:bg-neutral-800 text-neutral-300 font-bold text-base py-3.5 rounded-xl transition-all border border-neutral-800 active:scale-[0.98]">Cancel</button>
                <button type="submit" className="w-2/3 bg-blue-600 hover:bg-blue-500 text-white font-black text-base py-3.5 rounded-xl transition-all shadow-[0_0_20px_rgba(37,99,235,0.2)] active:scale-[0.98]">Launch Protocol</button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* ---------------------------------------------------------
          EVENING REFLECTION MODAL
      --------------------------------------------------------- */}
      {isCheckInOpen && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-md z-50 flex items-center justify-center p-4 sm:p-6" onClick={(e) => { if (e.target === e.currentTarget) setIsCheckInOpen(false); }}>
          <div className="bg-neutral-950 border border-neutral-800 w-full max-w-3xl max-h-[90vh] rounded-3xl shadow-2xl flex flex-col overflow-hidden">
            <div className="bg-neutral-900/50 p-5 sm:px-8 sm:py-6 border-b border-neutral-800 flex justify-between items-center shrink-0">
              <div>
                <h2 className="text-xl sm:text-2xl font-black text-white">Evening Reflection</h2>
                <p className="text-neutral-500 text-xs sm:text-sm mt-0.5">Review your day honestly.</p>
              </div>
              <button type="button" onClick={() => setIsCheckInOpen(false)} className="w-8 h-8 sm:w-10 sm:h-10 bg-neutral-800 hover:bg-neutral-700 rounded-full flex items-center justify-center text-neutral-400 hover:text-white transition-colors">✕</button>
            </div>
            <form onSubmit={submitCheckIn} className="p-5 sm:p-8 flex flex-col gap-6 overflow-y-auto">
              <div className="bg-neutral-900/30 p-4 rounded-2xl border border-neutral-800/50 flex items-center gap-4">
                <label className="text-xs font-bold text-neutral-500 uppercase tracking-wider shrink-0">Date Being Logged</label>
                <input type="date" required className="bg-black border border-neutral-800 p-2.5 rounded-lg text-white outline-none focus:border-blue-500 w-full max-w-[200px]" value={formDate} onChange={e => setFormDate(e.target.value)} />
              </div>
              <div className="grid grid-cols-2 sm:grid-cols-5 gap-3">
                <div className="sm:col-span-1"><label className="text-[10px] text-neutral-400 font-bold uppercase mb-1 block">Energy (1-10)</label><input type="number" min="1" max="10" className="w-full bg-black border border-neutral-800 p-2.5 rounded-lg text-white outline-none focus:border-blue-500 text-center font-mono text-sm" value={energy} onChange={e => setEnergy(e.target.value ? Number(e.target.value) : "")} /></div>
                <div className="sm:col-span-1"><label className="text-[10px] text-neutral-400 font-bold uppercase mb-1 block">Mood (1-10)</label><input type="number" min="1" max="10" className="w-full bg-black border border-neutral-800 p-2.5 rounded-lg text-white outline-none focus:border-blue-500 text-center font-mono text-sm" value={mood} onChange={e => setMood(e.target.value ? Number(e.target.value) : "")} /></div>
                <div className="sm:col-span-1"><label className="text-[10px] text-neutral-400 font-bold uppercase mb-1 block">Sleep (h)</label><input type="number" step="0.5" className="w-full bg-black border border-neutral-800 p-2.5 rounded-lg text-white outline-none focus:border-blue-500 text-center font-mono text-sm" value={sleep} onChange={e => setSleep(e.target.value ? Number(e.target.value) : "")} /></div>
                <div className="sm:col-span-1"><label className="text-[10px] text-neutral-400 font-bold uppercase mb-1 block">Deep Work</label><input type="number" step="0.5" className="w-full bg-black border border-neutral-800 p-2.5 rounded-lg text-white outline-none focus:border-blue-500 text-center font-mono text-sm" value={deepWork} onChange={e => setDeepWork(e.target.value ? Number(e.target.value) : "")} /></div>
                <div className="sm:col-span-1"><label className="text-[10px] text-neutral-400 font-bold uppercase mb-1 block">Distraction</label><input type="number" step="0.5" className="w-full bg-black border border-neutral-800 p-2.5 rounded-lg text-white outline-none focus:border-blue-500 text-center font-mono text-sm" value={distraction} onChange={e => setDistraction(e.target.value ? Number(e.target.value) : "")} /></div>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div><label className="text-xs font-bold text-green-500/80 uppercase tracking-wider mb-1.5 block">Biggest Win</label><textarea rows={2} className="w-full bg-black border border-neutral-800 p-3 rounded-xl text-white outline-none focus:border-green-500/50 resize-none text-sm leading-relaxed" value={biggestWin} onChange={e => setBiggestWin(e.target.value)} placeholder="What went perfectly?"></textarea></div>
                <div><label className="text-xs font-bold text-red-500/80 uppercase tracking-wider mb-1.5 block">Biggest Failure</label><textarea rows={2} className="w-full bg-black border border-neutral-800 p-3 rounded-xl text-white outline-none focus:border-red-500/50 resize-none text-sm leading-relaxed" value={biggestFailure} onChange={e => setBiggestFailure(e.target.value)} placeholder="Where did you slip up?"></textarea></div>
                <div><label className="text-xs font-bold text-purple-500/80 uppercase tracking-wider mb-1.5 block">What Avoided</label><textarea rows={2} className="w-full bg-black border border-neutral-800 p-3 rounded-xl text-white outline-none focus:border-purple-500/50 resize-none text-sm leading-relaxed" value={whatAvoided} onChange={e => setWhatAvoided(e.target.value)} placeholder="Did you dodge a bad habit?"></textarea></div>
                <div><label className="text-xs font-bold text-yellow-500/80 uppercase tracking-wider mb-1.5 block">Strategy for Tomorrow</label><textarea rows={2} className="w-full bg-black border border-neutral-800 p-3 rounded-xl text-white outline-none focus:border-yellow-500/50 resize-none text-sm leading-relaxed" value={whatCanBeDifferent} onChange={e => setWhatCanBeDifferent(e.target.value)} placeholder="How will you improve?"></textarea></div>
              </div>
              <div><label className="text-xs font-bold text-blue-500/80 uppercase tracking-wider mb-1.5 block">Open Journal</label><textarea rows={3} className="w-full bg-black border border-neutral-800 p-3 rounded-xl text-white outline-none focus:border-blue-500/50 resize-none font-serif text-sm leading-relaxed" value={journal} onChange={e => setJournal(e.target.value)} placeholder="Brain dump your thoughts..."></textarea></div>
              <div className="flex gap-3 pt-2 mt-auto">
                <button type="button" onClick={() => setIsCheckInOpen(false)} className="w-1/3 bg-neutral-900 hover:bg-neutral-800 text-neutral-300 font-bold text-base py-3.5 rounded-xl transition-all border border-neutral-800 active:scale-[0.98]">Cancel</button>
                <button type="submit" className="w-2/3 bg-blue-600 hover:bg-blue-500 text-white font-black text-base py-3.5 rounded-xl transition-all shadow-[0_0_20px_rgba(37,99,235,0.2)] active:scale-[0.98]">Commit Entry</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
