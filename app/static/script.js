  // document.addEventListener('DOMContentLoaded', function () {
  //   const toggleBtn = document.getElementById('theme-toggle');
  //   const body = document.body;

  //   // Set theme immediately to prevent flicker
  //   if (localStorage.getItem('theme') === 'dark') {
  //     body.classList.add('dark');
  //     toggleBtn.textContent = '☀️ Light';
  //   } else {
  //     toggleBtn.textContent = '🌙 Dark';
  //   }

  //   toggleBtn.addEventListener('click', () => {
  //     body.classList.add('theme-transition');
  //     body.classList.toggle('dark');
  //     const isDark = body.classList.contains('dark');
  //     toggleBtn.textContent = isDark ? '☀️ Light' : '🌙 Dark';
  //     localStorage.setItem('theme', isDark ? 'dark' : 'light');

  //     // Remove the transition class after animation
  //     setTimeout(() => {
  //       body.classList.remove('theme-transition');
  //     }, 400);
  //   });
  // });



  document.addEventListener('DOMContentLoaded', function () {
  const themeLink = document.getElementById('toggle-theme');
  const body = document.body;

  // Apply saved theme immediately
  if (localStorage.getItem('theme') === 'dark') {
    body.classList.add('dark');
  }

  // Add click event to the dropdown theme toggle
  themeLink.addEventListener('click', function (e) {
    e.preventDefault();
    body.classList.add('theme-transition');
    body.classList.toggle('dark');
    const isDark = body.classList.contains('dark');
    localStorage.setItem('theme', isDark ? 'dark' : 'light');

    // Smooth transition effect
    setTimeout(() => {
      body.classList.remove('theme-transition');
    }, 400);
  });
});