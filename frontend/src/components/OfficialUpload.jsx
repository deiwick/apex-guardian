import React, { useState, useRef } from 'react';

const OfficialUpload = () => {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState(''); // 'success', 'error', ''
  const fileInputRef = useRef(null);

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelection(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFileSelection(e.target.files[0]);
    }
  };

  const handleFileSelection = (selectedFile) => {
    setFile(selectedFile);
    setUploadStatus('');
    // Simple preview for images/videos
    if (selectedFile.type.startsWith('image/')) {
      const reader = new FileReader();
      reader.onload = (e) => setPreview(e.target.result);
      reader.readAsDataURL(selectedFile);
    } else {
      setPreview(null);
    }
  };

  const triggerSelect = () => {
    fileInputRef.current.click();
  };

  const handleUpload = async () => {
    if (!file) return;
    setIsUploading(true);
    setUploadStatus('');

    const formData = new FormData();
    formData.append('file', file);
    formData.append('metadata', JSON.stringify({ source: 'OfficialBroadcaster', timestamp: new Date().toISOString() }));

    try {
      // NOTE: Replace with actual backend API URL
      const response = await fetch('http://localhost:8000/api/upload', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        setUploadStatus('success');
        setFile(null);
        setPreview(null);
      } else {
        setUploadStatus('error');
      }
    } catch (error) {
      console.error('Upload failed', error);
      setUploadStatus('error');
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-900 p-6">
      <div className="max-w-xl w-full bg-slate-800 rounded-2xl shadow-2xl p-8 border border-slate-700">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-extrabold text-white tracking-tight">ApexGuardian</h1>
          <p className="text-slate-400 mt-2">Official Media Upload Portal</p>
        </div>

        <div
          className="border-2 border-dashed border-sky-500/50 rounded-xl p-10 flex flex-col items-center justify-center transition-all hover:bg-slate-700/50 hover:border-sky-400 cursor-pointer mb-6"
          onDragOver={handleDragOver}
          onDrop={handleDrop}
          onClick={triggerSelect}
        >
          <input
            type="file"
            className="hidden"
            ref={fileInputRef}
            onChange={handleFileChange}
            accept="image/*,video/*"
          />
          {preview ? (
            <div className="relative group">
               <img src={preview} alt="Preview" className="max-h-48 rounded-lg object-contain" />
               <div className="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center rounded-lg">
                 <p className="text-white font-medium">Change File</p>
               </div>
            </div>
          ) : (
            <div className="text-center">
              <svg className="mx-auto h-12 w-12 text-sky-400 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
              </svg>
              <p className="text-slate-300 font-medium text-lg">Drag & Drop official media</p>
              <p className="text-slate-500 text-sm mt-1">or click to browse from your computer</p>
            </div>
          )}
        </div>

        {file && (
          <div className="bg-slate-700/50 rounded-lg p-4 mb-6 flex justify-between items-center">
            <div className="truncate pr-4 text-slate-300 text-sm">{file.name}</div>
            <div className="text-xs text-sky-400 font-semibold">{(file.size / (1024 * 1024)).toFixed(2)} MB</div>
          </div>
        )}

        <button
          onClick={handleUpload}
          disabled={!file || isUploading}
          className={`w-full py-4 rounded-xl font-bold text-lg transition-all shadow-lg ${
            !file || isUploading
              ? 'bg-slate-600 text-slate-400 cursor-not-allowed'
              : 'bg-gradient-to-r from-sky-500 to-indigo-600 text-white hover:from-sky-400 hover:to-indigo-500 hover:shadow-sky-500/25'
          }`}
        >
          {isUploading ? (
             <span className="flex items-center justify-center">
               <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                 <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                 <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
               </svg>
               Securing Media...
             </span>
          ) : 'Submit for Protection'}
        </button>

        {uploadStatus === 'success' && (
          <div className="mt-6 p-4 bg-emerald-500/20 border border-emerald-500/50 rounded-xl text-emerald-400 text-center text-sm font-medium">
            Media securely processed and P-Hash registered.
          </div>
        )}
        {uploadStatus === 'error' && (
          <div className="mt-6 p-4 bg-rose-500/20 border border-rose-500/50 rounded-xl text-rose-400 text-center text-sm font-medium">
            Error processing upload. Please try again.
          </div>
        )}
      </div>
    </div>
  );
};

export default OfficialUpload;
