// Configuration for API endpoints and IDs. Replace with your provider values.
const API_CONFIG = {
  BASE_URL: 'https://api.example.com',
  API_KEY: 'YOUR_API_KEY',
  TEAM_ID: '1610612743', // Denver Nuggets
  PLAYER_ID: '203999', // Nikola Jokic
  AUTO_REFRESH_INTERVAL: 30000,
};

const apiClient = {
  async fetchCurrentNuggetsGame() {
    const url = `${API_CONFIG.BASE_URL}/nuggets/current-game?teamId=${API_CONFIG.TEAM_ID}`;
    try {
      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': API_CONFIG.API_KEY,
        },
      });

      if (!response.ok) {
        console.error('Bad response fetching game info', response.status);
        return null;
      }

      const data = await response.json();
      return transformGameResponse(data);
    } catch (error) {
      console.error('Network error fetching game info', error);
      return null;
    }
  },

  async fetchJokicStatsForGame(gameId) {
    const url = `${API_CONFIG.BASE_URL}/nuggets/game-stats?teamId=${API_CONFIG.TEAM_ID}&playerId=${API_CONFIG.PLAYER_ID}&gameId=${gameId ?? ''}`;
    try {
      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': API_CONFIG.API_KEY,
        },
      });

      if (!response.ok) {
        console.error('Bad response fetching Jokic stats', response.status);
        return null;
      }

      const data = await response.json();
      return transformJokicStatsResponse(data);
    } catch (error) {
      console.error('Network error fetching Jokic stats', error);
      return null;
    }
  },
};

function transformGameResponse(data) {
  if (!data) return null;

  const game = data.game ?? {};
  const status = game.status ?? 'unknown';
  const isGameToday = Boolean(game.isToday);
  const isLive = status === 'in_progress';
  const isFinal = status === 'final';
  const nuggetsAreHome = game.homeTeam === 'Nuggets';

  return {
    isGameToday,
    isGameLive: isLive,
    gameStatus: status,
    startTimeLocal: game.startTimeLocal ?? 'TBD',
    homeTeam: game.homeTeam ?? 'Nuggets',
    awayTeam: game.awayTeam ?? 'Opponent',
    nuggetsAreHome,
    score: {
      nuggets: Number(game.nuggetsScore ?? 0),
      opponent: Number(game.opponentScore ?? 0),
    },
    period: Number(game.period ?? 0),
    timeRemaining: game.timeRemaining ?? '',
    opponentName: game.opponentName ?? 'Opponent',
    gameId: game.id ?? null,
    isFinal,
  };
}

function transformJokicStatsResponse(data) {
  if (!data) return null;

  const stats = data.stats ?? {};
  return {
    playerName: stats.playerName ?? 'Nikola Jokic',
    points: Number(stats.points ?? 0),
    rebounds: Number(stats.rebounds ?? 0),
    assists: Number(stats.assists ?? 0),
    fieldGoalPercentage: Number(stats.fieldGoalPercentage ?? 0),
    threePointPercentage: Number(stats.threePointPercentage ?? 0),
    freeThrowPercentage: Number(stats.freeThrowPercentage ?? 0),
    isFinal: Boolean(stats.isFinal),
  };
}

const state = {
  gameInfo: null,
  jokicStats: null,
  loading: false,
  error: false,
  autoRefreshId: null,
  generatedMessage: 'Tap the button to craft a message.',
};

async function loadData() {
  setLoading(true);
  setError(false);
  renderLoading(true);

  const gameInfo = await apiClient.fetchCurrentNuggetsGame();
  state.gameInfo = gameInfo;

  if (!gameInfo) {
    setError(true);
    setLoading(false);
    render();
    return;
  }

  const jokicStats = await apiClient.fetchJokicStatsForGame(gameInfo.gameId);
  state.jokicStats = jokicStats;

  setLoading(false);
  render();
}

function setLoading(value) {
  state.loading = value;
}

function setError(value) {
  state.error = value;
}

function renderLoading(isLoading) {
  const loadingText = document.getElementById('loading-text');
  if (loadingText) loadingText.hidden = !isLoading;
}

