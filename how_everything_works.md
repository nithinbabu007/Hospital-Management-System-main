# How PrimeCare Medical Institute Works

A click-through guide: how to get around the site, what every button
does, and what's real vs. a demo stand-in. You only ever type **one**
address into your browser — everything else is clicking links and
buttons. Pair this with `run_on_another_pc.md` for setup instructions.

## Start here

1. Make sure the server is running (a terminal window showing
   `Starting development server...`).
2. Open your browser and type this **one** address:
   ```
   http://127.0.0.1:8000/
   ```
   That's the only address you'll ever need to type. Bookmark it if
   you like. Everything below is reached by clicking, not typing.

You'll land on the **public home page** — this is what a patient
visiting the hospital's website would see.

---

## The three areas of the site

There's one website, but three different "modes" depending on who's
using it:

| Area | Who it's for | How to get there |
|---|---|---|
| **Public site** | Patients / visitors | Where you land by default — no login |
| **Admin panel** | Hospital admin/staff | Click **"Admins Login"** in the top menu |
| **Doctor portal** | Doctors | Click **"Doctors Login"** in the top menu |

---

## 1. Public site — no login needed

The top menu bar is on every page: **Home | About | Doctors |
Appointments | Services | Contact | Admins Login | Doctors Login**.

- **Home** — click to come back here any time. Shows a preview of
  doctors in the system as cards (photo, name, department), with a
  **Book Appointment** button on each.
- **Doctors** — click for the full doctor directory: every doctor in
  the system as a card, with a search box to filter by doctor name and
  a dropdown to filter by specialty/department. Each card has a **Book
  Now** button that goes straight to booking with that doctor. This is
  a dedicated page (separate from Home) so you can browse and search
  the full doctor list without scrolling the home page.
- **About** — click for a static page about the hospital.
- **Services** — click for a static page listing hospital
  services/departments.
- **Contact** — click for a contact form. Fill it in and click
  **Send** (or similar) — it gets saved and shows up for the admin
  under **Messages**.
- **Appointments** — click to book. Walkthrough below.

### How to book an appointment (click by click)

1. Click **Appointments** in the top menu (or **Book Appointment** on
   any doctor card on the Home page).
2. Pick a **Department** from the dropdown — the **Doctor** dropdown
   below it fills in automatically with doctors from that department.
3. Fill in your name, email, phone, pick a doctor and a date, add a
   message if you like, then click **Submit** / **Book**.
4. You land on a payment page showing **"Pay ₹150"**.
5. Click the **Pay ₹150** button:
   - If the demo is running without real payment setup, you'll see a
     note that says **"Demo mode"** — clicking Pay just instantly
     pretends the payment succeeded. No card, no real money, no
     account needed.
   - If real payment keys are configured, a real Razorpay payment
     window pops up instead.
6. You're redirected back to the Appointments page with a success
   message. Your booking is now saved — it'll show up for the admin
   (under Appointments) and for the specific doctor you booked with
   (under their "My Appointments").

### The chatbot

There's a hospital-assistant chat box on the Home page. Type a
question about appointments, doctors, or payments and it replies. In
demo mode (no AI key configured) it gives one fixed canned answer
instead of a real AI response — still works, just not "smart."

---

## 2. Admin panel — for hospital staff

### Getting in

1. Click **"Admins Login"** in the top menu.
2. Type in the admin username and password. On a freshly set-up demo
   (see `run_on_another_pc.md`), the ready-to-use login is:
   ```
   Username: admin
   Password: admin123
   ```
   then click **Login**.
3. You'll land on an **"Enter OTP"** screen asking for a 6-digit code.
   - If the demo has no real email set up, **switch to the terminal
     window running the server** and look for a line like:
     ```
     ---Your OTP for admin login is 123456
     ```
     Type that 6-digit number into the OTP box and click **Verify**.
   - If real email is set up, the code was emailed instead — check
     that inbox.
4. You're in. You land on the **Dashboard**.

### Getting around (the left sidebar)

Everything in the admin panel is reached by clicking links in the left
sidebar — never type an address here.

