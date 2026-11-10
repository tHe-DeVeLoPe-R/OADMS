"""
Urwat il Wusqa Travels (UTW) - Operations Data Management System (DMS)
Flask Application - Single Role Architecture (Administrator).
Permit Data: Passport Number, Visa Number, Pilgrim WhatsApp, Date, Time, Status, Permit Type.
"""
import os
import json
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import check_password_hash
import db

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'utw-secret-key-zafar-786')

# Initialize DB on load
with app.app_context():
    db.init_db()

# -----------------------------------------------------------------------------
# Authentication & Access Control Decorator
# -----------------------------------------------------------------------------
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session or session['user'].get('username') != 'adminuser':
            flash("Administrator sign-in required.", "info")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# -----------------------------------------------------------------------------
# Authentication Routes
# -----------------------------------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        user = db.query_one("SELECT * FROM users WHERE username = %s", (username,))
        if user and check_password_hash(user['password_hash'], password):
            session['user'] = {
                'id': user['id'],
                'username': user['username'],
                'full_name': user['full_name'],
                'role': 'admin'
            }
            flash(f"Welcome back, {user['full_name']}! Administrator access granted.", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid administrator credentials. (Hint: adminuser / ZAFAR@786)", "danger")

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been signed out safely.", "info")
    return redirect(url_for('login'))

# -----------------------------------------------------------------------------
# Main Operational Dashboard
# -----------------------------------------------------------------------------
@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/dashboard')
@admin_required
def dashboard():
    from datetime import date
    today_str = date.today().isoformat()

    # --- All groups for dropdown ---
    groups = db.query_all("SELECT * FROM pilgrim_groups ORDER BY id DESC")

    # --- Determine selected group (URL param → session → first group) ---
    selected_group_code = request.args.get('group', '').strip()
    if not selected_group_code:
        selected_group_code = session.get('selected_group', '')
    if not selected_group_code and groups:
        selected_group_code = groups[0]['group_code']
    if selected_group_code:
        session['selected_group'] = selected_group_code

    # --- Auto-complete flights whose date has passed ---
    if selected_group_code:
        db.execute_stmt(
            "UPDATE flight_tracker SET status = 'Completed' WHERE route_type = 'Departure' AND flight_date < %s AND status != 'Completed' AND group_code = %s",
            (today_str, selected_group_code)
        )
        db.execute_stmt(
            "UPDATE flight_tracker SET status = 'Landed' WHERE route_type = 'Arrival' AND flight_date < %s AND status NOT IN ('Landed', 'Completed') AND group_code = %s",
            (today_str, selected_group_code)
        )

    # --- Get selected group object ---
    selected_group = next((g for g in groups if g['group_code'] == selected_group_code), None)
    active_pax = selected_group['total_pax'] if selected_group else 0

    # --- All queries filtered by selected group ---
    if selected_group_code:
        permits = db.query_all(
            "SELECT * FROM riaz_permits WHERE group_code = %s ORDER BY permit_date ASC, slot_time ASC",
            (selected_group_code,)
        )
        zyarat_list = db.query_all(
            "SELECT * FROM zyarat_logs WHERE group_code = %s ORDER BY zyarat_date DESC, id DESC",
            (selected_group_code,)
        )
        flights = db.query_all(
            "SELECT * FROM flight_tracker WHERE group_code = %s ORDER BY flight_date ASC, id DESC",
            (selected_group_code,)
        )
        hotels = db.query_all(
            "SELECT * FROM hotel_transfers WHERE group_code = %s ORDER BY check_in_date ASC",
            (selected_group_code,)
        )
        incidents = db.query_all(
            "SELECT * FROM operational_incidents WHERE (group_code = %s OR group_code IS NULL OR group_code = '') ORDER BY id DESC",
            (selected_group_code,)
        )
        pilgrims_roster = db.query_all(
            "SELECT * FROM pilgrims WHERE group_code = %s ORDER BY name ASC",
            (selected_group_code,)
        )
    else:
        permits = []
        zyarat_list = []
        flights = []
        hotels = []
        incidents = []
        pilgrims_roster = []

    total_permits = len(permits)
    upcoming_permits = sum(1 for p in permits if p.get('status') == 'Upcoming')
    completed_permits = sum(1 for p in permits if p.get('status') == 'Completed')
    missed_permits = sum(1 for p in permits if p.get('status') == 'Missed')
    open_incidents = [i for i in incidents if i.get('status') == 'Open']

    stats = {
        'active_pax': active_pax,
        'active_groups': len(groups),
        'total_permits': total_permits,
        'upcoming_permits': upcoming_permits,
        'completed_permits': completed_permits,
        'missed_permits': missed_permits,
        'zyarat_count': len(zyarat_list),
        'flights_count': len(flights)
    }

    # --- Chart 1: Donut – Permit Status ---
    permit_chart_data = {
        'labels': ['Upcoming', 'Completed', 'Missed'],
        'values': [upcoming_permits, completed_permits, missed_permits]
    }

    # --- Chart 2: Bar – Zyarat Attendance ---
    zyarat_labels = []
    zyarat_booked = []
    zyarat_actual = []
    for z in zyarat_list[:8]:
        dest = z.get('destination', 'Zyarat')
        if len(dest) > 18:
            dest = dest[:16] + '...'
        zyarat_labels.append(f"{z.get('city', '')} ({dest})")
        zyarat_booked.append(z.get('booked_pax', 0))
        zyarat_actual.append(z.get('actual_pax', 0))

    zyarat_chart_data = {
        'labels': zyarat_labels,
        'booked': zyarat_booked,
        'actual': zyarat_actual
    }

    # --- Chart 3: Line – Movement Timeline ---
    date_map = {}
    for f in flights:
        d = str(f.get('flight_date') or '')[:10]
        if d:
            date_map.setdefault(d, {'flights': 0, 'zyarat': 0})
            date_map[d]['flights'] += f.get('pax_count', 0)
    for z in zyarat_list:
        d = str(z.get('zyarat_date', ''))[:10]
        if d:
            date_map.setdefault(d, {'flights': 0, 'zyarat': 0})
            date_map[d]['zyarat'] += z.get('actual_pax', 0)

    timeline_labels = []
    timeline_flight_pax = []
    timeline_zyarat_pax = []
    for d in sorted(date_map.keys())[-7:]:
        timeline_labels.append(d)
        timeline_flight_pax.append(date_map[d]['flights'])
        timeline_zyarat_pax.append(date_map[d]['zyarat'])

    timeline_chart_data = {
        'labels': timeline_labels if timeline_labels else ['No Dates Logged'],
        'flights': timeline_flight_pax if timeline_flight_pax else [0],
        'zyarat': timeline_zyarat_pax if timeline_zyarat_pax else [0]
    }

    return render_template(
        'dashboard.html',
        stats=stats,
        permits=permits,
        zyarat_list=zyarat_list,
        flights=flights,
        hotels=hotels,
        incidents=incidents,
        open_incidents=open_incidents,
        groups=groups,
        selected_group_code=selected_group_code,
        selected_group=selected_group,
        pilgrims_roster=pilgrims_roster,
        permit_chart_data=json.dumps(permit_chart_data),
        zyarat_chart_data=json.dumps(zyarat_chart_data),
        timeline_chart_data=json.dumps(timeline_chart_data)
    )

# -----------------------------------------------------------------------------
# Data Entry Page
# -----------------------------------------------------------------------------
@app.route('/add_record')
@admin_required
def add_record():
    groups = db.query_all("SELECT * FROM pilgrim_groups ORDER BY id DESC")
    selected_group_code = session.get('selected_group', groups[0]['group_code'] if groups else '')
    selected_group = next((g for g in groups if g['group_code'] == selected_group_code), None)
    return render_template('add_record.html', groups=groups, selected_group_code=selected_group_code, selected_group=selected_group)

# -----------------------------------------------------------------------------
# Operational Data Submission Handlers
# -----------------------------------------------------------------------------
@app.route('/create_permit', methods=['POST'])
@admin_required
def create_permit():
    passport_number = request.form.get('passport_number', '').strip().upper()
    visa_number = request.form.get('visa_number', '').strip().upper()
    pilgrim_whatsapp = request.form.get('pilgrim_whatsapp', '').strip()
    permit_date = request.form.get('permit_date')
    slot_time = request.form.get('slot_time', '').strip()
    status = request.form.get('status', 'Upcoming')
    permit_type = request.form.get('permit_type', 'Own Permit')
    group_code = request.form.get('group_code', '').strip() or session.get('selected_group', '')

    db.execute_stmt("""
        INSERT INTO riaz_permits (group_code, passport_number, visa_number, pilgrim_whatsapp, permit_date, slot_time, status, permit_type)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (group_code, passport_number, visa_number, pilgrim_whatsapp, permit_date, slot_time, status, permit_type))

    flash(f"Riaz Ul Jannah Permit added: {passport_number} | Type: {permit_type} | Status: {status}", "success")
    return redirect(url_for('dashboard'))

@app.route('/update_permit_status/<int:permit_id>', methods=['POST'])
@admin_required
def update_permit_status(permit_id):
    new_status = request.form.get('status')
    if new_status in ['Upcoming', 'Completed', 'Missed']:
        db.execute_stmt("UPDATE riaz_permits SET status = %s WHERE id = %s", (new_status, permit_id))
        flash(f"Permit status updated to {new_status}.", "success")
    return redirect(url_for('dashboard'))

@app.route('/create_group', methods=['POST'])
@admin_required
def create_group():
    group_code = request.form.get('group_code', '').strip().upper()
    group_name = request.form.get('group_name', '').strip()
    total_pax = int(request.form.get('total_pax', 0))
    leader_name = request.form.get('leader_name', '').strip()
    leader_phone = request.form.get('leader_phone', '').strip()
    arrival_date = request.form.get('arrival_date') or None
    departure_date = request.form.get('departure_date') or None

    db.execute_stmt("""
        INSERT INTO pilgrim_groups (group_code, group_name, leader_name, leader_phone, total_pax, arrival_date, departure_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (group_code, group_name, leader_name, leader_phone, total_pax, arrival_date, departure_date))

    flash(f"Pilgrim Group '{group_code}' created successfully!", "success")
    return redirect(url_for('dashboard'))

@app.route('/create_flight', methods=['POST'])
@admin_required
def create_flight():
    group_code = request.form.get('group_code')
    flight_number = request.form.get('flight_number', '').strip().upper()
    airline = request.form.get('airline', '').strip()
    route_type = request.form.get('route_type', 'Arrival')
    airport = request.form.get('airport', 'Jeddah (JED)')
    flight_date = request.form.get('flight_date') or None
    flight_time = request.form.get('flight_time', '').strip()
    pax_count = int(request.form.get('pax_count', 0))
    transport_assigned = request.form.get('transport_assigned', '').strip()
    status = request.form.get('status', 'On Time')

    db.execute_stmt("""
        INSERT INTO flight_tracker (group_code, flight_number, airline, route_type, airport, flight_date, flight_time, pax_count, transport_assigned, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (group_code, flight_number, airline, route_type, airport, flight_date, flight_time, pax_count, transport_assigned, status))

    flash(f"Flight {flight_number} ({route_type}) added to schedule!", "success")
    return redirect(url_for('dashboard'))

@app.route('/create_zyarat', methods=['POST'])
@admin_required
def create_zyarat():
    city = request.form.get('city')
    group_code = request.form.get('group_code')
    destination = request.form.get('destination', '').strip()
    zyarat_date = request.form.get('zyarat_date')
    departure_time = request.form.get('departure_time', '').strip()
    bus_number = request.form.get('bus_number', '').strip()
    driver_name = request.form.get('driver_name', '').strip()
    driver_phone = request.form.get('driver_phone', '').strip()
    guide_murshid = request.form.get('guide_murshid', '').strip()
    booked_pax = int(request.form.get('booked_pax', 0))
    actual_pax = int(request.form.get('actual_pax', 0))
    status = request.form.get('status', 'Scheduled')
    notes = request.form.get('notes', '').strip()

    db.execute_stmt("""
        INSERT INTO zyarat_logs (group_code, city, zyarat_date, departure_time, destination, bus_number, driver_name, driver_phone, guide_murshid, booked_pax, actual_pax, status, notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (group_code, city, zyarat_date, departure_time, destination, bus_number, driver_name, driver_phone, guide_murshid, booked_pax, actual_pax, status, notes))

    flash(f"Zyarat trip '{destination}' saved!", "success")
    return redirect(url_for('dashboard'))

@app.route('/create_hotel', methods=['POST'])
@admin_required
def create_hotel():
    group_code = request.form.get('group_code')
    city = request.form.get('city', 'Madinah')
    hotel_name = request.form.get('hotel_name', '').strip()
    check_in_date = request.form.get('check_in_date')
    check_out_date = request.form.get('check_out_date')
    rooms_allocated = int(request.form.get('rooms_allocated', 0))
    voucher_status = request.form.get('voucher_status', 'Confirmed')
    assigned_coordinator = request.form.get('assigned_coordinator', '').strip()

    db.execute_stmt("""
        INSERT INTO hotel_transfers (group_code, city, hotel_name, check_in_date, check_out_date, rooms_allocated, voucher_status, assigned_coordinator)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (group_code, city, hotel_name, check_in_date, check_out_date, rooms_allocated, voucher_status, assigned_coordinator))

    flash(f"Hotel accommodation voucher for '{hotel_name}' saved!", "success")
    return redirect(url_for('dashboard'))

@app.route('/create_incident', methods=['POST'])
@admin_required
def create_incident():
    severity = request.form.get('severity')
    category = request.form.get('category', '').strip()
    group_code = request.form.get('group_code') or None
    description = request.form.get('description', '').strip()
    reported_by = session['user']['full_name']

    db.execute_stmt("""
        INSERT INTO operational_incidents (group_code, severity, category, description, reported_by, status)
        VALUES (%s, %s, %s, %s, %s, 'Open')
    """, (group_code, severity, category, description, reported_by))

    flash("Operational alert logged.", "warning")
    return redirect(url_for('dashboard'))

@app.route('/delete_entry/<string:model_type>/<int:item_id>', methods=['POST'])
@admin_required
def delete_entry(model_type, item_id):
    table_map = {
        'zyarat': 'zyarat_logs',
        'permit': 'riaz_permits',
        'flight': 'flight_tracker',
        'hotel': 'hotel_transfers',
        'group': 'pilgrim_groups',
        'incident': 'operational_incidents',
        'pilgrim': 'pilgrims'
    }
    table = table_map.get(model_type)
    if table:
        db.execute_stmt(f"DELETE FROM {table} WHERE id = %s", (item_id,))
        flash("Record removed successfully.", "info")
    return redirect(url_for('dashboard'))

# -----------------------------------------------------------------------------
# Pilgrim Roster — Add & View
# -----------------------------------------------------------------------------
@app.route('/create_pilgrim', methods=['POST'])
@admin_required
def create_pilgrim():
    group_code = request.form.get('group_code', '').strip() or session.get('selected_group', '')
    name = request.form.get('name', '').strip()
    reference_by = request.form.get('reference_by', '').strip()
    passport_number = request.form.get('passport_number', '').strip().upper()
    contact = request.form.get('contact', '').strip()
    address = request.form.get('address', '').strip()

    db.execute_stmt("""
        INSERT INTO pilgrims (group_code, name, reference_by, passport_number, contact, address)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (group_code, name, reference_by, passport_number, contact, address))

    flash(f"Pilgrim '{name}' added to group {group_code}.", "success")
    return redirect(url_for('dashboard'))

@app.route('/update_pilgrim/<int:pilgrim_id>', methods=['POST'])
@admin_required
def update_pilgrim(pilgrim_id):
    name = request.form.get('name', '').strip()
    reference_by = request.form.get('reference_by', '').strip()
    passport_number = request.form.get('passport_number', '').strip().upper()
    contact = request.form.get('contact', '').strip()
    address = request.form.get('address', '').strip()
    group_code = request.form.get('group_code', '').strip()

    if group_code:
        db.execute_stmt("""
            UPDATE pilgrims 
            SET name = %s, reference_by = %s, passport_number = %s, contact = %s, address = %s, group_code = %s
            WHERE id = %s
        """, (name, reference_by, passport_number, contact, address, group_code, pilgrim_id))
    else:
        db.execute_stmt("""
            UPDATE pilgrims 
            SET name = %s, reference_by = %s, passport_number = %s, contact = %s, address = %s
            WHERE id = %s
        """, (name, reference_by, passport_number, contact, address, pilgrim_id))

    flash(f"Pilgrim '{name}' details updated successfully.", "success")
    return redirect(url_for('dashboard'))

# -----------------------------------------------------------------------------
# Group Voucher — Public Printable Document
# -----------------------------------------------------------------------------
@app.route('/voucher/<path:group_code>')
def group_voucher(group_code):
    import socket
    from datetime import date
    group = db.query_one("SELECT * FROM pilgrim_groups WHERE group_code = %s", (group_code,))
    if not group:
        flash("Group not found.", "danger")
        return redirect(url_for('dashboard'))

    pilgrims = db.query_all(
        "SELECT * FROM pilgrims WHERE group_code = %s ORDER BY name ASC",
        (group_code,)
    )
    hotels = db.query_all(
        "SELECT * FROM hotel_transfers WHERE group_code = %s ORDER BY check_in_date ASC",
        (group_code,)
    )
    flights = db.query_all(
        "SELECT * FROM flight_tracker WHERE group_code = %s ORDER BY flight_date ASC",
        (group_code,)
    )

    # Detect phone-accessible LAN IP for local QR scanning
    def get_lan_ip():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "127.0.0.1"

    lan_ip = get_lan_ip()
    port_suffix = ":5000"
    if ':' in request.host:
        port_suffix = f":{request.host.split(':')[1]}"

    public_base = os.environ.get('PUBLIC_BASE_URL', '').rstrip('/')
    if public_base:
        default_qr_url = f"{public_base}/voucher/{group_code}"
    elif '127.0.0.1' in request.host or 'localhost' in request.host:
        default_qr_url = f"http://{lan_ip}{port_suffix}/voucher/{group_code}"
    else:
        default_qr_url = request.base_url

    return render_template('voucher.html',
                           group=group,
                           pilgrims=pilgrims,
                           hotels=hotels,
                           flights=flights,
                           default_qr_url=default_qr_url,
                           now=date.today().strftime('%d %B %Y'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting Urwat il Wusqa DMS Dashboard on http://0.0.0.0:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)
