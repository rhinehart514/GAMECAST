'use client';

import { useState, useEffect } from 'react';
import { getLeagueLeaders, getTeamPlayerStats, getSeasonStandings } from '@/lib/api';

interface AnalyticsDashboardProps {
  seasonId: string;
}

interface PlayerStat {
  player_id: number;
  player_name: string;
  team_code: string;
  position: string;
  games_played: number;
  goals: number;
  assists: number;
  points: number;
  goals_per_game: number;
  assists_per_game: number;
  points_per_game: number;
}

type StatCategory = 'points' | 'goals' | 'assists' | 'goals_per_game';

export default function AnalyticsDashboard({ seasonId }: AnalyticsDashboardProps) {
  const [statCategory, setStatCategory] = useState<StatCategory>('points');
  const [leaders, setLeaders] = useState<PlayerStat[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [limit, setLimit] = useState(20);
  const [teamFilter, setTeamFilter] = useState<string>('all');
  const [teams, setTeams] = useState<string[]>([]);

  // Load league leaders
  const loadLeaders = async () => {
    try {
      setLoading(true);
      setError(null);
      const result = await getLeagueLeaders(seasonId, statCategory, limit);
      setLeaders(result.leaders);

      // Extract unique teams
      const uniqueTeams = Array.from(new Set(result.leaders.map(p => p.team_code))).sort();
      setTeams(uniqueTeams);
    } catch (err: any) {
      setError(err.message || 'Failed to load leaders');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadLeaders();
  }, [seasonId, statCategory, limit]);

  // Filter leaders by team
  const filteredLeaders = teamFilter === 'all' 
    ? leaders 
    : leaders.filter(p => p.team_code === teamFilter);

  // Get stat display
  const getStatValue = (player: PlayerStat) => {
    switch (statCategory) {
      case 'points':
        return player.points;
      case 'goals':
        return player.goals;
      case 'assists':
        return player.assists;
      case 'goals_per_game':
        return player.goals_per_game.toFixed(2);
      default:
        return player.points;
    }
  };

  // Get stat label
  const getStatLabel = () => {
    switch (statCategory) {
      case 'points':
        return 'Points';
      case 'goals':
        return 'Goals';
      case 'assists':
        return 'Assists';
      case 'goals_per_game':
        return 'G/G';
      default:
        return 'Points';
    }
  };

  return (
    <div className="space-y-6 fade-in">
      {/* Header */}
      <div className="card p-6">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-2xl font-bold gradient-text">League Leaders</h2>
            <p className="text-sm text-muted-foreground mt-1">
              Top performers across the league
            </p>
          </div>
          <div className="text-3xl">📊</div>
        </div>

        {/* Controls */}
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
          {/* Stat Category */}
          <div>
            <label className="block text-sm font-medium text-muted-foreground mb-2">
              Stat Category
            </label>
            <select
              value={statCategory}
              onChange={(e) => setStatCategory(e.target.value as StatCategory)}
              className="w-full bg-background/50 border border-border rounded-lg px-4 py-2.5 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-accent"
            >
              <option value="points">Points</option>
              <option value="goals">Goals</option>
              <option value="assists">Assists</option>
              <option value="goals_per_game">Goals per Game</option>
            </select>
          </div>

          {/* Limit */}
          <div>
            <label className="block text-sm font-medium text-muted-foreground mb-2">
              Show Top
            </label>
            <select
              value={limit}
              onChange={(e) => setLimit(Number(e.target.value))}
              className="w-full bg-background/50 border border-border rounded-lg px-4 py-2.5 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-accent"
            >
              <option value={10}>10 Players</option>
              <option value={20}>20 Players</option>
              <option value={50}>50 Players</option>
              <option value={100}>100 Players</option>
            </select>
          </div>

          {/* Team Filter */}
          <div>
            <label className="block text-sm font-medium text-muted-foreground mb-2">
              Filter by Team
            </label>
            <select
              value={teamFilter}
              onChange={(e) => setTeamFilter(e.target.value)}
              className="w-full bg-background/50 border border-border rounded-lg px-4 py-2.5 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-accent"
            >
              <option value="all">All Teams</option>
              {teams.map(team => (
                <option key={team} value={team}>{team}</option>
              ))}
            </select>
          </div>

          {/* Refresh Button */}
          <div className="flex items-end">
            <button
              onClick={loadLeaders}
              disabled={loading}
              className="btn btn-secondary w-full"
            >
              {loading ? 'Loading...' : '🔄 Refresh'}
            </button>
          </div>
        </div>
      </div>

      {/* Error */}
      {error && (
        <div className="card p-4 bg-red-500/10 border-red-500/30">
          <div className="text-sm text-red-500">{error}</div>
        </div>
      )}

      {/* Leaders Table */}
      {loading ? (
        <div className="card p-12 text-center">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-accent mb-4"></div>
          <p className="text-muted-foreground">Loading leaders...</p>
        </div>
      ) : filteredLeaders.length === 0 ? (
        <div className="card p-12 text-center">
          <div className="text-4xl mb-4">📊</div>
          <p className="text-muted-foreground">
            No player stats available yet. Simulate some games to generate stats.
          </p>
        </div>
      ) : (
        <div className="card overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-background/50 border-b border-border">
                <tr>
                  <th className="px-6 py-4 text-left text-xs font-semibold text-muted-foreground uppercase tracking-wider">
                    Rank
                  </th>
                  <th className="px-6 py-4 text-left text-xs font-semibold text-muted-foreground uppercase tracking-wider">
                    Player
                  </th>
                  <th className="px-6 py-4 text-left text-xs font-semibold text-muted-foreground uppercase tracking-wider">
                    Team
                  </th>
                  <th className="px-6 py-4 text-center text-xs font-semibold text-muted-foreground uppercase tracking-wider">
                    GP
                  </th>
                  <th className="px-6 py-4 text-center text-xs font-semibold text-muted-foreground uppercase tracking-wider">
                    G
                  </th>
                  <th className="px-6 py-4 text-center text-xs font-semibold text-muted-foreground uppercase tracking-wider">
                    A
                  </th>
                  <th className="px-6 py-4 text-center text-xs font-semibold text-muted-foreground uppercase tracking-wider">
                    P
                  </th>
                  <th className="px-6 py-4 text-center text-xs font-semibold text-accent uppercase tracking-wider">
                    {getStatLabel()}
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border">
                {filteredLeaders.map((player, index) => (
                  <tr 
                    key={player.player_id}
                    className="hover:bg-accent/5 transition-colors"
                  >
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        {index < 3 ? (
                          <span className="text-xl mr-2">
                            {index === 0 ? '🥇' : index === 1 ? '🥈' : '🥉'}
                          </span>
                        ) : (
                          <span className="text-sm font-medium text-muted-foreground w-8">
                            {index + 1}
                          </span>
                        )}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-medium text-foreground">
                        {player.player_name}
                      </div>
                      <div className="text-xs text-muted-foreground">
                        {player.position}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full bg-accent/10 text-accent">
                        {player.team_code}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-center text-sm text-foreground">
                      {player.games_played}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-center text-sm text-foreground">
                      {player.goals}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-center text-sm text-foreground">
                      {player.assists}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-center text-sm text-foreground">
                      {player.points}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-center text-sm font-bold text-accent">
                      {getStatValue(player)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Stats Summary */}
      {!loading && filteredLeaders.length > 0 && (
        <div className="grid md:grid-cols-3 gap-4">
          <div className="card p-6">
            <div className="text-sm text-muted-foreground mb-1">Top Scorer</div>
            <div className="text-xl font-bold text-accent">
              {filteredLeaders[0]?.player_name}
            </div>
            <div className="text-sm text-muted-foreground mt-1">
              {filteredLeaders[0]?.points} points
            </div>
          </div>

          <div className="card p-6">
            <div className="text-sm text-muted-foreground mb-1">Most Goals</div>
            <div className="text-xl font-bold text-accent">
              {[...filteredLeaders].sort((a, b) => b.goals - a.goals)[0]?.player_name}
            </div>
            <div className="text-sm text-muted-foreground mt-1">
              {[...filteredLeaders].sort((a, b) => b.goals - a.goals)[0]?.goals} goals
            </div>
          </div>

          <div className="card p-6">
            <div className="text-sm text-muted-foreground mb-1">Most Assists</div>
            <div className="text-xl font-bold text-accent">
              {[...filteredLeaders].sort((a, b) => b.assists - a.assists)[0]?.player_name}
            </div>
            <div className="text-sm text-muted-foreground mt-1">
              {[...filteredLeaders].sort((a, b) => b.assists - a.assists)[0]?.assists} assists
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

