import json
import random
import string
import streamlit as st
from pathlib import Path
 
# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NeoBank",
    page_icon="🏦",
    layout="centered",
    initial_sidebar_state="collapsed",
)
 
# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');
 
/* ── Root palette ── */
:root {
    --bg:        #0b0f1a;
    --surface:   #111827;
    --card:      #161d2e;
    --border:    #1f2d45;
    --accent:    #00e5ff;
    --accent2:   #7c5cfc;
    --success:   #00e676;
    --danger:    #ff4d6d;
    --warn:      #ffb300;
    --text:      #e8edf5;
    --muted:     #6b7a99;
}
 
/* ── Global reset ── */
html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    font-family: 'DM Sans', sans-serif;
    color: var(--text);
}
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stSidebar"] { background: var(--surface) !important; }
 
/* ── Animated gradient mesh background ── */
[data-testid="stAppViewContainer"]::before {
    content: "";
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 60% 40% at 20% 10%, rgba(0,229,255,.07) 0%, transparent 70%),
        radial-gradient(ellipse 50% 50% at 80% 80%, rgba(124,92,252,.08) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
}
 
/* ── Typography ── */
h1, h2, h3 { font-family: 'Syne', sans-serif !important; letter-spacing: -0.02em; }
 
/* ── Hero header ── */
.hero {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
    position: relative;
}
.hero-logo {
    font-family: 'Syne', sans-serif;
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, var(--accent) 0%, var(--accent2) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.04em;
    line-height: 1;
}
.hero-tagline {
    color: var(--muted);
    font-size: 0.9rem;
    font-weight: 300;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-top: 0.3rem;
}
 
/* ── Balance card ── */
.balance-card {
    background: linear-gradient(135deg, #0e1e38 0%, #1a1040 100%);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 1.8rem 2rem;
    margin: 1rem 0;
    position: relative;
    overflow: hidden;
}
.balance-card::after {
    content: "◈";
    position: absolute;
    right: 1.5rem;
    top: 50%;
    transform: translateY(-50%);
    font-size: 5rem;
    opacity: 0.04;
    color: var(--accent);
}
.balance-label {
    font-size: 0.75rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.4rem;
}
.balance-amount {
    font-family: 'Syne', sans-serif;
    font-size: 2.4rem;
    font-weight: 700;
    color: var(--accent);
}
.balance-acno {
    margin-top: 0.8rem;
    font-size: 0.78rem;
    color: var(--muted);
    letter-spacing: 0.1em;
}
 
/* ── Info card ── */
.info-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    margin: 0.6rem 0;
}
.info-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.5rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
}
.info-row:last-child { border-bottom: none; }
.info-key {
    font-size: 0.78rem;
    color: var(--muted);
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
.info-val { font-size: 0.92rem; font-weight: 500; }
 
/* ── Pill badge ── */
.pill {
    display: inline-block;
    padding: 0.2rem 0.7rem;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.05em;
}
.pill-success { background: rgba(0,230,118,.12); color: var(--success); }
.pill-danger  { background: rgba(255,77,109,.12); color: var(--danger); }
.pill-warn    { background: rgba(255,179,0,.12);  color: var(--warn); }
 
/* ── Alert boxes ── */
.alert {
    border-radius: 12px;
    padding: 0.85rem 1.1rem;
    margin: 0.6rem 0;
    font-size: 0.88rem;
    border-left: 3px solid;
}
.alert-success { background: rgba(0,230,118,.08); border-color: var(--success); color: var(--success); }
.alert-danger  { background: rgba(255,77,109,.08); border-color: var(--danger);  color: var(--danger); }
.alert-info    { background: rgba(0,229,255,.08);  border-color: var(--accent);  color: var(--accent); }
 
/* ── Streamlit widget overrides ── */
[data-testid="stTextInput"] > div > div > input,
[data-testid="stNumberInput"] input {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
    padding: 0.55rem 0.8rem !important;
}
[data-testid="stTextInput"] > div > div > input:focus,
[data-testid="stNumberInput"] input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(0,229,255,0.15) !important;
}
label { color: var(--muted) !important; font-size: 0.82rem !important; letter-spacing: 0.05em !important; }
 
