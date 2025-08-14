'use client'

import { useState } from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { 
  Home, 
  Globe, 
  Database, 
  Server, 
  Settings, 
  Users, 
  Shield, 
  BarChart3,
  FileText,
  Mail,
  Box,
  HardDrive
} from 'lucide-react'

interface SidebarProps {
  isOpen: boolean
  onClose: () => void
}

const menuItems = [
  { name: 'Dashboard', href: '/', icon: Home },
  { name: 'Websites', href: '/websites', icon: Globe },
  { name: 'Databases', href: '/databases', icon: Database },
  { name: 'Docker', href: '/docker', icon: Box },
  { name: 'Files', href: '/files', icon: FileText },
  { name: 'System', href: '/system', icon: Server },
  { name: 'Users', href: '/users', icon: Users },
  { name: 'Security', href: '/security', icon: Shield },
  { name: 'Monitoring', href: '/monitoring', icon: BarChart3 },
  { name: 'Backups', href: '/backups', icon: HardDrive },
  { name: 'Logs', href: '/logs', icon: FileText },
  { name: 'Email', href: '/email', icon: Mail },
  { name: 'Settings', href: '/settings', icon: Settings },
]

export default function Sidebar({ isOpen, onClose }: SidebarProps) {
  const pathname = usePathname()

  return (
    <>
      {/* Overlay */}
      {isOpen && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-50 z-30 lg:hidden"
          onClick={onClose}
        />
      )}

      {/* Sidebar */}
      <aside className={`
        fixed left-0 top-0 z-40 h-screen w-64 transform bg-white border-r border-gray-200 transition-transform duration-300 ease-in-out lg:translate-x-0
        ${isOpen ? 'translate-x-0' : '-translate-x-full'}
      `}>
        <div className="flex flex-col h-full">
          {/* Logo */}
          <div className="flex items-center justify-center h-16 border-b border-gray-200">
            <div className="flex items-center space-x-2">
              <div className="h-8 w-8 bg-primary-600 rounded-lg flex items-center justify-center">
                <Server className="h-5 w-5 text-white" />
              </div>
              <span className="text-xl font-bold text-gray-900">Hosting Panel</span>
            </div>
          </div>

          {/* Navigation */}
          <nav className="flex-1 px-4 py-6 space-y-2">
            {menuItems.map((item) => {
              const isActive = pathname === item.href
              const Icon = item.icon
              
              return (
                <Link
                  key={item.name}
                  href={item.href}
                  className={`
                    flex items-center space-x-3 px-3 py-2 rounded-md text-sm font-medium transition-colors
                    ${isActive 
                      ? 'bg-primary-100 text-primary-700 border-r-2 border-primary-600' 
                      : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                    }
                  `}
                  onClick={() => {
                    if (window.innerWidth < 1024) {
                      onClose()
                    }
                  }}
                >
                  <Icon className={`h-5 w-5 ${isActive ? 'text-primary-600' : 'text-gray-400'}`} />
                  <span>{item.name}</span>
                </Link>
              )
            })}
          </nav>

          {/* Footer */}
          <div className="p-4 border-t border-gray-200">
            <div className="text-xs text-gray-500 text-center">
              <p>Modern Hosting Panel</p>
              <p>v1.0.0</p>
            </div>
          </div>
        </div>
      </aside>
    </>
  )
}
