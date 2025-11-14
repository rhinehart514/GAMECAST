'use client';

import { useState, useEffect } from 'react';
import { generatePlayoffs, simulatePlayoffRound, simulateAllPlayoffs, getPlayoffBracket } from '@/lib/api';

interface PlayoffBracketProps {
  seasonId: string;
}

interface Series {
  series_id: string;
  round: number;
  higher_seed: string;
  lower_seed: string;
  higher_seed_wins: number;
  lower_seed_wins: number;
  games_played: number;
  status: string;
  winner: string | null;
  games: any[];
}

interface Bracket {
  season_year: string;
  eastern_conference: Series[];
  western_conference: Series[];
  stanley_cup_finals: Series | null;
  champion: string | null;
}

export default function PlayoffBracket({ seasonId }: PlayoffBracketProps) {
  const [playoffId, setPlayoffId] = useState<string | null>(null);
  const [bracket, setBracket] = useState<Bracket | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [simulating, setSimulating] = useState(false);

  // Generate bracket from season
  const handleGenerateBracket = async () => {
    try {
      setLoading(true);
      setError(null);
      const result = await generatePlayoffs(seasonId);
      setPlayoffId(result.playoff_id);
      setBracket(result.bracket);
    } catch (err: any) {
      setError(err.message || 'Failed to generate playoffs');
    } finally {
      setLoading(false);
    }
  };

  // Simulate a specific round
  const handleSimulateRound = async (roundNumber: number) => {
    if (!playoffId) return;
    
    try {
      setSimulating(true);
      setError(null);
      const result = await simulatePlayoffRound(playoffId, roundNumber);
      setBracket(result.bracket);
    } catch (err: any) {
      setError(err.message || 'Failed to simulate round');
    } finally {
      setSimulating(false);
    }
  };

  // Simulate all remaining rounds
  const handleSimulateAll = async () => {
    if (!playoffId) return;
    
    try {
      setSimulating(true);
      setError(null);
      const result = await simulateAllPlayoffs(playoffId);
      setBracket(result.bracket);
    } catch (err: any) {
      setError(err.message || 'Failed to simulate playoffs');
    } finally {
      setSimulating(false);
    }
  };

  // Render series card
  const renderSeries = (series: Series) => {
    const isComplete = series.status === 'completed';
    const isInProgress = series.status === 'in_progress';

    return (
      <div
        key={series.series_id}
        className={`card p-4 space-y-2 ${isComplete ? 'border-accent/30' : ''}`}
      >
        <div className="flex items-center justify-between">
          <div className={`text-sm font-medium ${series.winner === series.higher_seed ? 'text-accent' : 'text-foreground'}`}>
            {series.higher_seed}
          </div>
          <div className="text-lg font-bold text-foreground">
            {series.higher_seed_wins}
          </div>
        </div>

        <div className="flex items-center justify-between">
          <div className={`text-sm font-medium ${series.winner === series.lower_seed ? 'text-accent' : 'text-foreground'}`}>
            {series.lower_seed}
          </div>
          <div className="text-lg font-bold text-foreground">
            {series.lower_seed_wins}
          </div>
        </div>

        {isComplete && (
          <div className="pt-2 border-t border-border/30">
            <div className="text-xs text-accent font-medium">
              {series.winner} wins {series.winner === series.higher_seed ? series.higher_seed_wins : series.lower_seed_wins}-{series.winner === series.higher_seed ? series.lower_seed_wins : series.higher_seed_wins}
            </div>
          </div>
        )}

        {isInProgress && (
          <div className="pt-2 border-t border-border/30">
            <div className="text-xs text-muted-foreground">
              Series in progress • Game {series.games_played + 1}
            </div>
          </div>
        )}
      </div>
    );
  };

  // Render conference bracket
  const renderConference = (conferenceName: string, series: Series[]) => {
    const round1 = series.filter(s => s.round === 1);
    const round2 = series.filter(s => s.round === 2);
    const round3 = series.filter(s => s.round === 3);

    return (
      <div className="space-y-6">
        <h3 className="text-xl font-bold text-foreground text-center">
          {conferenceName} Conference
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Round 1 */}
          <div className="space-y-3">
            <div className="text-sm font-medium text-muted-foreground text-center">
              Round 1
            </div>
            {round1.map(renderSeries)}
          </div>

          {/* Round 2 */}
          <div className="space-y-3">
            <div className="text-sm font-medium text-muted-foreground text-center">
              Round 2
            </div>
            {round2.length > 0 ? round2.map(renderSeries) : (
              <div className="card p-4 text-center text-muted-foreground text-sm">
                Round 1 not complete
              </div>
            )}
          </div>

          {/* Conference Finals */}
          <div className="space-y-3">
            <div className="text-sm font-medium text-muted-foreground text-center">
              Conference Finals
            </div>
            {round3.length > 0 ? round3.map(renderSeries) : (
              <div className="card p-4 text-center text-muted-foreground text-sm">
                Round 2 not complete
              </div>
            )}
          </div>
        </div>
      </div>
    );
  };

  if (!bracket) {
    return (
      <div className="card p-8 text-center space-y-4">
        <div className="text-4xl">🏆</div>
        <h3 className="text-2xl font-bold text-foreground">Generate Playoff Bracket</h3>
        <p className="text-muted-foreground">
          Create a playoff bracket from the current season standings
        </p>
        {error && (
          <div className="text-sm text-red-500 bg-red-500/10 px-4 py-2 rounded-lg">
            {error}
          </div>
        )}
        <button
          onClick={handleGenerateBracket}
          disabled={loading}
          className="btn btn-primary px-8 py-3"
        >
          {loading ? 'Generating...' : 'Generate Bracket'}
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-8 fade-in">
      {/* Header */}
      <div className="card p-6">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-2xl font-bold gradient-text">
              {bracket.season_year} Playoffs
            </h2>
            <p className="text-sm text-muted-foreground mt-1">
              Best-of-7 series • 16 teams
            </p>
          </div>
          {bracket.champion && (
            <div className="text-right">
              <div className="text-sm text-muted-foreground">Stanley Cup Champion</div>
              <div className="text-2xl font-bold text-accent">
                🏆 {bracket.champion}
              </div>
            </div>
          )}
        </div>

        {/* Controls */}
        {!bracket.champion && (
          <div className="flex flex-wrap gap-3 pt-4 border-t border-border">
            <button
              onClick={() => handleSimulateRound(1)}
              disabled={simulating}
              className="btn btn-secondary text-sm"
            >
              {simulating ? 'Simulating...' : 'Simulate Round 1'}
            </button>
            <button
              onClick={() => handleSimulateRound(2)}
              disabled={simulating}
              className="btn btn-secondary text-sm"
            >
              {simulating ? 'Simulating...' : 'Simulate Round 2'}
            </button>
            <button
              onClick={() => handleSimulateRound(3)}
              disabled={simulating}
              className="btn btn-secondary text-sm"
            >
              {simulating ? 'Simulating...' : 'Simulate Conf. Finals'}
            </button>
            <button
              onClick={() => handleSimulateRound(4)}
              disabled={simulating}
              className="btn btn-secondary text-sm"
            >
              {simulating ? 'Simulating...' : 'Simulate Finals'}
            </button>
            <div className="flex-1"></div>
            <button
              onClick={handleSimulateAll}
              disabled={simulating}
              className="btn btn-primary text-sm"
            >
              {simulating ? 'Simulating...' : '⚡ Simulate All'}
            </button>
          </div>
        )}

        {error && (
          <div className="mt-4 text-sm text-red-500 bg-red-500/10 px-4 py-2 rounded-lg">
            {error}
          </div>
        )}
      </div>

      {/* Eastern Conference */}
      {renderConference('Eastern', bracket.eastern_conference)}

      {/* Western Conference */}
      {renderConference('Western', bracket.western_conference)}

      {/* Stanley Cup Finals */}
      {bracket.stanley_cup_finals && (
        <div className="card p-6 space-y-4">
          <h3 className="text-xl font-bold text-foreground text-center">
            Stanley Cup Finals
          </h3>
          <div className="max-w-md mx-auto">
            {renderSeries(bracket.stanley_cup_finals)}
          </div>
        </div>
      )}
    </div>
  );
}

