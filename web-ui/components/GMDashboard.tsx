'use client';

import { useState, useEffect } from 'react';
import { getTeams, type Team } from '@/lib/api';
import {
  createGMCareer,
  getGMCareer,
  getGMRoster,
  updatePlayerRating,
  type GMCareerSummary,
  type Player
} from '@/lib/gm-api';

export default function GMDashboard() {
  // Creation state
  const [creating, setCreating] = useState(true);
  const [gmName, setGmName] = useState('');
  const [selectedTeam, setSelectedTeam] = useState<string>('');
  const [teams, setTeams] = useState<Team[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Career state
  const [careerId, setCareerId] = useState<string | null>(null);
  const [careerSummary, setCareerSummary] = useState<GMCareerSummary | null>(null);
  const [roster, setRoster] = useState<Player[]>([]);
  const [currentView, setCurrentView] = useState<'overview' | 'roster'>('overview');
  
  // Roster editing
  const [editingPlayer, setEditingPlayer] = useState<number | null>(null);
  const [editValues, setEditValues] = useState<{ overall: number; offensive: number; defensive: number }>({ overall: 0, offensive: 0, defensive: 0 });

  // Load teams for creation
  useEffect(() => {
    async function loadTeams() {
      try {
        setLoading(true);
        const teamsData = await getTeams();
        setTeams(teamsData.sort((a, b) => a.name.localeCompare(b.name)));
      } catch (err: any) {
        console.error('Failed to load teams', err);
        setError(`Failed to load teams: ${err.message || 'API not responding'}`);
      } finally {
        setLoading(false);
      }
    }
    loadTeams();
  }, []);

  // Create GM career
  const handleCreateCareer = async () => {
    if (!gmName || !selectedTeam) {
      setError('Please enter your name and select a team');
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const result = await createGMCareer(gmName, selectedTeam);
      setCareerId(result.career_id);
      setCreating(false);
      await loadCareer(result.career_id);
    } catch (err: any) {
      setError(err.message || 'Failed to create career');
    } finally {
      setLoading(false);
    }
  };

  // Load career data
  const loadCareer = async (id: string) => {
    setLoading(true);
    try {
      const [summary, rosterData] = await Promise.all([
        getGMCareer(id),
        getGMRoster(id)
      ]);
      setCareerSummary(summary);
      setRoster(rosterData.roster);
    } catch (err: any) {
      setError(err.message || 'Failed to load career');
    } finally {
      setLoading(false);
    }
  };

  // Start editing player
  const startEditPlayer = (player: Player) => {
    setEditingPlayer(player.player_id);
    setEditValues({
      overall: player.overall_rating,
      offensive: player.offensive_rating,
      defensive: player.defensive_rating
    });
  };

  // Save player edits
  const savePlayerEdit = async (playerId: number) => {
    if (!careerId) return;

    setLoading(true);
    setError(null);
    try {
      await updatePlayerRating(
        careerId,
        playerId,
        editValues.overall,
        editValues.offensive,
        editValues.defensive
      );
      // Reload roster
      const rosterData = await getGMRoster(careerId);
      setRoster(rosterData.roster);
      setEditingPlayer(null);
    } catch (err: any) {
      setError(err.message || 'Failed to update player');
    } finally {
      setLoading(false);
    }
  };

  // Creation screen
  if (creating) {
    return (
      <div className="space-y-6 fade-in">
        <div className="text-center">
          <h1 className="text-4xl font-bold gradient-text mb-2">GM Mode</h1>
          <p className="text-muted-foreground">Create your career and manage an NHL team</p>
        </div>

        <div className="card p-8 max-w-2xl mx-auto">
          <h2 className="text-2xl font-bold text-foreground mb-6">Create Your GM Career</h2>

          {/* Loading State */}
          {loading && teams.length === 0 && !error && (
            <div className="text-center py-12">
              <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-accent mb-4"></div>
              <p className="text-muted-foreground">Loading teams...</p>
            </div>
          )}

          {/* Error State */}
          {error && teams.length === 0 && (
            <div className="text-center py-12">
              <div className="text-4xl mb-4">⚠️</div>
              <p className="text-red-500 mb-4">{error}</p>
              <button
                onClick={() => window.location.reload()}
                className="btn btn-secondary"
              >
                Reload Page
              </button>
            </div>
          )}

          {/* Content when teams loaded */}
          {teams.length > 0 && (
            <>
              {/* GM Name Input */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-muted-foreground mb-2">
                  Your Name
                </label>
                <input
                  type="text"
                  value={gmName}
                  onChange={(e) => setGmName(e.target.value)}
                  placeholder="Enter your name..."
                  className="w-full px-4 py-3 bg-background/50 border border-border rounded-lg text-foreground focus:outline-none focus:ring-2 focus:ring-accent"
                />
              </div>

              {/* Team Selection */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-muted-foreground mb-2">
                  Select Your Team
                </label>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3 max-h-96 overflow-y-auto">
                  {teams.map((team) => (
                <button
                  key={team.code}
                  onClick={() => setSelectedTeam(team.code)}
                  className={`p-4 rounded-lg border-2 transition-all text-left ${
                    selectedTeam === team.code
                      ? 'border-accent bg-accent/10'
                      : 'border-border hover:border-accent/50'
                  }`}
                >
                  <div className="font-bold text-foreground text-sm">{team.code}</div>
                  <div className="text-xs text-muted-foreground">{team.city}</div>
                  <div className="text-xs text-muted-foreground">{team.name}</div>
                  </button>
                ))}
              </div>
            </div>

            {error && (
              <div className="mb-4 p-3 bg-red-500/10 border border-red-500/30 rounded-lg text-red-500 text-sm">
                {error}
              </div>
            )}

            <button
              onClick={handleCreateCareer}
              disabled={loading || !gmName || !selectedTeam}
              className="btn btn-primary w-full py-4 text-lg"
            >
              {loading ? 'Creating Career...' : 'Start GM Career 🏒'}
            </button>
          </>
          )}
        </div>
      </div>
    );
  }

  // Career dashboard
  if (!careerSummary) {
    return (
      <div className="card p-12 text-center">
        <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-accent mb-4"></div>
        <p className="text-muted-foreground">Loading career...</p>
      </div>
    );
  }

  return (
    <div className="space-y-6 fade-in">
      {/* Header */}
      <div className="card p-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold gradient-text">{careerSummary.career.gm_name}</h1>
            <p className="text-muted-foreground mt-1">
              GM of {careerSummary.team.full_name} • {careerSummary.team.conference} • {careerSummary.team.division}
            </p>
          </div>
          <div className="text-right">
            <div className="text-4xl mb-2">{careerSummary.career.championship_count > 0 ? '🏆' : '🏒'}</div>
            <div className="text-sm text-muted-foreground">Season {careerSummary.career.current_season}</div>
          </div>
        </div>
      </div>

      {/* Tab Navigation */}
      <div className="card p-2">
        <div className="flex gap-2">
          <button
            onClick={() => setCurrentView('overview')}
            className={`flex-1 px-6 py-3 rounded-lg font-semibold transition-all ${
              currentView === 'overview'
                ? 'bg-accent text-white shadow-lg'
                : 'text-muted-foreground hover:bg-muted hover:text-foreground'
            }`}
          >
            📊 Overview
          </button>
          <button
            onClick={() => setCurrentView('roster')}
            className={`flex-1 px-6 py-3 rounded-lg font-semibold transition-all ${
              currentView === 'roster'
                ? 'bg-accent text-white shadow-lg'
                : 'text-muted-foreground hover:bg-muted hover:text-foreground'
            }`}
          >
            👥 Roster ({roster.length})
          </button>
        </div>
      </div>

      {/* Overview Tab */}
      {currentView === 'overview' && (
        <div className="space-y-6">
          {/* Career Stats */}
          <div className="grid md:grid-cols-3 gap-4">
            <div className="card p-6">
              <div className="text-sm text-muted-foreground mb-1">Career Record</div>
              <div className="text-2xl font-bold text-foreground">
                {careerSummary.career.total_wins}-{careerSummary.career.total_losses}-{careerSummary.career.total_otl}
              </div>
              <div className="text-sm text-accent mt-1">{careerSummary.career.win_percentage.toFixed(1)}% Win Rate</div>
            </div>

            <div className="card p-6">
              <div className="text-sm text-muted-foreground mb-1">Playoff Appearances</div>
              <div className="text-2xl font-bold text-foreground">{careerSummary.career.playoff_appearances}</div>
              <div className="text-sm text-accent mt-1">
                {careerSummary.achievements.playoff_rate.toFixed(1)}% Rate
              </div>
            </div>

            <div className="card p-6">
              <div className="text-sm text-muted-foreground mb-1">Championships</div>
              <div className="text-2xl font-bold text-accent">
                {careerSummary.career.championship_count} 🏆
              </div>
              <div className="text-sm text-muted-foreground mt-1">
                {careerSummary.career.seasons_completed} seasons played
              </div>
            </div>
          </div>

          {/* Team Info */}
          <div className="card p-6">
            <h3 className="text-xl font-bold text-foreground mb-4">Team Information</h3>
            <div className="grid md:grid-cols-2 gap-4">
              <div>
                <div className="text-sm text-muted-foreground">Conference</div>
                <div className="text-lg font-semibold text-foreground">{careerSummary.team.conference}</div>
              </div>
              <div>
                <div className="text-sm text-muted-foreground">Division</div>
                <div className="text-lg font-semibold text-foreground">{careerSummary.team.division}</div>
              </div>
              <div>
                <div className="text-sm text-muted-foreground">Overall Strength</div>
                <div className="text-lg font-semibold text-accent">{careerSummary.team.overall_strength.toFixed(1)}</div>
              </div>
              <div>
                <div className="text-sm text-muted-foreground">Roster Size</div>
                <div className="text-lg font-semibold text-foreground">{careerSummary.team.roster_size} players</div>
              </div>
            </div>
          </div>

          {/* Getting Started */}
          <div className="card p-6">
            <h3 className="text-xl font-bold text-foreground mb-4">Getting Started</h3>
            <div className="space-y-3 text-sm text-muted-foreground">
              <p>✅ <span className="text-foreground">Career Created!</span> You are now the GM of {careerSummary.team.full_name}.</p>
              <p>👥 <span className="text-foreground">Manage Roster:</span> Click the "Roster" tab to view and edit your players.</p>
              <p>🎮 <span className="text-foreground">Simulate Seasons:</span> Go back to Season Mode and create a season to start managing your team.</p>
              <p>🏆 <span className="text-foreground">Win Championships:</span> Guide your team through seasons and playoffs to win the Stanley Cup!</p>
            </div>
          </div>
        </div>
      )}

      {/* Roster Tab */}
      {currentView === 'roster' && (
        <div className="card overflow-hidden">
          <div className="p-6 border-b border-border">
            <h3 className="text-xl font-bold text-foreground">Team Roster</h3>
            <p className="text-sm text-muted-foreground mt-1">
              Edit player ratings to customize your team
            </p>
          </div>

          {error && (
            <div className="m-6 p-3 bg-red-500/10 border border-red-500/30 rounded-lg text-red-500 text-sm">
              {error}
            </div>
          )}

          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-background/50 border-b border-border">
                <tr>
                  <th className="px-6 py-4 text-left text-xs font-semibold text-muted-foreground uppercase">Player</th>
                  <th className="px-6 py-4 text-center text-xs font-semibold text-muted-foreground uppercase">Pos</th>
                  <th className="px-6 py-4 text-center text-xs font-semibold text-muted-foreground uppercase">Overall</th>
                  <th className="px-6 py-4 text-center text-xs font-semibold text-muted-foreground uppercase">Offense</th>
                  <th className="px-6 py-4 text-center text-xs font-semibold text-muted-foreground uppercase">Defense</th>
                  <th className="px-6 py-4 text-center text-xs font-semibold text-muted-foreground uppercase">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border">
                {roster.map((player) => (
                  <tr key={player.player_id} className="hover:bg-accent/5 transition-colors">
                    <td className="px-6 py-4">
                      <div className="font-medium text-foreground">{player.name}</div>
                    </td>
                    <td className="px-6 py-4 text-center">
                      <span className="px-2 py-1 text-xs font-semibold rounded-full bg-accent/10 text-accent">
                        {player.position}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-center">
                      {editingPlayer === player.player_id ? (
                        <input
                          type="number"
                          min="0"
                          max="100"
                          value={editValues.overall}
                          onChange={(e) => setEditValues({ ...editValues, overall: parseInt(e.target.value) || 0 })}
                          className="w-16 px-2 py-1 bg-background border border-border rounded text-center"
                        />
                      ) : (
                        <span className="font-bold text-foreground">{player.overall_rating}</span>
                      )}
                    </td>
                    <td className="px-6 py-4 text-center">
                      {editingPlayer === player.player_id ? (
                        <input
                          type="number"
                          min="0"
                          max="100"
                          value={editValues.offensive}
                          onChange={(e) => setEditValues({ ...editValues, offensive: parseInt(e.target.value) || 0 })}
                          className="w-16 px-2 py-1 bg-background border border-border rounded text-center"
                        />
                      ) : (
                        <span className="text-foreground">{player.offensive_rating}</span>
                      )}
                    </td>
                    <td className="px-6 py-4 text-center">
                      {editingPlayer === player.player_id ? (
                        <input
                          type="number"
                          min="0"
                          max="100"
                          value={editValues.defensive}
                          onChange={(e) => setEditValues({ ...editValues, defensive: parseInt(e.target.value) || 0 })}
                          className="w-16 px-2 py-1 bg-background border border-border rounded text-center"
                        />
                      ) : (
                        <span className="text-foreground">{player.defensive_rating}</span>
                      )}
                    </td>
                    <td className="px-6 py-4 text-center">
                      {editingPlayer === player.player_id ? (
                        <div className="flex items-center justify-center gap-2">
                          <button
                            onClick={() => savePlayerEdit(player.player_id)}
                            disabled={loading}
                            className="btn btn-primary text-xs px-3 py-1"
                          >
                            Save
                          </button>
                          <button
                            onClick={() => setEditingPlayer(null)}
                            className="btn btn-ghost text-xs px-3 py-1"
                          >
                            Cancel
                          </button>
                        </div>
                      ) : (
                        <button
                          onClick={() => startEditPlayer(player)}
                          className="btn btn-secondary text-xs px-3 py-1"
                        >
                          Edit
                        </button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}

