/**
 * Urwat il Wusqa Travels (UTW) DMS - Client Scripts
 * Stakeholder Charts & Claymorphic Modal Popups
 */

// ----------------------------------------------------------------------------
// Claymorphic Modal / Popup Helpers
// ----------------------------------------------------------------------------
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }
}

// Close modal on escape key or clicking backdrop
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        document.querySelectorAll('.clay-modal-overlay.active').forEach(m => {
            m.classList.remove('active');
            document.body.style.overflow = '';
        });
    }
});

document.addEventListener('click', (e) => {
    if (e.target.classList.contains('clay-modal-overlay')) {
        e.target.classList.remove('active');
        document.body.style.overflow = '';
    }
});

// ----------------------------------------------------------------------------
// Stakeholder Interactive Charts (Chart.js)
// ----------------------------------------------------------------------------
function initCharts(permitData, zyaratData, timelineData) {
    // 1. Pie / Donut Chart: Riaz Ul Jannah Permit Status
    const permitCtx = document.getElementById('permitPieChart');
    if (permitCtx && permitData) {
        new Chart(permitCtx, {
            type: 'doughnut',
            data: {
                labels: permitData.labels,
                datasets: [{
                    data: permitData.values,
                    backgroundColor: ['#059669', '#d97706', '#ef4444', '#94a3b8'],
                    borderWidth: 2,
                    borderColor: '#ffffff',
                    hoverOffset: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            font: { family: 'Plus Jakarta Sans', weight: '700', size: 11 },
                            padding: 12,
                            boxWidth: 12
                        }
                    }
                },
                cutout: '62%'
            }
        });
    }

    // 2. Bar Chart: Zyarat Booked vs. Actual Boarded Pax
    const zyaratCtx = document.getElementById('zyaratBarChart');
    if (zyaratCtx && zyaratData) {
        new Chart(zyaratCtx, {
            type: 'bar',
            data: {
                labels: zyaratData.labels.length > 0 ? zyaratData.labels : ['No Excursions'],
                datasets: [
                    {
                        label: 'Booked Pax',
                        data: zyaratData.booked.length > 0 ? zyaratData.booked : [0],
                        backgroundColor: '#e2e8f0',
                        borderRadius: 8,
                        borderSkipped: false
                    },
                    {
                        label: 'Actual Boarded Pax',
                        data: zyaratData.actual.length > 0 ? zyaratData.actual : [0],
                        backgroundColor: '#059669',
                        borderRadius: 8,
                        borderSkipped: false
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                        labels: {
                            font: { family: 'Plus Jakarta Sans', weight: '700', size: 11 },
                            boxWidth: 12
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: { color: 'rgba(226, 232, 240, 0.6)' },
                        ticks: { font: { family: 'Plus Jakarta Sans', size: 10 } }
                    },
                    x: {
                        grid: { display: false },
                        ticks: { font: { family: 'Plus Jakarta Sans', size: 10 } }
                    }
                }
            }
        });
    }

    // 3. Line Chart: Travel & Ground Movement Timeline
    const timelineCtx = document.getElementById('timelineLineChart');
    if (timelineCtx && timelineData) {
        new Chart(timelineCtx, {
            type: 'line',
            data: {
                labels: timelineData.labels,
                datasets: [
                    {
                        label: 'Flight Passenger Volume',
                        data: timelineData.flights,
                        borderColor: '#7e22ce',
                        backgroundColor: 'rgba(126, 34, 206, 0.08)',
                        fill: true,
                        tension: 0.35,
                        pointBackgroundColor: '#7e22ce',
                        pointRadius: 4
                    },
                    {
                        label: 'Zyarat Transit Volume',
                        data: timelineData.zyarat,
                        borderColor: '#0284c7',
                        backgroundColor: 'rgba(2, 132, 199, 0.08)',
                        fill: true,
                        tension: 0.35,
                        pointBackgroundColor: '#0284c7',
                        pointRadius: 4
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                        labels: {
                            font: { family: 'Plus Jakarta Sans', weight: '700', size: 11 },
                            boxWidth: 12
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: { color: 'rgba(226, 232, 240, 0.6)' },
                        ticks: { font: { family: 'Plus Jakarta Sans', size: 10 } }
                    },
                    x: {
                        grid: { display: false },
                        ticks: { font: { family: 'Plus Jakarta Sans', size: 10 } }
                    }
                }
            }
        });
    }
}