function render() {
  const { gameInfo, jokicStats, loading, error } = state;
  const statusText = document.getElementById('status-text');
  const statusSubtext = document.getElementById('status-subtext');
  const statusDot = document.getElementById('status-dot');
  const errorText = document.getElementById('error-text');
  const scoreSection = document.getElementById('score-and-stats-section');
  const periodTime = document.getElementById('period-time');

  if (!statusText || !statusSubtext || !statusDot) return;

  errorText.hidden = !error;
  renderLoading(loading);

  if (error || !gameInfo) {
    statusText.textContent = 'Having trouble fetching the game right now.';
    statusSubtext.textContent = 'Try again in a few seconds.';
    setStatusDot(statusDot, 'idle');
    toggleScoreSection(false);
    return;
  }

  const { isGameToday, isGameLive, isFinal, opponentName, timeRemaining, period, nuggetsAreHome } = gameInfo;
  const opponentLabel = document.getElementById('opponent-label');
  opponentLabel.textContent = opponentName ?? 'Opponent';

  updateScore(gameInfo);
  updateStats(jokicStats);

  if (!isGameToday) {
    statusText.textContent = 'No Nuggets game right now.';
    statusSubtext.textContent = 'Check back later or hit refresh to be sure.';
    setStatusDot(statusDot, 'idle');
    toggleScoreSection(false);
    return;
  }

  if (!isGameLive && !isFinal) {
    statusText.textContent = 'The Nuggets start soon.';
    statusSubtext.textContent = `${nuggetsAreHome ? 'Home' : 'Road'} vs ${opponentName}. Tip at ${gameInfo.startTimeLocal}.`;
    setStatusDot(statusDot, 'upcoming');
    toggleScoreSection(false);
    return;
  }

  const nuggetsScore = gameInfo.score.nuggets;
  const opponentScore = gameInfo.score.opponent;
  statusText.textContent = isFinal ? 'Game finished.' : 'The Nuggets are playing right now!';
  const periodLabel = isFinal ? 'Final' : `Q${period}`;
  const timeLabel = isFinal ? 'Ended' : timeRemaining || 'In progress';
  statusSubtext.textContent = `${opponentName} | ${periodLabel} • ${timeLabel}`;
  setStatusDot(statusDot, isFinal ? 'final' : 'live');

  periodTime.textContent = `${nuggetsAreHome ? 'DEN' : opponentName} vs ${nuggetsAreHome ? opponentName : 'DEN'} • ${periodLabel}`;
  toggleScoreSection(true);
}

function updateScore(gameInfo) {
  const nuggetsScoreEl = document.getElementById('nuggets-score');
  const opponentScoreEl = document.getElementById('opponent-score');
  if (!nuggetsScoreEl || !opponentScoreEl || !gameInfo) return;

  nuggetsScoreEl.textContent = gameInfo.score.nuggets ?? '--';
  opponentScoreEl.textContent = gameInfo.score.opponent ?? '--';
}

function updateStats(jokicStats) {
  const pts = document.getElementById('pts');
  const reb = document.getElementById('reb');
  const ast = document.getElementById('ast');
  const fgp = document.getElementById('fgp');
  const tpp = document.getElementById('tpp');
  const ftp = document.getElementById('ftp');
  const statsNote = document.getElementById('stats-note');

  if (!pts || !reb || !ast || !fgp || !tpp || !ftp || !statsNote) return;

  if (!jokicStats) {
    pts.textContent = reb.textContent = ast.textContent = '--';
    fgp.textContent = 'FG%: --';
    tpp.textContent = '3P%: --';
    ftp.textContent = 'FT%: --';
    statsNote.textContent = '';
    return;
  }

  pts.textContent = jokicStats.points;
  reb.textContent = jokicStats.rebounds;
  ast.textContent = jokicStats.assists;
  fgp.textContent = `FG%: ${jokicStats.fieldGoalPercentage?.toFixed?.(1) ?? '--'}`;
  tpp.textContent = `3P%: ${jokicStats.threePointPercentage?.toFixed?.(1) ?? '--'}`;
  ftp.textContent = `FT%: ${jokicStats.freeThrowPercentage?.toFixed?.(1) ?? '--'}`;
  statsNote.textContent = jokicStats.isFinal ? 'Final stats' : 'Live stats';
}

function toggleScoreSection(show) {
  const section = document.getElementById('score-and-stats-section');
  if (section) section.hidden = !show;
}

function setStatusDot(dotEl, mode) {
  const colorMap = {
    live: '#2bd1ff',
    upcoming: '#f2a900',
    final: '#9ac0ff',
    idle: '#cfd9e2',
  };

  dotEl.style.background = colorMap[mode] ?? '#cfd9e2';
}

