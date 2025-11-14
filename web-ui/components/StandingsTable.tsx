'use client';

import { type SeasonStandings } from '@/lib/api';

interface StandingsTableProps {
  standings: SeasonStandings[];
  title?: string;
}

export default function StandingsTable({ standings, title }: StandingsTableProps) {
  // Sort by points (descending), then by points percentage
  const sortedStandings = [...standings].sort((a, b) => {
    if (b.points !== a.points) return b.points - a.points;
    return b.points_percentage - a.points_percentage;
  });

  return (
    <div className="glass rounded-xl overflow-hidden">
      {title && (
        <div className="bg-nhl-blue px-6 py-3 border-b border-nhl-ice/30">
          <h3 className="text-xl font-bold text-white">{title}</h3>
        </div>
      )}
      
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="bg-nhl-darker text-gray-400 text-xs uppercase tracking-wider">
              <th className="px-6 py-3 text-left font-semibold">Rank</th>
              <th className="px-6 py-3 text-left font-semibold">Team</th>
              <th className="px-6 py-3 text-center font-semibold">GP</th>
              <th className="px-6 py-3 text-center font-semibold">W</th>
              <th className="px-6 py-3 text-center font-semibold">L</th>
              <th className="px-6 py-3 text-center font-semibold">OTL</th>
              <th className="px-6 py-3 text-center font-semibold">PTS</th>
              <th className="px-6 py-3 text-center font-semibold">GF</th>
              <th className="px-6 py-3 text-center font-semibold">GA</th>
              <th className="px-6 py-3 text-center font-semibold">DIFF</th>
              <th className="px-6 py-3 text-center font-semibold">P%</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-nhl-blue/20">
            {sortedStandings.map((team, idx) => {
              const isPlayoffSpot = idx < 8;
              const isWildcard = idx >= 8 && idx < 10;
              
              return (
                <tr 
                  key={team.team_code}
                  className={`transition-colors hover:bg-nhl-blue/10 ${
                    isPlayoffSpot ? 'bg-green-900/10' : isWildcard ? 'bg-yellow-900/10' : ''
                  }`}
                >
                  <td className="px-6 py-4 text-center">
                    <span className={`font-bold ${
                      isPlayoffSpot ? 'text-green-400' : isWildcard ? 'text-yellow-400' : 'text-gray-400'
                    }`}>
                      {idx + 1}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <div className="font-semibold text-white">{team.team_name}</div>
                    <div className="text-xs text-gray-500">{team.team_code}</div>
                  </td>
                  <td className="px-6 py-4 text-center text-gray-300">{team.games_played}</td>
                  <td className="px-6 py-4 text-center font-semibold text-green-400">{team.wins}</td>
                  <td className="px-6 py-4 text-center font-semibold text-red-400">{team.losses}</td>
                  <td className="px-6 py-4 text-center font-semibold text-yellow-400">{team.otl}</td>
                  <td className="px-6 py-4 text-center">
                    <span className="font-bold text-nhl-ice text-lg">{team.points}</span>
                  </td>
                  <td className="px-6 py-4 text-center text-gray-300">{team.goals_for}</td>
                  <td className="px-6 py-4 text-center text-gray-300">{team.goals_against}</td>
                  <td className={`px-6 py-4 text-center font-semibold ${
                    team.goal_differential > 0 ? 'text-green-400' :
                    team.goal_differential < 0 ? 'text-red-400' : 'text-gray-400'
                  }`}>
                    {team.goal_differential > 0 ? '+' : ''}{team.goal_differential}
                  </td>
                  <td className="px-6 py-4 text-center text-gray-300">
                    {(team.points_percentage * 100).toFixed(1)}%
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {/* Legend */}
      <div className="bg-nhl-darker px-6 py-3 border-t border-nhl-blue/20 flex gap-6 text-xs">
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 bg-green-900/30 rounded"></div>
          <span className="text-gray-400">Playoff Position</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 bg-yellow-900/30 rounded"></div>
          <span className="text-gray-400">Wild Card</span>
        </div>
      </div>
    </div>
  );
}



