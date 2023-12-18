
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        console.log(entry)
        if (entry.isIntersecting) 
        {
          entry.target.classList.add("show");
        }
        else
        {
          entry.target.classList.remove("show");
        }
      });
    });
    const hiddenElements = document.querySelectorAll('.hidden');
    hiddenElements.forEach((element) => {
      observer.observe(element);
    });






// JavaScript code
document.addEventListener('DOMContentLoaded', function() {
  // Get the current URL path
  var currentPath = window.location.pathname;

  // Array of navigation links and their corresponding identifiers
  var navLinks = [
      { url: '/', identifier: 'home' },
      { url: '/ftpEngine', identifier: 'free_games' },
      { url: '/Pengine', identifier: 'games' },
      { url: '/recommendations', identifier: 'recommend' }
  ];

  // Loop through the navigation links and add the 'active' class to the matching link
  for (var i = 0; i < navLinks.length; i++) {
      var navLink = navLinks[i];
      var linkElement = document.querySelector('a[href="' + navLink.url + '"]');

      if (linkElement && currentPath === navLink.url) {
          linkElement.classList.add('active');
      }
  }
});
