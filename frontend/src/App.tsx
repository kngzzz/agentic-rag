import React, { useState } from 'react'; // Import useState
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import FileUpload from './components/FileUpload';
import ChatInterface from './components/ChatInterface';
import './App.css'; 

const queryClient = new QueryClient();

type ActiveTab = 'upload' | 'ask'; // Define possible tab states

function App() {
  const [activeTab, setActiveTab] = useState<ActiveTab>('upload'); // Default to upload tab

  const handleTabClick = (tabName: ActiveTab) => {
    setActiveTab(tabName);
  };

  return (
    <QueryClientProvider client={queryClient}>
      <div className="app-container">
        {/* Header */}
        <header className="app-header">
          <h1>JARVIS Demo</h1>
        </header>

        {/* Tabs */}
        <div className="app-tabs">
          <button 
            className={`tab-button ${activeTab === 'upload' ? 'active' : ''}`} 
            onClick={() => handleTabClick('upload')}
          >
            Upload Documents
          </button>
          <button 
            className={`tab-button ${activeTab === 'ask' ? 'active' : ''}`} 
            onClick={() => handleTabClick('ask')}
          >
            Ask JARVIS
          </button>
        </div>

        {/* Main Content Area */}
        <main className="app-main-content">
          {/* Conditional Rendering based on activeTab */}
          {activeTab === 'upload' && (
            <aside className="sidebar" id="upload-section">
              <h2>Upload Documents</h2>
              <FileUpload />
            </aside>
          )}
          {activeTab === 'ask' && (
            <section className="chat-area" id="ask-section">
              <h2>Ask JARVIS</h2>
              <ChatInterface />
            </section>
          )}
        </main>
      </div>
    </QueryClientProvider>
  );
}

export default App;
