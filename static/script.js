document.addEventListener("DOMContentLoaded", function() {
  // Chat functionality
  initializeChat();
  
  // Dynamic content loading
  loadDynamicContent();
  
  // Smooth scrolling for navigation
  initializeSmoothScrolling();
  
  // Theme toggle (if implemented)
  initializeThemeToggle();
  
  // Typing animation for hero text
  initializeTypingAnimation();
});

function initializeChat() {
  const chatWidget = document.querySelector('.chat-widget');
  const chatHeader = document.querySelector('.chat-header');
  const chatBody = document.querySelector('.chat-body');
  const inputField = document.getElementById("chat-input-field");
  const sendBtn = document.getElementById("chat-send-btn");
  const messagesDiv = document.getElementById("chat-messages");
  
  let isCollapsed = false;
  let isTyping = false;

  // Toggle chat widget
  chatHeader.addEventListener("click", () => {
    isCollapsed = !isCollapsed;
    chatWidget.classList.toggle("collapsed", isCollapsed);
    if (!isCollapsed) {
      inputField.focus();
    }
  });

  // Auto-focus on chat open
  chatHeader.addEventListener("click", () => {
    if (!isCollapsed) {
      setTimeout(() => inputField.focus(), 300);
    }
  });

  function appendMessage(sender, text, isHTML = false) {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("chat-message", sender);
    
    if (isHTML) {
      messageDiv.innerHTML = text;
    } else {
      messageDiv.textContent = text;
    }
    
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
  }

  function showTypingIndicator() {
    if (isTyping) return;
    isTyping = true;
    const typingDiv = document.createElement("div");
    typingDiv.classList.add("chat-message", "bot", "typing");
    typingDiv.innerHTML = '<div class="loading"></div> <span style="margin-left: 10px;">Surya is typing...</span>';
    messagesDiv.appendChild(typingDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
  }

  function hideTypingIndicator() {
    const typingIndicator = messagesDiv.querySelector('.typing');
    if (typingIndicator) {
      typingIndicator.remove();
    }
    isTyping = false;
  }

  async function sendMessage() {
    const msg = inputField.value.trim();
    if (!msg || isTyping) return;
    
    appendMessage("user", msg);
    inputField.value = "";
    showTypingIndicator();

    try {
      const resp = await fetch("/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: msg })
      });
      
      const data = await resp.json();
      hideTypingIndicator();
      
      if (data.answer) {
        // Format the response with better styling
        const formattedAnswer = formatBotResponse(data.answer);
        appendMessage("bot", formattedAnswer, true);
      } else {
        appendMessage("bot", "Sorry, I encountered an error. Please try again.");
      }
    } catch (err) {
      hideTypingIndicator();
      appendMessage("bot", "Sorry, I'm having trouble connecting. Please check your internet connection.");
    }
  }

  function formatBotResponse(text) {
    // Convert markdown-like formatting to HTML
    return text
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\n\n/g, '</p><p>')
      .replace(/\n/g, '<br>')
      .replace(/^(.*)$/, '<p>$1</p>');
  }

  sendBtn.addEventListener("click", sendMessage);

  inputField.addEventListener("keypress", function(e) {
    if (e.key === "Enter") {
      e.preventDefault();
      sendMessage();
    }
  });

  // Auto-resize input field
  inputField.addEventListener("input", function() {
    this.style.height = "auto";
    this.style.height = this.scrollHeight + "px";
  });

  // Welcome message
  setTimeout(() => {
    appendMessage("bot", "👋 Hi! I'm Surya's AI assistant. Ask me anything about his projects, skills, or experience!");
  }, 1000);
}

function loadDynamicContent() {
  // Load projects dynamically if on projects page
  if (window.location.pathname.includes('/projects')) {
    loadProjects();
  }
  
  // Load skills dynamically
  loadSkills();
}

async function loadProjects() {
  try {
    const response = await fetch('/api/projects');
    const projects = await response.json();
    
    const projectGrid = document.querySelector('.project-grid');
    if (!projectGrid) return;
    
    projectGrid.innerHTML = '';
    
    projects.forEach(project => {
      const projectCard = createProjectCard(project);
      projectGrid.appendChild(projectCard);
    });
  } catch (error) {
    console.error('Error loading projects:', error);
  }
}

