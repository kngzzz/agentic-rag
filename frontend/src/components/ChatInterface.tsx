import React, { useState, useCallback, useRef, useEffect } from 'react';
import { useMutation } from '@tanstack/react-query';
import { askQuestion } from '../apiClient';

interface Message {
  id: number;
  text: string;
  sender: 'user' | 'bot';
  sources?: any[]; // Store source documents if available
  thoughtProcess?: string; // Added to store agent's thought process
}

function ChatInterface() {
  const [input, setInput] = useState<string>('');
  const [messages, setMessages] = useState<Message[]>([]);
  const messageEndRef = useRef<HTMLDivElement>(null);

  const mutation = useMutation({
    mutationFn: askQuestion,
    onSuccess: (data) => {
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now(),
          text: data.answer || 'No answer received.',
          sender: 'bot',
          sources: data.sources,
          thoughtProcess: data.thought_process, // Store thought process
        },
      ]);
    },
    onError: (error: any) => {
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now(),
          text: `Error: ${error.response?.data?.detail || error.message}`,
          sender: 'bot',
        },
      ]);
    },
  });

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setInput(event.target.value);
  };

  const handleSend = useCallback(() => {
    if (input.trim() && !mutation.isPending) {
      const userMessage: Message = {
        id: Date.now(),
        text: input,
        sender: 'user',
      };
      setMessages((prev) => [...prev, userMessage]);
      mutation.mutate(input);
      setInput('');
    }
  }, [input, mutation]);

  const handleKeyPress = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === 'Enter') {
      handleSend();
    }
  };

  // Scroll to bottom when new messages arrive
  useEffect(() => {
    messageEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    // Use chat-interface class for the main container if needed, or remove if chat-area handles all styling
    <div className="chat-interface"> 
      {/* Changed message-list to chat-output */}
      <div className="chat-output"> 
        {messages.map((msg) => (
          // Keep message and sender classes for bubble styling
          <div key={msg.id} className={`message ${msg.sender}`}> 
            <p>{msg.text}</p>
            {msg.sender === 'bot' && msg.sources && msg.sources.length > 0 && (
              <div className="sources">
                <strong>Sources:</strong>
                <ul>
                  {msg.sources?.map((source, index) => (
                    // Assuming source.doc_metadata contains source_filename and chunk_index
                    <li key={index}>
                      {source.doc_metadata?.source_filename ?? 'Unknown Source'} (Chunk {source.doc_metadata?.chunk_index ?? 'N/A'})
                      {/* TODO: Optionally show source.content snippet or make clickable */}
                    </li>
                  ))}
                </ul>
              </div>
            )}
            {/* Display Thought Process */}
            {msg.sender === 'bot' && msg.thoughtProcess && (
              <details className="thought-process">
                <summary>Show Thought Process</summary>
                <pre>{msg.thoughtProcess}</pre>
              </details>
            )}
          </div>
        ))}
        {mutation.isPending && (
            <div className="message bot">
                <p><i>JARVIS is thinking...</i></p>
            </div>
        )}
        <div ref={messageEndRef} />
      </div>
      {/* Changed input-area to chat-input-area */}
      <div className="chat-input-area"> 
        <input
          type="text"
          value={input}
          onChange={handleInputChange}
          onKeyPress={handleKeyPress}
          placeholder="Ask a question..."
          disabled={mutation.isPending}
        />
        <button onClick={handleSend} disabled={!input.trim() || mutation.isPending}>
          {/* Use btn class from example CSS */}
          Send 
        </button>
      </div>
    </div>
  );
}

export default ChatInterface;
