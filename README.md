# Urwat il Wusqa Travels (UTW) - Operations DMS

Operational Data Management System (DMS) built specifically for Umrah ground logistics, monitoring Riaz Ul Jannah permits, Zyarat attendance, airport transfers, hotel check-ins, and ground incidents.

## 🚀 Key Features

- **Role-Based Access Control (RBAC):**
  - **Admin Account:** Username `adminuser` | Password `ZAFAR@786`
    - Has full rights to add/edit/delete groups, permits, Zyarat schedules, and flight logistics.
  - **Ground Guide Account:** Username `user` | Password `user@786`
    - Streamlined field view to monitor assigned pilgrims, update live boarding counts, view permits, and launch instant WhatsApp reminders.
- **🕌 Riaz Ul Jannah Permit Tracker:**
  - Segregated by gender (Nusuk slots differ for Men vs Women).
  - Color-coded statuses: Confirmed (Green), Pending (Amber), Missing (Red Alert).
  - Conflict warning detection (overlaps with flight arrivals or bus dispatches).
  - 1-Tap WhatsApp reminder button pre-filled with pilgrim name, slot time, and gate.
- **🚌 Zyarat & Group Movement Board:**
  - Automated attendance reconciliation (Booked Pax vs Actual Boarded Pax).
  - Live alerts when pilgrims are missing from bus departures.
  - Driver & Murshid assigned contact directory.
- **🎨 Modern Claymorphism Design System (Light Theme Only):**
  - Soft tactile 3D pillowy cards with high-contrast surfaces.
  - 100% responsive, mobile-first design with bottom navigation bar for ground field operations.
  - Maximum outdoor sunlight readability under Saudi Arabian sun.
- **💾 Dual Database Engine (MySQL + SQLite Fallback):**
  - Configured for standard **XAMPP / Local MySQL** on port 3306 (user `root`, password empty, database `utw_dms`).
  - Auto-initializes tables and seeds initial Umrah operational data.
  - Automatically falls back to SQLite (`utw_dms.db`) if MySQL is not running yet.

## 🏃 Quick Start

1. Open your terminal inside this directory:
   ```powershell
   cd "c:\Users\Lenovo\Desktop\UTW files\DMS"
   ```
2. Start the Flask application:
   ```powershell
   python app.py
   ```
3. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```
4. Sign in with:
   - **Username:** `adminuser`
   - **Password:** `ZAFAR@786`

