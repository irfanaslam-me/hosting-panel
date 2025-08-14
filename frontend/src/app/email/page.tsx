'use client'

import { useState, useEffect } from 'react'
import { Mail, Plus, Edit, Trash2, Eye, Send, RefreshCw, CheckCircle, AlertTriangle } from 'lucide-react'

interface EmailAccount {
  id: string
  email: string
  domain: string
  status: 'active' | 'inactive' | 'suspended'
  quota: string
  used: string
  created_at: string
  last_login: string
}

interface EmailStats {
  total_accounts: number
  active_accounts: number
  total_quota: string
  used_quota: string
  emails_sent_today: number
  emails_received_today: number
}

export default function EmailPage() {
  const [accounts, setAccounts] = useState<EmailAccount[]>([])
  const [stats, setStats] = useState<EmailStats | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchEmailData()
  }, [])

  const fetchEmailData = async () => {
    try {
      setLoading(true)
      
      // Fetch email accounts
      const accountsResponse = await fetch('/api/v1/email/accounts')
      if (accountsResponse.ok) {
        const accountsData = await accountsResponse.json()
        setAccounts(accountsData.accounts || [])
      }
      
      // Fetch email stats
      const statsResponse = await fetch('/api/v1/email/stats')
      if (statsResponse.ok) {
        const statsData = await statsResponse.json()
        setStats(statsData)
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch email data')
    } finally {
      setLoading(false)
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'bg-green-100 text-green-800'
      case 'inactive':
        return 'bg-gray-100 text-gray-800'
      case 'suspended':
        return 'bg-red-100 text-red-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const getQuotaPercentage = (used: string, quota: string) => {
    const usedNum = parseFloat(used.replace(/[^\d.]/g, ''))
    const quotaNum = parseFloat(quota.replace(/[^\d.]/g, ''))
    if (quotaNum === 0) return 0
    return (usedNum / quotaNum) * 100
  }

  const getQuotaColor = (percentage: number) => {
    if (percentage < 50) return 'text-green-600'
    if (percentage < 80) return 'text-yellow-600'
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
          onClick={fetchEmailData}
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
          <h1 className="text-3xl font-bold text-gray-900">Email Management</h1>
          <p className="text-gray-600 mt-2">Manage email accounts and settings</p>
        </div>
        <button className="btn btn-primary">
          <Plus className="h-4 w-4 mr-2" />
          Add Email Account
        </button>
      </div>

      {/* Stats */}
      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="card p-6">
            <div className="flex items-center">
              <div className="p-3 bg-blue-500 rounded-lg">
                <Mail className="h-6 w-6 text-white" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Total Accounts</p>
                <p className="text-2xl font-bold text-gray-900">{stats.total_accounts}</p>
              </div>
            </div>
          </div>
          <div className="card p-6">
            <div className="flex items-center">
              <div className="p-3 bg-green-500 rounded-lg">
                <CheckCircle className="h-6 w-6 text-white" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Active Accounts</p>
                <p className="text-2xl font-bold text-gray-900">{stats.active_accounts}</p>
              </div>
            </div>
          </div>
          <div className="card p-6">
            <div className="flex items-center">
              <div className="p-3 bg-purple-500 rounded-lg">
                <Send className="h-6 w-6 text-white" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Sent Today</p>
                <p className="text-2xl font-bold text-gray-900">{stats.emails_sent_today}</p>
              </div>
            </div>
          </div>
          <div className="card p-6">
            <div className="flex items-center">
              <div className="p-3 bg-orange-500 rounded-lg">
                <Mail className="h-6 w-6 text-white" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Received Today</p>
                <p className="text-2xl font-bold text-gray-900">{stats.emails_received_today}</p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Quota Overview */}
      {stats && (
        <div className="card">
          <div className="p-6 border-b border-gray-200">
            <h3 className="text-lg font-semibold text-gray-900">Storage Quota Overview</h3>
          </div>
          <div className="p-6">
            <div className="space-y-4">
              <div>
                <div className="flex justify-between text-sm mb-2">
                  <span className="text-gray-600">Total Quota</span>
                  <span className="font-medium text-gray-900">{stats.total_quota}</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className="h-2 rounded-full bg-primary-500"
                    style={{ width: `${(parseFloat(stats.used_quota.replace(/[^\d.]/g, '')) / parseFloat(stats.total_quota.replace(/[^\d.]/g, ''))) * 100}%` }}
                  ></div>
                </div>
                <div className="flex justify-between text-sm mt-1">
                  <span className="text-gray-500">Used: {stats.used_quota}</span>
                  <span className="text-gray-500">Available: {stats.total_quota}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Email Accounts List */}
      <div className="card">
        <div className="p-6 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900">Email Accounts</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Email Address
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Domain
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Quota Usage
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
              {accounts.length === 0 ? (
                <tr>
                  <td colSpan={6} className="px-6 py-12 text-center text-gray-500">
                    No email accounts found. Create your first email account to get started.
                  </td>
                </tr>
              ) : (
                accounts.map((account) => {
                  const quotaPercentage = getQuotaPercentage(account.used, account.quota)
                  return (
                    <tr key={account.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex items-center">
                          <div className="h-10 w-10 rounded-full bg-gray-300 flex items-center justify-center">
                            <Mail className="h-5 w-5 text-gray-600" />
                          </div>
                          <div className="ml-4">
                            <div className="text-sm font-medium text-gray-900">
                              {account.email}
                            </div>
                            <div className="text-sm text-gray-500">
                              Last login: {account.last_login ? new Date(account.last_login).toLocaleDateString() : 'Never'}
                            </div>
                          </div>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {account.domain}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(account.status)}`}>
                          {account.status}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="space-y-2">
                          <div className="flex justify-between text-sm">
                            <span className="text-gray-600">Usage</span>
                            <span className={`font-medium ${getQuotaColor(quotaPercentage)}`}>
                              {quotaPercentage.toFixed(1)}%
                            </span>
                          </div>
                          <div className="w-full bg-gray-200 rounded-full h-2">
                            <div 
                              className={`h-2 rounded-full ${getQuotaColor(quotaPercentage).replace('text-', 'bg-')}`}
                              style={{ width: `${quotaPercentage}%` }}
                            ></div>
                          </div>
                          <div className="text-xs text-gray-500">
                            {account.used} / {account.quota}
                          </div>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {new Date(account.created_at).toLocaleDateString()}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                        <div className="flex space-x-2">
                          <button className="text-blue-600 hover:text-blue-900" title="View">
                            <Eye className="h-4 w-4" />
                          </button>
                          <button className="text-yellow-600 hover:text-yellow-900" title="Edit">
                            <Edit className="h-4 w-4" />
                          </button>
                          <button className="text-red-600 hover:text-red-900" title="Delete">
                            <Trash2 className="h-4 w-4" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  )
                })
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Email Configuration */}
      <div className="card">
        <div className="p-6 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900">Email Configuration</h3>
        </div>
        <div className="p-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h4 className="text-md font-medium text-gray-900 mb-4">SMTP Settings</h4>
              <div className="space-y-3">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">SMTP Server</label>
                  <input type="text" className="input w-full" placeholder="smtp.example.com" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Port</label>
                  <input type="number" className="input w-full" placeholder="587" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Security</label>
                  <select className="input w-full">
                    <option>TLS</option>
                    <option>SSL</option>
                    <option>None</option>
                  </select>
                </div>
              </div>
            </div>
            <div>
              <h4 className="text-md font-medium text-gray-900 mb-4">IMAP Settings</h4>
              <div className="space-y-3">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">IMAP Server</label>
                  <input type="text" className="input w-full" placeholder="imap.example.com" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Port</label>
                  <input type="number" className="input w-full" placeholder="993" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Security</label>
                  <select className="input w-full">
                    <option>SSL/TLS</option>
                    <option>STARTTLS</option>
                    <option>None</option>
                  </select>
                </div>
              </div>
            </div>
          </div>
          <div className="mt-6">
            <button className="btn btn-primary">
              <RefreshCw className="h-4 w-4 mr-2" />
              Test Connection
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