- **Dashboard** — the home screen after login. Shows counts (number of
  departments, doctors, appointments, messages, attendance). A couple
  of extra chart widgets (world map, sales numbers) are leftover
  decoration from the page template and don't show real data — ignore
  those.
- **Doctors** — click to see a form for **adding a new doctor** (name,
  department, phone, email, qualification, and a photo upload). Fill
  it in and click **Add/Save**. There's also a **"View Doctors"**
  button/link nearby that shows the full list, where each row has
  **Edit** and **Delete** buttons.
- **Departments** — same idea: click to add a new department (name,
  description, phone, email, image), and a link to view the full list
  with Edit/Delete per row.
- **Appointments** — click to see every appointment anyone has booked
  through the public site: patient name, department, doctor, date, and
  a **Status** column (Pending/Confirmed/Cancelled). Each row also has
  an **Action** button — click **Cancel** to cancel a Confirmed/Pending
  appointment, or **Confirm** to reinstate a Cancelled one. The button
  label flips automatically depending on the current status. This
  works on any appointment in the system, for any doctor.
- **Messages** — click to see every contact-form submission from the
  public site.
- **Scan Attendance** — click to open a page for scanning a doctor's
  attendance QR code (see the attendance flow below).

Logging out: click your name/username in the top-right corner, then
click **Logout**.

---

## 3. Doctor portal — for doctors

### Getting in

1. Click **"Doctors Login"** in the top menu.
2. Type the doctor's **name** as the username (it must match a
   doctor already added in the admin panel, e.g. "Sarah").
3. Type the password. The rule for every doctor's password is:
   **the doctor's name followed by `123`.** So doctor "Sarah" always
   logs in with password `Sarah123`. This isn't something you set —
   it's just how this demo project generates doctor passwords. On a
   freshly set-up demo (see `run_on_another_pc.md`), three ready-to-use
   doctor logins are:
   | Username | Password |
   |---|---|
   | `Sarah` | `Sarah123` |
   | `James` | `James123` |
   | `Priya` | `Priya123` |
4. Click **Login**, then the same OTP screen as the admin login
   appears — check the server terminal window for the printed code if
   no real email is set up, type it in, click **Verify**.
5. You land on the doctor's **Dashboard**.

### Getting around (the left sidebar)

- **Dashboard** — welcome screen with the doctor's name and a total
  appointment count.
- **My Appointments** — click to see every appointment booked
  specifically with this doctor, with the same **Status** column and
  **Action** (Confirm/Cancel) button as the admin's Appointments page.
  A doctor can only confirm/cancel their *own* appointments — trying to
  act on another doctor's appointment (e.g. by guessing a URL) is
  blocked and shows a "not found" page instead.
- **Attendance** — click to see this month's Present/Absent count and
  whether today's attendance is already marked.

### Marking attendance (click by click)

1. Click **Attendance** in the sidebar, then click **Mark Attendance**
   (this only works once per day).
2. A QR code is generated and emailed to the doctor (or, in demo mode,
   the link is printed to the server terminal window instead).
3. Scanning that QR code (with a phone camera, or just opening the
   link directly in a browser) marks that day's attendance as
   **Present** and takes you to the admin's attendance list.
4. If you don't have a phone/scanner handy during a demo, just copy
   the link printed in the server terminal and open it in a new
   browser tab — same effect as scanning it.

---

## Login cheat sheet

| Role | Click | Username | Password | Code (OTP) |
|---|---|---|---|---|
| Admin | "Admins Login" | `admin` | `admin123` | printed in the server terminal window |
| Doctor | "Doctors Login" | `Sarah` / `James` / `Priya` | name + `123`, e.g. `Sarah123` | printed in the server terminal window |

(If you set up the admin account with a different username/password in
step 6 of `run_on_another_pc.md`, use that instead of `admin`/`admin123`.)

---

## What's real vs. a demo stand-in

| Feature | Out of the box (demo mode) | With real setup |
|---|---|---|
| Login codes (OTP) | Printed in the server terminal window | Really emailed |
| Payment | "Demo mode" — clicking Pay instantly succeeds, no charge | Real payment window, real charge |
| SMS after booking | Skipped silently (logged in the terminal) | Real text message sent |
| Chatbot | One fixed canned reply | Real AI-generated answer |