function generateDadTextMessage({ gameStatus, score, period, timeRemaining, jokicStats }) {
  const nuggetsScore = score?.nuggets ?? 0;
  const oppScore = score?.opponent ?? 0;
  const diff = nuggetsScore - oppScore;
  const isClose = Math.abs(diff) <= 5;
  const isAhead = diff > 0;

  const periodLabel = period >= 4 ? 'fourth' : period >= 3 ? 'third' : 'first half';
  const timeLabel = timeRemaining || 'right now';
  const line = `${jokicStats?.points ?? 0}-${jokicStats?.rebounds ?? 0}-${jokicStats?.assists ?? 0}`;

  if (gameStatus === 'no_game' || !gameStatus) {
    return "No game tonight, but Jokic still looks like an MVP. The way he's been running the offense is ridiculous.";
  }

  if (gameStatus === 'upcoming') {
    return `They tip soon vs ${state.gameInfo?.opponentName || 'a tough opponent'}. Curious to see if Jokic starts hunting assists early after the last game.`;
  }

  if (gameStatus === 'final') {
    const verdict = isAhead ? 'pulled it out' : 'couldn't get stops late';
    return `Final vs ${state.gameInfo?.opponentName || 'them'}: ${nuggetsScore}-${oppScore}. Jokic went ${line} and ${verdict}.`;
  }

  if (isClose) {
    return `Tight one in the ${periodLabel}, ${nuggetsScore}-${oppScore} with ${timeLabel} left. Jokic is at ${line} and running everything through the elbow.`;
  }

  if (isAhead) {
    return `Nuggets up ${Math.abs(diff)} in the ${periodLabel}, ${nuggetsScore}-${oppScore}. Jokic already at ${line}; they're feasting on cutters.`;
  }

  return `Down ${Math.abs(diff)} right now, ${nuggetsScore}-${oppScore}. Jokic is ${line} but the perimeter defense has been leaky.`;
}

function handleGenerateMessage() {
  const gameInfo = state.gameInfo;
  const jokicStats = state.jokicStats;

  const gameStatus = !gameInfo
    ? 'no_game'
    : !gameInfo.isGameToday
    ? 'no_game'
    : gameInfo.isFinal
    ? 'final'
    : gameInfo.isGameLive
    ? 'live'
    : 'upcoming';

  const message = generateDadTextMessage({
    gameStatus,
    score: gameInfo?.score,
    period: gameInfo?.period,
    timeRemaining: gameInfo?.timeRemaining,
    jokicStats,
  });

  state.generatedMessage = message;
  const messageText = document.getElementById('message-text');
  if (messageText) messageText.textContent = message;
}

async function copyMessage() {
  const feedback = document.getElementById('copy-feedback');
  const messageText = document.getElementById('message-text');
  if (!messageText) return;

  const text = messageText.textContent;
  if (!text) return;

  try {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      await navigator.clipboard.writeText(text);
      feedback.textContent = 'Copied!';
    } else {
      const range = document.createRange();
      range.selectNodeContents(messageText);
      const selection = window.getSelection();
      selection.removeAllRanges();
      selection.addRange(range);
      feedback.textContent = 'Copied! If not, press Ctrl/Cmd+C.';
    }
  } catch (err) {
    console.error('Copy failed', err);
    feedback.textContent = 'Could not copy. Select the text and copy manually.';
  }
}

function setupListeners() {
  const refreshBtn = document.getElementById('refresh-btn');
  const generateBtn = document.getElementById('generate-message-btn');
  const copyBtn = document.getElementById('copy-btn');
  const autoRefreshToggle = document.getElementById('auto-refresh-toggle');

  refreshBtn?.addEventListener('click', loadData);
  generateBtn?.addEventListener('click', handleGenerateMessage);
  copyBtn?.addEventListener('click', copyMessage);
  autoRefreshToggle?.addEventListener('change', (e) => {
    if (e.target.checked) {
      startAutoRefresh();
    } else {
      stopAutoRefresh();
    }
  });
}

function startAutoRefresh() {
  stopAutoRefresh();
  state.autoRefreshId = setInterval(loadData, API_CONFIG.AUTO_REFRESH_INTERVAL);
}

function stopAutoRefresh() {
  if (state.autoRefreshId) {
    clearInterval(state.autoRefreshId);
    state.autoRefreshId = null;
  }
}

document.addEventListener('visibilitychange', () => {
  const autoToggle = document.getElementById('auto-refresh-toggle');
  if (document.hidden) {
    stopAutoRefresh();
  } else if (autoToggle?.checked) {
    startAutoRefresh();
  }
});

function init() {
  setupListeners();
  loadData();
}

document.addEventListener('DOMContentLoaded', init);
