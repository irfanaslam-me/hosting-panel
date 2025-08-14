# Environment Configuration

## Setup Instructions

### 1. Create Environment File

Create a `.env.local` file in the frontend directory:

```bash
# Backend API Configuration
NEXT_PUBLIC_API_URL=http://202.83.171.116:8000

# Frontend Configuration  
NEXT_PUBLIC_FRONTEND_URL=http://202.83.171.116:3000

# Environment
NODE_ENV=development
```

### 2. Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API base URL | `http://202.83.171.116:8000` |
| `NEXT_PUBLIC_FRONTEND_URL` | Frontend URL | `http://202.83.171.116:3000` |
| `NODE_ENV` | Environment mode | `development` or `production` |

### 3. Docker Environment

For Docker deployment, add these to your docker-compose.yml:

```yaml
frontend:
  environment:
    - NEXT_PUBLIC_API_URL=http://hosting_panel_app:8000
    - NODE_ENV=production
```

### 4. API Endpoints

The frontend will make requests to:
- Dashboard: `{NEXT_PUBLIC_API_URL}/api/v1/dashboard/stats`
- Websites: `{NEXT_PUBLIC_API_URL}/api/v1/websites`
- Databases: `{NEXT_PUBLIC_API_URL}/api/v1/databases`
- Docker: `{NEXT_PUBLIC_API_URL}/api/v1/docker/*`
- System: `{NEXT_PUBLIC_API_URL}/api/v1/system/status`
- Users: `{NEXT_PUBLIC_API_URL}/api/v1/users`
- Settings: `{NEXT_PUBLIC_API_URL}/api/v1/settings`
- Files: `{NEXT_PUBLIC_API_URL}/api/v1/files`
- Email: `{NEXT_PUBLIC_API_URL}/api/v1/email/*`

### 5. Troubleshooting

If you see 404 errors:
1. Check that `NEXT_PUBLIC_API_URL` is correct
2. Verify backend is running on the specified port
3. Ensure CORS is configured on backend
4. Check network connectivity between frontend and backend

### 6. Development vs Production

- **Development**: Use `.env.local` with your local backend URL
- **Production**: Use environment variables in Docker or hosting platform
- **Docker**: Use internal service names (e.g., `hosting_panel_app:8000`)
