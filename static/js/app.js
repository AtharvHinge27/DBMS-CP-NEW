/**
 * InnoSphere - Core JavaScript Application Layer
 * Provides Fetch API wrapper, Toast notifications, and Sidebar controls.
 */

// Global API Fetch Utility
async function apiFetch(url, options = {}) {
    const defaultHeaders = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    };

    const config = {
        ...options,
        headers: {
            ...defaultHeaders,
            ...(options.headers || {})
        }
    };

    if (config.body && typeof config.body === 'object') {
        config.body = JSON.stringify(config.body);
    }

    try {
        const response = await fetch(url, config);
        const data = await response.json();

        if (response.status === 401 && !url.includes('/api/auth/me')) {
            showToast('Session expired. Redirecting to login...', 'warning');
            setTimeout(() => {
                window.location.href = '/login';
            }, 1200);
            return null;
        }

        return { ok: response.ok, status: response.status, data };
    } catch (error) {
        console.error(`[API ERROR] ${url}:`, error);
        showToast('Network error or server unavailable.', 'danger');
        return { ok: false, status: 500, data: { success: false, message: error.message } };
    }
}

// Global Toast Notification System
function showToast(message, type = 'info') {
    let container = document.getElementById('toastContainer');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toastContainer';
        container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
        document.body.appendChild(container);
    }

    const toastId = 'toast_' + Date.now();
    const bgClass = type === 'success' ? 'bg-success text-white' :
                    type === 'danger' ? 'bg-danger text-white' :
                    type === 'warning' ? 'bg-warning text-dark' : 'bg-primary text-white';

    const toastHtml = `
        <div id="${toastId}" class="toast align-items-center ${bgClass} border-0 shadow-sm" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="d-flex">
                <div class="toast-body fw-medium">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        </div>
    `;

    container.insertAdjacentHTML('beforeend', toastHtml);
    const toastElem = document.getElementById(toastId);
    const bsToast = new bootstrap.Toast(toastElem, { delay: 4000 });
    bsToast.show();

    toastElem.addEventListener('hidden.bs.toast', () => {
        toastElem.remove();
    });
}

// Sidebar Hamburger Toggle
function initSidebarToggle() {
    const toggleBtn = document.getElementById('sidebarToggleBtn');
    const sidebar = document.getElementById('appSidebar');
    const mainWrapper = document.getElementById('mainWrapper');

    if (toggleBtn && sidebar && mainWrapper) {
        toggleBtn.addEventListener('click', () => {
            if (window.innerWidth <= 991) {
                sidebar.classList.toggle('mobile-open');
            } else {
                sidebar.classList.toggle('collapsed');
                mainWrapper.classList.toggle('expanded');
            }
        });
    }
}

// Global User Logout
async function handleLogout() {
    const res = await apiFetch('/api/auth/logout', { method: 'POST' });
    if (res && res.data && res.data.success) {
        showToast('Logged out successfully.', 'info');
        window.location.href = '/login';
    }
}

// Copy Code to Clipboard
function copyToClipboard(text, successMsg = 'Copied to clipboard!') {
    navigator.clipboard.writeText(text).then(() => {
        showToast(successMsg, 'success');
    }).catch(err => {
        showToast('Failed to copy.', 'danger');
    });
}

// Notifications Loader
async function loadNotifications() {
    const badge = document.getElementById('notifBadge');
    const list = document.getElementById('notifDropdownList');
    if (!badge || !list) return;

    const res = await apiFetch('/api/notifications');
    if (res && res.ok && res.data && res.data.success) {
        const notifs = res.data.notifications || [];
        const unread = res.data.unread_count || 0;

        if (unread > 0) {
            badge.textContent = unread;
            badge.classList.remove('d-none');
        } else {
            badge.classList.add('d-none');
        }

        if (notifs.length === 0) {
            list.innerHTML = '<li class="dropdown-item text-muted text-center py-3">No notifications</li>';
            return;
        }

        list.innerHTML = notifs.map(n => `
            <li>
                <a class="dropdown-item py-2 px-3 border-bottom ${n.is_read ? '' : 'bg-light'}" href="${n.link || '#'}" onclick="markNotifRead(${n.notification_id})">
                    <div class="fw-bold small text-primary">${n.title}</div>
                    <div class="small text-secondary text-truncate" style="max-width: 280px;">${n.message}</div>
                    <div class="text-muted" style="font-size: 0.7rem;">${n.created_at}</div>
                </a>
            </li>
        `).join('') + `
            <li>
                <button class="dropdown-item text-center text-primary small py-2 fw-semibold" onclick="markAllNotifsRead()">
                    Mark all as read
                </button>
            </li>
        `;
    }
}

async function markNotifRead(id) {
    await apiFetch(`/api/notifications/${id}/read`, { method: 'POST' });
    loadNotifications();
}

async function markAllNotifsRead() {
    await apiFetch('/api/notifications/read-all', { method: 'POST' });
    loadNotifications();
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
    initSidebarToggle();
    loadNotifications();
});