function createProjectCard(project) {
  const card = document.createElement('div');
  card.classList.add('project-card');
  card.innerHTML = `
    <h3>${project.name}</h3>
    <p>${project.description}</p>
    <div class="tech-stack">
      ${project.tech_stack.map(tech => `<span class="tech-tag">${tech}</span>`).join('')}
    </div>
    <div class="project-links">
      ${project.github ? `<a href="${project.github}" target="_blank" class="project-link">GitHub</a>` : ''}
      ${project.demo ? `<a href="${project.demo}" target="_blank" class="project-link">Live Demo</a>` : ''}
    </div>
  `;
  return card;
}

async function loadSkills() {
  try {
    const response = await fetch('/api/skills');
    const skills = await response.json();
    
    const skillsContainer = document.querySelector('.skills-container');
    if (!skillsContainer) return;
    
    skillsContainer.innerHTML = '';
    
    Object.entries(skills).forEach(([category, skillList]) => {
      const skillCategory = createSkillCategory(category, skillList);
      skillsContainer.appendChild(skillCategory);
    });
  } catch (error) {
    console.error('Error loading skills:', error);
  }
}

function createSkillCategory(category, skills) {
  const categoryDiv = document.createElement('div');
  categoryDiv.classList.add('skill-category');
  
  const categoryName = category.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
  
  categoryDiv.innerHTML = `
    <h3>${categoryName}</h3>
    <div class="skill-list">
      ${skills.map(skill => `<span class="skill-item">${skill}</span>`).join('')}
    </div>
  `;
  
  return categoryDiv;
}

function initializeSmoothScrolling() {
  // Smooth scrolling for navigation links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });
}

function initializeThemeToggle() {
  // Theme toggle functionality (can be extended)
  const themeToggle = document.querySelector('.theme-toggle');
  if (themeToggle) {
    themeToggle.addEventListener('click', function() {
      document.body.classList.toggle('light-theme');
      localStorage.setItem('theme', document.body.classList.contains('light-theme') ? 'light' : 'dark');
    });
    
    // Load saved theme
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'light') {
      document.body.classList.add('light-theme');
    }
  }
}

function initializeTypingAnimation() {
  const dynamicName = document.getElementById('dynamic-name');
  if (dynamicName) {
    const name = dynamicName.textContent;
    dynamicName.textContent = '';
    let i = 0;
    
    function typeWriter() {
      if (i < name.length) {
        dynamicName.textContent += name.charAt(i);
        i++;
        setTimeout(typeWriter, 100);
      }
    }
    
    // Start typing animation after a delay
    setTimeout(typeWriter, 1000);
  }
}

// Intersection Observer for animations
function initializeScrollAnimations() {
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
      }
    });
  }, observerOptions);

  // Observe elements for scroll animations
  document.querySelectorAll('.project-card, .skill-category, section').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(30px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(el);
  });
}

// Initialize scroll animations when DOM is loaded
document.addEventListener('DOMContentLoaded', initializeScrollAnimations);

// Utility functions
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

// Handle window resize
window.addEventListener('resize', debounce(() => {
  // Recalculate any size-dependent elements
  const chatWidget = document.querySelector('.chat-widget');
  if (chatWidget && window.innerWidth < 768) {
    chatWidget.style.width = 'calc(100vw - 20px)';
  }
}, 250));

// Add some interactive effects
document.addEventListener('mousemove', (e) => {
  const cursor = document.querySelector('.custom-cursor');
  if (cursor) {
    cursor.style.left = e.clientX + 'px';
    cursor.style.top = e.clientY + 'px';
  }
});

// Performance optimization: Lazy load images
function lazyLoadImages() {
  const images = document.querySelectorAll('img[data-src]');
  const imageObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const img = entry.target;
        img.src = img.dataset.src;
        img.removeAttribute('data-src');
        imageObserver.unobserve(img);
      }
    });
  });

  images.forEach(img => imageObserver.observe(img));
}
document.addEventListener('DOMContentLoaded', lazyLoadImages);
