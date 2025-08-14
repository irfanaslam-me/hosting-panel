'use client'

import { useState, useEffect } from 'react'
import { 
  Globe, 
  Database, 
  Server, 
  Users, 
  Activity, 
  HardDrive,
  TrendingUp,
  AlertTriangle
} from 'lucide-react'

interface SystemStats {
  websites: number
  databases: number
  containers: number
  users: number
  cpuUsage: number
  memoryUsage: number
  diskUsage: number
  uptime: string
}

export default function Dashboard() {
  const [stats, setStats] = useState<SystemStats>({
    websites: 0,
    databases: 0,
    containers: 0,
    users: 0,
    cpuUsage: 0,
    memoryUsage: 0,
    diskUsage: 0,
    uptime: '0d 0h 0m'
  })

  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Simulate API call to get system stats
    const fetchStats = async () => {
      try {
        // In a real app, this would be an API call
        // const response = await fetch('/api/dashboard/stats')
        // const data = await response.json()
        
        // Simulated data for now
        setTimeout(() => {
          setStats({
            websites: 12,
            databases: 8,
            containers: 15,
            users: 5,
            cpuUsage: 23,
            memoryUsage: 67,
            diskUsage: 45,
            uptime: '15d 8h 32m'
          })
          setLoading(false)
        }, 1000)
      } catch (error) {
        console.error('Failed to fetch stats:', error)
        setLoading(false)
      }
    }

    fetchStats()
  }, [])

  const StatCard = ({ title, value, icon: Icon, color, change }: {
    title: string
    value: string | number
    icon: any
    color: string
    change?: string
  }) => (
    <div className="card p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-2xl font-bold text-gray-900">{value}</p>
          {change && (
            <p className="text-sm text-green-600 flex items-center mt-1">
              <TrendingUp className="h-4 w-4 mr-1" />
              {change}
            </p>
          )}
        </div>
        <div className={`p-3 rounded-lg ${color}`}>
          <Icon className="h-6 w-6 text-white" />
        </div>
      </div>
    </div>
  )

  const ProgressCard = ({ title, value, max, color }: {
    title: string
    value: number
    max: number
    color: string
  }) => (
    <div className="card p-6">
      <div className="flex items-center justify-between mb-2">
        <span className="text-sm font-medium text-gray-600">{title}</span>
        <span className="text-sm font-medium text-gray-900">{value}%</span>
      </div>
      <div className="w-full bg-gray-200 rounded-full h-2">
        <div 
          className={`h-2 rounded-full ${color}`}
          style={{ width: `${(value / max) * 100}%` }}
        ></div>
      </div>
    </div>
  )

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600 mt-2">Welcome to your hosting panel overview</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Active Websites"
          value={stats.websites}
          icon={Globe}
          color="bg-blue-500"
          change="+2 this week"
        />
        <StatCard
          title="Databases"
          value={stats.databases}
          icon={Database}
          color="bg-green-500"
          change="+1 this week"
        />
        <StatCard
          title="Docker Containers"
          value={stats.containers}
          icon={Server}
          color="bg-purple-500"
        />
        <StatCard
          title="Users"
          value={stats.users}
          icon={Users}
          color="bg-orange-500"
        />
      </div>

      {/* System Resources */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">System Resources</h3>
          <div className="space-y-4">
            <ProgressCard
              title="CPU Usage"
              value={stats.cpuUsage}
              max={100}
              color="bg-blue-500"
            />
            <ProgressCard
              title="Memory Usage"
              value={stats.memoryUsage}
              max={100}
              color="bg-green-500"
            />
            <ProgressCard
              title="Disk Usage"
              value={stats.diskUsage}
              max={100}
              color="bg-orange-500"
            />
          </div>
        </div>

        <div className="card p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">System Status</h3>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">System Uptime</span>
              <span className="text-sm font-medium text-gray-900">{stats.uptime}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Status</span>
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                <Activity className="h-3 w-3 mr-1" />
                Healthy
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Last Backup</span>
              <span className="text-sm font-medium text-gray-900">2 hours ago</span>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="card p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Activity</h3>
        <div className="space-y-3">
          <div className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
            <div className="h-2 w-2 bg-green-500 rounded-full"></div>
            <span className="text-sm text-gray-600">Website "example.com" deployed successfully</span>
            <span className="text-xs text-gray-400 ml-auto">2 min ago</span>
          </div>
          <div className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
            <div className="h-2 w-2 bg-blue-500 rounded-full"></div>
            <span className="text-sm text-gray-600">Database backup completed</span>
            <span className="text-xs text-gray-400 ml-auto">15 min ago</span>
          </div>
          <div className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
            <div className="h-2 w-2 bg-yellow-500 rounded-full"></div>
            <span className="text-sm text-gray-600">SSL certificate expires in 30 days</span>
            <span className="text-xs text-gray-400 ml-auto">1 hour ago</span>
          </div>
        </div>
      </div>
    </div>
  )
}
