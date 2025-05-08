import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api', // Use local development server
  headers: {
    'Content-Type': 'application/json',
  },
});

export const uploadFile = async (file: File) => {
  const formData = new FormData();
  formData.append('file', file);

  // Use 'multipart/form-data' for file uploads
  const response = await apiClient.post('/ingest/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const uploadFiles = async (files: File[]) => {
  // For batch uploads, we need to make multiple requests
  // (or update backend to accept multiple files)
  const formData = new FormData();
  
  // Add all files to formData
  files.forEach(file => {
    formData.append(`files`, file); // Use 'files' as the field name
  });

  // Use 'multipart/form-data' for file uploads
  const response = await apiClient.post('/ingest/upload-batch', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const askQuestion = async (question: string) => {
  const response = await apiClient.post('/query/ask', { question });
  return response.data;
};

export default apiClient;

