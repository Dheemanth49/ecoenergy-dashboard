// Main JavaScript for EcoEnergy Dashboard

// Global variables
let chartInstances = {};

// Initialize application when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

// Main initialization function
function initializeApp() {
    // Add fade-in animation to cards
    animateCards();
    
    // Initialize tooltips
    initializeTooltips();
    
    // Setup real-time updates
    setupRealTimeUpdates();
    
    // Initialize chart responsiveness
    setupChartResponsiveness();
}

// Animate cards on page load
function animateCards() {
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        setTimeout(() => {
            card.classList.add('fade-in-up');
        }, index * 100);
    });
}

// Initialize Bootstrap tooltips
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Setup real-time updates for dashboard
function setupRealTimeUpdates() {
    // Update dashboard every 5 minutes
    if (window.location.pathname === '/dashboard') {
        setInterval(updateDashboardData, 300000); // 5 minutes
    }
}

// Update dashboard data
function updateDashboardData() {
    // Refresh charts with new data
    refreshCharts();
    
    // Update statistics cards
    updateStatistics();
}

// Refresh all charts on the page
function refreshCharts() {
    const chartElements = document.querySelectorAll('[id$="Chart"]');
    chartElements.forEach(element => {
        if (element.id === 'consumptionChart') {
            updateConsumptionChart();
        } else if (element.id === 'emissionsChart') {
            updateEmissionsChart();
        } else if (element.id === 'forecastChart') {
            updateForecastChart();
        }
    });
}

// Update consumption chart
function updateConsumptionChart() {
    fetch('/api/chart_data?type=daily')
        .then(response => response.json())
        .then(data => {
            const update = {
                x: [data.labels],
                y: [data.consumption]
            };
            Plotly.restyle('consumptionChart', update, [0]);
        })
        .catch(error => console.error('Error updating consumption chart:', error));
}

// Update emissions chart
function updateEmissionsChart() {
    fetch('/api/chart_data?type=daily')
        .then(response => response.json())
        .then(data => {
            const update = {
                x: [data.labels],
                y: [data.emissions]
            };
            Plotly.restyle('emissionsChart', update, [0]);
        })
        .catch(error => console.error('Error updating emissions chart:', error));
}

// Update forecast chart
function updateForecastChart() {
    fetch('/api/forecast')
        .then(response => response.json())
        .then(data => {
            const update = {
                x: [data.dates],
                y: [data.forecast]
            };
            Plotly.restyle('forecastChart', update, [0]);
        })
        .catch(error => console.error('Error updating forecast chart:', error));
}

// Update statistics cards
function updateStatistics() {
    // This would fetch updated statistics and update the cards
    // Implementation depends on specific API endpoints
}

// Setup chart responsiveness
function setupChartResponsiveness() {
    window.addEventListener('resize', function() {
        Object.keys(chartInstances).forEach(chartId => {
            if (document.getElementById(chartId)) {
                Plotly.Plots.resize(chartId);
            }
        });
    });
}

// Utility function to format numbers
function formatNumber(num, decimals = 2) {
    return parseFloat(num).toFixed(decimals);
}

// Utility function to format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

// Show loading spinner
function showLoading(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = `
            <div class="d-flex justify-content-center align-items-center" style="height: 200px;">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
            </div>
        `;
    }
}

// Hide loading spinner
function hideLoading(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = '';
    }
}

// Show success message
function showSuccessMessage(message, duration = 3000) {
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-success alert-dismissible fade show position-fixed';
    alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    alertDiv.innerHTML = `
        <i class="fas fa-check-circle"></i> ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.parentNode.removeChild(alertDiv);
        }
    }, duration);
}

// Show error message
function showErrorMessage(message, duration = 5000) {
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-danger alert-dismissible fade show position-fixed';
    alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    alertDiv.innerHTML = `
        <i class="fas fa-exclamation-circle"></i> ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.parentNode.removeChild(alertDiv);
        }
    }, duration);
}

// Validate form inputs
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return false;
    
    const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.classList.add('is-invalid');
            isValid = false;
        } else {
            input.classList.remove('is-invalid');
            input.classList.add('is-valid');
        }
    });
    
    return isValid;
}

// Export data to CSV
function exportToCSV(data, filename) {
    const csvContent = "data:text/csv;charset=utf-8," 
        + data.map(row => row.join(",")).join("\n");
    
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", filename);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// Smooth scroll to element
function smoothScrollTo(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

// Check if user is online
function checkOnlineStatus() {
    if (!navigator.onLine) {
        showErrorMessage('You are currently offline. Some features may not work properly.');
    }
}

// Setup online/offline event listeners
window.addEventListener('online', function() {
    showSuccessMessage('Connection restored!');
});

window.addEventListener('offline', function() {
    showErrorMessage('Connection lost. Working in offline mode.');
});

// Initialize online status check
checkOnlineStatus();

// Debounce function for search inputs
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

// Local storage utilities
const Storage = {
    set: function(key, value) {
        try {
            localStorage.setItem(key, JSON.stringify(value));
        } catch (e) {
            console.error('Error saving to localStorage:', e);
        }
    },
    
    get: function(key) {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : null;
        } catch (e) {
            console.error('Error reading from localStorage:', e);
            return null;
        }
    },
    
    remove: function(key) {
        try {
            localStorage.removeItem(key);
        } catch (e) {
            console.error('Error removing from localStorage:', e);
        }
    }
};

// Theme management
const ThemeManager = {
    init: function() {
        const savedTheme = Storage.get('theme') || 'light';
        this.setTheme(savedTheme);
    },
    
    setTheme: function(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        Storage.set('theme', theme);
    },
    
    toggleTheme: function() {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        this.setTheme(newTheme);
    }
};

// Initialize theme manager
ThemeManager.init();