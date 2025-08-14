'use client'

import { useState, useEffect } from 'react'
import { FileText, Folder, Upload, Download, Trash2, Edit, Eye, MoreVertical } from 'lucide-react'

interface FileItem {
  id: string
  name: string
  type: 'file' | 'directory'
  size: string
  modified: string
  permissions: string
  path: string
}

export default function FilesPage() {
  const [files, setFiles] = useState<FileItem[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [currentPath, setCurrentPath] = useState('/')
  const [selectedFiles, setSelectedFiles] = useState<string[]>([])

  useEffect(() => {
    fetchFiles()
  }, [currentPath])

  const fetchFiles = async () => {
    try {
      setLoading(true)
      const response = await fetch(`/api/v1/files?path=${encodeURIComponent(currentPath)}`)
      if (!response.ok) {
        throw new Error('Failed to fetch files')
      }
      const data = await response.json()
      setFiles(data.files || [])
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch files')
    } finally {
      setLoading(false)
    }
  }

  const handleFileClick = (file: FileItem) => {
    if (file.type === 'directory') {
      setCurrentPath(file.path)
    }
  }

  const handleBackClick = () => {
    const parentPath = currentPath.split('/').slice(0, -1).join('/') || '/'
    setCurrentPath(parentPath)
  }

  const handleFileSelect = (fileId: string) => {
    setSelectedFiles(prev => 
      prev.includes(fileId) 
        ? prev.filter(id => id !== fileId)
        : [...prev, fileId]
    )
  }

  const handleSelectAll = () => {
    if (selectedFiles.length === files.length) {
      setSelectedFiles([])
    } else {
      setSelectedFiles(files.map(f => f.id))
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <div className="text-red-600 text-lg mb-4">Error: {error}</div>
        <button 
          onClick={fetchFiles}
          className="btn btn-primary"
        >
          Retry
        </button>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">File Manager</h1>
          <p className="text-gray-600 mt-2">Manage files and directories</p>
        </div>
        <div className="flex space-x-3">
          <button className="btn btn-secondary">
            <Upload className="h-4 w-4 mr-2" />
            Upload Files
          </button>
          <button className="btn btn-primary">
            <Folder className="h-4 w-4 mr-2" />
            New Folder
          </button>
        </div>
      </div>

      {/* Breadcrumb */}
      <div className="card p-4">
        <div className="flex items-center space-x-2 text-sm">
          <button
            onClick={() => setCurrentPath('/')}
            className="text-primary-600 hover:text-primary-800"
          >
            Home
          </button>
          {currentPath !== '/' && currentPath.split('/').filter(Boolean).map((segment, index, segments) => (
            <div key={index} className="flex items-center space-x-2">
              <span className="text-gray-400">/</span>
              <button
                onClick={() => {
                  const newPath = '/' + segments.slice(0, index + 1).join('/')
                  setCurrentPath(newPath)
                }}
                className="text-primary-600 hover:text-primary-800"
              >
                {segment}
              </button>
            </div>
          ))}
        </div>
      </div>

      {/* Toolbar */}
      <div className="card p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <button
              onClick={handleBackClick}
              disabled={currentPath === '/'}
              className="btn btn-secondary"
            >
              ← Back
            </button>
            <span className="text-sm text-gray-600">
              {selectedFiles.length} of {files.length} selected
            </span>
          </div>
          <div className="flex items-center space-x-2">
            {selectedFiles.length > 0 && (
              <>
                <button className="btn btn-secondary">
                  <Download className="h-4 w-4 mr-2" />
                  Download
                </button>
                <button className="btn btn-secondary">
                  <Edit className="h-4 w-4 mr-2" />
                  Rename
                </button>
                <button className="btn btn-danger">
                  <Trash2 className="h-4 w-4 mr-2" />
                  Delete
                </button>
              </>
            )}
          </div>
        </div>
      </div>

      {/* Files List */}
      <div className="card">
        <div className="p-6 border-b border-gray-200">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-semibold text-gray-900">Files & Folders</h3>
            <button
              onClick={handleSelectAll}
              className="text-sm text-primary-600 hover:text-primary-800"
            >
              {selectedFiles.length === files.length ? 'Deselect All' : 'Select All'}
            </button>
          </div>
        </div>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  <input
                    type="checkbox"
                    checked={selectedFiles.length === files.length && files.length > 0}
                    onChange={handleSelectAll}
                    className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                  />
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Name
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Size
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Modified
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Permissions
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {files.length === 0 ? (
                <tr>
                  <td colSpan={6} className="px-6 py-12 text-center text-gray-500">
                    No files found in this directory.
                  </td>
                </tr>
              ) : (
                files.map((file) => (
                  <tr key={file.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <input
                        type="checkbox"
                        checked={selectedFiles.includes(file.id)}
                        onChange={() => handleFileSelect(file.id)}
                        className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                      />
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div 
                        className="flex items-center cursor-pointer"
                        onClick={() => handleFileClick(file)}
                      >
                        {file.type === 'directory' ? (
                          <Folder className="h-5 w-5 text-blue-500 mr-3" />
                        ) : (
                          <FileText className="h-5 w-5 text-gray-400 mr-3" />
                        )}
                        <div>
                          <div className="text-sm font-medium text-gray-900">
                            {file.name}
                          </div>
                          <div className="text-sm text-gray-500">
                            {file.type === 'directory' ? 'Directory' : 'File'}
                          </div>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {file.type === 'directory' ? '--' : file.size}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {new Date(file.modified).toLocaleDateString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {file.permissions}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <div className="flex space-x-2">
                        {file.type === 'file' && (
                          <>
                            <button className="text-blue-600 hover:text-blue-900" title="View">
                              <Eye className="h-4 w-4" />
                            </button>
                            <button className="text-green-600 hover:text-green-900" title="Download">
                              <Download className="h-4 w-4" />
                            </button>
                          </>
                        )}
                        <button className="text-yellow-600 hover:text-yellow-900" title="Edit">
                          <Edit className="h-4 w-4" />
                        </button>
                        <button className="text-red-600 hover:text-red-900" title="Delete">
                          <Trash2 className="h-4 w-4" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* File Upload Area */}
      <div className="card p-6">
        <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
          <Upload className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">Upload Files</h3>
          <p className="text-gray-600 mb-4">
            Drag and drop files here, or click to browse
          </p>
          <button className="btn btn-primary">
            Choose Files
          </button>
        </div>
      </div>
    </div>
  )
}
