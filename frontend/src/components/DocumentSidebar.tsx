"use client";

import { useState, useEffect } from "react";
import { Upload, FileText, Plus, Search, Settings, MoreHorizontal } from "lucide-react";
import axios from "axios";

export default function DocumentSidebar() {
    const [uploading, setUploading] = useState(false);
    const [documents, setDocuments] = useState<string[]>([]);

    useEffect(() => {
        fetchDocuments();
    }, []);

    interface Document {
        id: number;
        filename: string;
    }

    const fetchDocuments = async () => {
        try {
            const response = await axios.get("http://localhost:8000/api/v1/documents/");
            setDocuments(response.data.map((doc: Document) => doc.filename));
        } catch (error) {
            console.error("Error fetching documents:", error);
        }
    };

    const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
        if (!e.target.files || e.target.files.length === 0) return;

        const file = e.target.files[0];
        setUploading(true);

        const formData = new FormData();
        formData.append("file", file);
        formData.append("project_id", "1");

        try {
            await axios.post("http://localhost:8000/api/v1/documents/upload", formData, {
                headers: {
                    "Content-Type": "multipart/form-data",
                },
            });
            await fetchDocuments();
        } catch (error) {
            console.error("Error uploading file:", error);
        } finally {
            setUploading(false);
        }
    };


    return (
        <div className="w-60 notion-sidebar h-full flex flex-col text-[14px]">
            {/* Workspace Header */}
            <div className="h-12 flex items-center px-4 hover:bg-[rgba(55,53,47,0.08)] cursor-pointer transition-colors">
                <div className="w-5 h-5 bg-orange-400 rounded-[3px] flex items-center justify-center text-white text-xs font-bold mr-2">
                    R
                </div>
                <span className="font-medium truncate flex-1">Research Studio</span>
                <div className="w-4 h-4 text-gray-400">
                    <span className="text-[10px]">▼</span>
                </div>
            </div>

            {/* Quick Actions */}
            <div className="px-2 py-2 space-y-0.5">
                <div className="notion-item">
                    <Search size={16} className="mr-2 text-gray-500" />
                    <span>Search</span>
                </div>
                <div className="notion-item">
                    <Settings size={16} className="mr-2 text-gray-500" />
                    <span>Settings</span>
                </div>
                <label className="notion-item group">
                    <div className="flex items-center w-full">
                        <div className="w-4 h-4 rounded-full bg-gray-200 flex items-center justify-center mr-2 group-hover:bg-gray-300 transition-colors">
                            <Plus size={10} className="text-gray-600" />
                        </div>
                        <span>New Page</span>
                    </div>
                    <input
                        type="file"
                        className="hidden"
                        onChange={handleFileUpload}
                        accept=".txt,.pdf,.md"
                    />
                </label>
            </div>

            {/* Favorites / Sections */}
            <div className="flex-1 overflow-y-auto px-2 pt-4">
                <div className="px-3 text-xs font-semibold text-gray-500 mb-1 flex justify-between group">
                    <span>PRIVATE</span>
                    <Plus size={12} className="opacity-0 group-hover:opacity-100 cursor-pointer hover:bg-gray-200 rounded" />
                </div>

                <ul className="space-y-0.5">
                    {documents.map((doc, idx) => (
                        <li key={idx} className="notion-item group justify-between">
                            <div className="flex items-center truncate">
                                <FileText size={16} className="mr-2 text-gray-400" />
                                <span className="truncate">{doc}</span>
                            </div>
                            <MoreHorizontal size={14} className="opacity-0 group-hover:opacity-100 text-gray-400 hover:text-gray-600" />
                        </li>
                    ))}
                    {documents.length === 0 && (
                        <li className="px-3 py-1 text-gray-400 italic text-xs">No pages yet</li>
                    )}
                </ul>

                {uploading && (
                    <div className="px-3 py-1 text-xs text-gray-400 animate-pulse">Adding page...</div>
                )}
            </div>

            {/* Bottom Action */}
            <div className="p-2 border-t border-[rgb(var(--border-color))]">
                <div className="notion-item">
                    <Plus size={16} className="mr-2 text-gray-500" />
                    <span>New Page</span>
                </div>
            </div>
        </div>
    );
}
