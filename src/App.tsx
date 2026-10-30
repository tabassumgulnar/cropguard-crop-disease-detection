import React, { useState } from 'react';
import advisoryData from '../advisory.json';
import { 
  ShieldAlert, 
  Sprout, 
  CloudSun, 
  Languages, 
  MapPin, 
  CheckCircle2, 
  AlertTriangle, 
  FileText, 
  Terminal,
  Activity,
  Layers,
  Search,
  ArrowRight,
  Upload,
  Camera,
  Check,
  X,
  ExternalLink,
  Info,
  Database,
  BarChart3,
  RefreshCw
} from 'lucide-react';

interface DemoReport {
  id: number;
  timestamp: string;
  crop: string;
  predicted_disease: string;
  confidence: number;
  location_name: string;
  weather_risk: string;
  is_uncertain: boolean;
  expert_status: 'Pending' | 'Confirmed' | 'Corrected';
  notes: string;
}

const INITIAL_DEMO_REPORTS: DemoReport[] = [
  { id: 1, timestamp: '2026-10-30 08:30', crop: 'tomato', predicted_disease: 'Tomato Early Blight (Alternaria solani)', confidence: 0.92, location_name: 'Pune Rural, MH', weather_risk: 'High (82% Humidity, 24°C)', is_uncertain: false, expert_status: 'Confirmed', notes: 'Verified concentric rings on lower leaves' },
  { id: 2, timestamp: '2026-10-30 07:15', crop: 'cotton', predicted_disease: 'Cotton Bacterial Blight / Angular Spot', confidence: 0.88, location_name: 'Jalgaon, MH', weather_risk: 'Medium (68% Humidity, 29°C)', is_uncertain: false, expert_status: 'Pending', notes: 'Water-soaked angular leaf lesions' },
  { id: 3, timestamp: '2026-10-29 18:45', crop: 'onion', predicted_disease: 'Onion Purple Blotch (Alternaria porri)', confidence: 0.94, location_name: 'Nashik, MH', weather_risk: 'High (85% Humidity, 22°C)', is_uncertain: false, expert_status: 'Confirmed', notes: 'Sunken violet-purple spots on foliage' },
  { id: 4, timestamp: '2026-10-29 15:20', crop: 'tomato', predicted_disease: 'Tomato Late Blight (Phytophthora infestans)', confidence: 0.48, location_name: 'Satara, MH', weather_risk: 'High (89% Humidity, 19°C)', is_uncertain: true, expert_status: 'Pending', notes: 'Borderline necrosis, needs field officer verification' },
  { id: 5, timestamp: '2026-10-29 11:10', crop: 'cotton', predicted_disease: 'Cotton Leaf Curl Disease (CLCuD)', confidence: 0.85, location_name: 'Nagpur, MH', weather_risk: 'Low (52% Humidity, 31°C)', is_uncertain: false, expert_status: 'Corrected', notes: 'Reclassified from nutrient deficiency to viral curl' },
  { id: 6, timestamp: '2026-10-28 14:00', crop: 'onion', predicted_disease: 'Onion Downy Mildew (Peronospora)', confidence: 0.91, location_name: 'Solapur, MH', weather_risk: 'Medium (72% Humidity, 26°C)', is_uncertain: false, expert_status: 'Confirmed', notes: 'Pale grayish-violet fuzzy growth on older leaves' },
];

