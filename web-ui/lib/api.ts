/**
 * API Client for NHL Simulation Game
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001';

export interface Team {
  code: string;
  name: string;
  city: string;
  division: string;
  conference: string;
  overall_strength: number;
  wins: number;
  losses: number;
  otl: number;
}

export interface GoalEvent {
  period: number;
  time_elapsed: number;
  team: string;
  scorer: string | null;
  scorer_id: number | null;
  primary_assist: string | null;
  secondary_assist: string | null;
  is_power_play: boolean;
  is_empty_net: boolean;
}

export interface PeriodSummary {
  period: number;
  home_goals: number;
  away_goals: number;
  goals: GoalEvent[];
}

export interface GameResult {
  home_team: string;
  away_team: string;
  home_score: number;
  away_score: number;
  winner: string | null;
  periods: number;
  home_shots: number;
  away_shots: number;
  period_scores: Record<string, PeriodSummary>;
  goal_scorers: string[];
}

export interface SeasonStandings {
  team_code: string;
  team_name: string;
  games_played: number;
  wins: number;
  losses: number;
  otl: number;
  points: number;
  goals_for: number;
  goals_against: number;
  goal_differential: number;
  points_percentage: number;
}

export interface Season {
  season_id: string;
  season_year: string;
  total_games: number;
  status: string;
}

/**
 * Fetch all NHL teams
 */
export async function getTeams(): Promise<Team[]> {
  const response = await fetch(`${API_BASE_URL}/teams`);
  if (!response.ok) throw new Error('Failed to fetch teams');
  return response.json();
}

/**
 * Simulate a single game
 */
export async function simulateGame(homeTeam: string, awayTeam: string): Promise<GameResult> {
  const response = await fetch(
    `${API_BASE_URL}/game/simulate?home_team=${homeTeam}&away_team=${awayTeam}`,
    { method: 'POST' }
  );
  if (!response.ok) throw new Error('Failed to simulate game');
  return response.json();
}

/**
 * Create a new season
 */
export async function createSeason(seasonYear: string = '2024-25'): Promise<Season> {
  const response = await fetch(
    `${API_BASE_URL}/season/create?season_year=${seasonYear}`,
    { method: 'POST' }
  );
  if (!response.ok) throw new Error('Failed to create season');
  return response.json();
}

/**
 * Simulate games in a season
 */
export async function simulateSeasonGames(
  seasonId: string,
  numGames: number = 10
): Promise<{ games_simulated: number; total_games_played: number; status: string }> {
  const response = await fetch(
    `${API_BASE_URL}/season/${seasonId}/simulate?num_games=${numGames}`,
    { method: 'POST' }
  );
  if (!response.ok) throw new Error('Failed to simulate season games');
  return response.json();
}

/**
 * Get season standings
 */
export async function getSeasonStandings(
  seasonId: string,
  conference?: string
): Promise<SeasonStandings[]> {
  const url = conference
    ? `${API_BASE_URL}/season/${seasonId}/standings?conference=${conference}`
    : `${API_BASE_URL}/season/${seasonId}/standings`;
  
  const response = await fetch(url);
  if (!response.ok) throw new Error('Failed to fetch standings');
  return response.json();
}

/**
 * Get season games
 */
export async function getSeasonGames(
  seasonId: string,
  playedOnly: boolean = false
): Promise<{ season_id: string; games: any[] }> {
  const response = await fetch(
    `${API_BASE_URL}/season/${seasonId}/games?played_only=${playedOnly}`
  );
  if (!response.ok) throw new Error('Failed to fetch games');
  return response.json();
}

/**
 * Generate playoff bracket from season standings
 */
export async function generatePlayoffs(
  seasonId: string
): Promise<{ playoff_id: string; bracket: any; status: string }> {
  const response = await fetch(
    `${API_BASE_URL}/season/${seasonId}/playoffs/generate`,
    { method: 'POST' }
  );
  if (!response.ok) throw new Error('Failed to generate playoffs');
  return response.json();
}

/**
 * Simulate a playoff round
 */
export async function simulatePlayoffRound(
  playoffId: string,
  roundNumber: number
): Promise<{ playoff_id: string; bracket: any; status: string }> {
  const response = await fetch(
    `${API_BASE_URL}/playoffs/${playoffId}/simulate/round?round_number=${roundNumber}`,
    { method: 'POST' }
  );
  if (!response.ok) throw new Error('Failed to simulate playoff round');
  return response.json();
}

/**
 * Simulate all remaining playoffs
 */
export async function simulateAllPlayoffs(
  playoffId: string
): Promise<{ playoff_id: string; bracket: any; champion: string; status: string }> {
  const response = await fetch(
    `${API_BASE_URL}/playoffs/${playoffId}/simulate/all`,
    { method: 'POST' }
  );
  if (!response.ok) throw new Error('Failed to simulate playoffs');
  return response.json();
}

/**
 * Get playoff bracket status
 */
export async function getPlayoffBracket(
  playoffId: string
): Promise<{ playoff_id: string; bracket: any; champion: string | null; status: string }> {
  const response = await fetch(
    `${API_BASE_URL}/playoffs/${playoffId}/bracket`
  );
  if (!response.ok) throw new Error('Failed to fetch bracket');
  return response.json();
}

/**
 * Get league leaders for a specific stat
 */
export async function getLeagueLeaders(
  seasonId: string,
  stat: string = 'points',
  limit: number = 10
): Promise<{ leaders: any[] }> {
  const response = await fetch(
    `${API_BASE_URL}/season/${seasonId}/stats/leaders?stat=${stat}&limit=${limit}`
  );
  if (!response.ok) throw new Error('Failed to fetch leaders');
  return response.json();
}

/**
 * Get team player stats
 */
export async function getTeamPlayerStats(
  seasonId: string,
  teamCode: string
): Promise<{ players: any[] }> {
  const response = await fetch(
    `${API_BASE_URL}/season/${seasonId}/stats/team/${teamCode}`
  );
  if (!response.ok) throw new Error('Failed to fetch team stats');
  return response.json();
}


