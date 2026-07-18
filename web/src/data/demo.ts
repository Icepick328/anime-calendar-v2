export type Release = {
  title: string;
  episode: string;
  time: string;
  provider: string;
  kind: "Sub" | "Dub" | "Movie";
};

export type WatchingItem = {
  title: string;
  progress: number;
  total: number;
  nextEpisode: string;
  available: boolean;
};

export const todayReleases: Release[] = [
  { title: "Frieren: Beyond Journey's End", episode: "Episode 19", time: "8:00 AM", provider: "Crunchyroll", kind: "Dub" },
  { title: "One Piece", episode: "Episode 1151", time: "10:00 AM", provider: "Crunchyroll", kind: "Sub" },
  { title: "DAN DA DAN", episode: "Episode 15", time: "12:30 PM", provider: "Netflix", kind: "Sub" },
  { title: "The Apothecary Diaries", episode: "Episode 38", time: "5:00 PM", provider: "Crunchyroll", kind: "Dub" },
];

export const upcomingReleases: Release[] = [
  { title: "Kaiju No. 8", episode: "Season 2 Premiere", time: "Tomorrow · 7:00 AM", provider: "Crunchyroll", kind: "Sub" },
  { title: "My Dress-Up Darling", episode: "Episode 16", time: "Tomorrow · 9:30 AM", provider: "Crunchyroll", kind: "Sub" },
  { title: "Demon Slayer: Infinity Castle", episode: "Movie", time: "Saturday · 6:00 PM", provider: "Theatrical", kind: "Movie" },
];

export const continueWatching: WatchingItem[] = [
  { title: "Frieren: Beyond Journey's End", progress: 18, total: 28, nextEpisode: "Episode 19", available: true },
  { title: "The Apothecary Diaries", progress: 36, total: 48, nextEpisode: "Episode 37", available: true },
  { title: "One Piece", progress: 1148, total: 1151, nextEpisode: "Episode 1149", available: true },
];
