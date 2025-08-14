#!/bin/bash

# Frontend Environment Setup Script

echo "🚀 Setting up Frontend Environment..."

# Check if .env.local already exists
if [ -f ".env.local" ]; then
    echo "⚠️  .env.local already exists. Backing up to .env.local.backup"
    cp .env.local .env.local.backup
fi

# Get backend URL from user
echo ""
echo "Please enter your backend API URL:"
echo "Example: http://202.83.171.116:8000"
read -p "Backend URL: " BACKEND_URL

# Get frontend URL from user
echo ""
echo "Please enter your frontend URL:"
echo "Example: http://202.83.171.116:3000"
read -p "Frontend URL: " FRONTEND_URL

# Create .env.local file
cat > .env.local << EOF
# Backend API Configuration
NEXT_PUBLIC_API_URL=${BACKEND_URL}

# Frontend Configuration
NEXT_PUBLIC_FRONTEND_URL=${FRONTEND_URL}

# Environment
NODE_ENV=development
EOF

echo ""
echo "✅ Environment file created successfully!"
echo "📁 File: .env.local"
echo ""
echo "Contents:"
echo "=================="
cat .env.local
echo "=================="
echo ""
echo "🎯 Next steps:"
echo "1. Verify the URLs are correct"
echo "2. Restart your development server: npm run dev"
echo "3. Check the browser console for any API errors"
echo ""
echo "🔧 If you need to modify the URLs later, edit .env.local"
