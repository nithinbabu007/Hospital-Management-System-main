# Running PrimeCare Medical Institute on a Different PC

This project is a Django hospital-management demo (admin panel, doctor
portal, patient site). The `venv/` folder already in this repo was built
on someone else's computer and **will not work** anywhere else — its
`python.exe` points at a path that only existed on that machine. Follow
the steps below to set it up fresh.

## 1. Prerequisites

- **Python 3.12** (3.11+ should also work). Check with:
  ```powershell
  python --version
  ```
  If missing, install from https://www.python.org/downloads/ and make
  sure "Add Python to PATH" is checked during install.
- **Git** (optional, only if you cloned instead of copying the folder).

## 2. Get the project onto the new PC

Copy the whole project folder over (or `git clone` the repo), **except**
you do not need to copy the `venv/` folder — it's dead weight and won't
run. If you already copied it, just delete it:

```powershell
cd "D:\GIT\Hospital-Management-System-main\Hospital-Management-System-main"
Remove-Item -Recurse -Force venv       # the old, broken venv, if present
Remove-Item -Recurse -Force venv_new   # if present, also PC-specific
```

## 3. Create a fresh virtual environment

```powershell
cd "D:\GIT\Hospital-Management-System-main\Hospital-Management-System-main"
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Your prompt should now start with `(venv)`. If PowerShell blocks the
activation script with a execution-policy error, run this once (as the
current user, no admin needed) and try activating again:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

## 4. Install dependencies

There's no `requirements.txt` in this repo, so install the packages the
code imports directly:

```powershell
pip install django djangorestframework python-dotenv pillow qrcode razorpay twilio requests
```

(If you'd rather pin exact versions, see **Known-good versions** at the
bottom of this file.)

## 5. Set up the database

```powershell
python manage.py migrate
```

This creates `db.sqlite3` in the project root with all required tables.

## 6. Create an admin login

The admin panel (`/primecare/prime/`) and Django admin (`/admin/`) both
need a real Django user:

```powershell
python manage.py createsuperuser
```

Enter a username, email, and password when prompted. (Email can be
anything, e.g. `admin@example.com` — it doesn't need to be real unless
you configure real SMTP, see step 8.)

**Suggested demo credentials** (matches what `how_everything_works.md`
uses in its examples, so the two files stay consistent):

```
Username: admin
Email:    admin@example.com
Password: admin123
```

You can type whatever you like instead — just remember it, since there's
no "forgot password" page in this demo.

## 7. Add demo content (departments & doctors)

The site is empty until you add departments and doctors. Easiest way —
open a Django shell and paste this in one go:

```powershell
python manage.py shell
```

```python
from adminapp.models import departmentdb, doctordb

departmentdb.objects.get_or_create(dpt_name="Cardiology", defaults={
    "dpt_des": "Heart and cardiovascular care",
    "dpt_phone": "9876543210",
    "dpt_email": "cardiology@primecare.demo",
})
departmentdb.objects.get_or_create(dpt_name="Neurology", defaults={
    "dpt_des": "Brain and nervous system care",
    "dpt_phone": "9876543211",
    "dpt_email": "neurology@primecare.demo",
})
departmentdb.objects.get_or_create(dpt_name="Orthopedics", defaults={
    "dpt_des": "Bone and joint care",
    "dpt_phone": "9876543212",
    "dpt_email": "orthopedics@primecare.demo",
})

