'use client'

import { useState, useEffect } from 'react'
import { 
  BarChart3, 
  Users, 
  Globe, 
  Database, 
  Box, 
  Server, 
  Activity, 
  TrendingUp,
  AlertTriangle,
  CheckCircle,
  Clock
} from 'lucide-react'
import { api, API_ENDPOINTS } from '@/lib/api'

interface DashboardStats {
  websites: {
    total: number
    active: number
    inactive: number
    ssl_issues: number
  }
  databases: {
    total: number
    running: number
    stopped: number
  }
  docker: {
    containers: number
    running: number
    images: number
  }
  system: {
    cpu_usage: number
    memory_usage: number
    disk_usage: number
    uptime: string
  }
  users: {
    total: number
    active: number
    online: number
  }
  recent_activity: {
    id: string
    type: 'website' | 'database' | 'docker' | 'user' | 'system'
    action: string
    timestamp: string
    status: 'success' | 'warning' | 'error'
  }[]
}

export default function Dashboard() {
  const [stats, setStats] = useState<DashboardStats | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchDashboardStats()
    const interval = setInterval(fetchDashboardStats, 30000) // Refresh every 30 seconds
    return () => clearInterval(interval)
  }, [])

  const fetchDashboardStats = async () => {
    try {
      const data = await api.get<DashboardStats>(API_ENDPOINTS.dashboard.stats)
      setStats(data)
      setLoading(false)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch dashboard stats')
      setLoading(false)
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'success':
        return <CheckCircle className="h-4 w-4 text-green-500" />
      case 'warning':
        return <AlertTriangle className="h-4 w-4 text-yellow-500" />
      case 'error':
        return <AlertTriangle className="h-4 w-4 text-red-500" />
      default:
        return <Clock className="h-4 w-4 text-gray-500" />
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'success':
        return 'text-green-600'
      case 'warning':
        return 'text-yellow-600'
      case 'error':
        return 'text-red-600'
      default:
        return 'text-gray-600'
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
          onClick={fetchDashboardStats}
          className="btn btn-primary"
        >
          Retry
        </button>
      </div>
    )
  }

  if (!stats) {
    return (
      <div className="text-center py-12">
        <div className="text-gray-600 text-lg">No dashboard data available</div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-600 mt-2">Overview of your hosting panel</p>
        </div>
        <div className="flex items-center space-x-2">
          <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
          <span className="text-sm text-gray-600">Live</span>
        </div>
      </div>

      {/* Main Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {/* Websites */}
        <div className="card p-6">
          <div className="flex items-center">
            <div className="p-3 bg-blue-500 rounded-lg">
              <Globe className="h-6 w-6 text-white" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Websites</p>
              <p className="text-2xl font-bold text-gray-900">{stats.websites.total}</p>
              <p className="text-sm text-gray-500">
                {stats.websites.active} active, {stats.websites.ssl_issues} SSL issues
              </p>
            </div>
          </div>
        </div>

        {/* Databases */}
        <div className="card p-6">
          <div className="flex items-center">
            <div className="p-3 bg-green-500 rounded-lg">
              <Database className="h-6 w-6 text-white" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Databases</p>
              <p className="text-2xl font-bold text-gray-900">{stats.databases.total}</p>
              <p className="text-sm text-gray-500">
                {stats.databases.running} running, {stats.databases.stopped} stopped
              </p>
            </div>
          </div>
        </div>

        {/* Docker */}
        <div className="card p-6">
          <div className="flex items-center">
            <div className="p-3 bg-purple-500 rounded-lg">
              <Box className="h-6 w-6 text-white" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Docker</p>
              <p className="text-2xl font-bold text-gray-900">{stats.docker.containers}</p>
              <p className="text-sm text-gray-500">
                {stats.docker.running} running, {stats.docker.images} images
              </p>
            </div>
          </div>
        </div>

        {/* Users */}
        <div className="card p-6">
          <div className="flex items-center">
            <div className="p-3 bg-orange-500 rounded-lg">
              <Users className="h-6 w-6 text-white" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Users</p>
              <p className="text-2xl font-bold text-gray-900">{stats.users.total}</p>
              <p className="text-sm text-gray-500">
                {stats.users.active} active, {stats.users.online} online
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* System Performance */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* System Resources */}
        <div className="card">
          <div className="p-6 border-b border-gray-200">
            <h3 className="text-lg font-semibold text-gray-900">System Resources</h3>
          </div>
          <div className="p-6 space-y-4">
            <div>
              <div className="flex justify-between text-sm mb-2">
                <span className="text-gray-600">CPU Usage</span>
                <span className={`font-medium ${getUsageColor(stats.system.cpu_usage)}`}>
                  {stats.system.cpu_usage.toFixed(1)}%
                </span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div 
                  className={`h-2 rounded-full ${getUsageColor(stats.system.cpu_usage).replace('text-', 'bg-')}`}
                  style={{ width: `${stats.system.cpu_usage}%` }}
                ></div>
              </div>
            </div>
            
            <div>
              <div className="flex justify-between text-sm mb-2">
                <span className="text-gray-600">Memory Usage</span>
                <span className={`font-medium ${getUsageColor(stats.system.memory_usage)}`}>
                  {stats.system.memory_usage.toFixed(1)}%
                </span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div 
                  className={`h-2 rounded-full ${getUsageColor(stats.system.memory_usage).replace('text-', 'bg-')}`}
                  style={{ width: `${stats.system.memory_usage}%` }}
                ></div>
              </div>
            </div>
            
            <div>
              <div className="flex justify-between text-sm mb-2">
                <span className="text-gray-600">Disk Usage</span>
                <span className={`font-medium ${getUsageColor(stats.system.disk_usage)}`}>
                  {stats.system.disk_usage.toFixed(1)}%
                </span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div 
                  className={`h-2 rounded-full ${getUsageColor(stats.system.disk_usage).replace('text-', 'bg-')}`}
                  style={{ width: `${stats.system.disk_usage}%` }}
                ></div>
              </div>
            </div>

            <div className="pt-4 border-t border-gray-200">
              <div className="flex items-center text-sm text-gray-600">
                <Server className="h-4 w-4 mr-2" />
                Uptime: {stats.system.uptime}
              </div>
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="card">
          <div className="p-6 border-b border-gray-200">
            <h3 className="text-lg font-semibold text-gray-900">Quick Actions</h3>
          </div>
          <div className="p-6 space-y-3">
            <button className="w-full btn btn-primary">
              <Globe className="h-4 w-4 mr-2" />
              Add Website
            </button>
            <button className="w-full btn btn-secondary">
              <Database className="h-4 w-4 mr-2" />
              Create Database
            </button>
            <button className="w-full btn btn-secondary">
              <Box className="h-4 w-4 mr-2" />
              New Docker Container
            </button>
            <button className="w-full btn btn-secondary">
              <Users className="h-4 w-4 mr-2" />
              Add User
            </button>
          </div>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="card">
        <div className="p-6 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900">Recent Activity</h3>
        </div>
        <div className="p-6">
          {stats.recent_activity.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              No recent activity
            </div>
          ) : (
            <div className="space-y-4">
              {stats.recent_activity.map((activity) => (
                <div key={activity.id} className="flex items-center space-x-4 p-4 bg-gray-50 rounded-lg">
                  <div className="flex-shrink-0">
                    {getStatusIcon(activity.status)}
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className={`text-sm font-medium ${getStatusColor(activity.status)}`}>
                      {activity.action}
                    </p>
                    <p className="text-sm text-gray-500">
                      {activity.type} • {new Date(activity.timestamp).toLocaleString()}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* System Health */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card p-6 text-center">
          <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-green-100 flex items-center justify-center">
            <CheckCircle className="h-8 w-8 text-green-600" />
          </div>
          <h4 className="text-lg font-medium text-gray-900">System Health</h4>
          <p className="text-sm text-gray-600 mb-2">All services running normally</p>
          <div className="text-2xl font-bold text-green-600">100%</div>
        </div>

        <div className="card p-6 text-center">
          <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-blue-100 flex items-center justify-center">
            <Activity className="h-8 w-8 text-blue-600" />
          </div>
          <h4 className="text-lg font-medium text-gray-900">Performance</h4>
          <p className="text-sm text-gray-600 mb-2">Optimal resource usage</p>
          <div className="text-2xl font-bold text-blue-600">95%</div>
        </div>

        <div className="card p-6 text-center">
          <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-purple-100 flex items-center justify-center">
            <TrendingUp className="h-8 w-8 text-purple-600" />
          </div>
          <h4 className="text-lg font-medium text-gray-900">Uptime</h4>
          <p className="text-sm text-gray-600 mb-2">System reliability</p>
          <div className="text-2xl font-bold text-purple-600">99.9%</div>
        </div>
      </div>
    </div>
  )
}
