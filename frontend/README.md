# Hosting Panel Frontend

A modern, responsive frontend for the Modern Hosting Panel built with Next.js, TypeScript, and Tailwind CSS.

## Features

- 🎨 **Modern UI/UX**: Clean, professional design with Tailwind CSS
- 📱 **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- ⚡ **Fast Performance**: Built with Next.js for optimal performance
- 🔒 **Type Safety**: Full TypeScript support for better development experience
- 🎯 **Component-Based**: Reusable components for maintainable code
- 🌐 **API Integration**: Seamlessly connects to the backend API

## Tech Stack

- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **State Management**: React Hooks
- **HTTP Client**: Axios
- **Forms**: React Hook Form with Zod validation

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn
- Docker (optional)

### Development Setup

1. **Install dependencies**:
   ```bash
   npm install
   ```

2. **Start development server**:
   ```bash
   npm run dev
   ```

3. **Open your browser**:
   Navigate to [http://localhost:3000](http://localhost:3000)

### Docker Setup

1. **Build and run with Docker**:
   ```bash
   docker-compose up -d --build
   ```

2. **Access the application**:
   Navigate to [http://localhost:3000](http://localhost:3000)

## Project Structure

```
src/
├── app/                 # Next.js App Router
│   ├── globals.css     # Global styles
│   ├── layout.tsx      # Root layout
│   └── page.tsx        # Home page
├── components/          # Reusable components
│   ├── Dashboard.tsx   # Main dashboard
│   ├── Header.tsx      # Top navigation
│   └── Sidebar.tsx     # Side navigation
└── lib/                # Utility functions
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint

## Environment Variables

Create a `.env.local` file in the frontend directory:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## API Integration

The frontend communicates with the backend API through:

- **Base URL**: Configurable via `NEXT_PUBLIC_API_URL`
- **API Routes**: `/api/*` endpoints
- **Authentication**: JWT-based auth system
- **Real-time Updates**: WebSocket support for live data

## Components

### Dashboard
- System overview with statistics
- Resource usage monitoring
- Recent activity feed
- Quick action buttons

### Navigation
- Responsive sidebar navigation
- Mobile-friendly header
- Breadcrumb navigation
- User menu and notifications

### Data Display
- Data tables with sorting/filtering
- Charts and graphs
- Status indicators
- Progress bars

## Styling

The application uses Tailwind CSS with a custom design system:

- **Colors**: Primary, secondary, success, warning, danger
- **Typography**: Inter font family
- **Spacing**: Consistent spacing scale
- **Components**: Pre-built component classes
- **Animations**: Smooth transitions and micro-interactions

## Development Guidelines

1. **Component Structure**: Use functional components with TypeScript
2. **State Management**: Prefer local state with React hooks
3. **Styling**: Use Tailwind CSS utility classes
4. **Type Safety**: Define proper interfaces for all props and data
5. **Performance**: Implement proper loading states and error handling

## Deployment

### Production Build

1. **Build the application**:
   ```bash
   npm run build
   ```

2. **Start production server**:
   ```bash
   npm run start
   ```

### Docker Production

1. **Build production image**:
   ```bash
   docker build -t hosting-panel-frontend .
   ```

2. **Run container**:
   ```bash
   docker run -p 3000:3000 hosting-panel-frontend
   ```

## Contributing

1. Follow the existing code style
2. Add proper TypeScript types
3. Include responsive design considerations
4. Test on multiple devices and browsers
5. Update documentation as needed

## License

This project is part of the Modern Hosting Panel and follows the same license terms.