/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, var(--accent) 0%, var(--accent2) 100%) !important;
    color: #0b0f1a !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.6rem 1.4rem !important;
    transition: opacity .2s, transform .15s !important;
    letter-spacing: 0.03em !important;
}
.stButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active { transform: translateY(0) !important; }
 
/* Secondary / danger button variants via classes on parent */
div[data-btn="danger"] .stButton > button {
    background: linear-gradient(135deg, var(--danger) 0%, #c0193b 100%) !important;
    color: #fff !important;
}
div[data-btn="ghost"] .stButton > button {
    background: transparent !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
}
div[data-btn="ghost"] .stButton > button:hover { border-color: var(--accent) !important; color: var(--accent) !important; }
 
/* ── Tabs ── */
[data-testid="stTabs"] [role="tablist"] {
    background: var(--surface) !important;
    border-radius: 12px !important;
    padding: 4px !important;
    gap: 2px !important;
    border: 1px solid var(--border) !important;
}
[data-testid="stTabs"] button[role="tab"] {
    border-radius: 8px !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    color: var(--muted) !important;
    padding: 0.4rem 0.9rem !important;
    transition: all .2s !important;
}
[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, rgba(0,229,255,.15) 0%, rgba(124,92,252,.15) 100%) !important;
    color: var(--text) !important;
}
 
/* ── Divider ── */
hr { border-color: var(--border) !important; margin: 1rem 0 !important; }
 
/* ── Selectbox ── */
[data-testid="stSelectbox"] > div > div {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
}
 
/* ── Remove Streamlit branding ── */
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)
 
# ── Database helpers ───────────────────────────────────────────────────────────
DATABASE = "database.json"
 
def _load():
    if Path(DATABASE).exists():
        with open(DATABASE) as f:
            return json.loads(f.read())
    return []
 
def _save(data):
    with open(DATABASE, "w") as f:
        f.write(json.dumps(data))
 
def _gen_acno(data):
    while True:
        chars = random.choices(string.ascii_uppercase, k=8) + random.choices(string.digits, k=4)
        random.shuffle(chars)
        acno = "".join(chars)
        if not any(u["Accountno"] == acno for u in data):
            return acno
 
def _auth(data, acno, pin):
    return next((u for u in data if u["Accountno"] == acno and u["pin"] == pin), None)
 
# ── Session state init ─────────────────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = None
if "page" not in st.session_state:
    st.session_state.page = "home"   # home | dashboard
if "msg" not in st.session_state:
    st.session_state.msg = None      # (type, text)
 
def show_msg():
    if st.session_state.msg:
        t, txt = st.session_state.msg
        cls = {"success": "alert-success", "error": "alert-danger", "info": "alert-info"}.get(t, "alert-info")
        st.markdown(f'<div class="alert {cls}">{"✓" if t=="success" else "✗" if t=="error" else "ℹ"} &nbsp;{txt}</div>', unsafe_allow_html=True)
        st.session_state.msg = None
 
def logout():
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.page = "home"
 
