import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { ThemeProvider } from '@/components/theme-provider'
import { Toaster } from '@/components/ui/toaster'
import { Navigation } from '@/components/Navigation'
import { LoadingScreen } from '@/components/LoadingScreen'
import { HomePage } from '@/pages/HomePage'
import CosmicPortal from '@/pages/CosmicPortal'
import { LabPage } from '@/pages/LabPage'
import { AgentsPage } from '@/pages/AgentsPage'
import { LevelsPage } from '@/pages/LevelsPage'
import CrewShowcase from '@/pages/CrewShowcase'
import { StateProvider } from '@/contexts/StateContext'
import './App.css'

function App() {
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    // Simular carga inicial del laboratorio
    const timer = setTimeout(() => {
      setIsLoading(false)
    }, 2500)

    return () => clearTimeout(timer)
  }, [])

  if (isLoading) {
    return <LoadingScreen />
  }

  return (
    <ThemeProvider defaultTheme="dark" storageKey="synceros-theme">
      <StateProvider>
        <Router>
          <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
            <Navigation />
            <main className="container mx-auto px-4 py-8">
              <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/cosmic" element={<CosmicPortal />} />
                <Route path="/lab" element={<LabPage />} />
                <Route path="/crew" element={<CrewShowcase />} />
                <Route path="/agents" element={<AgentsPage />} />
                <Route path="/levels" element={<LevelsPage />} />
                <Route path="/levels/:levelId" element={<LevelsPage />} />
              </Routes>
            </main>
            <Toaster />
          </div>
        </Router>
      </StateProvider>
    </ThemeProvider>
  )
}

export default App
