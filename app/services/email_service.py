"""
Email service for managing email accounts and server setup
"""

import subprocess
import os
from typing import Dict, Any
from sqlalchemy.orm import Session
from app.core.database import EmailAccount


class EmailService:
    """Service for managing email accounts and server setup"""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def create_email_account(self, email: str, password: str, domain: str, quota: int, owner_id: int) -> EmailAccount:
        """Create a new email account"""
        # Create email account using useradd and mailutils
        username = email.split('@')[0]
        
        # Create system user
        subprocess.run([
            "useradd", "-m", "-s", "/bin/bash", username
        ], check=True)
        
        # Set password
        subprocess.run([
            "echo", f"{username}:{password}", "|", "chpasswd"
        ], shell=True, check=True)
        
        # Create mail directory
        mail_dir = f"/home/{username}/Maildir"
        subprocess.run(["mkdir", "-p", mail_dir], check=True)
        subprocess.run(["chown", "-R", f"{username}:{username}", f"/home/{username}"], check=True)
        
        # Create email account record
        account = EmailAccount(
            email=email,
            password=password,
            domain=domain,
            quota=quota,
            owner_id=owner_id
        )
        
        self.db.add(account)
        self.db.commit()
        self.db.refresh(account)
        
        return account
    
    async def delete_email_account(self, account_id: int):
        """Delete an email account"""
        account = self.db.query(EmailAccount).filter(EmailAccount.id == account_id).first()
        if not account:
            raise ValueError("Email account not found")
        
        username = account.email.split('@')[0]
        
        # Delete system user
        subprocess.run([
            "userdel", "-r", username
        ], check=True)
        
        # Delete email account record
        self.db.delete(account)
        self.db.commit()
    
    async def setup_email_server(self) -> Dict[str, Any]:
        """Setup email server (Postfix + Dovecot)"""
        try:
            # Install required packages
            subprocess.run([
                "apt-get", "update"
            ], check=True)
            
            subprocess.run([
                "apt-get", "install", "-y", "postfix", "dovecot-core", "dovecot-imapd", "dovecot-pop3d"
            ], check=True)
            
            # Configure Postfix
            await self._configure_postfix()
            
            # Configure Dovecot
            await self._configure_dovecot()
            
            # Start and enable services
            subprocess.run(["systemctl", "enable", "postfix"], check=True)
            subprocess.run(["systemctl", "start", "postfix"], check=True)
            subprocess.run(["systemctl", "enable", "dovecot"], check=True)
            subprocess.run(["systemctl", "start", "dovecot"], check=True)
            
            return {"success": True, "message": "Email server setup completed"}
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def get_server_status(self) -> Dict[str, Any]:
        """Get email server status"""
        try:
            # Check Postfix status
            postfix_status = subprocess.run([
                "systemctl", "is-active", "postfix"
            ], capture_output=True, text=True)
            
            # Check Dovecot status
            dovecot_status = subprocess.run([
                "systemctl", "is-active", "dovecot"
            ], capture_output=True, text=True)
            
            return {
                "postfix": {
                    "status": "active" if postfix_status.returncode == 0 else "inactive",
                    "running": postfix_status.returncode == 0
                },
                "dovecot": {
                    "status": "active" if dovecot_status.returncode == 0 else "inactive",
                    "running": dovecot_status.returncode == 0
                }
            }
        
        except Exception as e:
            return {"error": str(e)}
    
    async def _configure_postfix(self):
        """Configure Postfix"""
        # Main configuration
        main_cf = """# Basic Postfix configuration
myhostname = mail.example.com
mydomain = example.com
myorigin = $mydomain
inet_interfaces = all
inet_protocols = ipv4
mydestination = $myhostname, localhost.$mydomain, localhost, $mydomain
mynetworks = 127.0.0.0/8, 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16
home_mailbox = Maildir/
smtpd_sasl_auth_enable = yes
smtpd_sasl_security_options = noanonymous
smtpd_sasl_local_domain = $myhostname
smtpd_recipient_restrictions = permit_sasl_authenticated, permit_mynetworks, reject_unauth_destination
smtpd_tls_security_level = may
smtpd_tls_auth_only = yes
smtpd_tls_cert_file = /etc/ssl/certs/ssl-cert-snakeoil.pem
smtpd_tls_key_file = /etc/ssl/private/ssl-cert-snakeoil.key
"""
        
        with open("/etc/postfix/main.cf", "w") as f:
            f.write(main_cf)
        
        # Master configuration
        master_cf = """# Postfix master process configuration
smtp      inet  n       -       n       -       -       smtpd
submission inet n       -       n       -       -       smtpd
  -o syslog_name=postfix/submission
  -o smtpd_tls_security_level=encrypt
  -o smtpd_sasl_auth_enable=yes
  -o smtpd_reject_unlisted_recipient=no
  -o smtpd_client_restrictions=$mua_client_restrictions
  -o smtpd_helo_restrictions=$mua_helo_restrictions
  -o smtpd_sender_restrictions=$mua_sender_restrictions
  -o smtpd_recipient_restrictions=
  -o smtpd_relay_restrictions=permit_sasl_authenticated,reject
  -o milter_macro_daemon_name=ORIGINATING
smtps     inet  n       -       n       -       -       smtpd
  -o syslog_name=postfix/smtps
  -o smtpd_tls_wrappermode=yes
  -o smtpd_sasl_auth_enable=yes
  -o smtpd_reject_unlisted_recipient=no
  -o smtpd_client_restrictions=$mua_client_restrictions
  -o smtpd_helo_restrictions=$mua_helo_restrictions
  -o smtpd_sender_restrictions=$mua_sender_restrictions
  -o smtpd_recipient_restrictions=
  -o smtpd_relay_restrictions=permit_sasl_authenticated,reject
  -o milter_macro_daemon_name=ORIGINATING
pickup    unix  n       -       n       60      1       pickup
cleanup   unix  n       -       n       -       0       cleanup
qmgr      unix  n       -       n       300     1       qmgr
tlsmgr    unix  -       -       n       1000?   1       tlsmgr
rewrite   unix  -       -       n       -       -       trivial-rewrite
bounce    unix  -       -       n       -       0       bounce
defer     unix  -       -       n       -       0       bounce
trace     unix  -       -       n       -       0       bounce
verify    unix  -       -       n       -       1       verify
flush     unix  n       -       n       1000?   0       flush
proxymap  unix  -       -       n       -       -       proxymap
proxywrite unix -       -       n       -       1       proxymap
smtp      unix  -       -       n       -       -       smtp
relay     unix  -       -       n       -       -       smtp
error     unix  -       -       n       -       -       error
retry     unix  -       -       n       -       -       error
discard   unix  -       -       n       -       -       discard
lmtp      unix  -       -       n       -       -       lmtp
anvil     unix  -       -       n       -       1       anvil
scache    unix  -       -       n       -       1       scache
"""
        
        with open("/etc/postfix/master.cf", "w") as f:
            f.write(master_cf)
    
    async def _configure_dovecot(self):
        """Configure Dovecot"""
        # Main configuration
        dovecot_conf = """# Dovecot configuration
protocols = imap pop3
listen = *
mail_location = maildir:~/Maildir
mail_privileged_group = mail
mail_access_groups = mail
userdb {
  driver = passwd
}
passdb {
  driver = pam
}
ssl = no
disable_plaintext_auth = no
"""
        
        with open("/etc/dovecot/conf.d/10-mail.conf", "w") as f:
            f.write(dovecot_conf)
        
        # Authentication configuration
        auth_conf = """# Authentication configuration
disable_plaintext_auth = no
auth_mechanisms = plain login
"""
        
        with open("/etc/dovecot/conf.d/10-auth.conf", "w") as f:
            f.write(auth_conf)
        
        # Master configuration
        master_conf = """# Master configuration
service imap-login {
  inet_listener imap {
    port = 143
  }
}
service pop3-login {
  inet_listener pop3 {
    port = 110
  }
}
service lmtp {
  unix_listener lmtp {
  }
}
service imap {
}
service pop3 {
}
service auth {
  unix_listener auth-userdb {
  }
  unix_listener /var/spool/postfix/private/auth {
    mode = 0666
    user = postfix
    group = postfix
  }
}
service auth-worker {
}
service dict {
  unix_listener dict {
  }
}
"""
        
        with open("/etc/dovecot/conf.d/10-master.conf", "w") as f:
            f.write(master_conf) 