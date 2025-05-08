import React, { useState, useCallback } from 'react';
import { useMutation } from '@tanstack/react-query';
import { uploadFile } from '../apiClient';

function FileUpload() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [message, setMessage] = useState<string>('');

  const mutation = useMutation({
    mutationFn: uploadFile,
    onSuccess: (data) => {
      setMessage(data.message || 'File uploaded successfully!');
      setSelectedFile(null); // Clear selection after successful upload
      // Optionally: trigger a refetch of documents or update UI elsewhere
    },
    onError: (error: any) => {
      setMessage(`Upload failed: ${error.response?.data?.detail || error.message}`);
    },
  });

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setSelectedFile(event.target.files[0]);
      setMessage(''); // Clear previous messages
    }
  };

  const handleUpload = useCallback(() => {
    if (selectedFile) {
      setMessage('Uploading...');
      mutation.mutate(selectedFile);
    }
  }, [selectedFile, mutation]);

  return (
    <div className="file-upload">
      {/* Wrap input in a styled label */}
      <label htmlFor="file-input" className="file-upload-label">
        {selectedFile ? 'Change File' : 'Choose File'}
      </label>
      <input 
        id="file-input" 
        type="file" 
        onChange={handleFileChange} 
        accept=".pdf,.txt,.md,.json,.docx,.pptx" 
        className="file-input-hidden" // Add class to hide
      />
      {/* Display selected file name separately */}
      {selectedFile && (
        <p className="selected-file-info">Selected: {selectedFile.name} ({(selectedFile.size / 1024).toFixed(2)} KB)</p>
      )}
      <button onClick={handleUpload} disabled={!selectedFile || mutation.isPending}>
        {mutation.isPending ? 'Uploading...' : 'Upload File'}
      </button>
      {message && <p className={`message ${mutation.isError ? 'error' : ''}`}>{message}</p>}
    </div>
  );
}

export default FileUpload;
