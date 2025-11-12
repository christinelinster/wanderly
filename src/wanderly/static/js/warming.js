// Poll /ready until it returns 200, then redirect to the app's login page.
const poll = async (attempt = 1) => {
  const attemptsEl = document.getElementById('attempts');
  if (attemptsEl) {
    attemptsEl.textContent = `Attempt ${attempt} — checking readiness...`;
  }

  try {
    const res = await fetch('/ready', { method: 'GET', cache: 'no-store' });
    if (res.ok) {
      window.location = '/login';
    } else {
      setTimeout(() => poll(attempt + 1), 5000);
    }
  } catch {
    setTimeout(() => poll(attempt + 1), 5000);
  }
};

poll();
