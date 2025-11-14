'use client';

import { useState } from 'react';
import TeamSelector from '@/components/TeamSelector';
import GameViewer from '@/components/GameViewer';
import SeasonDashboard from '@/components/SeasonDashboard';
import GMDashboard from '@/components/GMDashboard';
import type { Team } from '@/lib/api';

type Mode = 'menu' | 'game' | 'season' | 'gm';
type GameState = 'select' | 'simulate';

export default function Home() {
  const [mode, setMode] = useState<Mode>('menu');
  const [gameState, setGameState] = useState<GameState>('select');
  const [homeTeam, setHomeTeam] = useState<Team | null>(null);
  const [awayTeam, setAwayTeam] = useState<Team | null>(null);

  const handleTeamsSelected = (home: Team, away: Team) => {
    setHomeTeam(home);
    setAwayTeam(away);
    setGameState('simulate');
  };

  const handleBackToTeams = () => {
    setGameState('select');
  };

  const handleBackToMenu = () => {
    setMode('menu');
    setGameState('select');
    setHomeTeam(null);
    setAwayTeam(null);
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Subtle gradient background */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[1000px] h-[1000px] bg-accent opacity-[0.03] rounded-full blur-3xl"></div>
      </div>

      {/* Content */}
      <div className="relative z-10">
        {/* Header */}
        <header className="border-b border-border/50 backdrop-blur-xl bg-background/80">
          <div className="container mx-auto px-6 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="text-2xl">🏒</div>
                <div>
                  <h1 className="text-lg font-semibold gradient-text">NHL Simulator</h1>
                  <p className="text-xs text-muted-foreground">AI-Powered Game Engine</p>
                </div>
              </div>
              {mode !== 'menu' && (
                <button
                  onClick={handleBackToMenu}
                  className="btn btn-ghost text-sm"
                >
                  ← Back
                </button>
              )}
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="container mx-auto px-6 py-12 max-w-6xl">
          {mode === 'menu' && (
            <div className="space-y-12 fade-in">
              {/* Hero Section */}
              <div className="text-center space-y-4 max-w-3xl mx-auto">
                <h2 className="text-5xl md:text-6xl font-bold gradient-text tracking-tight">
                  Simulate NHL Games
                </h2>
                <p className="text-lg text-muted-foreground leading-relaxed">
                  Experience realistic hockey simulations powered by machine learning. 
                  Real teams, real players, intelligent gameplay.
                </p>
              </div>

              {/* Mode Selection Cards */}
              <div className="grid md:grid-cols-3 gap-6">
                {/* Game Mode Card */}
                <button
                  onClick={() => setMode('game')}
                  className="card group p-8 text-left hover:scale-[1.02] active:scale-[0.98]"
                >
                  <div className="flex items-start justify-between mb-6">
                    <div className="text-4xl">🎮</div>
                    <div className="opacity-0 group-hover:opacity-100 transition-opacity">
                      <svg className="w-5 h-5 text-accent" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                      </svg>
                    </div>
                  </div>
                  <h3 className="text-2xl font-semibold text-foreground mb-3 group-hover:text-accent transition-colors">
                    Single Game
                  </h3>
                  <p className="text-sm text-muted-foreground leading-relaxed mb-6">
                    Simulate matchups between any two teams. See player-level stats, period breakdowns, and detailed scoring summaries.
                  </p>
                  <div className="flex items-center gap-2 text-sm font-medium text-accent">
                    <span>Start Simulation</span>
                    <span className="group-hover:translate-x-1 transition-transform">→</span>
                  </div>
                </button>

                {/* Season Mode Card */}
                <button
                  onClick={() => setMode('season')}
                  className="card group p-8 text-left hover:scale-[1.02] active:scale-[0.98]"
                >
                  <div className="flex items-start justify-between mb-6">
                    <div className="text-4xl">🏆</div>
                    <div className="opacity-0 group-hover:opacity-100 transition-opacity">
                      <svg className="w-5 h-5 text-accent" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                      </svg>
                    </div>
                  </div>
                  <h3 className="text-2xl font-semibold text-foreground mb-3 group-hover:text-accent transition-colors">
                    Full Season
                  </h3>
                  <p className="text-sm text-muted-foreground leading-relaxed mb-6">
                    Run complete 82-game seasons. Track standings, playoff races, and watch the season unfold game by game.
                  </p>
                  <div className="flex items-center gap-2 text-sm font-medium text-accent">
                    <span>Start Season</span>
                    <span className="group-hover:translate-x-1 transition-transform">→</span>
                  </div>
                </button>

                {/* GM Mode Card */}
                <button
                  onClick={() => setMode('gm')}
                  className="card group p-8 text-left hover:scale-[1.02] active:scale-[0.98] border-2 border-accent/30"
                >
                  <div className="flex items-start justify-between mb-6">
                    <div className="text-4xl">🎯</div>
                    <div className="opacity-0 group-hover:opacity-100 transition-opacity">
                      <svg className="w-5 h-5 text-accent" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                      </svg>
                    </div>
                  </div>
                  <div className="flex items-center gap-2 mb-3">
                    <h3 className="text-2xl font-semibold text-foreground group-hover:text-accent transition-colors">
                      GM Mode
                    </h3>
                    <span className="px-2 py-1 text-xs font-bold rounded-full bg-accent text-white">NEW</span>
                  </div>
                  <p className="text-sm text-muted-foreground leading-relaxed mb-6">
                    Manage your own NHL team! Edit rosters, adjust player ratings, and build a championship dynasty.
                  </p>
                  <div className="flex items-center gap-2 text-sm font-medium text-accent">
                    <span>Start Career</span>
                    <span className="group-hover:translate-x-1 transition-transform">→</span>
                  </div>
                </button>
              </div>

              {/* Features Grid */}
              <div className="grid md:grid-cols-3 gap-6">
                <div className="card p-6">
                  <div className="text-3xl mb-4">🤖</div>
                  <h4 className="font-semibold text-foreground mb-2">AI-Powered</h4>
                  <p className="text-sm text-muted-foreground leading-relaxed">
                    Machine learning guides every simulation for realistic outcomes and intelligent decision-making.
                  </p>
                </div>
                <div className="card p-6">
                  <div className="text-3xl mb-4">📊</div>
                  <h4 className="font-semibold text-foreground mb-2">Real NHL Data</h4>
                  <p className="text-sm text-muted-foreground leading-relaxed">
                    All 32 teams with actual rosters, player ratings, and authentic season statistics.
                  </p>
                </div>
                <div className="card p-6">
                  <div className="text-3xl mb-4">👤</div>
                  <h4 className="font-semibold text-foreground mb-2">Player Stats</h4>
                  <p className="text-sm text-muted-foreground leading-relaxed">
                    See who scored, who assisted, with realistic stat distribution and timestamps.
                  </p>
                </div>
              </div>

              {/* Footer Note */}
              <div className="text-center pt-8 border-t border-border">
                <p className="text-xs text-muted-foreground">
                  Powered by Python • FastAPI • Next.js • Machine Learning
                </p>
              </div>
            </div>
          )}

          {mode === 'game' && (
            <div className="max-w-6xl mx-auto">
              {gameState === 'select' && (
                <TeamSelector onTeamsSelected={handleTeamsSelected} />
              )}
              {gameState === 'simulate' && homeTeam && awayTeam && (
                <GameViewer
                  homeTeam={homeTeam}
                  awayTeam={awayTeam}
                  onBack={handleBackToTeams}
                />
              )}
            </div>
          )}

          {mode === 'season' && (
            <div className="max-w-7xl mx-auto">
              <SeasonDashboard />
            </div>
          )}

          {mode === 'gm' && (
            <div className="max-w-7xl mx-auto">
              <GMDashboard />
            </div>
          )}
        </main>

        {/* Footer */}
        <footer className="border-t border-border mt-20">
          <div className="container mx-auto px-6 py-8 text-center">
            <p className="text-sm text-muted-foreground">
              NHL Simulation Game • Built with AI & Machine Learning
            </p>
            <p className="text-xs text-muted-foreground mt-2">
              Simulation using real NHL team data for educational purposes
            </p>
          </div>
        </footer>
      </div>
    </div>
  );
}
