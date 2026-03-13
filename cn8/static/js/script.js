/*
  CareerNova — Global JavaScript utilities
*/

// Generic circular progress bar drawer
function drawCircleProgress(canvasId, percentage, color) {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const cx = canvas.width / 2;
  const cy = canvas.height / 2;
  const radius = cx - 10;
  const startAngle = -Math.PI / 2;

  let current = 0;
  const target = percentage;
  const step = target / 60;

  function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Background track
    ctx.beginPath();
    ctx.arc(cx, cy, radius, 0, 2 * Math.PI);
    ctx.strokeStyle = 'rgba(255,255,255,0.06)';
    ctx.lineWidth = 8;
    ctx.stroke();

    // Progress arc
    ctx.beginPath();
    ctx.arc(cx, cy, radius, startAngle, startAngle + (2 * Math.PI * (current / 100)));
    ctx.strokeStyle = color;
    ctx.lineWidth = 8;
    ctx.lineCap = 'round';
    ctx.stroke();

    if (current < target) {
      current = Math.min(current + step, target);
      requestAnimationFrame(draw);
    }
  }
  draw();
}

// Animate all progress bars (class .progress-fill with data-pct attribute)
function animateProgressBars() {
  document.querySelectorAll('[data-pct]').forEach(el => {
    const pct = parseFloat(el.getAttribute('data-pct'));
    if (!isNaN(pct)) {
      setTimeout(() => {
        el.style.width = pct + '%';
      }, 300);
    }
  });
}

document.addEventListener('DOMContentLoaded', animateProgressBars);
