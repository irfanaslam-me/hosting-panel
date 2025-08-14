'use client'

import { useState, useEffect } from 'react'
import { Server, Cpu, HardDrive, Activity, Thermometer, Zap, Wifi, Database } from 'lucide-react'

interface SystemStatus {
  cpu: {
    usage_percent: number
    cores: number
    temperature: number
  }
  memory: {
    total: string
    used: string
    available: string
    usage_percent: number
  }
  disk: {
    total: string
    used: string
    available: string
    usage_percent: number
  }
  network: {
    bytes_sent: string
    bytes_recv: string
    packets_sent: number
    packets_recv: number
  }
  system: {
    uptime: string
    load_average: number[]
    os: string
    kernel: string
  }
  services: {
    name: string
    status: 'running' | 'stopped' | 'error'
    uptime: string
  }[]
}

export default function SystemPage() {
  const [systemStatus, setSystemStatus] = useState<SystemStatus | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchSystemStatus()
    const interval = setInterval(fetchSystemStatus, 5000) // Refresh every 5 seconds
    return () => clearInterval(interval)
  }, [])

  const fetchSystemStatus = async () => {
    try {
      const response = await fetch('/api/v1/system/status')
      if (!response.ok) {
        throw new Error('Failed to fetch system status')
      }
      const data = await response.json()
      setSystemStatus(data)
      setLoading(false)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch system status')
      setLoading(false)
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'running':
        return 'bg-green-100 text-green-800'
      case 'stopped':
        return 'bg-gray-100 text-gray-800'
      case 'error':
        return 'bg-red-100 text-red-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const getUsageColor = (usage: number) => {
    if (usage < 50) return 'text-green-600'
    if (usage < 80) return 'text-yellow-600'
    return 'text-red-600'
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
          onClick={fetchSystemStatus}
          className="btn btn-primary"
        >
          Retry
        </button>
      </div>
    )
  }

  if (!systemStatus) {
    return (
      <div className="text-center py-12">
        <div className="text-gray-600 text-lg">No system data available</div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">System Status</h1>
          <p className="text-gray-600 mt-2">Real-time server monitoring and metrics</p>
        </div>
        <div className="flex items-center space-x-2">
          <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
          <span className="text-sm text-gray-600">Live</span>
        </div>
      </div>

      {/* System Overview */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="card p-6">
          <div className="flex items-center">
            <div className="p-3 bg-blue-500 rounded-lg">
              <Cpu className="h-6 w-6 text-white" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">CPU Usage</p>
              <p className={`text-2xl font-bold ${getUsageColor(systemStatus.cpu.usage_percent)}`}>
                {systemStatus.cpu.usage_percent.toFixed(1)}%
              </p>
              <p className="text-sm text-gray-500">{systemStatus.cpu.cores} cores</p>
            </div>
          </div>
        </div>

        <div className="card p-6">
          <div className="flex items-center">
            <div className="p-3 bg-green-500 rounded-lg">
              <Activity className="h-6 w-6 text-white" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Memory Usage</p>
              <p className={`text-2xl font-bold ${getUsageColor(systemStatus.memory.usage_percent)}`}>
                {systemStatus.memory.usage_percent.toFixed(1)}%
              </p>
              <p className="text-sm text-gray-500">{systemStatus.memory.used} / {systemStatus.memory.total}</p>
            </div>
          </div>
        </div>

        <div className="card p-6">
          <div className="flex items-center">
            <div className="p-3 bg-purple-500 rounded-lg">
              <HardDrive className="h-6 w-6 text-white" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Disk Usage</p>
              <p className={`text-2xl font-bold ${getUsageColor(systemStatus.disk.usage_percent)}`}>
                {systemStatus.disk.usage_percent.toFixed(1)}%
              </p>
              <p className="text-sm text-gray-500">{systemStatus.disk.used} / {systemStatus.disk.total}</p>
            </div>
          </div>
        </div>

        <div className="card p-6">
          <div className="flex items-center">
            <div className="p-3 bg-orange-500 rounded-lg">
              <Thermometer className="h-6 w-6 text-white" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Temperature</p>
              <p className="text-2xl font-bold text-gray-900">
                {systemStatus.cpu.temperature}°C
              </p>
              <p className="text-sm text-gray-500">CPU</p>
            </div>
          </div>
        </div>
      </div>

      {/* Detailed Metrics */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* System Information */}
        <div className="card">
          <div className="p-6 border-b border-gray-200">
            <h3 className="text-lg font-semibold text-gray-900">System Information</h3>
          </div>
          <div className="p-6 space-y-4">
            <div className="flex justify-between">
              <span className="text-gray-600">Operating System</span>
              <span className="font-medium">{systemStatus.system.os}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Kernel</span>
              <span className="font-medium">{systemStatus.system.kernel}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Uptime</span>
              <span className="font-medium">{systemStatus.system.uptime}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Load Average</span>
              <span className="font-medium">
                {systemStatus.system.load_average.map((load, i) => (
                  <span key={i} className="mr-2">{load.toFixed(2)}</span>
                ))}
              </span>
            </div>
          </div>
        </div>

        {/* Network Statistics */}
        <div className="card">
          <div className="p-6 border-b border-gray-200">
            <h3 className="text-lg font-semibold text-gray-900">Network Statistics</h3>
          </div>
          <div className="p-6 space-y-4">
            <div className="flex justify-between">
              <span className="text-gray-600">Bytes Sent</span>
              <span className="font-medium">{systemStatus.network.bytes_sent}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Bytes Received</span>
              <span className="font-medium">{systemStatus.network.bytes_recv}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Packets Sent</span>
              <span className="font-medium">{systemStatus.network.packets_sent.toLocaleString()}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Packets Received</span>
              <span className="font-medium">{systemStatus.network.packets_recv.toLocaleString()}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Services Status */}
      <div className="card">
        <div className="p-6 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900">Services Status</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Service
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Uptime
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {systemStatus.services.map((service) => (
                <tr key={service.name} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <Server className="h-5 w-5 text-gray-400 mr-3" />
                      <div className="text-sm font-medium text-gray-900">
                        {service.name}
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(service.status)}`}>
                      {service.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {service.uptime}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Performance Charts Placeholder */}
      <div className="card">
        <div className="p-6 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900">Performance Charts</h3>
          <p className="text-sm text-gray-600 mt-1">Real-time performance monitoring</p>
        </div>
        <div className="p-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="w-24 h-24 mx-auto mb-4 rounded-full border-8 border-gray-200 flex items-center justify-center">
                <div className="text-2xl font-bold text-primary-600">
                  {systemStatus.cpu.usage_percent.toFixed(0)}%
                </div>
              </div>
              <p className="text-sm font-medium text-gray-900">CPU</p>
            </div>
            <div className="text-center">
              <div className="w-24 h-24 mx-auto mb-4 rounded-full border-8 border-gray-200 flex items-center justify-center">
                <div className="text-2xl font-bold text-primary-600">
                  {systemStatus.memory.usage_percent.toFixed(0)}%
                </div>
              </div>
              <p className="text-sm font-medium text-gray-900">Memory</p>
            </div>
            <div className="text-center">
              <div className="w-24 h-24 mx-auto mb-4 rounded-full border-8 border-gray-200 flex items-center justify-center">
                <div className="text-2xl font-bold text-primary-600">
                  {systemStatus.disk.usage_percent.toFixed(0)}%
                </div>
              </div>
              <p className="text-sm font-medium text-gray-900">Disk</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
