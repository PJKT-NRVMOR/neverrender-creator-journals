import { useState, useEffect } from 'react';

const ASPECT_RATIOS = ["16:9 (Default Cinema)", "9:16 (Vertical Social Shorts)", "2.39:1 (Anamorphic Widescreen)"];
const ENVIRONMENTS = ["Urban Core Neon Hub", "Suburban Outskirts/Wasteland", "Vertical Core Elevator", "Deep Transit Terminal"];
const LIGHTING_PROFILES = ["High-Contrast Three-Point Atmospheric", "Raking Sunset Golden Hour", "Volumetric Mist Diffusion", "Low-Light Cyberpunk Fluorescence"];
const PHENOMENA_OPTS = ["Anamorphic Chromatic Aberration", "Prism Flare Refractions", "3% Handheld Micro-shake", "MRMC Flair Kinematic tracking"];

function App() {
  const [contexts, setContexts] = useState([]);
  const [formData, setFormData] = useState({
    subject: '',
    lens: '',
    vector: '',
    aspectRatio: ASPECT_RATIOS[0],
    environment: ENVIRONMENTS[0],
    lighting: LIGHTING_PROFILES[0],
    phenomena: [],
    tokenLock: '',
    selectedContexts: []
  });
  const [compiledXML, setCompiledXML] = useState('');
  const [isCompiling, setIsCompiling] = useState(false);

  useEffect(() => {
    fetch('http://localhost:3001/api/contexts')
      .then(res => res.json())
      .then(data => {
        if (data.files) setContexts(data.files);
      })
      .catch(err => console.error("Failed to fetch context files", err));
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleCheckboxChange = (e, field) => {
    const { value, checked } = e.target;
    setFormData(prev => {
      const arr = prev[field];
      if (checked) {
        return { ...prev, [field]: [...arr, value] };
      } else {
        return { ...prev, [field]: arr.filter(item => item !== value) };
      }
    });
  };

  const compilePrompt = async () => {
    setIsCompiling(true);
    try {
      const res = await fetch('http://localhost:3001/api/compile', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      const data = await res.json();
      if (data.result) {
        setCompiledXML(data.result);
      }
    } catch (err) {
      console.error(err);
      setCompiledXML("ERROR: Failed to connect to local compiler backend.");
    }
    setIsCompiling(false);
  };

  const copyToClipboard = () => {
    navigator.clipboard.writeText(compiledXML);
  };

  return (
    <div className="min-h-screen relative overflow-hidden text-neutral-200 p-6 flex flex-col md:flex-row gap-6 font-sans">
      <div className="fixed inset-0 scanlines z-50"></div>
      
      {/* Background Ambience */}
      <div className="fixed inset-0 pointer-events-none z-0">
        <div className="absolute top-[-10%] left-[-10%] w-[50vw] h-[50vw] bg-themePrimary opacity-10 rounded-full blur-[120px] mix-blend-screen animate-pulse duration-1000"></div>
        <div className="absolute bottom-[-20%] right-[-10%] w-[60vw] h-[60vw] bg-themeSecondary opacity-10 rounded-full blur-[150px] mix-blend-screen animate-pulse delay-700 duration-1000"></div>
      </div>

      <div className="relative z-10 w-full max-w-2xl flex flex-col gap-6 h-full overflow-y-auto pr-2" style={{ maxHeight: 'calc(100vh - 48px)' }}>
        <header className="glass-panel rounded-xl p-6 flex items-center justify-between border-t-2 border-themePrimary">
          <div>
            <h1 className="text-2xl font-black text-white tracking-widest uppercase" style={{ textShadow: '0 0 10px #00ffff' }}>Omni Prompt Studio</h1>
            <p className="font-terminal text-xs text-themeSecondary mt-1">v12.4 // LOCAL COMPILER ACTIVE</p>
          </div>
          <div className="w-3 h-3 rounded-full bg-themeTertiary animate-pulse shadow-[0_0_10px_#ffbf00]"></div>
        </header>

        <main className="glass-panel rounded-xl p-6 flex flex-col gap-5">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="flex flex-col gap-1">
              <label className="font-terminal text-[10px] text-themeSecondary uppercase">Subject</label>
              <input type="text" name="subject" value={formData.subject} onChange={handleInputChange} className="bg-black/50 border border-white/10 rounded p-2 text-sm focus:border-themeSecondary outline-none transition" placeholder="e.g. Asher, Neon Ronin" />
            </div>
            <div className="flex flex-col gap-1">
              <label className="font-terminal text-[10px] text-themeSecondary uppercase">Camera Lens</label>
              <input type="text" name="lens" value={formData.lens} onChange={handleInputChange} className="bg-black/50 border border-white/10 rounded p-2 text-sm focus:border-themeSecondary outline-none transition" placeholder="e.g. 24mm Anamorphic" />
            </div>
            <div className="flex flex-col gap-1 md:col-span-2">
              <label className="font-terminal text-[10px] text-themeSecondary uppercase">Camera Vector</label>
              <input type="text" name="vector" value={formData.vector} onChange={handleInputChange} className="bg-black/50 border border-white/10 rounded p-2 text-sm focus:border-themeSecondary outline-none transition" placeholder="e.g. Right-to-Left Tracking" />
            </div>
          </div>

          <div className="border-t border-white/10 my-2"></div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="flex flex-col gap-1">
              <label className="font-terminal text-[10px] text-themeTertiary uppercase">Aspect Ratio</label>
              <select name="aspectRatio" value={formData.aspectRatio} onChange={handleInputChange} className="bg-black/50 border border-white/10 rounded p-2 text-xs outline-none text-white focus:border-themeTertiary">
                {ASPECT_RATIOS.map(opt => <option key={opt} value={opt}>{opt}</option>)}
              </select>
            </div>
            <div className="flex flex-col gap-1">
              <label className="font-terminal text-[10px] text-themeTertiary uppercase">Environment Matrix</label>
              <select name="environment" value={formData.environment} onChange={handleInputChange} className="bg-black/50 border border-white/10 rounded p-2 text-xs outline-none text-white focus:border-themeTertiary">
                {ENVIRONMENTS.map(opt => <option key={opt} value={opt}>{opt}</option>)}
              </select>
            </div>
            <div className="flex flex-col gap-1">
              <label className="font-terminal text-[10px] text-themeTertiary uppercase">Lighting Profile</label>
              <select name="lighting" value={formData.lighting} onChange={handleInputChange} className="bg-black/50 border border-white/10 rounded p-2 text-xs outline-none text-white focus:border-themeTertiary">
                {LIGHTING_PROFILES.map(opt => <option key={opt} value={opt}>{opt}</option>)}
              </select>
            </div>
          </div>

          <div className="border-t border-white/10 my-2"></div>

          <div className="flex flex-col gap-2">
            <label className="font-terminal text-[10px] text-themePrimary uppercase">Optical Phenomena</label>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
              {PHENOMENA_OPTS.map(opt => (
                <label key={opt} className="flex items-center gap-2 text-xs cursor-pointer hover:text-white transition">
                  <input type="checkbox" value={opt} onChange={(e) => handleCheckboxChange(e, 'phenomena')} className="accent-themePrimary" />
                  {opt}
                </label>
              ))}
            </div>
          </div>

          <div className="flex flex-col gap-1 mt-2">
            <label className="font-terminal text-[10px] text-themeQuaternary uppercase">Asset Token Lock</label>
            <input type="text" name="tokenLock" value={formData.tokenLock} onChange={handleInputChange} className="bg-black/50 border border-white/10 rounded p-2 text-sm focus:border-themeQuaternary outline-none transition" placeholder="e.g. --seed 4567 or /paths/char.jpg" />
          </div>

          <div className="border-t border-white/10 my-2"></div>

          <div className="flex flex-col gap-2">
            <label className="font-terminal text-[10px] text-themeSecondary uppercase flex justify-between">
              <span>AGENTS/TO Context Injection</span>
              <span className="text-white/50">{contexts.length} files detected</span>
            </label>
            <div className="flex flex-col gap-2 bg-black/30 border border-white/10 p-3 rounded max-h-[150px] overflow-y-auto">
              {contexts.map(file => (
                <label key={file} className="flex items-center gap-2 text-xs cursor-pointer hover:text-white transition">
                  <input type="checkbox" value={file} onChange={(e) => handleCheckboxChange(e, 'selectedContexts')} className="accent-themeSecondary" />
                  {file}
                </label>
              ))}
              {contexts.length === 0 && <div className="text-xs text-white/30 italic">No .md, .txt, or .json files found in context directory.</div>}
            </div>
          </div>

          <button 
            onClick={compilePrompt}
            disabled={isCompiling}
            className="mt-4 neon-border bg-themeQuaternary/20 hover:bg-themePrimary/20 text-white font-black uppercase tracking-widest py-4 rounded-xl transition duration-300 shadow-[0_0_20px_rgba(255,0,127,0.2)] active:scale-95"
          >
            {isCompiling ? 'Compiling Matrix...' : 'Compile Omni Prompt'}
          </button>
        </main>
      </div>

      {/* Output Console */}
      <div className="relative z-10 w-full flex flex-col gap-4 h-full" style={{ maxHeight: 'calc(100vh - 48px)' }}>
        <div className="glass-panel rounded-xl p-4 flex-1 flex flex-col">
          <div className="flex items-center justify-between mb-3 border-b border-white/10 pb-3">
            <span className="font-terminal text-xs text-themeSecondary uppercase">Output Buffer</span>
            <button 
              onClick={copyToClipboard}
              className="bg-black/50 hover:bg-white/10 border border-white/20 px-3 py-1.5 rounded text-xs font-bold transition flex items-center gap-2"
            >
              <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"></path></svg>
              COPY XML
            </button>
          </div>
          <textarea 
            readOnly 
            value={compiledXML}
            className="flex-1 bg-black/60 border border-white/5 rounded-lg p-4 font-terminal text-[11px] text-themeTertiary outline-none resize-none focus:border-themeSecondary transition w-full"
            placeholder="<OMNI_PROMPT>&#10;  Waiting for compilation engine...&#10;</OMNI_PROMPT>"
          ></textarea>
        </div>
      </div>
    </div>
  )
}

export default App;
