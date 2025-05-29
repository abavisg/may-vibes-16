import './index.css';

const PRO_AVATAR = 'https://images.unsplash.com/photo-1511367461989-f85a21fda167?auto=format&fit=crop&w=256&q=80';
const CON_AVATAR = 'https://images.unsplash.com/photo-1508214751196-bcfd4ca60f91?auto=format&fit=crop&w=256&q=80';
const MOD_AVATAR = 'https://images.unsplash.com/photo-1464983953574-0892a716854b?auto=format&fit=crop&w=256&q=80';

export default function App() {
  return (
    <div className="debate-outer bg-[#222] min-h-screen flex flex-col items-center justify-center">
      <div className="debate-container w-full max-w-6xl mx-auto flex flex-col min-h-[90vh] rounded-3xl overflow-hidden shadow-xl bg-white" style={{boxShadow: '0 2px 24px 0 rgba(0,0,0,0.10)'}}>
        {/* Header */}
        <header className="flex items-center px-10 py-6 bg-white border-b border-gray-200" style={{borderTopLeftRadius: '1.5rem', borderTopRightRadius: '1.5rem'}}>
          <div className="font-bold text-xl flex-1">Debate Day</div>
          <div className="flex-1 flex justify-center">
            <input
              type="text"
              placeholder="Enter topic"
              className="debate-topic-input text-center text-gray-400 text-base bg-transparent border-0 border-b border-gray-200 focus:outline-none focus:border-black w-64"
              disabled
            />
          </div>
          <div className="flex-1 flex justify-end items-center gap-3">
            <select className="debate-round-select bg-transparent text-gray-600 text-base focus:outline-none cursor-pointer">
              <option>1 Round</option>
            </select>
            <button className="debate-btn border border-black rounded-full px-5 py-1 text-black bg-white hover:bg-gray-100">Start</button>
            <button className="debate-btn border border-black rounded-full px-5 py-1 text-black bg-white hover:bg-gray-100">Reset</button>
          </div>
        </header>

        {/* Main Debate Area */}
        <div className="flex flex-1 min-h-0">
          {/* Pro Debater */}
          <div className="flex-1 flex flex-col items-center justify-center bg-white">
            <div className="flex flex-col items-center">
              <div className="w-48 h-48 rounded-full overflow-hidden mb-4 shadow-lg">
                <img src={PRO_AVATAR} alt="Pro Debater" className="w-full h-full object-cover" />
              </div>
              <div className="text-lg text-black font-medium">Pro Debater</div>
            </div>
          </div>
          {/* Con Debater */}
          <div className="flex-1 flex flex-col items-center justify-center bg-black">
            <div className="flex flex-col items-center">
              <div className="w-48 h-48 rounded-full overflow-hidden mb-4 shadow-lg">
                <img src={CON_AVATAR} alt="Con Debater" className="w-full h-full object-cover" />
              </div>
              <div className="text-lg text-white font-medium">Con Debater</div>
            </div>
          </div>
        </div>

        {/* Moderator */}
        <div className="bg-[#f4f4f4] flex items-center justify-center py-10" style={{borderBottomLeftRadius: '1.5rem', borderBottomRightRadius: '1.5rem'}}>
          <div className="flex flex-col items-center">
            <div className="w-32 h-32 rounded-full overflow-hidden mb-2 shadow-lg">
              <img src={MOD_AVATAR} alt="Moderator" className="w-full h-full object-cover" />
            </div>
            <div className="text-lg text-black font-medium">Moderator</div>
          </div>
        </div>
      </div>
    </div>
  );
}
