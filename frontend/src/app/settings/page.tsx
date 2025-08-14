'use client'

import { useState, useEffect } from 'react'
import { Settings, Save, RefreshCw, Shield, Globe, Database, Server, Bell, Mail } from 'lucide-react'

interface SystemSettings {
  general: {
    site_name: string
    site_description: string
    admin_email: string
    timezone: string
    language: string
  }
  security: {
    session_timeout: number
    max_login_attempts: number
    require_2fa: boolean
    allowed_hosts: string[]
  }
  email: {
    smtp_host: string
    smtp_port: number
    smtp_username: string
    smtp_password: string
    from_email: string
    from_name: string
  }
  backup: {
    auto_backup: boolean
    backup_retention_days: number
    backup_time: string
    backup_path: string
  }
}

export default function SettingsPage() {
  const [settings, setSettings] = useState<SystemSettings | null>(null)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState<string | null>(null)

  useEffect(() => {
    fetchSettings()
  }, [])

  const fetchSettings = async () => {
    try {
      setLoading(true)
      const response = await fetch('/api/v1/settings')
      if (!response.ok) {
        throw new Error('Failed to fetch settings')
      }
      const data = await response.json()
      setSettings(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch settings')
    } finally {
      setLoading(false)
    }
  }

  const handleSave = async () => {
    if (!settings) return
    
    try {
      setSaving(true)
      setError(null)
      setSuccess(null)
      
      const response = await fetch('/api/v1/settings', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(settings),
      })
      
      if (!response.ok) {
        throw new Error('Failed to save settings')
      }
      
      setSuccess('Settings saved successfully!')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to save settings')
    } finally {
      setSaving(false)
    }
  }

  const handleInputChange = (section: keyof SystemSettings, field: string, value: any) => {
    if (!settings) return
    
    setSettings({
      ...settings,
      [section]: {
        ...settings[section],
        [field]: value,
      },
    })
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  if (!settings) {
    return (
      <div className="text-center py-12">
        <div className="text-gray-600 text-lg">No settings available</div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Settings</h1>
          <p className="text-gray-600 mt-2">Configure system settings and preferences</p>
        </div>
        <div className="flex space-x-3">
          <button 
            onClick={fetchSettings}
            className="btn btn-secondary"
            disabled={saving}
          >
            <RefreshCw className="h-4 w-4 mr-2" />
            Refresh
          </button>
          <button 
            onClick={handleSave}
            className="btn btn-primary"
            disabled={saving}
          >
            <Save className="h-4 w-4 mr-2" />
            {saving ? 'Saving...' : 'Save Changes'}
          </button>
        </div>
      </div>

      {/* Success/Error Messages */}
      {success && (
        <div className="bg-green-50 border border-green-200 rounded-md p-4">
          <div className="flex">
            <div className="flex-shrink-0">
              <div className="w-5 h-5 bg-green-400 rounded-full flex items-center justify-center">
                <div className="w-2 h-2 bg-white rounded-full"></div>
              </div>
            </div>
            <div className="ml-3">
              <p className="text-sm font-medium text-green-800">{success}</p>
            </div>
          </div>
        </div>
      )}

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-md p-4">
          <div className="flex">
            <div className="flex-shrink-0">
              <div className="w-5 h-5 bg-red-400 rounded-full flex items-center justify-center">
                <div className="w-2 h-2 bg-white rounded-full"></div>
              </div>
            </div>
            <div className="ml-3">
              <p className="text-sm font-medium text-red-800">{error}</p>
            </div>
          </div>
        </div>
      )}

      {/* General Settings */}
      <div className="card">
        <div className="p-6 border-b border-gray-200">
          <div className="flex items-center">
            <Globe className="h-5 w-5 text-gray-400 mr-3" />
            <h3 className="text-lg font-semibold text-gray-900">General Settings</h3>
          </div>
        </div>
        <div className="p-6 space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Site Name
              </label>
              <input
                type="text"
                value={settings.general.site_name}
                onChange={(e) => handleInputChange('general', 'site_name', e.target.value)}
                className="input w-full"
                placeholder="My Hosting Panel"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Admin Email
              </label>
              <input
                type="email"
                value={settings.general.admin_email}
                onChange={(e) => handleInputChange('general', 'admin_email', e.target.value)}
                className="input w-full"
                placeholder="admin@example.com"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Timezone
              </label>
              <select
                value={settings.general.timezone}
                onChange={(e) => handleInputChange('general', 'timezone', e.target.value)}
                className="input w-full"
              >
                <option value="UTC">UTC</option>
                <option value="America/New_York">America/New_York</option>
                <option value="Europe/London">Europe/London</option>
                <option value="Asia/Tokyo">Asia/Tokyo</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Language
              </label>
              <select
                value={settings.general.language}
                onChange={(e) => handleInputChange('general', 'language', e.target.value)}
                className="input w-full"
              >
                <option value="en">English</option>
                <option value="es">Spanish</option>
                <option value="fr">French</option>
                <option value="de">German</option>
              </select>
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Site Description
            </label>
            <textarea
              value={settings.general.site_description}
              onChange={(e) => handleInputChange('general', 'site_description', e.target.value)}
              className="input w-full"
              rows={3}
              placeholder="Description of your hosting panel"
            />
          </div>
        </div>
      </div>

      {/* Security Settings */}
      <div className="card">
        <div className="p-6 border-b border-gray-200">
          <div className="flex items-center">
            <Shield className="h-5 w-5 text-gray-400 mr-3" />
            <h3 className="text-lg font-semibold text-gray-900">Security Settings</h3>
          </div>
        </div>
        <div className="p-6 space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Session Timeout (minutes)
              </label>
              <input
                type="number"
                value={settings.security.session_timeout}
                onChange={(e) => handleInputChange('security', 'session_timeout', parseInt(e.target.value))}
                className="input w-full"
                min="5"
                max="1440"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Max Login Attempts
              </label>
              <input
                type="number"
                value={settings.security.max_login_attempts}
                onChange={(e) => handleInputChange('security', 'max_login_attempts', parseInt(e.target.value))}
                className="input w-full"
                min="3"
                max="10"
              />
            </div>
          </div>
          <div className="flex items-center">
            <input
              type="checkbox"
              id="require_2fa"
              checked={settings.security.require_2fa}
              onChange={(e) => handleInputChange('security', 'require_2fa', e.target.checked)}
              className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
            />
            <label htmlFor="require_2fa" className="ml-2 block text-sm text-gray-900">
              Require Two-Factor Authentication for Admin Users
            </label>
          </div>
        </div>
      </div>

      {/* Email Settings */}
      <div className="card">
        <div className="p-6 border-b border-gray-200">
          <div className="flex items-center">
            <Mail className="h-5 w-5 text-gray-400 mr-3" />
            <h3 className="text-lg font-semibold text-gray-900">Email Settings</h3>
          </div>
        </div>
        <div className="p-6 space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                SMTP Host
              </label>
              <input
                type="text"
                value={settings.email.smtp_host}
                onChange={(e) => handleInputChange('email', 'smtp_host', e.target.value)}
                className="input w-full"
                placeholder="smtp.gmail.com"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                SMTP Port
              </label>
              <input
                type="number"
                value={settings.email.smtp_port}
                onChange={(e) => handleInputChange('email', 'smtp_port', parseInt(e.target.value))}
                className="input w-full"
                placeholder="587"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                SMTP Username
              </label>
              <input
                type="text"
                value={settings.email.smtp_username}
                onChange={(e) => handleInputChange('email', 'smtp_username', e.target.value)}
                className="input w-full"
                placeholder="your-email@gmail.com"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                SMTP Password
              </label>
              <input
                type="password"
                value={settings.email.smtp_password}
                onChange={(e) => handleInputChange('email', 'smtp_password', e.target.value)}
                className="input w-full"
                placeholder="••••••••"
              />
            </div>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                From Email
              </label>
              <input
                type="email"
                value={settings.email.from_email}
                onChange={(e) => handleInputChange('email', 'from_email', e.target.value)}
                className="input w-full"
                placeholder="noreply@example.com"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                From Name
              </label>
              <input
                type="text"
                value={settings.email.from_name}
                onChange={(e) => handleInputChange('email', 'from_name', e.target.value)}
                className="input w-full"
                placeholder="Hosting Panel"
              />
            </div>
          </div>
        </div>
      </div>

      {/* Backup Settings */}
      <div className="card">
        <div className="p-6 border-b border-gray-200">
          <div className="flex items-center">
            <Database className="h-5 w-5 text-gray-400 mr-3" />
            <h3 className="text-lg font-semibold text-gray-900">Backup Settings</h3>
          </div>
        </div>
        <div className="p-6 space-y-4">
          <div className="flex items-center">
            <input
              type="checkbox"
              id="auto_backup"
              checked={settings.backup.auto_backup}
              onChange={(e) => handleInputChange('backup', 'auto_backup', e.target.checked)}
              className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
            />
            <label htmlFor="auto_backup" className="ml-2 block text-sm text-gray-900">
              Enable Automatic Backups
            </label>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Backup Retention (days)
              </label>
              <input
                type="number"
                value={settings.backup.backup_retention_days}
                onChange={(e) => handleInputChange('backup', 'backup_retention_days', parseInt(e.target.value))}
                className="input w-full"
                min="1"
                max="365"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Backup Time
              </label>
              <input
                type="time"
                value={settings.backup.backup_time}
                onChange={(e) => handleInputChange('backup', 'backup_time', e.target.value)}
                className="input w-full"
              />
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Backup Path
            </label>
            <input
              type="text"
              value={settings.backup.backup_path}
              onChange={(e) => handleInputChange('backup', 'backup_path', e.target.value)}
              className="input w-full"
              placeholder="/var/backups/hosting-panel"
            />
          </div>
        </div>
      </div>
    </div>
  )
}