# ══════════════════════════════════════════════════════════════════════════════
#  HOME PAGE  (Login / Register)
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "home":
 
    st.markdown("""
    <div class="hero">
        <div class="hero-logo">◈ NeoBank</div>
        <div class="hero-tagline">Next-gen digital banking</div>
    </div>
    """, unsafe_allow_html=True)
 
    show_msg()
 
    tab_login, tab_register = st.tabs(["🔑  Sign In", "✦  Open Account"])
 
    # ── LOGIN ──
    with tab_login:
        st.markdown("<br>", unsafe_allow_html=True)
        acno_in = st.text_input("Account Number", placeholder="e.g. A3KP92BZ1T4M", key="l_acno")
        pin_in  = st.text_input("PIN", type="password", placeholder="4-digit PIN", key="l_pin")
        st.markdown("<br>", unsafe_allow_html=True)
 
        if st.button("Sign In  →", use_container_width=True, key="btn_login"):
            data = _load()
            if not pin_in.isdigit() or len(pin_in) != 4:
                st.session_state.msg = ("error", "PIN must be exactly 4 digits.")
                st.rerun()
            else:
                user = _auth(data, acno_in.strip(), int(pin_in))
                if user:
                    st.session_state.logged_in = True
                    st.session_state.user = user
                    st.session_state.page = "dashboard"
                    st.session_state.msg = ("success", f"Welcome back, {user['name']}!")
                    st.rerun()
                else:
                    st.session_state.msg = ("error", "Invalid account number or PIN.")
                    st.rerun()
 
    # ── REGISTER ──
    with tab_register:
        st.markdown("<br>", unsafe_allow_html=True)
        r_name  = st.text_input("Full Name", placeholder="Jane Doe", key="r_name")
        r_age   = st.number_input("Age", min_value=1, max_value=120, value=18, key="r_age")
        r_email = st.text_input("Email Address", placeholder="jane@example.com", key="r_email")
        r_pin   = st.text_input("Choose a 4-digit PIN", type="password", max_chars=4, key="r_pin")
        st.markdown("<br>", unsafe_allow_html=True)
 
        if st.button("Create Account  →", use_container_width=True, key="btn_register"):
            data = _load()
            if not r_name.strip():
                st.session_state.msg = ("error", "Name cannot be empty.")
            elif r_age < 12:
                st.session_state.msg = ("error", "Minimum age to open an account is 12.")
            elif not r_pin.isdigit() or len(r_pin) != 4:
                st.session_state.msg = ("error", "PIN must be exactly 4 digits.")
            else:
                new_user = {
                    "name": r_name.strip(),
                    "age": int(r_age),
                    "email": r_email.strip(),
                    "Accountno": _gen_acno(data),
                    "pin": int(r_pin),
                    "balance": 0,
                }
                data.append(new_user)
                _save(data)
                st.session_state.msg = ("success", f"Account created! Your Account No: {new_user['Accountno']}  — Save it safely.")
            st.rerun()
 
