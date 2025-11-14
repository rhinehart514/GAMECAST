'use client';

import { useState } from 'react';
import { simulateGame, type GameResult, type Team } from '@/lib/api';

interface GameViewerProps {
  homeTeam: Team;
  awayTeam: Team;
  onBack: () => void;
}

export default function GameViewer({ homeTeam, awayTeam, onBack }: GameViewerProps) {
  const [result, setResult] = useState<GameResult | null>(null);
  const [simulating, setSimulating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const runSimulation = async () => {
    setSimulating(true);
    setError(null);
    try {
      const gameResult = await simulateGame(homeTeam.code, awayTeam.code);
      setResult(gameResult);
    } catch (err) {
      setError('Failed to simulate game. Make sure the Game API is running on port 8001.');
      console.error(err);
    } finally {
      setSimulating(false);
    }
  };

  return (
    <div className="space-y-6 fade-in">
      {/* Header */}
      <div className="flex items-center justify-between">
        <button
          onClick={onBack}
          className="btn btn-ghost"
        >
          ← Back to Teams
        </button>
        <h1 className="text-2xl font-bold gradient-text">Game Simulation</h1>
        <div className="w-32"></div>
      </div>

      {/* Matchup Card */}
      <div className="card p-8">
        <div className="flex items-center justify-between gap-8">
          {/* Away Team */}
          <div className="text-center flex-1">
            <div className="text-xl font-bold text-foreground mb-1">
              {awayTeam.city} {awayTeam.name}
            </div>
            <div className="text-xs text-muted-foreground mb-3">
              {awayTeam.division} • {awayTeam.wins}-{awayTeam.losses}-{awayTeam.otl}
            </div>
            <div className="inline-flex flex-col items-center px-4 py-2 bg-muted rounded-lg">
              <div className="text-xs text-muted-foreground">Strength</div>
              <div className="text-xl font-mono font-bold text-accent">
                {awayTeam.overall_strength.toFixed(1)}
              </div>
            </div>
            {result && (
              <div className="mt-6">
                <div className="text-5xl font-bold text-foreground">{result.away_score}</div>
                <div className="text-xs text-muted-foreground mt-2">{result.away_shots} shots</div>
              </div>
            )}
          </div>

          {/* VS/@ */}
          <div className="text-center px-4">
            <div className="text-3xl font-bold text-muted-foreground">@</div>
            {result && (
              <div className="mt-2 text-xs font-medium text-muted-foreground">
                {result.periods > 3 ? (result.periods === 4 ? 'OT' : 'SO') : 'Final'}
              </div>
            )}
          </div>

          {/* Home Team */}
          <div className="text-center flex-1">
            <div className="text-xl font-bold text-foreground mb-1">
              {homeTeam.city} {homeTeam.name}
            </div>
            <div className="text-xs text-muted-foreground mb-3">
              {homeTeam.division} • {homeTeam.wins}-{homeTeam.losses}-{homeTeam.otl}
            </div>
            <div className="inline-flex flex-col items-center px-4 py-2 bg-muted rounded-lg">
              <div className="text-xs text-muted-foreground">Strength</div>
              <div className="text-xl font-mono font-bold text-accent">
                {homeTeam.overall_strength.toFixed(1)}
              </div>
            </div>
            {result && (
              <div className="mt-6">
                <div className="text-5xl font-bold text-foreground">{result.home_score}</div>
                <div className="text-xs text-muted-foreground mt-2">{result.home_shots} shots</div>
              </div>
            )}
          </div>
        </div>

        {/* Simulate Button */}
        {!result && !simulating && (
          <div className="mt-8">
            <button
              onClick={runSimulation}
              className="btn btn-primary w-full h-12 text-base"
            >
              Start Simulation
            </button>
          </div>
        )}

        {/* Simulating State */}
        {simulating && (
          <div className="mt-8 text-center py-8">
            <div className="spinner w-12 h-12 mx-auto"></div>
            <p className="mt-4 text-sm text-muted-foreground">Running ML-guided simulation...</p>
            <p className="text-xs text-muted-foreground mt-1">This may take 30-60 seconds</p>
          </div>
        )}

        {/* Error State */}
        {error && (
          <div className="mt-8 card p-4 bg-destructive/10 border-destructive/50">
            <p className="text-sm text-destructive text-center">{error}</p>
          </div>
        )}
      </div>

      {/* Results */}
      {result && (
        <div className="space-y-6 fade-in">
          {/* Winner Card */}
          <div className="card p-6 text-center">
            <div className="text-sm font-medium text-muted-foreground mb-2">Winner</div>
            <div className="text-3xl font-bold gradient-accent">
              {result.winner === homeTeam.code 
                ? `${homeTeam.city} ${homeTeam.name}` 
                : `${awayTeam.city} ${awayTeam.name}`}
            </div>
          </div>

          {/* Stats Grid */}
          <div className="grid grid-cols-3 gap-4">
            <div className="card p-4 text-center">
              <div className="text-2xl font-bold text-foreground">{result.away_shots}</div>
              <div className="text-xs text-muted-foreground mt-1">Away Shots</div>
            </div>
            <div className="card p-4 text-center">
              <div className="text-2xl font-bold text-accent">{result.periods > 3 ? result.periods - 3 : 0}</div>
              <div className="text-xs text-muted-foreground mt-1">Extra Periods</div>
            </div>
            <div className="card p-4 text-center">
              <div className="text-2xl font-bold text-foreground">{result.home_shots}</div>
              <div className="text-xs text-muted-foreground mt-1">Home Shots</div>
            </div>
          </div>

          {/* Period Breakdown */}
          {Object.keys(result.period_scores).length > 0 && (
            <div className="card p-6">
              <h3 className="text-lg font-semibold text-foreground mb-4">Period Breakdown</h3>
              <div className="space-y-1">
                <div className="grid grid-cols-4 gap-3 text-center text-xs font-medium text-muted-foreground mb-2">
                  <div className="text-left">Team</div>
                  <div>1st</div>
                  <div>2nd</div>
                  <div>3rd</div>
                </div>
                <div className="grid grid-cols-4 gap-3 text-center text-sm">
                  <div className="text-left font-semibold text-foreground">{awayTeam.code}</div>
                  <div className="text-foreground font-mono">{result.period_scores['1']?.away_goals || 0}</div>
                  <div className="text-foreground font-mono">{result.period_scores['2']?.away_goals || 0}</div>
                  <div className="text-foreground font-mono">{result.period_scores['3']?.away_goals || 0}</div>
                </div>
                <div className="grid grid-cols-4 gap-3 text-center text-sm">
                  <div className="text-left font-semibold text-foreground">{homeTeam.code}</div>
                  <div className="text-foreground font-mono">{result.period_scores['1']?.home_goals || 0}</div>
                  <div className="text-foreground font-mono">{result.period_scores['2']?.home_goals || 0}</div>
                  <div className="text-foreground font-mono">{result.period_scores['3']?.home_goals || 0}</div>
                </div>
              </div>
            </div>
          )}

          {/* Scoring Summary */}
          {result.goal_scorers && result.goal_scorers.length > 0 && (
            <div className="card p-6">
              <h3 className="text-lg font-semibold text-foreground mb-4">Scoring Summary</h3>
              <div className="space-y-4">
                {Object.entries(result.period_scores)
                  .sort(([a], [b]) => parseInt(a) - parseInt(b))
                  .map(([periodNum, period]) => (
                    period.goals.length > 0 && (
                      <div key={periodNum}>
                        <div className="text-xs font-semibold text-muted-foreground mb-3">
                          Period {periodNum}
                        </div>
                        <div className="space-y-2">
                          {period.goals.map((goal, idx) => {
                            const mins = Math.floor(goal.time_elapsed / 60);
                            const secs = goal.time_elapsed % 60;
                            const isHomeGoal = goal.team === homeTeam.code;
                            
                            return (
                              <div 
                                key={idx} 
                                className={`flex items-start gap-3 p-3 rounded-lg border transition-colors ${
                                  isHomeGoal 
                                    ? 'bg-accent/5 border-accent/20 hover:bg-accent/10' 
                                    : 'bg-muted border-border hover:bg-card-hover'
                                }`}
                              >
                                <div className="text-xs font-mono text-muted-foreground min-w-[45px] pt-0.5">
                                  {mins}:{secs.toString().padStart(2, '0')}
                                </div>
                                <div className="flex-1 min-w-0">
                                  <div className="font-semibold text-foreground text-sm">
                                    {goal.scorer || 'Unknown'}
                                    {goal.is_power_play && (
                                      <span className="badge badge-primary ml-2">PP</span>
                                    )}
                                    {goal.is_empty_net && (
                                      <span className="badge badge-danger ml-2">EN</span>
                                    )}
                                  </div>
                                  {(goal.primary_assist || goal.secondary_assist) && (
                                    <div className="text-xs text-muted-foreground mt-1">
                                      Assists: {[goal.primary_assist, goal.secondary_assist]
                                        .filter(Boolean)
                                        .join(', ')}
                                    </div>
                                  )}
                                  <div className="text-xs text-muted-foreground mt-0.5">
                                    {isHomeGoal ? homeTeam.code : awayTeam.code}
                                  </div>
                                </div>
                              </div>
                            );
                          })}
                        </div>
                      </div>
                    )
                  ))}
              </div>
            </div>
          )}

          {/* Simulate Again */}
          <button
            onClick={() => {
              setResult(null);
              runSimulation();
            }}
            className="btn btn-secondary w-full h-11"
          >
            Simulate Again
          </button>
        </div>
      )}
    </div>
  );
}
