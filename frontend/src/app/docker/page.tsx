'use client'

import { useState, useEffect } from 'react'
import { Box, Plus, Play, Square, RotateCcw, Trash2, Eye, Download } from 'lucide-react'

interface DockerContainer {
  id: string
  name: string
  image: string
  status: 'running' | 'stopped' | 'exited' | 'created'
  ports: string[]
  created: string
  size: string
}

interface DockerImage {
  id: string
  repository: string
  tag: string
  size: string
  created: string
}

export default function DockerPage() {
  const [containers, setContainers] = useState<DockerContainer[]>([])
  const [images, setImages] = useState<DockerImage[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [activeTab, setActiveTab] = useState<'containers' | 'images'>('containers')

  useEffect(() => {
    fetchDockerData()
  }, [])

  const fetchDockerData = async () => {
    try {
      setLoading(true)
      
      // Fetch containers
      const containersResponse = await fetch('/api/v1/docker/containers')
      if (containersResponse.ok) {
        const containersData = await containersResponse.json()
        setContainers(containersData.containers || [])
      }
      
      // Fetch images
      const imagesResponse = await fetch('/api/v1/docker/images')
      if (imagesResponse.ok) {
        const imagesData = await imagesResponse.json()
        setImages(imagesData.images || [])
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch Docker data')
    } finally {
      setLoading(false)
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'running':
        return 'bg-green-100 text-green-800'
      case 'stopped':
        return 'bg-gray-100 text-gray-800'
      case 'exited':
        return 'bg-red-100 text-red-800'
      case 'created':
        return 'bg-blue-100 text-blue-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const handleContainerAction = async (containerId: string, action: 'start' | 'stop' | 'restart') => {
    try {
      const response = await fetch(`/api/v1/docker/containers/${containerId}/${action}`, {
        method: 'POST'
      })
      if (response.ok) {
        // Refresh data after action
        fetchDockerData()
      }
    } catch (err) {
      console.error(`Failed to ${action} container:`, err)
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
          onClick={fetchDockerData}
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
          <h1 className="text-3xl font-bold text-gray-900">Docker Management</h1>
          <p className="text-gray-600 mt-2">Manage your Docker containers and images</p>
        </div>
        <button className="btn btn-primary">
          <Plus className="h-4 w-4 mr-2" />
          New Container
        </button>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="card p-6">
          <div className="flex items-center">
            <div className="p-3 bg-blue-500 rounded-lg">
              <Box className="h-6 w-6 text-white" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Total Containers</p>
              <p className="text-2xl font-bold text-gray-900">{containers.length}</p>
            </div>
          </div>
        </div>
        <div className="card p-6">
          <div className="flex items-center">
            <div className="p-3 bg-green-500 rounded-lg">
              <Box className="h-6 w-6 text-white" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Running</p>
              <p className="text-2xl font-bold text-gray-900">
                {containers.filter(c => c.status === 'running').length}
              </p>
            </div>
          </div>
        </div>
        <div className="card p-6">
          <div className="flex items-center">
            <div className="p-3 bg-yellow-500 rounded-lg">
              <Box className="h-6 w-6 text-white" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Stopped</p>
              <p className="text-2xl font-bold text-gray-900">
                {containers.filter(c => c.status === 'stopped').length}
              </p>
            </div>
          </div>
        </div>
        <div className="card p-6">
          <div className="flex items-center">
            <div className="p-3 bg-purple-500 rounded-lg">
              <Box className="h-6 w-6 text-white" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Images</p>
              <p className="text-2xl font-bold text-gray-900">{images.length}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="card">
        <div className="border-b border-gray-200">
          <nav className="-mb-px flex space-x-8 px-6">
            <button
              onClick={() => setActiveTab('containers')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'containers'
                  ? 'border-primary-500 text-primary-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Containers ({containers.length})
            </button>
            <button
              onClick={() => setActiveTab('images')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'images'
                  ? 'border-primary-500 text-primary-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Images ({images.length})
            </button>
          </nav>
        </div>

        <div className="p-6">
          {activeTab === 'containers' ? (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Name
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Image
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Status
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Ports
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {containers.length === 0 ? (
                    <tr>
                      <td colSpan={5} className="px-6 py-12 text-center text-gray-500">
                        No containers found. Create your first container to get started.
                      </td>
                    </tr>
                  ) : (
                    containers.map((container) => (
                      <tr key={container.id} className="hover:bg-gray-50">
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="flex items-center">
                            <Box className="h-5 w-5 text-gray-400 mr-3" />
                            <div>
                              <div className="text-sm font-medium text-gray-900">
                                {container.name}
                              </div>
                              <div className="text-sm text-gray-500">
                                {container.id.substring(0, 12)}
                              </div>
                            </div>
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {container.image}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(container.status)}`}>
                            {container.status}
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {container.ports.length > 0 ? container.ports.join(', ') : 'No ports'}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                          <div className="flex space-x-2">
                            {container.status === 'stopped' && (
                              <button 
                                onClick={() => handleContainerAction(container.id, 'start')}
                                className="text-green-600 hover:text-green-900"
                                title="Start"
                              >
                                <Play className="h-4 w-4" />
                              </button>
                            )}
                            {container.status === 'running' && (
                              <button 
                                onClick={() => handleContainerAction(container.id, 'stop')}
                                className="text-yellow-600 hover:text-yellow-900"
                                title="Stop"
                              >
                                <Square className="h-4 w-4" />
                              </button>
                            )}
                            <button 
                              onClick={() => handleContainerAction(container.id, 'restart')}
                              className="text-blue-600 hover:text-blue-900"
                              title="Restart"
                            >
                              <RotateCcw className="h-4 w-4" />
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
          ) : (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Repository
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Tag
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Size
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Created
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {images.length === 0 ? (
                    <tr>
                      <td colSpan={5} className="px-6 py-12 text-center text-gray-500">
                        No images found. Pull your first image to get started.
                      </td>
                    </tr>
                  ) : (
                    images.map((image) => (
                      <tr key={image.id} className="hover:bg-gray-50">
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="flex items-center">
                            <Box className="h-5 w-5 text-gray-400 mr-3" />
                            <div>
                              <div className="text-sm font-medium text-gray-900">
                                {image.repository}
                              </div>
                              <div className="text-sm text-gray-500">
                                {image.id.substring(0, 12)}
                              </div>
                            </div>
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {image.tag}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {image.size}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {new Date(image.created).toLocaleDateString()}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                          <div className="flex space-x-2">
                            <button className="text-blue-600 hover:text-blue-900" title="View">
                              <Eye className="h-4 w-4" />
                            </button>
                            <button className="text-green-600 hover:text-green-900" title="Pull">
                              <Download className="h-4 w-4" />
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
          )}
        </div>
      </div>
    </div>
  )
}
