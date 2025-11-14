'use client';

import { useState, useEffect } from 'react';
import { 
  createSeason, 
  simulateSeasonGames, 
  getSeasonStandings,
  type SeasonStandings 
} from '@/lib/api';
import StandingsTable from './StandingsTable';
import PlayoffBracket from './PlayoffBracket';
import AnalyticsDashboard from './AnalyticsDashboard';

type TabView = 'standings' | 'analytics' | 'playoffs';

export default function SeasonDashboard() {
  const [seasonId, setSeasonId] = useState<string | null>(null);
  const [seasonYear, setSeasonYear] = useState('2024-25');
  const [simulating, setSimulating] = useState(false);
  const [gamesPlayed, setGamesPlayed] = useState(0);
  const [totalGames, setTotalGames] = useState(1312); // 32 teams * 82 games / 2
  const [standings, setStandings] = useState<SeasonStandings[]>([]);
  const [selectedConference, setSelectedConference] = useState<'all' | 'Eastern' | 'Western'>('all');
  const [error, setError] = useState<string | null>(null);
  const [currentTab, setCurrentTab] = useState<TabView>('standings');

  const handleCreateSeason = async () => {
    setError(null);
    try {
      const season = await createSeason(seasonYear);
      setSeasonId(season.season_id);
      loadStandings(season.season_id);
    } catch (err) {
      setError('Failed to create season. Make sure the Game API is running on port 8001.');
      console.error(err);
    }
  };

  const handleSimulateGames = async (numGames: number) => {
    if (!seasonId) return;
    
    setSimulating(true);
    setError(null);
    try {
      const result = await simulateSeasonGames(seasonId, numGames);
      setGamesPlayed(result.total_games_played);
      await loadStandings(seasonId);
    } catch (err) {
      setError('Failed to simulate games. Make sure the Game API is running.');
      console.error(err);
    } finally {
      setSimulating(false);
    }
  };

  const loadStandings = async (sid: string) => {
    try {
      const data = await getSeasonStandings(sid);
      setStandings(data);
      
      // Calculate total games played
      const totalPlayed = data.reduce((sum, team) => sum + team.games_played, 0) / 2;
      setGamesPlayed(totalPlayed);
    } catch (err) {
      console.error('Failed to load standings:', err);
    }
  };

  const filteredStandings = selectedConference === 'all' 
    ? standings 
    : standings; // Note: API would need to support conference filtering

  const progress = (gamesPlayed / totalGames) * 100;
  const seasonComplete = gamesPlayed >= totalGames;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="text-center">
        <h1 className="text-4xl font-bold gradient-text mb-2">Season Simulator</h1>
        <p className="text-gray-400">Simulate an entire NHL season with ML-guided gameplay</p>
      </div>

      {!seasonId ? (
        // Create Season Card
        <div className="glass rounded-xl p-8 text-center max-w-md mx-auto">
          <h2 className="text-2xl font-bold text-white mb-6">Create New Season</h2>
          
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-400 mb-2">Season Year</label>
            <input
              type="text"
              value={seasonYear}
              onChange={(e) => setSeasonYear(e.target.value)}
              className="w-full px-4 py-3 bg-nhl-darker border border-nhl-blue rounded-lg text-white text-center text-lg focus:outline-none focus:ring-2 focus:ring-nhl-ice"
              placeholder="2024-25"
            />
          </div>

          <button
            onClick={handleCreateSeason}
            className="w-full py-4 bg-gradient-to-r from-nhl-blue to-nhl-ice rounded-lg font-bold text-white text-lg transition-all hover:scale-105"
          >
            Create Season 🏒
          </button>

          {error && (
            <div className="mt-4 p-3 bg-red-900/20 border border-red-500/50 rounded-lg text-red-400 text-sm">
              {error}
            </div>
          )}
        </div>
      ) : (
        <>
          {/* Progress Bar */}
          <div className="glass rounded-xl p-6">
            <div className="flex justify-between items-center mb-3">
              <div>
                <h3 className="text-lg font-bold text-white">Season Progress</h3>
                <p className="text-sm text-gray-400">{seasonYear} Regular Season</p>
              </div>
              <div className="text-right">
                <div className="text-2xl font-bold text-nhl-ice">{gamesPlayed}</div>
                <div className="text-xs text-gray-400">of {totalGames} games</div>
              </div>
            </div>
            
            <div className="w-full bg-nhl-darker rounded-full h-4 overflow-hidden">
              <div 
                className="bg-gradient-to-r from-nhl-blue to-nhl-ice h-full rounded-full transition-all duration-500 flex items-center justify-end pr-2"
                style={{ width: `${Math.min(progress, 100)}%` }}
              >
                {progress > 10 && (
                  <span className="text-xs font-bold text-white">{progress.toFixed(0)}%</span>
                )}
              </div>
            </div>
          </div>

          {/* Simulation Controls */}
          <div className="glass rounded-xl p-6">
            <h3 className="text-lg font-bold text-white mb-4">Simulate Games</h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              <button
                onClick={() => handleSimulateGames(10)}
                disabled={simulating || gamesPlayed >= totalGames}
                className="py-3 bg-nhl-blue hover:bg-nhl-blue/80 rounded-lg font-semibold transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                +10 Games
              </button>
              <button
                onClick={() => handleSimulateGames(82)}
                disabled={simulating || gamesPlayed >= totalGames}
                className="py-3 bg-nhl-blue hover:bg-nhl-blue/80 rounded-lg font-semibold transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                +1 Week (82)
              </button>
              <button
                onClick={() => handleSimulateGames(328)}
                disabled={simulating || gamesPlayed >= totalGames}
                className="py-3 bg-nhl-blue hover:bg-nhl-blue/80 rounded-lg font-semibold transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                +1 Month
              </button>
              <button
                onClick={() => handleSimulateGames(totalGames - gamesPlayed)}
                disabled={simulating || gamesPlayed >= totalGames}
                className="py-3 bg-gradient-to-r from-nhl-blue to-nhl-ice hover:opacity-80 rounded-lg font-bold transition-opacity disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Complete Season
              </button>
            </div>

            {simulating && (
              <div className="mt-4 flex items-center justify-center gap-3 text-gray-400">
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-nhl-ice"></div>
                <span>Simulating games with ML guidance...</span>
              </div>
            )}

            {error && (
              <div className="mt-4 p-3 bg-red-900/20 border border-red-500/50 rounded-lg text-red-400 text-sm">
                {error}
              </div>
            )}
          </div>

          {/* Tab Navigation */}
          <div className="card p-2">
            <div className="flex gap-2">
              <button
                onClick={() => setCurrentTab('standings')}
                className={`flex-1 px-6 py-3 rounded-lg font-semibold transition-all ${
                  currentTab === 'standings'
                    ? 'bg-accent text-white shadow-lg'
                    : 'text-muted-foreground hover:bg-muted hover:text-foreground'
                }`}
              >
                📊 Standings
              </button>
              <button
                onClick={() => setCurrentTab('analytics')}
                disabled={gamesPlayed < 10}
                className={`flex-1 px-6 py-3 rounded-lg font-semibold transition-all disabled:opacity-50 disabled:cursor-not-allowed ${
                  currentTab === 'analytics'
                    ? 'bg-accent text-white shadow-lg'
                    : 'text-muted-foreground hover:bg-muted hover:text-foreground'
                }`}
              >
                📈 Analytics
              </button>
              <button
                onClick={() => setCurrentTab('playoffs')}
                disabled={gamesPlayed < totalGames * 0.8}
                className={`flex-1 px-6 py-3 rounded-lg font-semibold transition-all disabled:opacity-50 disabled:cursor-not-allowed ${
                  currentTab === 'playoffs'
                    ? 'bg-accent text-white shadow-lg'
                    : 'text-muted-foreground hover:bg-muted hover:text-foreground'
                }`}
              >
                🏆 Playoffs
              </button>
            </div>
            {gamesPlayed < 10 && currentTab !== 'standings' && (
              <p className="text-xs text-muted-foreground text-center mt-2">
                Simulate at least 10 games to view analytics
              </p>
            )}
            {gamesPlayed < totalGames * 0.8 && currentTab === 'playoffs' && (
              <p className="text-xs text-muted-foreground text-center mt-2">
                Complete at least 80% of season to access playoffs
              </p>
            )}
          </div>

          {/* Tab Content */}
          {currentTab === 'standings' && standings.length > 0 && (
            <div className="fade-in">
              {/* Conference Filter */}
              <div className="flex justify-center gap-3 mb-6">
                <button
                  onClick={() => setSelectedConference('all')}
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                    selectedConference === 'all'
                      ? 'bg-accent text-white'
                      : 'bg-muted text-muted-foreground hover:bg-card-hover'
                  }`}
                >
                  All Teams
                </button>
                <button
                  onClick={() => setSelectedConference('Eastern')}
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                    selectedConference === 'Eastern'
                      ? 'bg-accent text-white'
                      : 'bg-muted text-muted-foreground hover:bg-card-hover'
                  }`}
                >
                  Eastern
                </button>
                <button
                  onClick={() => setSelectedConference('Western')}
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                    selectedConference === 'Western'
                      ? 'bg-accent text-white'
                      : 'bg-muted text-muted-foreground hover:bg-card-hover'
                  }`}
                >
                  Western
                </button>
              </div>
              <StandingsTable 
                standings={filteredStandings} 
                title={`${selectedConference === 'all' ? 'League' : selectedConference + ' Conference'} Standings`}
              />
            </div>
          )}
          
          {currentTab === 'analytics' && seasonId && (
            <AnalyticsDashboard seasonId={seasonId} />
          )}
          
          {currentTab === 'playoffs' && seasonId && (
            <PlayoffBracket seasonId={seasonId} />
          )}
        </>
      )}
    </div>
  );
}


