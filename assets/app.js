// NeuroInsight Hub - JavaScript Application Logic (Fixed Navigation)

// Application data from the provided JSON
const appData = {
  company_metrics: {
    total_employees: 1247,
    neurodiverse_employees: 187,
    neurodiverse_percentage: 15.0,
    adhd_employees: 89,
    autism_employees: 52,
    dyslexia_employees: 46,
    retention_rate: 92.3,
    satisfaction_score: 4.2,
    productivity_increase: 18.5
  },
  adhd_statistics: {
    global_prevalence: 5.0,
    france_adults: 3.0,
    france_children: 3.5,
    male_female_ratio: 2.3,
    persistence_adulthood: 66.0,
    comorbidity_rate: 50.0
  },
  autism_statistics: {
    global_prevalence: 1.0,
    employment_rate: 22.0,
    unemployment_rate: 85.0,
    europe_population: 7000000,
    workplace_participation: 42.0
  },
  performance_metrics: [
    {
      department: "IT",
      neurodiverse_ratio: 22.4,
      productivity_index: 118.7,
      innovation_score: 8.9,
      team_satisfaction: 4.3
    },
    {
      department: "Design",
      neurodiverse_ratio: 28.1,
      productivity_index: 125.2,
      innovation_score: 9.4,
      team_satisfaction: 4.5
    },
    {
      department: "Finance",
      neurodiverse_ratio: 11.8,
      productivity_index: 108.3,
      innovation_score: 7.1,
      team_satisfaction: 3.9
    }
  ]
};

// Initialize application when DOM loads
document.addEventListener('DOMContentLoaded', function() {
  initializeNavigation();
  initializeCharts();
  initializeForms();
  initializeInteractiveElements();
});

// Fixed Navigation Management
function initializeNavigation() {
  const navItems = document.querySelectorAll('.nav-item[data-module]');
  const modules = document.querySelectorAll('.module');

  // Ensure all modules are hidden except dashboard initially
  modules.forEach(module => {
    module.classList.remove('active');
  });
  document.getElementById('dashboard').classList.add('active');

  navItems.forEach(item => {
    item.addEventListener('click', function(e) {
      e.preventDefault();
      
      const moduleId = this.getAttribute('data-module');
      console.log('Clicking module:', moduleId); // Debug log
      
      // Verify the module exists
      const targetModule = document.getElementById(moduleId);
      if (!targetModule) {
        console.error('Module not found:', moduleId);
        return;
      }
      
      // Remove active class from all nav items and modules
      navItems.forEach(nav => nav.classList.remove('active'));
      modules.forEach(module => module.classList.remove('active'));
      
      // Add active class to clicked nav item
      this.classList.add('active');
      
      // Show corresponding module
      targetModule.classList.add('active');
      
      // Initialize module-specific functionality
      initializeModuleContent(moduleId);
    });
  });
}

// Initialize module-specific content
function initializeModuleContent(moduleId) {
  switch(moduleId) {
    case 'dashboard':
      updateDashboardMetrics();
      // Recreate charts if they don't exist
      setTimeout(() => {
        if (!document.querySelector('#diversityChart canvas').chart) {
          createDiversityChart();
          createDepartmentChart();
        }
      }, 100);
      break;
    case 'observatoire':
      setTimeout(() => {
        createEvolutionChart();
      }, 100);
      break;
    case 'tdah':
      // Reset form if needed
      const tdahForm = document.getElementById('tdahForm');
      if (tdahForm) {
        tdahForm.reset();
        document.getElementById('tdahResult').classList.add('hidden');
      }
      break;
    case 'autisme':
      // Reset form if needed
      const autismeForm = document.getElementById('autismeForm');
      if (autismeForm) {
        autismeForm.reset();
        document.getElementById('autismeResult').classList.add('hidden');
      }
      break;
  }
}

// Chart Initialization
function initializeCharts() {
  // Wait for DOM to be fully loaded
  setTimeout(() => {
    createDiversityChart();
    createDepartmentChart();
  }, 100);
}

