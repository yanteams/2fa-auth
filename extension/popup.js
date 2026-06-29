const API_URL = 'https://2fa-auth-production-159d.up.railway.app/api/accounts';
let accounts = [];

// DOM Elements
const accountsList = document.getElementById('accountsList');
const searchInput = document.getElementById('searchInput');
const progressBar = document.getElementById('progress-bar');
const addBtn = document.getElementById('addBtn');
const addModal = document.getElementById('addModal');
const cancelAddBtn = document.getElementById('cancelAddBtn');
const addForm = document.getElementById('addForm');

// Initialization
async function init() {
  await fetchAccounts();
  setInterval(updateUI, 1000);
}

// Fetch from API
async function fetchAccounts() {
  try {
    const res = await fetch(API_URL);
    if (!res.ok) throw new Error("API Error");
    accounts = await res.json();
    renderAccounts();
  } catch (error) {
    accountsList.innerHTML = `<div class="loading" style="color: var(--danger-color)">Không thể kết nối đến Backend trên Railway. Vui lòng kiểm tra lại link hoặc server.</div>`;
  }
}

// Render Accounts
async function renderAccounts() {
  const query = searchInput.value.toLowerCase();
  const filtered = accounts.filter(acc => 
    acc.name.toLowerCase().includes(query) || 
    (acc.username && acc.username.toLowerCase().includes(query))
  );

  if (filtered.length === 0) {
    accountsList.innerHTML = `<div class="loading">Không tìm thấy tài khoản nào. Bấm ➕ để thêm mới.</div>`;
    return;
  }

  let html = '';
  for (const acc of filtered) {
    const code = await window.generateTOTP(acc.secret_key);
    html += `
      <div class="account-card" data-id="${acc.id}">
        <div class="acc-header">
          <span class="acc-name">${acc.name}</span>
          <span class="badge" style="font-size:10px; background:#e3f2fd; color:#1976d2; padding:2px 6px; border-radius:10px;">${acc.key_type}</span>
        </div>
        ${acc.username ? `<div class="acc-username">👤 ${acc.username}</div>` : ''}
        <div class="acc-code" title="Bấm để copy mã" onclick="copyToClipboard('${code}', 'Mã 6 số')">${code}</div>
        <div class="acc-actions">
          ${acc.password ? `<button class="action-btn" onclick="copyToClipboard('${acc.password}', 'Mật khẩu')">🔑 Copy MK</button>` : ''}
          <button class="action-btn" onclick="deleteAccount(${acc.id})">🗑️ Xoá</button>
        </div>
      </div>
    `;
  }
  accountsList.innerHTML = html;
  updateProgressBar();
}

// Update loop
function updateUI() {
  const remaining = window.getRemainingTime();
  if (remaining === 30) {
    // Regenerate codes when timer resets
    renderAccounts();
  }
  updateProgressBar();
}

function updateProgressBar() {
  const remaining = window.getRemainingTime();
  const percent = (remaining / 30) * 100;
  progressBar.style.width = `${percent}%`;
  
  if (remaining <= 5) {
    progressBar.style.backgroundColor = 'var(--danger-color)';
  } else if (remaining <= 10) {
    progressBar.style.backgroundColor = '#fd7e14';
  } else {
    progressBar.style.backgroundColor = 'var(--accent-color)';
  }
}

// Clipboard
async function copyToClipboard(text, type) {
  try {
    await navigator.clipboard.writeText(text);
  } catch (err) {
    console.error('Failed to copy!', err);
  }
}

// Delete Account
window.deleteAccount = async (id) => {
  if (!confirm("Bạn có chắc chắn muốn xoá tài khoản này?")) return;
  try {
    await fetch(`${API_URL}/${id}`, { method: 'DELETE' });
    await fetchAccounts();
  } catch (err) {
    alert("Xoá thất bại!");
  }
};

// Events
searchInput.addEventListener('input', renderAccounts);

addBtn.addEventListener('click', () => {
  addModal.classList.remove('hidden');
});

cancelAddBtn.addEventListener('click', () => {
  addModal.classList.add('hidden');
  addForm.reset();
});

addForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const newAcc = {
    name: document.getElementById('addName').value.trim(),
    username: document.getElementById('addUsername').value.trim() || null,
    password: document.getElementById('addPassword').value || null,
    secret_key: document.getElementById('addSecret').value.replace(/\s|-|:/g, ''),
    key_type: "TOTP"
  };

  try {
    const res = await fetch(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newAcc)
    });
    if (res.ok) {
      addModal.classList.add('hidden');
      addForm.reset();
      await fetchAccounts();
    } else {
      const err = await res.json();
      alert("Lỗi: " + JSON.stringify(err));
    }
  } catch (err) {
    alert("Lỗi kết nối Backend.");
  }
});

// Start
document.addEventListener('DOMContentLoaded', init);
