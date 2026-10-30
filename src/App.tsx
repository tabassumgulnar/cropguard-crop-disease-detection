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
  Search
} from 'lucide-react';

export default function App() {
  const [selectedCrop, setSelectedCrop] = useState<'tomato' | 'cotton' | 'onion'>('tomato');
  const [selectedLang, setSelectedLang] = useState<'en' | 'hi' | 'mr'>('en');
  const [searchQuery, setSearchQuery] = useState('');
  const [activeTab, setActiveTab] = useState<'overview' | 'advisory' | 'terminal'>('overview');

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

  return (
    <div className="min-h-screen bg-slate-50 text-slate-800 flex flex-col font-sans">
      {/* Top Banner */}
      <header className="bg-emerald-900 text-white shadow-md border-b border-emerald-800">
        <div className="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8 flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div className="flex items-center space-x-3">
            <div className="bg-emerald-700 p-2.5 rounded-xl shadow-inner">
              <Sprout className="w-7 h-7 text-emerald-200" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-2xl font-bold tracking-tight">CropGuard</h1>
              </div>
              <p className="text-emerald-200 text-sm">
                Early Crop Disease & Pest Detection • Integrated Pest Management (IPM)
              </p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <div className="flex items-center bg-emerald-950/60 rounded-lg p-1 border border-emerald-700/50">
              <Languages className="w-4 h-4 text-emerald-300 ml-2 mr-1" />
              <button 
                onClick={() => setSelectedLang('en')}
                className={`px-2.5 py-1 text-xs font-semibold rounded ${selectedLang === 'en' ? 'bg-emerald-600 text-white' : 'text-emerald-200 hover:text-white'}`}
              >
                English
              </button>
              <button 
                onClick={() => setSelectedLang('hi')}
                className={`px-2.5 py-1 text-xs font-semibold rounded ${selectedLang === 'hi' ? 'bg-emerald-600 text-white' : 'text-emerald-200 hover:text-white'}`}
              >
                हिन्दी
              </button>
              <button 
                onClick={() => setSelectedLang('mr')}
                className={`px-2.5 py-1 text-xs font-semibold rounded ${selectedLang === 'mr' ? 'bg-emerald-600 text-white' : 'text-emerald-200 hover:text-white'}`}
              >
                मराठी
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Nav Tabs */}
      <nav className="bg-white border-b border-slate-200 shadow-xs">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex space-x-6">
          <button
            onClick={() => setActiveTab('overview')}
            className={`py-3 px-2 border-b-2 text-sm font-semibold flex items-center gap-2 ${
              activeTab === 'overview'
                ? 'border-emerald-600 text-emerald-700'
                : 'border-transparent text-slate-500 hover:text-slate-700'
            }`}
          >
            <Activity className="w-4 h-4" /> System Overview & Diagnostic Status
          </button>
          <button
            onClick={() => setActiveTab('advisory')}
            className={`py-3 px-2 border-b-2 text-sm font-semibold flex items-center gap-2 ${
              activeTab === 'advisory'
                ? 'border-emerald-600 text-emerald-700'
                : 'border-transparent text-slate-500 hover:text-slate-700'
            }`}
          >
            <FileText className="w-4 h-4" /> IPM Advisory Catalog ({selectedLang.toUpperCase()})
          </button>
          <button
            onClick={() => setActiveTab('terminal')}
            className={`py-3 px-2 border-b-2 text-sm font-semibold flex items-center gap-2 ${
              activeTab === 'terminal'
                ? 'border-emerald-600 text-emerald-700'
                : 'border-transparent text-slate-500 hover:text-slate-700'
            }`}
          >
            <Terminal className="w-4 h-4" /> Streamlit Execution & Testing
          </button>
        </div>
      </nav>

      {/* Main Content Area */}
      <main className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8 flex-1 w-full">
        {/* Top Notification Badge */}
        <div className="mb-6 bg-emerald-50 border border-emerald-200 rounded-xl p-4 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
          <div className="flex items-center gap-3">
            <span className="flex h-3 w-3 relative">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-3 w-3 bg-emerald-500"></span>
            </span>
            <div>
              <p className="text-sm font-semibold text-emerald-900">
                CropGuard Architecture Ready: Python Streamlit App + SQLite Database Active
              </p>
              <p className="text-xs text-emerald-700">
                Includes pre-seeded Maharashtra field surveillance records, Hugging Face vision models, and Open-Meteo risk scoring.
              </p>
            </div>
          </div>
          <button 
            onClick={() => setActiveTab('terminal')}
            className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-emerald-700 text-white text-xs font-semibold rounded-lg hover:bg-emerald-800 transition"
          >
            <Terminal className="w-3.5 h-3.5" /> Launch Streamlit Guide
          </button>
        </div>

        {activeTab === 'overview' && (
          <div className="space-y-6">
            {/* Quick Metrics */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs">
                <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Target Crops</div>
                <div className="mt-2 text-2xl font-bold text-slate-800">Tomato, Cotton, Onion</div>
                <div className="mt-1 text-xs text-emerald-600 flex items-center gap-1">
                  <CheckCircle2 className="w-3.5 h-3.5" /> 11 Pathogen Profiles
                </div>
              </div>

              <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs">
                <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Safety Confidence Gate</div>
                <div className="mt-2 text-2xl font-bold text-amber-600">&lt; 60% Threshold</div>
                <div className="mt-1 text-xs text-slate-600">Suppresses false chemical advice</div>
              </div>

              <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs">
                <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Weather Risk Engine</div>
                <div className="mt-2 text-2xl font-bold text-blue-600">Open-Meteo API</div>
                <div className="mt-1 text-xs text-slate-600">Zero-key live temp/humidity/rain</div>
              </div>

              <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs">
                <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Demo GIS Records</div>
                <div className="mt-2 text-2xl font-bold text-emerald-700">32 Field Reports</div>
                <div className="mt-1 text-xs text-slate-600">Pune, Nashik, Jalgaon, Nagpur</div>
              </div>
            </div>

            {/* Feature Modules */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-xs flex flex-col justify-between">
                <div>
                  <div className="w-10 h-10 rounded-lg bg-emerald-100 text-emerald-700 flex items-center justify-center mb-4">
                    <Sprout className="w-5 h-5" />
                  </div>
                  <h3 className="text-lg font-bold text-slate-800 mb-2">1. Farmer Diagnostic Portal</h3>
                  <p className="text-sm text-slate-600 mb-4 leading-relaxed">
                    Leaf upload or live camera photo classification using pretrained Hugging Face transformers. Returns top-3 ranked predictions with probability bars and flags uncertain cases below 60%.
                  </p>
                </div>
                <div className="text-xs font-medium text-emerald-800 bg-emerald-50 px-3 py-2 rounded-lg border border-emerald-100">
                  Entrypoint: <code>pages/1_🌾_Farmer_Diagnosis.py</code>
                </div>
              </div>

              <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-xs flex flex-col justify-between">
                <div>
                  <div className="w-10 h-10 rounded-lg bg-blue-100 text-blue-700 flex items-center justify-center mb-4">
                    <CloudSun className="w-5 h-5" />
                  </div>
                  <h3 className="text-lg font-bold text-slate-800 mb-2">2. Weather Epidemiology</h3>
                  <p className="text-sm text-slate-600 mb-4 leading-relaxed">
                    Fetches ambient temperature, humidity, rainfall, and wind speed. Rule-based model scores fungal incubation and vector pest multiplication risk into Low, Medium, and High alerts.
                  </p>
                </div>
                <div className="text-xs font-medium text-blue-800 bg-blue-50 px-3 py-2 rounded-lg border border-blue-100">
                  Engine: <code>weather.py</code>
                </div>
              </div>

              <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-xs flex flex-col justify-between">
                <div>
                  <div className="w-10 h-10 rounded-lg bg-amber-100 text-amber-700 flex items-center justify-center mb-4">
                    <ShieldAlert className="w-5 h-5" />
                  </div>
                  <h3 className="text-lg font-bold text-slate-800 mb-2">3. Officer GIS Dashboard</h3>
                  <p className="text-sm text-slate-600 mb-4 leading-relaxed">
                    Interactive Folium map with severity markers, regional epidemic heatmaps, incidence charts, and a human-in-the-loop "Confirm / Correct Label" workflow for active learning.
                  </p>
                </div>
                <div className="text-xs font-medium text-amber-800 bg-amber-50 px-3 py-2 rounded-lg border border-amber-100">
                  Entrypoint: <code>pages/2_🛡️_Officer_Dashboard.py</code>
                </div>
              </div>
            </div>

            {/* Architectural Workflow Diagram */}
            <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-xs">
              <h3 className="text-lg font-bold text-slate-800 mb-4 flex items-center gap-2">
                <Layers className="w-5 h-5 text-emerald-600" /> System Flow
              </h3>
              <div className="p-4 bg-slate-900 text-emerald-400 rounded-lg font-mono text-xs sm:text-sm overflow-x-auto">
                <pre>{`[ Farmer Leaf Photo ]  ──▶ [ Hugging Face Vision Model / Heuristic Engine ]
                                  │
                                  ▼ Top-3 Predictions with Confidences
[ Field GPS Lat/Lon ]  ──▶ [ Open-Meteo Weather API ] ──▶ [ Fungal/Pest Risk ]
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

        {activeTab === 'advisory' && (
          <div className="space-y-6">
            {/* Filter Bar */}
            <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs flex flex-col sm:flex-row gap-4 items-center justify-between">
              <div className="flex items-center gap-2 w-full sm:w-auto">
                <span className="text-xs font-bold text-slate-500 uppercase">Crop:</span>
                {(['tomato', 'cotton', 'onion'] as const).map((crop) => (
                  <button
                    key={crop}
                    onClick={() => setSelectedCrop(crop)}
                    className={`px-3 py-1.5 text-xs font-bold uppercase rounded-lg border transition ${
                      selectedCrop === crop
                        ? 'bg-emerald-700 text-white border-emerald-700'
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
                  className="w-full pl-9 pr-3 py-1.5 text-sm border border-slate-300 rounded-lg focus:outline-emerald-600"
                />
              </div>
            </div>

            {/* Disease Cards */}
            <div className="space-y-4">
              {diseases.map(([key, info]) => {
                const langData = info[selectedLang] || info.en;
                return (
                  <div key={key} className="bg-white border border-slate-200 rounded-xl p-6 shadow-xs">
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

                    <p className="text-sm text-slate-700 mb-4 bg-slate-50 p-3 rounded-lg border border-slate-100">
                      <strong>Symptoms:</strong> {langData.symptoms}
                    </p>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div className="bg-emerald-50/50 border border-emerald-100 rounded-lg p-3">
                        <h5 className="text-xs font-bold text-emerald-900 uppercase mb-2 flex items-center gap-1">
                          <Sprout className="w-3.5 h-3.5 text-emerald-600" /> Cultural Practices
                        </h5>
                        <ul className="text-xs text-slate-700 space-y-1 list-disc pl-4">
                          {langData.cultural.map((item: string, i: number) => (
                            <li key={i}>{item}</li>
                          ))}
                        </ul>
                      </div>

                      <div className="bg-blue-50/50 border border-blue-100 rounded-lg p-3">
                        <h5 className="text-xs font-bold text-blue-900 uppercase mb-2 flex items-center gap-1">
                          <ShieldAlert className="w-3.5 h-3.5 text-blue-600" /> Biological Controls
                        </h5>
                        <ul className="text-xs text-slate-700 space-y-1 list-disc pl-4">
                          {langData.biological.map((item: string, i: number) => (
                            <li key={i}>{item}</li>
                          ))}
                        </ul>
                      </div>

                      <div className="bg-amber-50/50 border border-amber-100 rounded-lg p-3">
                        <h5 className="text-xs font-bold text-amber-900 uppercase mb-2 flex items-center gap-1">
                          <AlertTriangle className="w-3.5 h-3.5 text-amber-600" /> Chemical (Strictly Last Resort)
                        </h5>
                        <ul className="text-xs text-slate-700 space-y-1 list-disc pl-4">
                          {langData.chemical_last.map((item: string, i: number) => (
                            <li key={i}>{item}</li>
                          ))}
                        </ul>
                      </div>

                      <div className="bg-purple-50/50 border border-purple-100 rounded-lg p-3">
                        <h5 className="text-xs font-bold text-purple-900 uppercase mb-2 flex items-center gap-1">
                          <CheckCircle2 className="w-3.5 h-3.5 text-purple-600" /> Safety Notes & PHI
                        </h5>
                        <ul className="text-xs text-slate-700 space-y-1 list-disc pl-4">
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
              <strong>Official Disclaimer:</strong> {disclaimer}
            </div>
          </div>
        )}

        {activeTab === 'terminal' && (
          <div className="space-y-6">
            <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-xs">
              <h3 className="text-lg font-bold text-slate-900 mb-2">How to Run the Python Streamlit App</h3>
              <p className="text-sm text-slate-600 mb-4">
                The full Python Streamlit multi-page application is completely coded and structured in this repository. Follow these two commands to run it:
              </p>

              <div className="space-y-3 font-mono text-sm">
                <div className="bg-slate-950 text-slate-100 p-4 rounded-lg">
                  <div className="text-slate-400 text-xs mb-1"># 1. Install dependencies:</div>
                  <code className="text-emerald-400">pip install -r requirements.txt</code>
                </div>

                <div className="bg-slate-950 text-slate-100 p-4 rounded-lg">
                  <div className="text-slate-400 text-xs mb-1"># 2. Launch the Streamlit application:</div>
                  <code className="text-emerald-400">streamlit run app.py</code>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-xs">
              <h3 className="text-lg font-bold text-slate-900 mb-3">Project File Structure Verification</h3>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
                <div className="p-3 bg-slate-50 border rounded-lg">
                  <span className="font-bold text-emerald-800">app.py</span>
                  <p className="text-slate-600">Main hub, system stats, system architecture</p>
                </div>
                <div className="p-3 bg-slate-50 border rounded-lg">
                  <span className="font-bold text-emerald-800">pages/1_🌾_Farmer_Diagnosis.py</span>
                  <p className="text-slate-600">Photo input, Open-Meteo weather risk, &lt;60% safety gate</p>
                </div>
                <div className="p-3 bg-slate-50 border rounded-lg">
                  <span className="font-bold text-emerald-800">pages/2_🛡️_Officer_Dashboard.py</span>
                  <p className="text-slate-600">Folium map, Maharashtra heatmaps, Confirm/Correct label</p>
                </div>
                <div className="p-3 bg-slate-50 border rounded-lg">
                  <span className="font-bold text-emerald-800">pages/3_📚_Disease_Advisory.py</span>
                  <p className="text-slate-600">Searchable trilingual IPM catalog (EN, HI, MR)</p>
                </div>
                <div className="p-3 bg-slate-50 border rounded-lg">
                  <span className="font-bold text-emerald-800">advisory.json</span>
                  <p className="text-slate-600">11 diseases in 3 languages, no invented dosages, safe IPM</p>
                </div>
                <div className="p-3 bg-slate-50 border rounded-lg">
                  <span className="font-bold text-emerald-800">db.py</span>
                  <p className="text-slate-600">SQLite persistence, 32 Maharashtra demo reports</p>
                </div>
                <div className="p-3 bg-slate-50 border rounded-lg">
                  <span className="font-bold text-emerald-800">weather.py</span>
                  <p className="text-slate-600">Open-Meteo live atmospheric query & risk scoring</p>
                </div>
                <div className="p-3 bg-slate-50 border rounded-lg">
                  <span className="font-bold text-emerald-800">model.py</span>
                  <p className="text-slate-600">Hugging Face transformers pipeline & visual heuristic fallback</p>
                </div>
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-slate-900 text-slate-400 py-6 border-t border-slate-800 text-xs">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row justify-between items-center gap-3">
          <div>
            CropGuard: an open-source crop disease and pest detection tool
          </div>
          <div>
            Adheres strictly to ICAR, KVK, and Integrated Pest Management (IPM) guidelines
          </div>
        </div>
      </footer>
    </div>
  );
}
