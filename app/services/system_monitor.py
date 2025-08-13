"""
System monitoring service
"""

import psutil
import subprocess
import asyncio
import os
from datetime import datetime
from typing import Dict, Any, List
from app.core.config import settings


class SystemMonitor:
    """System monitoring service"""
    
    _instance = None
    _monitoring_task = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SystemMonitor, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.monitoring_data = {}
    
    @classmethod
    def start(cls):
        """Start system monitoring"""
        if cls._monitoring_task is None:
            cls._monitoring_task = asyncio.create_task(cls._monitor_loop())
    
    @classmethod
    def stop(cls):
        """Stop system monitoring"""
        if cls._monitoring_task:
            cls._monitoring_task.cancel()
            cls._monitoring_task = None
    
    @classmethod
    async def _monitor_loop(cls):
        """Monitoring loop"""
        monitor = cls()
        while True:
            try:
                # Update monitoring data
                monitor.monitoring_data = await monitor._collect_system_data()
                await asyncio.sleep(settings.MONITORING_INTERVAL)
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Monitoring error: {e}")
                await asyncio.sleep(60)  # Wait before retrying
    
    async def get_system_status(self) -> Dict[str, Any]:
        """Get overall system status"""
        return {
            "status": "healthy",
            "uptime": self._get_uptime(),
            "load_average": self._get_load_average(),
            "memory_usage": self._get_memory_usage(),
            "disk_usage": self._get_disk_usage(),
            "cpu_usage": self._get_cpu_usage(),
            "network_status": self._get_network_status(),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def get_resource_usage(self) -> Dict[str, Any]:
        """Get detailed resource usage"""
        return {
            "cpu": {
                "usage_percent": psutil.cpu_percent(interval=1),
                "count": psutil.cpu_count(),
                "frequency": psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None
            },
            "memory": {
                "total": psutil.virtual_memory().total,
                "available": psutil.virtual_memory().available,
                "used": psutil.virtual_memory().used,
                "percent": psutil.virtual_memory().percent
            },
            "disk": {
                "partitions": self._get_disk_partitions(),
                "io_counters": psutil.disk_io_counters()._asdict() if psutil.disk_io_counters() else None
            },
            "network": {
                "interfaces": self._get_network_interfaces(),
                "connections": len(psutil.net_connections())
            }
        }
    
    async def get_services_status(self) -> Dict[str, Any]:
        """Get status of system services"""
        services = [
            settings.WEB_SERVER,  # nginx or apache
            "mysql",  # or mariadb
            "php-fpm",
            "docker",
            "redis"
        ]
        
        status = {}
        for service in services:
            status[service] = await self._check_service_status(service)
        
        return status
    
    async def restart_service(self, service_name: str) -> Dict[str, Any]:
        """Restart a system service"""
        try:
            result = subprocess.run(
                ["systemctl", "restart", service_name],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return {"success": True, "message": f"Service {service_name} restarted successfully"}
            else:
                return {"success": False, "error": result.stderr}
        
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Service restart timed out"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def get_logs(self, service: str = None, lines: int = 100) -> Dict[str, Any]:
        """Get system logs"""
        try:
            if service:
                log_file = f"/var/log/{service}/error.log"
                if not os.path.exists(log_file):
                    log_file = f"/var/log/{service}.log"
            else:
                log_file = "/var/log/syslog"
            
            if not os.path.exists(log_file):
                return {"error": f"Log file not found: {log_file}"}
            
            result = subprocess.run(
                ["tail", "-n", str(lines), log_file],
                capture_output=True,
                text=True
            )
            
            return {
                "service": service or "system",
                "log_file": log_file,
                "lines": lines,
                "content": result.stdout
            }
        
        except Exception as e:
            return {"error": str(e)}
    
    async def create_system_backup(self) -> Dict[str, Any]:
        """Create a full system backup"""
        try:
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"system_backup_{timestamp}.tar.gz"
            backup_path = os.path.join(settings.BACKUP_PATH, backup_filename)
            
            # Create backup of important directories
            subprocess.run([
                "tar", "-czf", backup_path,
                "--exclude=/proc", "--exclude=/sys", "--exclude=/tmp",
                "--exclude=/var/tmp", "--exclude=/var/cache",
                "/etc", "/var/www", "/var/log", "/home"
            ], check=True)
            
            return {
                "success": True,
                "backup_path": backup_path,
                "size": os.path.getsize(backup_path)
            }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def check_updates(self) -> Dict[str, Any]:
        """Check for system updates"""
        try:
            # Update package list
            subprocess.run(["apt-get", "update"], check=True)
            
            # Check for available updates
            result = subprocess.run([
                "apt-get", "-s", "upgrade"
            ], capture_output=True, text=True, check=True)
            
            # Parse output to count updates
            lines = result.stdout.split('\n')
            upgrade_count = 0
            for line in lines:
                if line.startswith('The following packages will be upgraded:'):
                    # Count the number of packages
                    upgrade_count = len([l for l in lines if l.strip().startswith(' ') and l.strip().endswith(')')])
                    break
            
            return {
                "updates_available": upgrade_count > 0,
                "upgrade_count": upgrade_count,
                "last_check": datetime.utcnow().isoformat()
            }
        
        except Exception as e:
            return {"error": str(e)}
    
    async def install_updates(self) -> Dict[str, Any]:
        """Install system updates"""
        try:
            result = subprocess.run([
                "apt-get", "upgrade", "-y"
            ], capture_output=True, text=True, timeout=1800)  # 30 minutes timeout
            
            if result.returncode == 0:
                return {"success": True, "message": "Updates installed successfully"}
            else:
                return {"success": False, "error": result.stderr}
        
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Update installation timed out"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _collect_system_data(self) -> Dict[str, Any]:
        """Collect system monitoring data"""
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "cpu_usage": psutil.cpu_percent(),
            "memory_usage": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage('/').percent,
            "load_average": psutil.getloadavg()
        }
    
    def _get_uptime(self) -> float:
        """Get system uptime in seconds"""
        return time.time() - psutil.boot_time()
    
    def _get_load_average(self) -> List[float]:
        """Get system load average"""
        return list(psutil.getloadavg())
    
    def _get_memory_usage(self) -> Dict[str, Any]:
        """Get memory usage information"""
        mem = psutil.virtual_memory()
        return {
            "total": mem.total,
            "used": mem.used,
            "available": mem.available,
            "percent": mem.percent
        }
    
    def _get_disk_usage(self) -> Dict[str, Any]:
        """Get disk usage information"""
        disk = psutil.disk_usage('/')
        return {
            "total": disk.total,
            "used": disk.used,
            "free": disk.free,
            "percent": disk.percent
        }
    
    def _get_cpu_usage(self) -> float:
        """Get CPU usage percentage"""
        return psutil.cpu_percent(interval=1)
    
    def _get_network_status(self) -> Dict[str, Any]:
        """Get network status"""
        net_io = psutil.net_io_counters()
        return {
            "bytes_sent": net_io.bytes_sent,
            "bytes_recv": net_io.bytes_recv,
            "packets_sent": net_io.packets_sent,
            "packets_recv": net_io.packets_recv
        }
    
    def _get_disk_partitions(self) -> List[Dict[str, Any]]:
        """Get disk partition information"""
        partitions = []
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                partitions.append({
                    "device": partition.device,
                    "mountpoint": partition.mountpoint,
                    "fstype": partition.fstype,
                    "total": usage.total,
                    "used": usage.used,
                    "free": usage.free,
                    "percent": usage.percent
                })
            except PermissionError:
                continue
        return partitions
    
    def _get_network_interfaces(self) -> Dict[str, Any]:
        """Get network interface information"""
        interfaces = {}
        for interface, addresses in psutil.net_if_addrs().items():
            interfaces[interface] = {
                "addresses": [addr.address for addr in addresses if addr.family == psutil.AF_INET],
                "mac": next((addr.address for addr in addresses if addr.family == psutil.AF_LINK), None)
            }
        return interfaces
    
    async def _check_service_status(self, service_name: str) -> Dict[str, Any]:
        """Check status of a system service"""
        try:
            result = subprocess.run([
                "systemctl", "is-active", service_name
            ], capture_output=True, text=True, timeout=10)
            
            is_active = result.returncode == 0
            status = "active" if is_active else "inactive"
            
            # Get additional service info
            try:
                info_result = subprocess.run([
                    "systemctl", "show", service_name, "--property=LoadState,ActiveState,SubState"
                ], capture_output=True, text=True, timeout=10)
                
                service_info = {}
                for line in info_result.stdout.split('\n'):
                    if '=' in line:
                        key, value = line.split('=', 1)
                        service_info[key] = value
                
                return {
                    "status": status,
                    "active": is_active,
                    "load_state": service_info.get("LoadState", "unknown"),
                    "active_state": service_info.get("ActiveState", "unknown"),
                    "sub_state": service_info.get("SubState", "unknown")
                }
            
            except Exception:
                return {
                    "status": status,
                    "active": is_active
                }
        
        except subprocess.TimeoutExpired:
            return {"status": "timeout", "active": False}
        except Exception:
            return {"status": "error", "active": False}


# Import time module for uptime calculation
import time 