Everything else — booking, adding/editing/deleting doctors and
departments, confirming/cancelling appointments, viewing appointments
and messages, doctor attendance and QR codes, and the search boxes on
the Home and Doctors pages — is fully real, no stand-ins.

## A few harmless quirks worth knowing

- The admin/doctor login code (OTP) is emailed to that admin's/doctor's
  own email address (as set in the admin panel). In demo mode (no real
  Gmail credentials configured), no email actually goes out — the OTP
  is instead printed to the server terminal window, which always works
  regardless of what email address is on file.
- The admin Dashboard has a couple of decorative chart widgets left
  over from the page's visual template — they show fixed placeholder
  numbers, not real data. Don't worry about them.
- Doctors added without a profile photo now show a generic placeholder
  photo instead of a broken image (this used to crash the page; it's
  been fixed), both on the public site and in the doctor's own
  dashboard.

## A 10-minute demo script to show someone

1. **Public site**: Home → click **Doctors** → search/filter for a
   doctor → click that doctor's **Book Now** → fill in the form → pay
   (demo mode, instant) → see the success message.
2. **Admin panel**: click "Admins Login" → log in (`admin`/`admin123`)
   → enter the OTP from the terminal → Dashboard (the counts went up)
   → click Appointments (see the one you just booked, status
   "Confirmed") → click **Cancel** on it, watch the status flip to
   "Cancelled" and the button change to **Confirm** → click Doctors →
   add a new doctor → click Departments → add a new department.
3. **Doctor portal**: click "Doctors Login" → log in as the doctor you
   just booked with (e.g. `Sarah`/`Sarah123`) → enter the OTP → click
   My Appointments (see the booking, with its own Confirm/Cancel
   button) → click Attendance → Mark Attendance → open the QR link
   from the terminal → you land on the admin's attendance list showing
   "Present."
4. Back on the public site, click Doctors again — the new doctor you
   added in step 2 now shows up in the list, searchable by name and
   department.

---

## Technical reference (addresses behind each click)

You never need these to use the site — they're here only if you want
to understand what's happening under the hood, or need to share a
direct link with someone else.

| Click | Address |
|---|---|
| Home | `http://127.0.0.1:8000/` |
| Doctors (public listing) | `/doctors_page/` |
| About | `/about_page/` |
| Services | `/service_page/` |
| Contact | `/contact_page/` |
| Appointments | `/appointment_page/` |
| Admins Login | `/primecare/prime/` |
| Doctors Login | `/doctors/sigin_page/` |
| Admin Dashboard | `/primecare/admin_page/` |
| Admin: Doctors (add) | `/primecare/view_doctors` |
| Admin: Doctors (list) | `/primecare/doctor_list` |
| Admin: Departments (add) | `/primecare/view_departments` |
| Admin: Departments (list) | `/primecare/view_department/` |
| Admin: Appointments | `/primecare/appoinment_list` |
| Admin: Cancel an appointment | `/primecare/cancel_appointment/<id>/` (button, not typed) |
| Admin: Confirm an appointment | `/primecare/confirm_appointment/<id>/` (button, not typed) |
| Admin: Messages | `/primecare/message_list` |
| Admin: Scan Attendance | `/primecare/scan_page/` |
| Admin: View Attendance | `/primecare/view_attendance/` (not linked in the sidebar — reached via the QR flow or by typing this address) |
| Doctor Dashboard | `/doctors/doctor_page/` |
| Doctor: My Appointments | `/doctors/doctor_appointments/` |
| Doctor: Cancel an appointment | `/doctors/cancel_appointment/<id>/` (button, not typed; doctor-owned only) |
| Doctor: Confirm an appointment | `/doctors/confirm_appointment/<id>/` (button, not typed; doctor-owned only) |
| Doctor: Attendance | `/doctors/attendance_page/` |
| Django's built-in admin (raw database editing, not part of the demo) | `/admin/` |
