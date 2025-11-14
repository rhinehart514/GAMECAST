'use client';

import { useState, useEffect } from 'react';
import { getTeams, type Team } from '@/lib/api';

interface TeamSelectorProps {
  onTeamsSelected: (homeTeam: Team, awayTeam: Team) => void;
  disabled?: boolean;
}

export default function TeamSelector({ onTeamsSelected, disabled }: TeamSelectorProps) {
  const [teams, setTeams] = useState<Team[]>([]);
  const [homeTeam, setHomeTeam] = useState<Team | null>(null);
  const [awayTeam, setAwayTeam] = useState<Team | null>(null);
  const [loading, setLoading] = useState(true);
  const [searchHome, setSearchHome] = useState('');
  const [searchAway, setSearchAway] = useState('');

  useEffect(() => {
    loadTeams();
  }, []);

  const loadTeams = async () => {
    try {
      const data = await getTeams();
      setTeams(data);
    } catch (error) {
      console.error('Error loading teams:', error);
    } finally {
      setLoading(false);
    }
  };

  const filteredHomeTeams = teams.filter(t => 
    t.name.toLowerCase().includes(searchHome.toLowerCase()) ||
    t.city.toLowerCase().includes(searchHome.toLowerCase()) ||
    t.code.toLowerCase().includes(searchHome.toLowerCase())
  );

  const filteredAwayTeams = teams.filter(t => 
    t.name.toLowerCase().includes(searchAway.toLowerCase()) ||
    t.city.toLowerCase().includes(searchAway.toLowerCase()) ||
    t.code.toLowerCase().includes(searchAway.toLowerCase())
  );

  const handleSubmit = () => {
    if (homeTeam && awayTeam && homeTeam.code !== awayTeam.code) {
      onTeamsSelected(homeTeam, awayTeam);
    }
  };

  if (loading) {
    return (
      <div className="card p-12 text-center fade-in">
        <div className="spinner w-12 h-12 mx-auto"></div>
        <p className="mt-6 text-sm text-muted-foreground">Loading teams...</p>
      </div>
    );
  }

  return (
    <div className="space-y-6 fade-in">
      <div className="text-center">
        <h2 className="text-3xl font-bold gradient-text mb-2">Select Matchup</h2>
        <p className="text-sm text-muted-foreground">Choose home and away teams to simulate</p>
      </div>
      
      <div className="grid md:grid-cols-2 gap-6">
        {/* Home Team */}
        <div className="card p-6 space-y-4">
          <div>
            <label className="block text-sm font-medium text-foreground mb-3 flex items-center gap-2">
              <span>🏠</span>
              <span>Home Team</span>
            </label>
            <input
              type="text"
              placeholder="Search teams..."
              value={searchHome}
              onChange={(e) => setSearchHome(e.target.value)}
              className="input w-full"
              disabled={disabled}
            />
          </div>
          
          <div className="h-96 overflow-y-auto space-y-2 pr-1">
            {filteredHomeTeams.map((team) => (
              <button
                key={team.code}
                onClick={() => setHomeTeam(team)}
                disabled={disabled || team.code === awayTeam?.code}
                className={`w-full p-3 rounded-lg text-left transition-all ${
                  homeTeam?.code === team.code
                    ? 'bg-accent text-white border border-accent'
                    : 'bg-card hover:bg-card-hover border border-border hover:border-border-hover'
                } ${team.code === awayTeam?.code ? 'opacity-30 cursor-not-allowed' : ''}`}
              >
                <div className="flex justify-between items-center gap-3">
                  <div className="flex-1 min-w-0">
                    <div className="font-semibold text-sm truncate">
                      {team.city} {team.name}
                    </div>
                    <div className="text-xs text-muted-foreground mt-0.5">
                      {team.division}
                    </div>
                  </div>
                  <div className="text-right shrink-0">
                    <div className="text-xs font-mono font-semibold text-accent">
                      {team.overall_strength.toFixed(1)}
                    </div>
                    <div className="text-xs text-muted-foreground">{team.code}</div>
                  </div>
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Away Team */}
        <div className="card p-6 space-y-4">
          <div>
            <label className="block text-sm font-medium text-foreground mb-3 flex items-center gap-2">
              <span>✈️</span>
              <span>Away Team</span>
            </label>
            <input
              type="text"
              placeholder="Search teams..."
              value={searchAway}
              onChange={(e) => setSearchAway(e.target.value)}
              className="input w-full"
              disabled={disabled}
            />
          </div>
          
          <div className="h-96 overflow-y-auto space-y-2 pr-1">
            {filteredAwayTeams.map((team) => (
              <button
                key={team.code}
                onClick={() => setAwayTeam(team)}
                disabled={disabled || team.code === homeTeam?.code}
                className={`w-full p-3 rounded-lg text-left transition-all ${
                  awayTeam?.code === team.code
                    ? 'bg-accent text-white border border-accent'
                    : 'bg-card hover:bg-card-hover border border-border hover:border-border-hover'
                } ${team.code === homeTeam?.code ? 'opacity-30 cursor-not-allowed' : ''}`}
              >
                <div className="flex justify-between items-center gap-3">
                  <div className="flex-1 min-w-0">
                    <div className="font-semibold text-sm truncate">
                      {team.city} {team.name}
                    </div>
                    <div className="text-xs text-muted-foreground mt-0.5">
                      {team.division}
                    </div>
                  </div>
                  <div className="text-right shrink-0">
                    <div className="text-xs font-mono font-semibold text-accent">
                      {team.overall_strength.toFixed(1)}
                    </div>
                    <div className="text-xs text-muted-foreground">{team.code}</div>
                  </div>
                </div>
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Matchup Preview */}
      {homeTeam && awayTeam && (
        <div className="card p-6 fade-in">
          <div className="flex items-center justify-between gap-6">
            <div className="text-center flex-1">
              <div className="text-sm font-medium text-muted-foreground mb-1">Away</div>
              <div className="text-lg font-semibold text-foreground">{awayTeam.code}</div>
              <div className="text-xs text-muted-foreground mt-1">{awayTeam.wins}-{awayTeam.losses}-{awayTeam.otl}</div>
              <div className="text-sm font-mono font-semibold text-accent mt-2">{awayTeam.overall_strength.toFixed(1)}</div>
            </div>
            
            <div className="text-muted-foreground">
              <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </div>
            
            <div className="text-center flex-1">
              <div className="text-sm font-medium text-muted-foreground mb-1">Home</div>
              <div className="text-lg font-semibold text-foreground">{homeTeam.code}</div>
              <div className="text-xs text-muted-foreground mt-1">{homeTeam.wins}-{homeTeam.losses}-{homeTeam.otl}</div>
              <div className="text-sm font-mono font-semibold text-accent mt-2">{homeTeam.overall_strength.toFixed(1)}</div>
            </div>
          </div>
        </div>
      )}

      {/* Simulate Button */}
      <button
        onClick={handleSubmit}
        disabled={!homeTeam || !awayTeam || homeTeam.code === awayTeam.code || disabled}
        className="btn btn-primary w-full h-12 text-base font-semibold"
      >
        {disabled ? (
          <span className="flex items-center gap-2">
            <div className="spinner w-4 h-4"></div>
            Simulating...
          </span>
        ) : homeTeam && awayTeam && homeTeam.code !== awayTeam.code ? (
          `Simulate Game`
        ) : (
          'Select both teams to continue'
        )}
      </button>
    </div>
  );
}
