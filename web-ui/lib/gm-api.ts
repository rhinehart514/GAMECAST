/**
 * GM Mode API Client
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001';

export interface GMCareer {
  career_id: string;
  gm_name: string;
  team_code: string;
  team_name: string;
  current_season: string;
  seasons_completed: number;
  total_wins: number;
  total_losses: number;
  total_otl: number;
  win_percentage: number;
  playoff_appearances: number;
  championship_count: number;
  championships: string[];
  season_records: Record<string, any>;
  created_at: string;
}

export interface Player {
  player_id: number;
  name: string;
  position: string;
  overall_rating: number;
  offensive_rating: number;
  defensive_rating: number;
}

export interface GMCareerSummary {
  career: GMCareer;
  team: {
    code: string;
    name: string;
    full_name: string;
    city: string;
    conference: string;
    division: string;
    overall_strength: number;
    roster_size: number;
  };
  achievements: {
    seasons_played: number;
    playoff_rate: number;
    championships: number;
  };
}

/**
 * Create a new GM career
 */
export async function createGMCareer(
  gmName: string,
  teamCode: string,
  seasonYear: string = '2024-25'
): Promise<{ career_id: string; gm_name: string; team_code: string; team_name: string; season_year: string; status: string }> {
  const response = await fetch(
    `${API_BASE_URL}/gm/create?gm_name=${encodeURIComponent(gmName)}&team_code=${teamCode}&season_year=${seasonYear}`,
    { method: 'POST' }
  );
  if (!response.ok) throw new Error('Failed to create GM career');
  return response.json();
}

/**
 * Get GM career details
 */
export async function getGMCareer(careerId: string): Promise<GMCareerSummary> {
  const response = await fetch(`${API_BASE_URL}/gm/${careerId}`);
  if (!response.ok) throw new Error('Failed to fetch GM career');
  return response.json();
}

/**
 * Get GM team roster
 */
export async function getGMRoster(careerId: string): Promise<{ career_id: string; team_code: string; team_name: string; roster: Player[] }> {
  const response = await fetch(`${API_BASE_URL}/gm/${careerId}/roster`);
  if (!response.ok) throw new Error('Failed to fetch roster');
  return response.json();
}

/**
 * Update player rating
 */
export async function updatePlayerRating(
  careerId: string,
  playerId: number,
  overall?: number,
  offensive?: number,
  defensive?: number
): Promise<Player> {
  const params = new URLSearchParams();
  if (overall !== undefined) params.append('overall', overall.toString());
  if (offensive !== undefined) params.append('offensive', offensive.toString());
  if (defensive !== undefined) params.append('defensive', defensive.toString());

  const response = await fetch(
    `${API_BASE_URL}/gm/${careerId}/player/${playerId}?${params.toString()}`,
    { method: 'PUT' }
  );
  if (!response.ok) throw new Error('Failed to update player');
  return response.json();
}

/**
 * List all GM careers
 */
export async function listGMCareers(): Promise<{ careers: Array<{ career_id: string; gm_name: string; team_code: string; team_name: string; seasons_completed: number; championships: number }> }> {
  const response = await fetch(`${API_BASE_URL}/gm/careers`);
  if (!response.ok) throw new Error('Failed to list careers');
  return response.json();
}