// Diversity Distribution Chart
function createDiversityChart() {
  const canvas = document.querySelector('#diversityChart canvas');
  if (!canvas) {
    console.error('Diversity chart canvas not found');
    return;
  }

  // Destroy existing chart if it exists
  if (canvas.chart) {
    canvas.chart.destroy();
  }

  const ctx = canvas.getContext('2d');
  
  canvas.chart = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['TDAH', 'Autisme', 'Dyslexie', 'Neurotypiques'],
      datasets: [{
        data: [
          appData.company_metrics.adhd_employees,
          appData.company_metrics.autism_employees,
          appData.company_metrics.dyslexia_employees,
          appData.company_metrics.total_employees - appData.company_metrics.neurodiverse_employees
        ],
        backgroundColor: ['#1FB8CD', '#FFC185', '#B4413C', '#5D878F'],
        borderWidth: 2,
        borderColor: '#041e28'
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'bottom',
          labels: {
            color: '#c4bc74',
            padding: 20,
            font: {
              size: 12
            }
          }
        }
      }
    }
  });
}

// Department Performance Chart
function createDepartmentChart() {
  const canvas = document.querySelector('#departmentChart canvas');
  if (!canvas) {
    console.error('Department chart canvas not found');
    return;
  }

  // Destroy existing chart if it exists
  if (canvas.chart) {
    canvas.chart.destroy();
  }

  const ctx = canvas.getContext('2d');
  const departments = appData.performance_metrics.map(d => d.department);
  const productivityData = appData.performance_metrics.map(d => d.productivity_index);
  const neurodiverseData = appData.performance_metrics.map(d => d.neurodiverse_ratio);

  canvas.chart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: departments,
      datasets: [
        {
          label: 'Productivité',
          data: productivityData,
          backgroundColor: '#1FB8CD',
          borderColor: '#1FB8CD',
          borderWidth: 1,
          yAxisID: 'y'
        },
        {
          label: 'Neurodivers %',
          data: neurodiverseData,
          backgroundColor: '#FFC185',
          borderColor: '#FFC185',
          borderWidth: 1,
          yAxisID: 'y1'
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: {
        mode: 'index',
        intersect: false,
      },
      scales: {
        x: {
          ticks: {
            color: '#c4bc74'
          },
          grid: {
            color: 'rgba(196, 188, 116, 0.2)'
          }
        },
        y: {
          type: 'linear',
          display: true,
          position: 'left',
          ticks: {
            color: '#c4bc74'
          },
          grid: {
            color: 'rgba(196, 188, 116, 0.2)'
          }
        },
        y1: {
          type: 'linear',
          display: true,
          position: 'right',
          ticks: {
            color: '#c4bc74'
          },
          grid: {
            drawOnChartArea: false,
          },
        },
      },
      plugins: {
        legend: {
          labels: {
            color: '#c4bc74'
          }
        }
      }
    }
  });
}

// Evolution Chart for Observatoire
function createEvolutionChart() {
  const canvas = document.querySelector('#evolutionChart canvas');
  if (!canvas) {
    console.error('Evolution chart canvas not found');
    return;
  }

  // Destroy existing chart if it exists
  if (canvas.chart) {
    canvas.chart.destroy();
  }

  const ctx = canvas.getContext('2d');
  
  // Generate sample evolution data
  const months = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Jun'];
  const tdahData = [2.8, 2.9, 3.0, 3.1, 3.0, 3.0];
  const autismeData = [0.9, 0.95, 1.0, 1.0, 1.05, 1.0];

  canvas.chart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: months,
      datasets: [
        {
          label: 'TDAH %',
          data: tdahData,
          borderColor: '#1FB8CD',
          backgroundColor: 'rgba(31, 184, 205, 0.1)',
          tension: 0.4,
          fill: true
        },
        {
          label: 'Autisme %',
          data: autismeData,
          borderColor: '#FFC185',
          backgroundColor: 'rgba(255, 193, 133, 0.1)',
          tension: 0.4,
          fill: true
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          ticks: {
            color: '#c4bc74'
          },
          grid: {
            color: 'rgba(196, 188, 116, 0.2)'
          }
        },
        y: {
          ticks: {
            color: '#c4bc74'
          },
          grid: {
            color: 'rgba(196, 188, 116, 0.2)'
          }
        }
      },
      plugins: {
        legend: {
          labels: {
            color: '#c4bc74'
          }
        }
      }
    }
  });
}

// Form Management
function initializeForms() {
  // TDAH Form
  const tdahForm = document.getElementById('tdahForm');
  if (tdahForm) {
    tdahForm.addEventListener('submit', handleTDAHSubmission);
  }

  // Autisme Form
  const autismeForm = document.getElementById('autismeForm');
  if (autismeForm) {
    autismeForm.addEventListener('submit', handleAutismeSubmission);
  }
}

