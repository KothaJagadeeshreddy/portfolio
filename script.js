// Toggle navbar in mobile view
let menu = document.querySelector('#menu');
let navbar = document.querySelector('.navbar');

menu.onclick = () => {
  menu.classList.toggle('fa-times');
  navbar.classList.toggle('active');
};

// Remove toggle on scroll or link click
window.onscroll = () => {
  menu.classList.remove('fa-times');
  navbar.classList.remove('active');

  // Scroll to top button toggle
  let scrollTop = document.querySelector('#scroll-top');
  if (window.scrollY > 300) {
    scrollTop.style.display = 'block';
  } else {
    scrollTop.style.display = 'none';
  }

  // Active link switching on scroll
  let sections = document.querySelectorAll('section');
  let navLinks = document.querySelectorAll('header nav ul li a');

  sections.forEach((sec) => {
    let top = window.scrollY;
    let offset = sec.offsetTop - 150;
    let height = sec.offsetHeight;
    let id = sec.getAttribute('id');

    if (top >= offset && top < offset + height) {
      navLinks.forEach((link) => {
        link.classList.remove('active');
        document
          .querySelector('header nav ul li a[href*=' + id + ']')
          .classList.add('active');
      });
    }
  });
};

// Scroll to top button
document.querySelector('#scroll-top').onclick = () => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
};

// Typing text effect
const typedText = document.querySelector('.typing-text');
const typingPhrases = ['Software Development', 'Java Enthusiast', 'Problem Solver', 'Tech Learner'];
let index = 0, charIndex = 0;
let isDeleting = false;
let delay = 100;

function typeEffect() {
  if (typedText) {
    let currentPhrase = typingPhrases[index];
    if (isDeleting) {
      typedText.textContent = currentPhrase.substring(0, charIndex--);
      delay = 60;
    } else {
      typedText.textContent = currentPhrase.substring(0, charIndex++);
      delay = 100;
    }

    if (!isDeleting && charIndex === currentPhrase.length) {
      delay = 1500;
      isDeleting = true;
    } else if (isDeleting && charIndex === 0) {
      isDeleting = false;
      index = (index + 1) % typingPhrases.length;
      delay = 500;
    }

    setTimeout(typeEffect, delay);
  }
}
typeEffect();

// Tilt effect (requires vanilla-tilt.js or similar lib)
const tiltImages = document.querySelectorAll('.tilt');
tiltImages.forEach((img) => {
  VanillaTilt.init(img, {
    max: 15,
    speed: 400,
    glare: true,
    'max-glare': 0.2,
  });
});