# ══════════════════════════════════════════════════════════════════════════════
#  DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "dashboard":
 
    # Refresh user from DB on each run
    db = _load()
    fresh = next((u for u in db if u["Accountno"] == st.session_state.user["Accountno"]), None)
    if not fresh:
        logout(); st.rerun()
    st.session_state.user = fresh
    user = fresh
 
    # ── Top bar ──
    c1, c2 = st.columns([3, 1])
    with c1:
        st.markdown(f'<div class="hero-logo" style="font-size:1.6rem; text-align:left; padding:0.5rem 0;">◈ NeoBank</div>', unsafe_allow_html=True)
    with c2:
        if st.button("Sign Out", key="signout"):
            logout(); st.rerun()
 
    show_msg()
 
    # ── Balance card ──
    st.markdown(f"""
    <div class="balance-card">
        <div class="balance-label">Available Balance</div>
        <div class="balance-amount">₹{user['balance']:,.2f}</div>
        <div class="balance-acno">Account No &nbsp;·&nbsp; {user['Accountno']}</div>
    </div>
    """, unsafe_allow_html=True)
 
    st.markdown("<br>", unsafe_allow_html=True)
 
    # ── Navigation tabs ──
    tabs = st.tabs(["👤 Profile", "⬇ Deposit", "⬆ Withdraw", "↔ Transfer", "✏ Edit", "🗑 Close"])
 
    # ── PROFILE ──────────────────────────────────────────────────────────────
    with tabs[0]:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="info-card">
            <div class="info-row"><span class="info-key">Name</span><span class="info-val">{user['name']}</span></div>
            <div class="info-row"><span class="info-key">Age</span><span class="info-val">{user['age']}</span></div>
            <div class="info-row"><span class="info-key">Email</span><span class="info-val">{user['email']}</span></div>
            <div class="info-row"><span class="info-key">Account No</span><span class="info-val" style="font-family:monospace">{user['Accountno']}</span></div>
            <div class="info-row"><span class="info-key">Balance</span><span class="info-val" style="color:var(--accent)">₹{user['balance']:,.2f}</span></div>
            <div class="info-row"><span class="info-key">Status</span><span class="pill pill-success">Active</span></div>
        </div>
        """, unsafe_allow_html=True)
 
    # ── DEPOSIT ───────────────────────────────────────────────────────────────
    with tabs[1]:
        st.markdown("<br>", unsafe_allow_html=True)
        dep_amt = st.number_input("Amount to Deposit (₹)", min_value=1, step=100, key="dep_amt")
        dep_pin = st.text_input("Confirm PIN", type="password", max_chars=4, key="dep_pin")
        st.markdown("<br>", unsafe_allow_html=True)
 
        if st.button("Deposit  →", use_container_width=True, key="btn_dep"):
            if not dep_pin.isdigit() or len(dep_pin) != 4:
                st.session_state.msg = ("error", "Invalid PIN format.")
            elif int(dep_pin) != user["pin"]:
                st.session_state.msg = ("error", "Incorrect PIN.")
            elif dep_amt <= 0:
                st.session_state.msg = ("error", "Amount must be greater than 0.")
            else:
                for u in db:
                    if u["Accountno"] == user["Accountno"]:
                        u["balance"] += dep_amt
                        break
                _save(db)
                st.session_state.msg = ("success", f"₹{dep_amt:,.0f} deposited successfully.")
            st.rerun()
 
    # ── WITHDRAW ──────────────────────────────────────────────────────────────
    with tabs[2]:
        st.markdown("<br>", unsafe_allow_html=True)
        wd_amt = st.number_input("Amount to Withdraw (₹)", min_value=1, step=100, key="wd_amt")
        wd_pin = st.text_input("Confirm PIN", type="password", max_chars=4, key="wd_pin")
        st.markdown("<br>", unsafe_allow_html=True)
 
        if st.button("Withdraw  →", use_container_width=True, key="btn_wd"):
            if not wd_pin.isdigit() or len(wd_pin) != 4:
                st.session_state.msg = ("error", "Invalid PIN format.")
            elif int(wd_pin) != user["pin"]:
                st.session_state.msg = ("error", "Incorrect PIN.")
            elif wd_amt <= 0:
                st.session_state.msg = ("error", "Amount must be greater than 0.")
            elif wd_amt > user["balance"]:
                st.session_state.msg = ("error", f"Insufficient balance. Available: ₹{user['balance']:,.2f}")
            else:
                for u in db:
                    if u["Accountno"] == user["Accountno"]:
                        u["balance"] -= wd_amt
                        break
                _save(db)
                st.session_state.msg = ("success", f"₹{wd_amt:,.0f} withdrawn successfully.")
            st.rerun()
 
    # ── TRANSFER ──────────────────────────────────────────────────────────────
    with tabs[3]:
        st.markdown("<br>", unsafe_allow_html=True)
        tr_to  = st.text_input("Recipient Account Number", placeholder="Enter account number", key="tr_to")
        tr_amt = st.number_input("Amount to Transfer (₹)", min_value=1, step=100, key="tr_amt")
        tr_pin = st.text_input("Confirm PIN", type="password", max_chars=4, key="tr_pin")
        st.markdown("<br>", unsafe_allow_html=True)
 
        if st.button("Transfer  →", use_container_width=True, key="btn_tr"):
            if not tr_pin.isdigit() or len(tr_pin) != 4:
                st.session_state.msg = ("error", "Invalid PIN format.")
            elif int(tr_pin) != user["pin"]:
                st.session_state.msg = ("error", "Incorrect PIN.")
            elif tr_to.strip() == user["Accountno"]:
                st.session_state.msg = ("error", "Cannot transfer to your own account.")
            else:
                recipient = next((u for u in db if u["Accountno"] == tr_to.strip()), None)
                if not recipient:
                    st.session_state.msg = ("error", "Recipient account not found.")
                elif tr_amt > user["balance"]:
                    st.session_state.msg = ("error", f"Insufficient balance. Available: ₹{user['balance']:,.2f}")
                else:
                    for u in db:
                        if u["Accountno"] == user["Accountno"]:
                            u["balance"] -= tr_amt
                        elif u["Accountno"] == tr_to.strip():
                            u["balance"] += tr_amt
                    _save(db)
                    st.session_state.msg = ("success", f"₹{tr_amt:,.0f} transferred to {recipient['name']} successfully.")
            st.rerun()
 
    # ── EDIT PROFILE ──────────────────────────────────────────────────────────
    with tabs[4]:
        st.markdown("<br>", unsafe_allow_html=True)
        ed_name  = st.text_input("Name",  value=user["name"],  key="ed_name")
        ed_age   = st.number_input("Age", value=user["age"], min_value=12, max_value=120, key="ed_age")
        ed_email = st.text_input("Email", value=user["email"], key="ed_email")
 
        st.markdown("---")
        st.markdown('<span style="color:var(--muted); font-size:0.8rem;">CHANGE PIN &nbsp;(leave blank to keep current)</span>', unsafe_allow_html=True)
        ed_newpin = st.text_input("New PIN", type="password", max_chars=4, key="ed_newpin")
        ed_curpin = st.text_input("Current PIN (required to save)", type="password", max_chars=4, key="ed_curpin")
        st.markdown("<br>", unsafe_allow_html=True)
 
        if st.button("Save Changes  →", use_container_width=True, key="btn_edit"):
            if not ed_curpin.isdigit() or len(ed_curpin) != 4:
                st.session_state.msg = ("error", "Invalid current PIN.")
            elif int(ed_curpin) != user["pin"]:
                st.session_state.msg = ("error", "Incorrect current PIN.")
            else:
                for u in db:
                    if u["Accountno"] == user["Accountno"]:
                        u["name"]  = ed_name.strip() or user["name"]
                        u["age"]   = int(ed_age)
                        u["email"] = ed_email.strip() or user["email"]
                        if ed_newpin:
                            if ed_newpin.isdigit() and len(ed_newpin) == 4:
                                u["pin"] = int(ed_newpin)
                            else:
                                st.session_state.msg = ("error", "New PIN must be 4 digits. Other changes saved.")
                                _save(db)
                                st.rerun()
                        break
                _save(db)
                st.session_state.msg = ("success", "Profile updated successfully.")
            st.rerun()
 
    # ── CLOSE ACCOUNT ─────────────────────────────────────────────────────────
    with tabs[5]:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div class="alert alert-danger">
            ⚠ &nbsp;This action is <strong>permanent</strong>. All data will be erased.
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        del_confirm = st.text_input("Type  DELETE  to confirm", key="del_confirm")
        del_pin     = st.text_input("Enter your PIN", type="password", max_chars=4, key="del_pin")
        st.markdown("<br>", unsafe_allow_html=True)
 
        with st.container():
            st.markdown('<div data-btn="danger">', unsafe_allow_html=True)
            close_btn = st.button("Close My Account", use_container_width=True, key="btn_close")
            st.markdown('</div>', unsafe_allow_html=True)
 
        if close_btn:
            if del_confirm.strip() != "DELETE":
                st.session_state.msg = ("error", 'Please type DELETE (all caps) to confirm.')
            elif not del_pin.isdigit() or len(del_pin) != 4:
                st.session_state.msg = ("error", "Invalid PIN format.")
            elif int(del_pin) != user["pin"]:
                st.session_state.msg = ("error", "Incorrect PIN.")
            else:
                db = [u for u in db if u["Accountno"] != user["Accountno"]]
                _save(db)
                st.session_state.msg = ("info", "Your account has been closed. Goodbye!")
                logout()
            st.rerun()