// TDAH Form Handler
function handleTDAHSubmission(e) {
  e.preventDefault();
  
  const formData = new FormData(e.target);
  const responses = {
    q1: parseInt(formData.get('q1')) || 0,
    q2: parseInt(formData.get('q2')) || 0,
    q3: parseInt(formData.get('q3')) || 0,
    q4: parseInt(formData.get('q4')) || 0
  };

  // Calculate weighted score
  const weights = [1.2, 1.3, 1.1, 1.0];
  const questions = [responses.q1, responses.q2, responses.q3, responses.q4];
  
  let totalScore = 0;
  let maxScore = 0;
  
  questions.forEach((response, index) => {
    totalScore += response * weights[index];
    maxScore += 3 * weights[index];
  });
  
  const percentageScore = (totalScore / maxScore) * 100;
  
  // Display results
  displayTDAHResults(percentageScore, responses);
}

function displayTDAHResults(score, responses) {
  const resultPanel = document.getElementById('tdahResult');
  if (!resultPanel) return;

  let interpretation = '';
  let recommendations = '';
  
  if (score < 30) {
    interpretation = 'Score faible - Peu d\'indicateurs TDAH';
    recommendations = 'Aucune action particulière nécessaire. Suivi de routine recommandé.';
  } else if (score < 60) {
    interpretation = 'Score modéré - Quelques indicateurs présents';
    recommendations = 'Évaluation complémentaire recommandée. Considérer des aménagements légers.';
  } else {
    interpretation = 'Score élevé - Indicateurs significatifs';
    recommendations = 'Évaluation professionnelle fortement recommandée. Aménagements workplace prioritaires.';
  }

  resultPanel.innerHTML = `
    <h3>Résultats du Screening TDAH</h3>
    <div class="score-display">
      <div class="score-value">${Math.round(score)}%</div>
      <div class="score-interpretation">${interpretation}</div>
    </div>
    <div class="recommendations">
      <h4>Recommandations:</h4>
      <p>${recommendations}</p>
    </div>
    <div class="next-steps">
      <button class="btn btn--primary btn--sm">Programmer Évaluation</button>
      <button class="btn btn--secondary btn--sm">Télécharger Rapport</button>
    </div>
  `;
  
  resultPanel.classList.remove('hidden');
}

// Autisme Form Handler
function handleAutismeSubmission(e) {
  e.preventDefault();
  
  const formData = new FormData(e.target);
  const responses = {
    a1: parseInt(formData.get('a1')) || 0,
    a2: parseInt(formData.get('a2')) || 0,
    a3: parseInt(formData.get('a3')) || 0
  };

  // Calculate weighted score
  const weights = [1.4, 1.2, 1.3];
  const questions = [responses.a1, responses.a2, responses.a3];
  
  let totalScore = 0;
  let maxScore = 0;
  
  questions.forEach((response, index) => {
    totalScore += response * weights[index];
    maxScore += 3 * weights[index];
  });
  
  const percentageScore = (totalScore / maxScore) * 100;
  
  // Display results
  displayAutismeResults(percentageScore, responses);
}

function displayAutismeResults(score, responses) {
  const resultPanel = document.getElementById('autismeResult');
  if (!resultPanel) return;

  let interpretation = '';
  let recommendations = '';
  
  if (score < 35) {
    interpretation = 'Score faible - Peu d\'indicateurs autistiques';
    recommendations = 'Profil neurotypique probable. Suivi standard approprié.';
  } else if (score < 65) {
    interpretation = 'Score modéré - Certains traits présents';
    recommendations = 'Évaluation approfondie recommandée. Aménagements sensoriels possibles.';
  } else {
    interpretation = 'Score élevé - Indicateurs significatifs';
    recommendations = 'Évaluation spécialisée fortement recommandée. Plan d\'accommodations prioritaire.';
  }

  resultPanel.innerHTML = `
    <h3>Résultats du Screening Autisme</h3>
    <div class="score-display">
      <div class="score-value">${Math.round(score)}%</div>
      <div class="score-interpretation">${interpretation}</div>
    </div>
    <div class="recommendations">
      <h4>Recommandations:</h4>
      <p>${recommendations}</p>
    </div>
    <div class="accommodation-suggestions">
      <h4>Aménagements Suggérés:</h4>
      <ul>
        <li>Instructions écrites détaillées</li>
        <li>Environnement de travail calme</li>
        <li>Horaires flexibles</li>
        <li>Pause régulières</li>
      </ul>
    </div>
    <div class="next-steps">
      <button class="btn btn--primary btn--sm">Programmer Évaluation</button>
      <button class="btn btn--secondary btn--sm">Télécharger Rapport</button>
    </div>
  `;
  
  resultPanel.classList.remove('hidden');
}