export default function App() {
  const [selectedCrop, setSelectedCrop] = useState<'tomato' | 'cotton' | 'onion'>('tomato');
  const [selectedLang, setSelectedLang] = useState<'en' | 'hi' | 'mr'>('en');
  const [searchQuery, setSearchQuery] = useState('');
  const [activeTab, setActiveTab] = useState<'overview' | 'farmer' | 'officer' | 'advisory' | 'terminal'>('overview');

  // Interactive Farmer Diagnostic state
  const [selectedSample, setSelectedSample] = useState<'early_blight' | 'bacterial_blight' | 'purple_blotch' | 'uncertain'>('early_blight');
  const [diagnosticFeedback, setDiagnosticFeedback] = useState<string | null>(null);

  // Interactive Officer Dashboard state
  const [reports, setReports] = useState<DemoReport[]>(INITIAL_DEMO_REPORTS);
  const [officerNote, setOfficerNote] = useState('');
  const [selectedReportId, setSelectedReportId] = useState<number | null>(null);

  const diseases = Object.entries(advisoryData.diseases).filter(([_, info]) => {
    if (info.crop !== selectedCrop) return false;
    if (!searchQuery) return true;
    const langObj = info[selectedLang] || info.en;
    const term = searchQuery.toLowerCase();
    return (
      langObj.name.toLowerCase().includes(term) ||
      info.scientific_name.toLowerCase().includes(term) ||
      langObj.symptoms.toLowerCase().includes(term)
    );
  });

  const disclaimer = advisoryData.disclaimer[selectedLang] || advisoryData.disclaimer.en;

  // Diagnostic sample presets
  const sampleData = {
    early_blight: {
      crop: 'Tomato',
      disease: 'Tomato Early Blight (Alternaria solani)',
      confidence: 0.92,
      is_uncertain: false,
      probabilities: [
        { label: 'Early Blight (Alternaria solani)', pct: 92 },
        { label: 'Late Blight (Phytophthora infestans)', pct: 5 },
        { label: 'Leaf Mold (Passalora fulva)', pct: 3 },
      ],
      weather: { temp: '24°C', humidity: '82%', rain: '0.8 mm', risk: 'High Fungal Risk' },
      image: 'https://images.unsplash.com/photo-1592417817098-8f3d6910985c?w=600&auto=format&fit=crop&q=80',
      adviceKey: 'tomato_early_blight',
    },
    bacterial_blight: {
      crop: 'Cotton',
      disease: 'Cotton Bacterial Blight / Angular Leaf Spot',
      confidence: 0.89,
      is_uncertain: false,
      probabilities: [
        { label: 'Bacterial Blight (Xanthomonas)', pct: 89 },
        { label: 'Leaf Curl Disease (CLCuD)', pct: 7 },
        { label: 'Bollworm Damage', pct: 4 },
      ],
      weather: { temp: '29°C', humidity: '68%', rain: '0.0 mm', risk: 'Medium Risk' },
      image: 'https://images.unsplash.com/photo-1605000797499-95a51c5269ae?w=600&auto=format&fit=crop&q=80',
      adviceKey: 'cotton_bacterial_blight',
    },
    purple_blotch: {
      crop: 'Onion',
      disease: 'Onion Purple Blotch (Alternaria porri)',
      confidence: 0.94,
      is_uncertain: false,
      probabilities: [
        { label: 'Purple Blotch (Alternaria porri)', pct: 94 },
        { label: 'Stemphylium Leaf Blight', pct: 4 },
        { label: 'Downy Mildew', pct: 2 },
      ],
      weather: { temp: '22°C', humidity: '86%', rain: '2.4 mm', risk: 'High Spore Incubation' },
      image: 'https://images.unsplash.com/photo-1508747703725-719777637510?w=600&auto=format&fit=crop&q=80',
      adviceKey: 'onion_purple_blotch',
    },
    uncertain: {
      crop: 'Tomato',
      disease: 'Tomato Late Blight (Phytophthora infestans)',
      confidence: 0.44,
      is_uncertain: true,
      probabilities: [
        { label: 'Late Blight (Phytophthora)', pct: 44 },
        { label: 'Septoria Leaf Spot', pct: 32 },
        { label: 'Bacterial Speck', pct: 24 },
      ],
      weather: { temp: '20°C', humidity: '76%', rain: '0.0 mm', risk: 'Moderate Risk' },
      image: 'https://images.unsplash.com/photo-1592417817098-8f3d6910985c?w=600&auto=format&fit=crop&q=80',
      adviceKey: 'tomato_late_blight',
    },
  }[selectedSample];

  const handleUpdateStatus = (id: number, newStatus: 'Confirmed' | 'Corrected') => {
    setReports(prev => prev.map(r => r.id === id ? { ...r, expert_status: newStatus, notes: officerNote || r.notes } : r));
    setSelectedReportId(null);
    setOfficerNote('');
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-800 flex flex-col font-sans">
      {/* Top Header Banner */}
      <header className="bg-emerald-950 text-white shadow-lg border-b border-emerald-900">
        <div className="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8 flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div className="flex items-center space-x-3.5">
            <img 
              src="/logo.jpeg" 
              alt="CropGuard Logo" 
              className="w-13 h-13 rounded-full object-cover shadow-md border-2 border-emerald-400 bg-white shrink-0"
            />
            <div>
              <div className="flex items-center gap-2.5">
                <h1 className="text-2xl font-black tracking-tight text-white">CropGuard</h1>
                <span className="bg-emerald-500/20 text-emerald-300 text-xs font-semibold px-2.5 py-0.5 rounded-full border border-emerald-500/30">
                  Agro-Informatics Suite
                </span>
              </div>
              <p className="text-emerald-200/90 text-xs sm:text-sm font-medium">
                Early Foliar Disease & Pest Detection • Live Weather Epidemiology • Integrated Pest Management (IPM)
              </p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <div className="flex items-center bg-emerald-900/80 rounded-xl p-1 border border-emerald-800/80 shadow-inner">
              <Languages className="w-4 h-4 text-emerald-300 ml-2 mr-1" />
              <button 
                onClick={() => setSelectedLang('en')}
                className={`px-3 py-1 text-xs font-bold rounded-lg transition ${selectedLang === 'en' ? 'bg-emerald-600 text-white shadow-xs' : 'text-emerald-200 hover:text-white'}`}
              >
                English
              </button>
              <button 
                onClick={() => setSelectedLang('hi')}
                className={`px-3 py-1 text-xs font-bold rounded-lg transition ${selectedLang === 'hi' ? 'bg-emerald-600 text-white shadow-xs' : 'text-emerald-200 hover:text-white'}`}
              >
                हिन्दी
              </button>
              <button 
                onClick={() => setSelectedLang('mr')}
                className={`px-3 py-1 text-xs font-bold rounded-lg transition ${selectedLang === 'mr' ? 'bg-emerald-600 text-white shadow-xs' : 'text-emerald-200 hover:text-white'}`}
              >
                मराठी
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation Bar */}
      <nav className="bg-white border-b border-slate-200 shadow-xs sticky top-0 z-30">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex space-x-1 sm:space-x-4 overflow-x-auto">
          <button
            onClick={() => setActiveTab('overview')}
            className={`py-3.5 px-3 border-b-2 text-xs sm:text-sm font-bold flex items-center gap-2 whitespace-nowrap transition ${
              activeTab === 'overview'
                ? 'border-emerald-600 text-emerald-800 bg-emerald-50/50'
                : 'border-transparent text-slate-600 hover:text-slate-900 hover:border-slate-300'
            }`}
          >
            <Activity className="w-4 h-4 text-emerald-600" /> Home Dashboard
          </button>
          <button
            onClick={() => setActiveTab('farmer')}
            className={`py-3.5 px-3 border-b-2 text-xs sm:text-sm font-bold flex items-center gap-2 whitespace-nowrap transition ${
              activeTab === 'farmer'
                ? 'border-emerald-600 text-emerald-800 bg-emerald-50/50'
                : 'border-transparent text-slate-600 hover:text-slate-900 hover:border-slate-300'
            }`}
          >
            <Sprout className="w-4 h-4 text-emerald-600" /> Farmer Diagnostic Portal
          </button>
          <button
            onClick={() => setActiveTab('officer')}
            className={`py-3.5 px-3 border-b-2 text-xs sm:text-sm font-bold flex items-center gap-2 whitespace-nowrap transition ${
              activeTab === 'officer'
                ? 'border-emerald-600 text-emerald-800 bg-emerald-50/50'
                : 'border-transparent text-slate-600 hover:text-slate-900 hover:border-slate-300'
            }`}
          >
            <ShieldAlert className="w-4 h-4 text-blue-600" /> Officer Surveillance Hub
          </button>
          <button
            onClick={() => setActiveTab('advisory')}
            className={`py-3.5 px-3 border-b-2 text-xs sm:text-sm font-bold flex items-center gap-2 whitespace-nowrap transition ${
              activeTab === 'advisory'
                ? 'border-emerald-600 text-emerald-800 bg-emerald-50/50'
                : 'border-transparent text-slate-600 hover:text-slate-900 hover:border-slate-300'
            }`}
          >
            <FileText className="w-4 h-4 text-purple-600" /> IPM Advisory Catalog
          </button>
          <button
            onClick={() => setActiveTab('terminal')}
            className={`py-3.5 px-3 border-b-2 text-xs sm:text-sm font-bold flex items-center gap-2 whitespace-nowrap transition ${
              activeTab === 'terminal'
                ? 'border-emerald-600 text-emerald-800 bg-emerald-50/50'
                : 'border-transparent text-slate-600 hover:text-slate-900 hover:border-slate-300'
            }`}
          >
            <Terminal className="w-4 h-4 text-slate-700" /> Streamlit CLI Guide
          </button>
        </div>
      </nav>

      {/* Main Container */}
      <main className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8 flex-1 w-full space-y-8">
        
        {/* TAB 1: OVERVIEW & DASHBOARD */}
        {activeTab === 'overview' && (
          <div className="space-y-8">
            {/* Top Status Callout */}
            <div className="bg-gradient-to-r from-emerald-50 via-teal-50 to-emerald-50 border border-emerald-200 rounded-2xl p-5 shadow-xs flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
              <div className="flex items-center gap-4">
                <img 
                  src="/logo.jpeg" 
                  alt="CropGuard Emblem" 
                  className="w-12 h-12 rounded-full object-cover shadow-sm border border-emerald-400 bg-white shrink-0"
                />
                <div>
                  <h2 className="text-sm sm:text-base font-bold text-emerald-950">
                    Live Agro-Surveillance Database Active (cropguard.db)
                  </h2>
                  <p className="text-xs sm:text-sm text-emerald-800">
                    Pre-seeded with 32 Maharashtra district surveillance reports (Pune, Nashik, Jalgaon, Nagpur, Satara, Solapur).
                  </p>
                </div>
              </div>
              <div className="flex items-center gap-2 shrink-0">
                <button
                  onClick={() => setActiveTab('farmer')}
                  className="px-3.5 py-2 bg-emerald-700 text-white text-xs font-bold rounded-xl hover:bg-emerald-800 transition shadow-xs flex items-center gap-1.5"
                >
                  <Sprout className="w-3.5 h-3.5" /> Test Farmer Edge
                </button>
                <button
                  onClick={() => setActiveTab('officer')}
                  className="px-3.5 py-2 bg-white text-slate-700 border border-slate-300 text-xs font-bold rounded-xl hover:bg-slate-50 transition shadow-xs flex items-center gap-1.5"
                >
                  <ShieldAlert className="w-3.5 h-3.5 text-blue-600" /> Officer Records
                </button>
              </div>
            </div>

            {/* Verified Database Statistics */}
            <div>
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-3">
                <h3 className="text-lg font-bold text-slate-900 flex items-center gap-2">
                  <BarChart3 className="w-5 h-5 text-emerald-600" /> Surveillance Database Metrics
                </h3>
                <span className="text-xs font-medium text-slate-500 bg-white px-2.5 py-1 rounded-md border border-slate-200">
                  Source: SQLite <code>cropguard.db</code> (32 Demo Field Reports)
                </span>
              </div>

              <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3.5">
                <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-xs flex flex-col justify-between">
                  <div className="text-xs font-bold text-slate-500 uppercase tracking-wider">Total Reports</div>
                  <div className="mt-2 text-3xl font-extrabold text-emerald-900">32</div>
                  <div className="mt-1 text-xs text-slate-500">Stored in SQLite</div>
                </div>

                <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-xs flex flex-col justify-between">
                  <div className="text-xs font-bold text-red-700 uppercase tracking-wider">Pending Review</div>
                  <div className="mt-2 text-3xl font-extrabold text-red-600">10</div>
                  <div className="mt-1 text-xs text-slate-500">Awaiting Extension Officer</div>
                </div>

                <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-xs flex flex-col justify-between">
                  <div className="text-xs font-bold text-emerald-700 uppercase tracking-wider">Confirmed</div>
                  <div className="mt-2 text-3xl font-extrabold text-emerald-600">13</div>
                  <div className="mt-1 text-xs text-slate-500">Ground-Truth Validated</div>
                </div>

                <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-xs flex flex-col justify-between">
                  <div className="text-xs font-bold text-amber-700 uppercase tracking-wider">Corrected</div>
                  <div className="mt-2 text-3xl font-extrabold text-amber-600">9</div>
                  <div className="mt-1 text-xs text-slate-500">Active Learning Dataset</div>
                </div>

                <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-xs flex flex-col justify-between col-span-2 sm:col-span-1">
                  <div className="text-xs font-bold text-orange-700 uppercase tracking-wider">Uncertain (&lt;60%)</div>
                  <div className="mt-2 text-3xl font-extrabold text-orange-600">6</div>
                  <div className="mt-1 text-xs text-slate-500">Safeguard Gate Enforced</div>
                </div>
              </div>
            </div>

            {/* THREE CORE NAVIGATION CARDS: FIXED BLANK APPEARANCE, UNIFORM HEIGHT, HIGH CONTRAST */}
            <div>
              <div className="mb-4">
                <h3 className="text-xl font-bold text-slate-900">CropGuard Core Modules</h3>
                <p className="text-sm text-slate-600">Select any dedicated module below to launch the interactive workflow.</p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {/* CARD 1: FARMER PORTAL */}
                <div className="bg-white rounded-2xl border border-slate-200 border-t-4 border-t-emerald-600 p-6 shadow-sm flex flex-col justify-between min-h-[300px] hover:shadow-md transition">
                  <div>
                    <div className="flex items-center justify-between mb-4">
                      <div className="w-12 h-12 rounded-xl bg-emerald-100 text-emerald-800 flex items-center justify-center font-bold">
                        <Sprout className="w-6 h-6 text-emerald-700" />
                      </div>
                      <span className="text-xs font-bold uppercase tracking-wider text-emerald-700 bg-emerald-50 px-2.5 py-1 rounded-md border border-emerald-100">
                        Farmer Edge
                      </span>
                    </div>

                    <h4 className="text-lg font-bold text-slate-900 mb-2">
                      1. Farmer Diagnostic Portal
                    </h4>

                    <p className="text-sm text-slate-600 leading-relaxed mb-4">
                      Instant leaf photo disease classification for Tomato, Cotton, and Onion. Returns top-3 probability breakdown, live Open-Meteo weather risk scoring, and a strict &lt;60% safety threshold.
                    </p>
                  </div>

                  <div className="pt-4 border-t border-slate-100">
                    <button
                      onClick={() => setActiveTab('farmer')}
                      className="w-full py-2.5 px-4 bg-emerald-700 hover:bg-emerald-800 text-white text-xs font-bold rounded-xl transition flex items-center justify-center gap-2 shadow-xs"
                    >
                      Open Farmer Diagnostic Portal <ArrowRight className="w-4 h-4" />
                    </button>
                  </div>
                </div>

                {/* CARD 2: OFFICER DASHBOARD */}
                <div className="bg-white rounded-2xl border border-slate-200 border-t-4 border-t-blue-600 p-6 shadow-sm flex flex-col justify-between min-h-[300px] hover:shadow-md transition">
                  <div>
                    <div className="flex items-center justify-between mb-4">
                      <div className="w-12 h-12 rounded-xl bg-blue-100 text-blue-800 flex items-center justify-center font-bold">
                        <ShieldAlert className="w-6 h-6 text-blue-700" />
                      </div>
                      <span className="text-xs font-bold uppercase tracking-wider text-blue-700 bg-blue-50 px-2.5 py-1 rounded-md border border-blue-100">
                        GIS Surveillance
                      </span>
                    </div>

                    <h4 className="text-lg font-bold text-slate-900 mb-2">
                      2. Officer Surveillance Hub
                    </h4>

                    <p className="text-sm text-slate-600 leading-relaxed mb-4">
                      Spatial disease distribution maps, regional epidemic cluster heatmaps across Maharashtra districts, surveillance audit logs, and a human-in-the-loop "Confirm / Correct Label" tool for expert active learning.
                    </p>
                  </div>

                  <div className="pt-4 border-t border-slate-100">
                    <button
                      onClick={() => setActiveTab('officer')}
                      className="w-full py-2.5 px-4 bg-blue-700 hover:bg-blue-800 text-white text-xs font-bold rounded-xl transition flex items-center justify-center gap-2 shadow-xs"
                    >
                      Open Officer Surveillance Hub <ArrowRight className="w-4 h-4" />
                    </button>
                  </div>
                </div>

                {/* CARD 3: ADVISORY CATALOG */}
                <div className="bg-white rounded-2xl border border-slate-200 border-t-4 border-t-purple-600 p-6 shadow-sm flex flex-col justify-between min-h-[300px] hover:shadow-md transition">
                  <div>
                    <div className="flex items-center justify-between mb-4">
                      <div className="w-12 h-12 rounded-xl bg-purple-100 text-purple-800 flex items-center justify-center font-bold">
                        <FileText className="w-6 h-6 text-purple-700" />
                      </div>
                      <span className="text-xs font-bold uppercase tracking-wider text-purple-700 bg-purple-50 px-2.5 py-1 rounded-md border border-purple-100">
                        Trilingual IPM
                      </span>
                    </div>

                    <h4 className="text-lg font-bold text-slate-900 mb-2">
                      3. Trilingual IPM Advisory Catalog
                    </h4>

                    <p className="text-sm text-slate-600 leading-relaxed mb-4">
                      Comprehensive plant pathology advisory covering 11 pathogens in English, हिन्दी (Hindi), and मराठी (Marathi). Follows ICAR & KVK guidelines prioritizing Cultural and Biological controls over chemical sprays.
                    </p>
                  </div>

                  <div className="pt-4 border-t border-slate-100">
                    <button
                      onClick={() => setActiveTab('advisory')}
                      className="w-full py-2.5 px-4 bg-purple-700 hover:bg-purple-800 text-white text-xs font-bold rounded-xl transition flex items-center justify-center gap-2 shadow-xs"
                    >
                      Browse Trilingual IPM Catalog <ArrowRight className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </div>
            </div>

            {/* Architecture Workflow Box */}
            <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs">
              <h3 className="text-lg font-bold text-slate-900 mb-4 flex items-center gap-2">
                <Layers className="w-5 h-5 text-emerald-600" /> System Flow & Edge Safekeeping
              </h3>
              <div className="p-4 bg-slate-950 text-emerald-400 rounded-xl font-mono text-xs sm:text-sm overflow-x-auto">
                <pre>{`[ Farmer Leaf Photo ]  ──▶ [ Public ViT / MobileNet Vision Engine ]
                                  │
                                  ▼ Top-3 Predictions with Confidence Scores
[ Field GPS Lat/Lon ]  ──▶ [ Open-Meteo Weather API ] ──▶ [ Rule-based Fungal/Pest Risk ]
                                  │
                                  ▼
           ┌────────────────────────────────────────────────────────┐
           │ Confidence Safety Check:                               │
           │  - Top Conf < 60% ──▶ "Uncertain – Consult AO"         │
           │  - Top Conf ≥ 60% ──▶ Trilingual IPM Advisory          │
           └────────────────────────────────────────────────────────┘
                                  │
                                  ▼
                     [ SQLite: cropguard.db ]
                                  │
                                  ▼
           ┌────────────────────────────────────────────────────────┐
           │ Agriculture Officer Surveillance & Active Learning:    │
           │  - Folium Markers & Epidemic Heatmaps                  │
           │  - Incident Audit Table & CSV Export                   │
           │  - "Confirm / Correct Label" Ground-Truth Verification │
           └────────────────────────────────────────────────────────┘`}</pre>
              </div>
            </div>
          </div>
        )}

        {/* TAB 2: INTERACTIVE FARMER DIAGNOSTIC PORTAL */}
        {activeTab === 'farmer' && (
          <div className="space-y-6">
            <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-100 pb-4 mb-6">
                <div>
                  <h3 className="text-xl font-bold text-slate-900 flex items-center gap-2">
                    <Sprout className="w-6 h-6 text-emerald-600" /> Interactive Farmer Diagnostic Edge
                  </h3>
                  <p className="text-xs sm:text-sm text-slate-600">
                    Test leaf classification against live weather conditions and inspect the &lt;60% safety threshold.
                  </p>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-xs font-bold text-slate-500 uppercase">Test Leaf Sample:</span>
                  <select 
                    value={selectedSample}
                    onChange={(e: any) => setSelectedSample(e.target.value)}
                    className="text-xs font-semibold px-3 py-1.5 bg-slate-50 border border-slate-300 rounded-lg focus:outline-emerald-600"
                  >
                    <option value="early_blight">🍅 Tomato Early Blight (High Conf)</option>
                    <option value="bacterial_blight">🌿 Cotton Bacterial Blight (High Conf)</option>
                    <option value="purple_blotch">🧅 Onion Purple Blotch (High Conf)</option>
                    <option value="uncertain">⚠️ Uncertain Sample (&lt;60% Safeguard)</option>
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
                {/* Left: Leaf Preview & Weather */}
                <div className="lg:col-span-5 space-y-4">
                  <div className="relative rounded-xl overflow-hidden border border-slate-200 bg-slate-100 aspect-video flex items-center justify-center">
                    <img 
                      src={sampleData.image} 
                      alt="Sample leaf" 
                      className="w-full h-full object-cover"
                    />
                    <div className="absolute bottom-3 left-3 bg-slate-900/80 text-white text-xs px-2.5 py-1 rounded-md backdrop-blur-xs">
                      {sampleData.crop} Sample Leaf
                    </div>
                  </div>

                  {/* Weather Risk Card */}
                  <div className="bg-blue-50/70 border border-blue-200 rounded-xl p-4">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-xs font-bold text-blue-900 flex items-center gap-1.5">
                        <CloudSun className="w-4 h-4 text-blue-600" /> Live Agro-Weather (Open-Meteo)
                      </span>
                      <span className="text-xs font-extrabold text-blue-700 bg-blue-100 px-2 py-0.5 rounded">
                        {sampleData.weather.risk}
                      </span>
                    </div>
                    <div className="grid grid-cols-3 gap-2 text-center text-xs">
                      <div className="bg-white p-2 rounded-lg border border-blue-100">
                        <div className="text-slate-500">Temp</div>
                        <div className="font-bold text-slate-800">{sampleData.weather.temp}</div>
                      </div>
                      <div className="bg-white p-2 rounded-lg border border-blue-100">
                        <div className="text-slate-500">Humidity</div>
                        <div className="font-bold text-slate-800">{sampleData.weather.humidity}</div>
                      </div>
                      <div className="bg-white p-2 rounded-lg border border-blue-100">
                        <div className="text-slate-500">Rain</div>
                        <div className="font-bold text-slate-800">{sampleData.weather.rain}</div>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Right: Diagnosis & Safeguard */}
                <div className="lg:col-span-7 space-y-4">
                  <div className="bg-slate-100/80 border border-slate-200 rounded-xl p-3 text-xs text-slate-700">
                    ℹ️ <strong>Preliminary Screening Notice:</strong> Predictions are automated screening estimates to assist field scouting, not certified laboratory or molecular tests.
                  </div>

                  {sampleData.is_uncertain ? (
                    <div className="bg-amber-50 border-2 border-amber-300 rounded-xl p-5 text-amber-950">
                      <div className="flex items-center gap-2 mb-2 font-bold text-base text-amber-900">
                        <AlertTriangle className="w-5 h-5 text-amber-600" />
                        Low-Confidence Visual Match ({Math.round(sampleData.confidence * 100)}%) — Additional Observations Recommended
                      </div>
                      <p className="text-xs sm:text-sm text-amber-800 leading-relaxed mb-3">
                        Confidence is below the strict 60% reliability gate. Symptoms may overlap with nutrient deficiency or secondary molds.
                      </p>
                      <div className="bg-white p-3 rounded-lg border border-amber-200 text-xs space-y-1.5 text-amber-900">
                        <strong>📸 Photo improvement tips:</strong>
                        <ul className="list-disc pl-4 space-y-0.5 text-slate-700">
                          <li>Focus sharply on active lesion margins where green meets brown.</li>
                          <li>Flip the leaf to check the underside for fungal sporulation or insect pests.</li>
                          <li>Shoot in diffused daytime light without flash glare or deep shadows.</li>
                        </ul>
                      </div>
                    </div>
                  ) : (
                    <div className="bg-emerald-50 border border-emerald-200 rounded-xl p-5">
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-xs font-bold text-emerald-800 uppercase tracking-wider">Candidate Match</span>
                        <span className="text-xs font-black text-emerald-900 bg-emerald-200/60 px-2.5 py-0.5 rounded-full">
                          {Math.round(sampleData.confidence * 100)}% Match Confidence
                        </span>
                      </div>
                      <h4 className="text-lg font-black text-emerald-950">{sampleData.disease}</h4>
                      <p className="text-xs text-emerald-700 mt-1">
                        High-confidence screening match. Structured 5-step management protocol available below.
                      </p>
                    </div>
                  )}

                  {/* Top-3 Probability Distribution */}
                  <div className="bg-white border border-slate-200 rounded-xl p-4 space-y-3">
                    <h5 className="text-xs font-bold text-slate-600 uppercase tracking-wider">
                      Predicted Probability Distribution (Top-3)
                    </h5>
                    {sampleData.probabilities.map((item, idx) => (
                      <div key={idx} className="space-y-1">
                        <div className="flex justify-between text-xs font-semibold">
                          <span className="text-slate-700">{item.label}</span>
                          <span className="text-slate-900">{item.pct}%</span>
                        </div>
                        <div className="w-full bg-slate-100 rounded-full h-2 overflow-hidden">
                          <div 
                            className={`h-full rounded-full transition-all ${
                              idx === 0 ? (sampleData.is_uncertain ? 'bg-amber-500' : 'bg-emerald-600') : 'bg-slate-300'
                            }`}
                            style={{ width: `${item.pct}%` }}
                          />
                        </div>
                      </div>
                    ))}
                  </div>

                  {/* 5 Structured Protocol Accordion */}
                  <div className="space-y-2 text-xs">
                    <details className="bg-slate-50 border border-slate-200 rounded-xl p-3" open>
                      <summary className="font-bold text-slate-800 cursor-pointer">
                        🔍 A. Possible Disease & Observed Symptoms
                      </summary>
                      <p className="mt-2 text-slate-600">
                        {sampleData.disease} on {sampleData.crop}. Concentric rings, water-soaked margins, or viral curling depending on pathogen. Weather risk currently at {sampleData.weather.risk}.
                      </p>
                    </details>

                    <details className="bg-slate-50 border border-slate-200 rounded-xl p-3" open>
                      <summary className="font-bold text-slate-800 cursor-pointer">
                        ⚡ B. Immediate Steps (First 24–48 Hours)
                      </summary>
                      <p className="mt-2 text-slate-600">
                        Prune and destroy infected lower leaves (never compost). Sterilize pruning shears with 70% alcohol. Halt overhead sprinkler irrigation immediately.
                      </p>
                    </details>

                    <details className="bg-slate-50 border border-slate-200 rounded-xl p-3">
                      <summary className="font-bold text-slate-800 cursor-pointer">
                        🛡️ C. Disease Prevention Methods
                      </summary>
                      <p className="mt-2 text-slate-600">
                        Practice 2-year crop rotation with non-hosts (cereals/pulses). Plant certified disease-free seeds. Maintain recommended spacing for canopy aeration.
                      </p>
                    </details>

                    <details className="bg-slate-50 border border-slate-200 rounded-xl p-3">
                      <summary className="font-bold text-slate-800 cursor-pointer">
                        💧 D. Crop Hygiene, Watering & Drainage
                      </summary>
                      <p className="mt-2 text-slate-600">
                        Drip irrigate at root level early in the morning. Build raised beds (15–20 cm) and clear field drainage furrows to prevent waterlogged crowns.
                      </p>
                    </details>

                    <details className="bg-slate-50 border border-slate-200 rounded-xl p-3">
                      <summary className="font-bold text-slate-800 cursor-pointer">
                        🏛️ E. When to Seek Agricultural Expert Confirmation
                      </summary>
                      <p className="mt-2 text-slate-600">
                        Contact local KVK or Agriculture Officer if symptoms spread to &gt;15–20% of the plot within 72 hours, stem cankers form, or plants wilt despite moist soil.
                      </p>
                    </details>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* TAB 3: OFFICER SURVEILLANCE HUB */}
        {activeTab === 'officer' && (
          <div className="space-y-6">
            <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-100 pb-4 mb-6">
                <div>
                  <h3 className="text-xl font-bold text-slate-900 flex items-center gap-2">
                    <ShieldAlert className="w-6 h-6 text-blue-600" /> Officer Spatial GIS & Human-in-the-Loop Review
                  </h3>
                  <p className="text-xs sm:text-sm text-slate-600">
                    Audit farm incident reports, inspect weather risks, and confirm or correct ground-truth labels.
                  </p>
                </div>
                <div className="text-xs font-bold text-blue-800 bg-blue-50 px-3 py-1.5 rounded-lg border border-blue-100">
                  {reports.length} Reports Loaded (Maharashtra Districts)
                </div>
              </div>

              {/* Reports Table */}
              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs text-slate-700 border-collapse">
                  <thead>
                    <tr className="bg-slate-100 text-slate-600 font-bold uppercase tracking-wider border-b border-slate-200">
                      <th className="py-3 px-3">ID</th>
                      <th className="py-3 px-3">Date</th>
                      <th className="py-3 px-3">Crop</th>
                      <th className="py-3 px-3">Diagnosis</th>
                      <th className="py-3 px-3">Conf</th>
                      <th className="py-3 px-3">District</th>
                      <th className="py-3 px-3">Weather Risk</th>
                      <th className="py-3 px-3">Status</th>
                      <th className="py-3 px-3 text-right">Action</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {reports.map((r) => (
                      <tr key={r.id} className="hover:bg-slate-50 transition">
                        <td className="py-3 px-3 font-mono font-bold text-slate-800">#{r.id}</td>
                        <td className="py-3 px-3 text-slate-500 whitespace-nowrap">{r.timestamp}</td>
                        <td className="py-3 px-3 font-semibold capitalize">{r.crop}</td>
                        <td className="py-3 px-3 font-medium text-slate-900 max-w-xs truncate">{r.predicted_disease}</td>
                        <td className="py-3 px-3 font-bold">
                          <span className={r.is_uncertain ? 'text-red-600' : 'text-emerald-700'}>
                            {Math.round(r.confidence * 100)}%
                          </span>
                        </td>
                        <td className="py-3 px-3 whitespace-nowrap">{r.location_name}</td>
                        <td className="py-3 px-3 text-xs text-slate-600 whitespace-nowrap">{r.weather_risk}</td>
                        <td className="py-3 px-3">
                          <span className={`px-2 py-0.5 rounded-full text-xs font-bold ${
                            r.expert_status === 'Confirmed' 
                              ? 'bg-emerald-100 text-emerald-800' 
                              : r.expert_status === 'Corrected'
                              ? 'bg-amber-100 text-amber-800'
                              : 'bg-red-100 text-red-800'
                          }`}>
                            {r.expert_status}
                          </span>
                        </td>
                        <td className="py-3 px-3 text-right">
                          <button
                            onClick={() => setSelectedReportId(r.id)}
                            className="px-2.5 py-1 bg-blue-600 hover:bg-blue-700 text-white rounded font-bold text-xs transition"
                          >
                            Review
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              {/* Expert Review Modal / Box */}
              {selectedReportId !== null && (
                <div className="mt-6 p-5 bg-blue-50/80 border border-blue-200 rounded-xl space-y-3">
                  <div className="flex items-center justify-between">
                    <h4 className="text-sm font-bold text-blue-950 flex items-center gap-1.5">
                      <CheckCircle2 className="w-4 h-4 text-blue-700" /> Active Learning Verification: Report #{selectedReportId}
                    </h4>
                    <button 
                      onClick={() => setSelectedReportId(null)}
                      className="text-slate-400 hover:text-slate-600 text-xs font-bold"
                    >
                      Cancel
                    </button>
                  </div>
                  <input
                    type="text"
                    placeholder="Enter officer notes or field verification observation..."
                    value={officerNote}
                    onChange={(e) => setOfficerNote(e.target.value)}
                    className="w-full p-2.5 text-xs bg-white border border-blue-200 rounded-lg focus:outline-blue-600"
                  />
                  <div className="flex gap-2">
                    <button
                      onClick={() => handleUpdateStatus(selectedReportId, 'Confirmed')}
                      className="px-3 py-1.5 bg-emerald-700 text-white font-bold text-xs rounded-lg hover:bg-emerald-800 transition"
                    >
                      ✓ Confirm Diagnosis
                    </button>
                    <button
                      onClick={() => handleUpdateStatus(selectedReportId, 'Corrected')}
                      className="px-3 py-1.5 bg-amber-600 text-white font-bold text-xs rounded-lg hover:bg-amber-700 transition"
                    >
                      ✎ Correct Label (Active Learning)
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {/* TAB 4: TRILINGUAL IPM ADVISORY CATALOG */}
        {activeTab === 'advisory' && (
          <div className="space-y-6">
            <div className="bg-white p-4 rounded-2xl border border-slate-200 shadow-xs flex flex-col sm:flex-row gap-4 items-center justify-between">
              <div className="flex items-center gap-2 w-full sm:w-auto">
                <span className="text-xs font-bold text-slate-500 uppercase">Crop:</span>
                {(['tomato', 'cotton', 'onion'] as const).map((crop) => (
                  <button
                    key={crop}
                    onClick={() => setSelectedCrop(crop)}
                    className={`px-3.5 py-1.5 text-xs font-bold uppercase rounded-xl border transition ${
                      selectedCrop === crop
                        ? 'bg-emerald-700 text-white border-emerald-700 shadow-xs'
                        : 'bg-white text-slate-700 border-slate-200 hover:bg-slate-50'
                    }`}
                  >
                    {crop === 'tomato' ? '🍅 Tomato' : crop === 'cotton' ? '🌿 Cotton' : '🧅 Onion'}
                  </button>
                ))}
              </div>

              <div className="relative w-full sm:w-72">
                <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
                <input
                  type="text"
                  placeholder="Search symptoms or pathogens..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-9 pr-3 py-1.5 text-sm border border-slate-300 rounded-xl focus:outline-emerald-600"
                />
              </div>
            </div>

            {/* Disease Cards */}
            <div className="space-y-4">
              {diseases.map(([key, info]) => {
                const langData = info[selectedLang] || info.en;
                return (
                  <div key={key} className="bg-white border border-slate-200 rounded-2xl p-6 shadow-xs">
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-100 pb-3 mb-4">
                      <div>
                        <h4 className="text-lg font-bold text-slate-900">{langData.name}</h4>
                        <p className="text-xs text-slate-500">
                          <strong>Scientific Name:</strong> <em>{info.scientific_name}</em> | {langData.pathogen}
                        </p>
                      </div>
                      <span className="px-2.5 py-1 text-xs font-bold bg-slate-100 text-slate-700 rounded-md uppercase self-start">
                        {info.crop}
                      </span>
                    </div>

                    <p className="text-sm text-slate-700 mb-4 bg-slate-50 p-3 rounded-xl border border-slate-100">
                      <strong>Symptoms:</strong> {langData.symptoms}
                    </p>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div className="bg-emerald-50/60 border border-emerald-100 rounded-xl p-3.5">
                        <h5 className="text-xs font-bold text-emerald-900 uppercase mb-2 flex items-center gap-1.5">
                          <Sprout className="w-4 h-4 text-emerald-600" /> Cultural Practices
                        </h5>
                        <ul className="text-xs text-slate-700 space-y-1.5 list-disc pl-4">
                          {langData.cultural.map((item: string, i: number) => (
                            <li key={i}>{item}</li>
                          ))}
                        </ul>
                      </div>

                      <div className="bg-blue-50/60 border border-blue-100 rounded-xl p-3.5">
                        <h5 className="text-xs font-bold text-blue-900 uppercase mb-2 flex items-center gap-1.5">
                          <ShieldAlert className="w-4 h-4 text-blue-600" /> Biological Controls
                        </h5>
                        <ul className="text-xs text-slate-700 space-y-1.5 list-disc pl-4">
                          {langData.biological.map((item: string, i: number) => (
                            <li key={i}>{item}</li>
                          ))}
                        </ul>
                      </div>

                      <div className="bg-amber-50/60 border border-amber-100 rounded-xl p-3.5">
                        <h5 className="text-xs font-bold text-amber-900 uppercase mb-2 flex items-center gap-1.5">
                          <AlertTriangle className="w-4 h-4 text-amber-600" /> Chemical (Strictly Last Resort)
                        </h5>
                        <ul className="text-xs text-slate-700 space-y-1.5 list-disc pl-4">
                          {langData.chemical_last.map((item: string, i: number) => (
                            <li key={i}>{item}</li>
                          ))}
                        </ul>
                      </div>

                      <div className="bg-purple-50/60 border border-purple-100 rounded-xl p-3.5">
                        <h5 className="text-xs font-bold text-purple-900 uppercase mb-2 flex items-center gap-1.5">
                          <CheckCircle2 className="w-4 h-4 text-purple-600" /> Safety Notes & PHI
                        </h5>
                        <ul className="text-xs text-slate-700 space-y-1.5 list-disc pl-4">
                          {langData.safety_notes.map((item: string, i: number) => (
                            <li key={i}>{item}</li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>

            {/* Official Disclaimer */}
            <div className="bg-amber-50 border-l-4 border-amber-500 p-4 rounded-r-xl text-xs text-amber-900">
              <strong>Official ICAR / KVK Advisory Disclaimer:</strong> {disclaimer}
            </div>
          </div>
        )}

        {/* TAB 5: STREAMLIT CLI GUIDE */}
        {activeTab === 'terminal' && (
          <div className="space-y-6">
            <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs">
              <h3 className="text-lg font-bold text-slate-900 mb-2">How to Run the Python Streamlit App</h3>
              <p className="text-sm text-slate-600 mb-4">
                The full Python Streamlit multi-page application is completely coded and structured in this repository. Follow these two commands to run it locally or on your server:
              </p>

              <div className="space-y-3 font-mono text-sm">
                <div className="bg-slate-950 text-slate-100 p-4 rounded-xl">
                  <div className="text-slate-400 text-xs mb-1"># 1. Install dependencies:</div>
                  <code className="text-emerald-400">pip install -r requirements.txt</code>
                </div>

                <div className="bg-slate-950 text-slate-100 p-4 rounded-xl">
                  <div className="text-slate-400 text-xs mb-1"># 2. Launch the Streamlit application:</div>
                  <code className="text-emerald-400">streamlit run app.py</code>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs">
              <h3 className="text-lg font-bold text-slate-900 mb-3">Project File Structure Verification</h3>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
                <div className="p-3 bg-slate-50 border rounded-xl">
                  <span className="font-bold text-emerald-800">app.py</span>
                  <p className="text-slate-600">Main hub, system stats, system architecture</p>
                </div>
                <div className="p-3 bg-slate-50 border rounded-xl">
                  <span className="font-bold text-emerald-800">pages/1_🌾_Farmer_Diagnosis.py</span>
                  <p className="text-slate-600">Photo input, Open-Meteo weather risk, &lt;60% safety gate</p>
                </div>
                <div className="p-3 bg-slate-50 border rounded-xl">
                  <span className="font-bold text-emerald-800">pages/2_🛡️_Officer_Dashboard.py</span>
                  <p className="text-slate-600">Folium map, Maharashtra heatmaps, Confirm/Correct label</p>
                </div>
                <div className="p-3 bg-slate-50 border rounded-xl">
                  <span className="font-bold text-emerald-800">pages/3_📚_Disease_Advisory.py</span>
                  <p className="text-slate-600">Searchable trilingual IPM catalog (EN, HI, MR)</p>
                </div>
                <div className="p-3 bg-slate-50 border rounded-xl">
                  <span className="font-bold text-emerald-800">advisory.json</span>
                  <p className="text-slate-600">11 diseases in 3 languages, no invented dosages, safe IPM</p>
                </div>
                <div className="p-3 bg-slate-50 border rounded-xl">
                  <span className="font-bold text-emerald-800">db.py</span>
                  <p className="text-slate-600">SQLite persistence, 32 Maharashtra demo reports</p>
                </div>
                <div className="p-3 bg-slate-50 border rounded-xl">
                  <span className="font-bold text-emerald-800">weather.py</span>
                  <p className="text-slate-600">Open-Meteo live atmospheric query & risk scoring</p>
                </div>
                <div className="p-3 bg-slate-50 border rounded-xl">
                  <span className="font-bold text-emerald-800">model.py</span>
                  <p className="text-slate-600">Hugging Face transformers pipeline & visual heuristic fallback</p>
                </div>
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-slate-900 text-slate-400 py-6 border-t border-slate-800 text-xs mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row justify-between items-center gap-3">
          <div className="flex items-center gap-2.5">
            <img 
              src="/logo.jpeg" 
              alt="CropGuard Logo" 
              className="w-6 h-6 rounded-full object-cover border border-slate-700 bg-white shrink-0"
            />
            <span>CropGuard: an open-source crop disease and pest detection tool</span>
          </div>
          <div>
            Adheres strictly to ICAR, KVK, and Integrated Pest Management (IPM) guidelines
          </div>
        </div>
      </footer>
    </div>
  );
}