doctordb.objects.get_or_create(doc_phone="9000000001", defaults={
    "doc_name": "Sarah",
    "doc_dpt": "Cardiology",
    "doc_email": "sarah@primecare.demo",
    "doc_quali": "MD Cardiology",
})
doctordb.objects.get_or_create(doc_phone="9000000002", defaults={
    "doc_name": "James",
    "doc_dpt": "Neurology",
    "doc_email": "james@primecare.demo",
    "doc_quali": "MD Neurology",
})
doctordb.objects.get_or_create(doc_phone="9000000003", defaults={
    "doc_name": "Priya",
    "doc_dpt": "Orthopedics",
    "doc_email": "priya@primecare.demo",
    "doc_quali": "MS Orthopedics",
})
exit()
```

This matches the demo data already referenced in `how_everything_works.md`
(three departments, three doctors — Sarah, James, Priya). Add more
departments/doctors the same way, or just use the admin panel UI once
you've logged in (step 9) — "Add Department" / "Add Doctor" forms let you
upload real images too. New doctors immediately appear on the public
site's **Doctors** page (`/doctors_page/`) and the Home page doctor grid.

**Doctor portal login password rule:** the code sets each doctor's
password to `<doc_name>123`. So a doctor named `Sarah` logs in at
`/doctors/sigin_page/` with username `Sarah`, password `Sarah123`. Using
the seed data above, the three ready-to-use doctor logins are:

| Username | Password |
|---|---|
| `Sarah` | `Sarah123` |
| `James` | `James123` |
| `Priya` | `Priya123` |

## 8. (Optional) Real email / payment / SMS / AI chatbot

By default this project needs a Gmail app password, Razorpay keys,
Twilio credentials, and an OpenRouter API key — none of which are
required for a basic demo if the code has been patched to degrade
gracefully when they're missing (console-printed OTPs, simulated
payment, skipped SMS, canned chatbot reply). If your copy of this repo
already has those fallbacks, skip this step entirely and go to step 9.

To use the **real** integrations instead, create a file named `.env` in
the project root (same folder as `manage.py`):

```env
EMAIL_HOST_USER=youraddress@gmail.com
EMAIL_HOST_PASSWORD=your-16-char-gmail-app-password

RAZORPAY_KEY_ID=rzp_test_xxxxxxxx
RAZORPAY_KEY_SECRET=xxxxxxxxxxxxxxxx

OPENROUTER_API_KEY=sk-or-xxxxxxxx

TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxx
```

Notes:
- Gmail requires an **App Password**, not your normal password (Google
  account → Security → App passwords; needs 2-Step Verification on).
- Razorpay test keys are free from the Razorpay dashboard (test mode).
- Twilio trial accounts can only SMS verified numbers.
- Without this `.env` file (or with it only partially filled in), the
  OTP for admin/doctor login is printed to the terminal running
  `runserver` instead of emailed — watch that terminal when logging in.

## 9. Run the server

```powershell
python manage.py runserver
```

Leave this terminal open — it's the running server. Open a browser to:

| URL | What it is |
|---|---|
| `http://127.0.0.1:8000/` | Public patient home page |
| `http://127.0.0.1:8000/doctors_page/` | Public "Doctors" listing page (search + Book Now) |
| `http://127.0.0.1:8000/primecare/prime/` | Admin login |
| `http://127.0.0.1:8000/doctors/sigin_page/` | Doctor login |
| `http://127.0.0.1:8000/admin/` | Django's built-in admin |

You don't actually need to type most of these — once the server is
running, `http://127.0.0.1:8000/` is the only address a new user needs
to type; everything else is a click away. See `how_everything_works.md`
for the full click-by-click walkthrough, including the admin/doctor
login credentials above and how to confirm/cancel appointments.

Admin and doctor logins require entering an OTP after the password —
if you didn't set up real email (step 8), check the `runserver`
terminal window for a line like:

```
---Your OTP for admin login is 123456
```

## 10. Stopping the server

`Ctrl+C` in the terminal running `runserver`.

Next time, you only need steps 3 (activate, not create) and 9:

```powershell
cd "D:\GIT\Hospital-Management-System-main\Hospital-Management-System-main"
.\venv\Scripts\Activate.ps1
python manage.py runserver
```

---

## Troubleshooting

- **`ModuleNotFoundError: No module named 'X'`** — a package is missing;
  run `pip install X` inside the activated venv and try again.
- **`'venv_new' is not recognized...` / activation fails** — you're
  pointing at a venv folder that doesn't belong to this PC. Delete it
  and redo step 3.
- **OTP login never seems to arrive** — if no `.env` email credentials
  are set, the OTP is printed to the terminal running the server, not
  emailed. Scroll up in that terminal.
- **Images show as broken** — department/doctor images live in
  `media/`. If you added new departments/doctors without uploading an
  image, Django will show a blank image area (fine for a demo) — this
  only errors out if the code tries to read `.url` on a doctor that was
  never given an image; the patched views in this repo already guard
  against that for the public home page.
- **Port 8000 already in use** — run on a different port:
  `python manage.py runserver 127.0.0.1:8001`.

## Known-good versions (optional, for exact reproducibility)

```
Django==6.0.2
djangorestframework==3.16.1
python-dotenv==1.2.2
pillow==12.1.1
qrcode==8.2
razorpay==2.0.1
twilio==9.10.3
requests==2.32.5
```

Install with: `pip install -r run_on_another_pc_requirements.txt` if you
save the block above into that file, or just pass them individually to
`pip install`.