// Interactive Elements
function initializeInteractiveElements() {
  // NeuroScreen test buttons
  const testButtons = document.querySelectorAll('.assessment-card .btn');
  testButtons.forEach(button => {
    button.addEventListener('click', function() {
      const testName = this.closest('.assessment-card').querySelector('h3').textContent;
      launchNeuroscientificTest(testName);
    });
  });

  // Report generation buttons
  const reportButtons = document.querySelectorAll('.report-actions .btn');
  reportButtons.forEach(button => {
    button.addEventListener('click', function() {
      if (this.textContent.includes('Générer')) {
        generateMonthlyReport();
      } else if (this.textContent.includes('Exporter')) {
        exportData();
      } else if (this.textContent.includes('Planifier')) {
        scheduleReport();
      }
    });
  });

  // Dashboard refresh button
  const refreshButtons = document.querySelectorAll('.header-actions .btn--secondary');
  refreshButtons.forEach(button => {
    if (button.textContent.includes('Actualiser')) {
      button.addEventListener('click', refreshDashboard);
    }
  });
}

// Neuroscientific Test Launcher
function launchNeuroscientificTest(testName) {
  // Simulate test launch
  const modal = createTestModal(testName);
  document.body.appendChild(modal);
  
  // Simulate test completion after 3 seconds
  setTimeout(() => {
    completeTest(testName, modal);
  }, 3000);
}

function createTestModal(testName) {
  const modal = document.createElement('div');
  modal.className = 'test-modal';
  modal.innerHTML = `
    <div class="modal-overlay">
      <div class="modal-content">
        <h3>Test en cours: ${testName}</h3>
        <div class="test-progress">
          <div class="progress-bar">
            <div class="progress-fill"></div>
          </div>
          <p>Veuillez suivre les instructions à l'écran...</p>
        </div>
        <button class="btn btn--secondary" onclick="this.closest('.test-modal').remove()">Annuler</button>
      </div>
    </div>
  `;
  
  // Add CSS for modal
  const style = document.createElement('style');
  style.textContent = `
    .test-modal {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      z-index: 1000;
    }
    .modal-overlay {
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(0, 0, 0, 0.8);
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .modal-content {
      background: #041e28;
      border: 1px solid #c4bc74;
      border-radius: 12px;
      padding: 2rem;
      max-width: 400px;
      width: 90%;
      text-align: center;
    }
    .progress-bar {
      width: 100%;
      height: 8px;
      background: rgba(196, 188, 116, 0.2);
      border-radius: 4px;
      margin: 1rem 0;
      overflow: hidden;
    }
    .progress-fill {
      height: 100%;
      background: #c4bc74;
      width: 0%;
      animation: progress 3s linear forwards;
    }
    @keyframes progress {
      to { width: 100%; }
    }
  `;
  modal.appendChild(style);
  
  return modal;
}

function completeTest(testName, modal) {
  // Generate random score
  const score = Math.floor(Math.random() * 40) + 60; // 60-99
  
  modal.querySelector('.modal-content').innerHTML = `
    <h3>Test Terminé: ${testName}</h3>
    <div class="test-result">
      <div class="score-display">
        <div class="score-value">${score}/100</div>
        <div class="score-label">Score obtenu</div>
      </div>
      <p>Votre performance se situe dans la moyenne normale.</p>
    </div>
    <div class="test-actions">
      <button class="btn btn--primary" onclick="this.closest('.test-modal').remove()">Voir Détails</button>
      <button class="btn btn--secondary" onclick="this.closest('.test-modal').remove()">Fermer</button>
    </div>
  `;
  
  // Update results section
  updateTestResults(testName, score);
}

function updateTestResults(testName, score) {
  const resultsGrid = document.querySelector('.results-grid');
  if (!resultsGrid) return;
  
  const newResult = document.createElement('div');
  newResult.className = 'result-item';
  newResult.innerHTML = `
    <span class="test-name">${testName}</span>
    <span class="test-score">Score: ${score}/100</span>
    <span class="test-date">${new Date().toLocaleDateString('fr-FR')}</span>
  `;
  
  resultsGrid.insertBefore(newResult, resultsGrid.firstChild);
}

// Dashboard Functions
function updateDashboardMetrics() {
  // Animate metrics (simple example)
  const metricValues = document.querySelectorAll('.metric-value');
  metricValues.forEach(value => {
    value.style.transform = 'scale(1.05)';
    setTimeout(() => {
      value.style.transform = 'scale(1)';
    }, 200);
  });
}

