"use client";
import { useState, useEffect } from "react";
import api from "@/lib/api";

export default function Dashboard() {
  const [token, setToken] = useState<string | null>(null);
  const [entries, setEntries] = useState<any[]>([]);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  // 1. Check if user is already logged in on page load
  useEffect(() => {
    const savedToken = localStorage.getItem("token");
    if (savedToken) {
      setToken(savedToken);
      fetchEntries();
    }
  }, []);

  // 2. Handle Login Submission
  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      // FastAPI expects "Form Data" not JSON for the login route!
      const formData = new URLSearchParams();
      formData.append("username", email);
      formData.append("password", password);

      const res = await api.post("/auth/login", formData, {
        headers: { "Content-Type": "application/x-www-form-urlencoded" }
      });
      
      const newToken = res.data.access_token;
      localStorage.setItem("token", newToken); // Save token to browser
      setToken(newToken);
      setError("");
      fetchEntries(); // Fetch data immediately after login
    } catch (err) {
      setError("Invalid credentials. Did you use the right email/password?");
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    setToken(null);
    setEntries([]);
  };

  // 3. Fetch the Daily Entries from FastAPI
  const fetchEntries = async () => {
    try {
      const res = await api.get("/daily-entries/");
      setEntries(res.data);
    } catch (err) {
      console.error("Failed to fetch entries", err);
      handleLogout(); // If token is expired or invalid, log them out
    }
  };

  // ---------------------------------------------------------
  // UI: If not logged in, show the Login Screen
  // ---------------------------------------------------------
  if (!token) {
    return (
      <div className="min-h-screen bg-neutral-950 flex flex-col items-center justify-center text-neutral-100">
        <div className="mb-8 text-center">
          <h1 className="text-4xl font-black tracking-tight text-white mb-2">Mentor</h1>
          <p className="text-neutral-400">Behavioral Accountability System</p>
        </div>

        <form onSubmit={handleLogin} className="bg-neutral-900/50 p-8 rounded-2xl border border-neutral-800 w-96 flex flex-col gap-4 backdrop-blur-sm shadow-2xl">
          {error && <p className="text-red-400 text-sm font-medium bg-red-900/20 p-3 rounded-lg border border-red-900/50">{error}</p>}
          <input 
            type="email" 
            placeholder="Email Address" 
            className="bg-neutral-950 p-3.5 rounded-xl border border-neutral-800 outline-none focus:border-blue-500 transition-colors text-white placeholder:text-neutral-600"
            value={email} onChange={e => setEmail(e.target.value)}
          />
          <input 
            type="password" 
            placeholder="Password" 
            className="bg-neutral-950 p-3.5 rounded-xl border border-neutral-800 outline-none focus:border-blue-500 transition-colors text-white placeholder:text-neutral-600"
            value={password} onChange={e => setPassword(e.target.value)}
          />
          <button type="submit" className="bg-white text-black hover:bg-neutral-200 p-3.5 rounded-xl font-bold mt-4 transition-all active:scale-[0.98]">
            Enter Mentor
          </button>
        </form>
      </div>
    );
  }

  // ---------------------------------------------------------
  // UI: If logged in, show the Dashboard Screen
  // ---------------------------------------------------------
  return (
    <div className="min-h-screen bg-neutral-950 text-neutral-100 p-8 font-sans selection:bg-blue-500/30">
      <div className="max-w-4xl mx-auto">
        
        {/* Header */}
        <div className="flex justify-between items-center mb-12 border-b border-neutral-800/50 pb-6">
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-white">Execution Log</h1>
            <p className="text-neutral-500 text-sm mt-1">Your recent daily entries</p>
          </div>
          <button onClick={handleLogout} className="text-neutral-500 hover:text-white transition-colors text-sm font-medium bg-neutral-900 px-4 py-2 rounded-lg border border-neutral-800 hover:border-neutral-700">
            Sign Out
          </button>
        </div>

        {/* Content */}
        {entries.length === 0 ? (
          <div className="text-center py-20 border border-dashed border-neutral-800 rounded-2xl bg-neutral-900/20">
            <p className="text-neutral-500">No behavioral data found yet.</p>
          </div>
        ) : (
          <div className="grid gap-6">
            {entries.map((entry) => (
              <div key={entry.id} className="bg-neutral-900/40 border border-neutral-800/60 p-6 rounded-2xl flex flex-col gap-5 hover:border-neutral-700 transition-colors">
                
                {/* Card Header */}
                <div className="flex justify-between items-center">
                  <h2 className="text-xl font-semibold text-white tracking-tight">{entry.date}</h2>
                  {entry.energy_score && (
                    <span className="text-xs font-bold text-neutral-400 bg-neutral-950 px-3 py-1.5 rounded-full border border-neutral-800">
                      Energy: {entry.energy_score}/10
                    </span>
                  )}
                </div>
                
                {/* Metrics Grid */}
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                  <div className="bg-neutral-950 p-4 rounded-xl border border-neutral-800/50 flex flex-col justify-between">
                    <p className="text-neutral-500 text-[10px] uppercase tracking-widest font-bold mb-2">Sleep</p>
                    <p className="font-mono text-xl text-white">{entry.sleep_hours || 0}<span className="text-sm text-neutral-500 ml-1">hrs</span></p>
                  </div>
                  <div className="bg-neutral-950 p-4 rounded-xl border border-neutral-800/50 flex flex-col justify-between">
                    <p className="text-neutral-500 text-[10px] uppercase tracking-widest font-bold mb-2">Deep Work</p>
                    <p className="font-mono text-xl text-white">{entry.deep_work_hours || 0}<span className="text-sm text-neutral-500 ml-1">hrs</span></p>
                  </div>
                  <div className="bg-neutral-950 p-4 rounded-xl border border-neutral-800/50 flex flex-col justify-between">
                    <p className="text-neutral-500 text-[10px] uppercase tracking-widest font-bold mb-2">Distraction</p>
                    <p className="font-mono text-xl text-white">{entry.distraction_hours || 0}<span className="text-sm text-neutral-500 ml-1">hrs</span></p>
                  </div>
                  <div className="bg-neutral-950 p-4 rounded-xl border border-neutral-800/50 flex flex-col justify-between">
                    <p className="text-neutral-500 text-[10px] uppercase tracking-widest font-bold mb-2">Mood</p>
                    <p className="font-mono text-xl text-white">{entry.mood_score || '—'}<span className="text-sm text-neutral-500 ml-1">/10</span></p>
                  </div>
                </div>

                {/* Journal Entry */}
                {entry.journal_entry && (
                  <div className="mt-2 bg-neutral-950/50 p-4 rounded-xl border border-neutral-800/30">
                    <p className="text-neutral-400 text-sm leading-relaxed italic">
                      "{entry.journal_entry}"
                    </p>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