function refreshDashboard() {
  const button = event.target;
  button.textContent = 'Actualisation...';
  button.disabled = true;
  
  // Simulate data refresh
  setTimeout(() => {
    button.textContent = 'Actualiser';
    button.disabled = false;
    updateDashboardMetrics();
    
    // Show notification
    showNotification('Données actualisées avec succès', 'success');
  }, 2000);
}

// Report Functions
function generateMonthlyReport() {
  showNotification('Génération du rapport mensuel en cours...', 'info');
  
  setTimeout(() => {
    showNotification('Rapport mensuel généré avec succès', 'success');
  }, 2000);
}

function exportData() {
  showNotification('Export des données en cours...', 'info');
  
  // Simulate data export
  setTimeout(() => {
    const csvData = generateCSVData();
    downloadCSV(csvData, 'neuroinsight_data.csv');
    showNotification('Données exportées avec succès', 'success');
  }, 1500);
}

function scheduleReport() {
  showNotification('Planification du rapport configurée', 'success');
}

// Utility Functions
function generateCSVData() {
  const data = [
    ['Département', 'Employés Neurodivers %', 'Productivité', 'Innovation', 'Satisfaction'],
    ...appData.performance_metrics.map(dept => [
      dept.department,
      dept.neurodiverse_ratio,
      dept.productivity_index,
      dept.innovation_score,
      dept.team_satisfaction
    ])
  ];
  
  return data.map(row => row.join(',')).join('\n');
}

function downloadCSV(csvContent, filename) {
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  const link = document.createElement('a');
  const url = URL.createObjectURL(blob);
  
  link.setAttribute('href', url);
  link.setAttribute('download', filename);
  link.style.visibility = 'hidden';
  
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

function showNotification(message, type = 'info') {
  const notification = document.createElement('div');
  notification.className = `notification notification--${type}`;
  notification.innerHTML = `
    <div class="notification-content">
      <span class="notification-message">${message}</span>
      <button class="notification-close" onclick="this.parentElement.parentElement.remove()">×</button>
    </div>
  `;
  
  // Add notification styles
  const style = document.createElement('style');
  style.textContent = `
    .notification {
      position: fixed;
      top: 20px;
      right: 20px;
      z-index: 1000;
      min-width: 300px;
      padding: 1rem;
      border-radius: 8px;
      border-left: 4px solid;
      background: rgba(0, 0, 0, 0.9);
      color: white;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
      animation: slideIn 0.3s ease-out;
    }
    .notification--success { border-left-color: #1FB8CD; }
    .notification--error { border-left-color: #FF5459; }
    .notification--warning { border-left-color: #FFC185; }
    .notification--info { border-left-color: #c4bc74; }
    .notification-content {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .notification-close {
      background: none;
      border: none;
      color: white;
      font-size: 18px;
      cursor: pointer;
      padding: 0 0 0 1rem;
    }
    @keyframes slideIn {
      from { transform: translateX(100%); opacity: 0; }
      to { transform: translateX(0); opacity: 1; }
    }
  `;
  
  document.head.appendChild(style);
  document.body.appendChild(notification);
  
  // Auto remove after 5 seconds
  setTimeout(() => {
    if (notification.parentElement) {
      notification.remove();
    }
  }, 5000);
}

// Real-time data simulation
function simulateRealTimeUpdates() {
  setInterval(() => {
    // Randomly update some metrics
    if (Math.random() < 0.1) { // 10% chance every interval
      const metrics = document.querySelectorAll('.metric-value');
      if (metrics.length > 0) {
        const randomMetric = metrics[Math.floor(Math.random() * metrics.length)];
        const currentValue = parseFloat(randomMetric.textContent);
        const variation = (Math.random() - 0.5) * 2; // -1 to +1
        const newValue = Math.max(0, currentValue + variation);
        
        if (randomMetric.textContent.includes('%')) {
          randomMetric.textContent = newValue.toFixed(1) + '%';
        } else if (randomMetric.textContent.includes('/')) {
          randomMetric.textContent = newValue.toFixed(1) + '/5';
        } else {
          randomMetric.textContent = Math.round(newValue);
        }
        
        // Add visual feedback
        randomMetric.style.color = variation > 0 ? '#1FB8CD' : '#FF5459';
        setTimeout(() => {
          randomMetric.style.color = '#c4bc74';
        }, 1000);
      }
    }
  }, 10000); // Every 10 seconds
}

// Start real-time updates
setTimeout(simulateRealTimeUpdates, 5000); // Start after 5 seconds