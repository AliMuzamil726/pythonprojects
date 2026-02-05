# blood_management_with_model.py
import sqlite3
from datetime import datetime, timedelta
from collections import defaultdict
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Image, Spacer, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from sklearn.linear_model import LinearRegression
import numpy as np

# -------------------------------------------------
# Configuration
# -------------------------------------------------
DB_NAME = "blood_bank.db"
PDF_TITLE = "Blood Bank Stock & Forecast Report"
THRESHOLDS = {"high": 10, "medium": 5}
FORECAST_DAYS = 30          # how many days ahead the model predicts
MODEL_PATH = "demand_model.pkl"   # not persisted – rebuilt each run

# -------------------------------------------------
# Database layer
# -------------------------------------------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS donors (
                       donor_id TEXT PRIMARY KEY,
                       name TEXT NOT NULL,
                       blood_type TEXT NOT NULL,
                       last_donation TEXT)""")
    cur.execute("""CREATE TABLE IF NOT EXISTS recipients (
                       recipient_id TEXT PRIMARY KEY,
                       name TEXT NOT NULL,
                       blood_type TEXT NOT NULL,
                       required_units INTEGER NOT NULL,
                       request_date TEXT NOT NULL)""")
    cur.execute("""CREATE TABLE IF NOT EXISTS inventory (
                       blood_type TEXT,
                       donation_date TEXT,
                       units INTEGER,
                       PRIMARY KEY (blood_type, donation_date))""")
    conn.commit()
    conn.close()

def execute(query, params=()):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(query, params)
    conn.commit()
    rows = cur.fetchall()
    conn.close()
    return rows

# -------------------------------------------------
# Business logic (unchanged)
# -------------------------------------------------
COMPATIBILITY = {
    "O-": ["O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+"],
    "O+": ["O+", "A+", "B+", "AB+"],
    "A-": ["A-", "A+", "AB-", "AB+"],
    "A+": ["A+", "AB+"],
    "B-": ["B-", "B+", "AB-", "AB+"],
    "B+": ["B+", "AB+"],
    "AB-": ["AB-", "AB+"],
    "AB+": ["AB+"],
}
def compatible(donor_bt, recipient_bt):
    return recipient_bt in COMPATIBILITY.get(donor_bt, [])

def add_donor(donor_id, name, blood_type):
    execute("INSERT INTO donors VALUES (?,?,?,?)",
            (donor_id, name, blood_type, None))

def record_donation(donor_id, units, donation_date):
    donor_bt = execute("SELECT blood_type FROM donors WHERE donor_id=?", (donor_id,))[0][0]
    execute("""INSERT OR REPLACE INTO inventory (blood_type, donation_date, units)
               VALUES (?,?,COALESCE((SELECT units FROM inventory WHERE blood_type=? AND donation_date=?),0)+?)""",
            (donor_bt, donation_date, donor_bt, donation_date, units))
    execute("UPDATE donors SET last_donation=? WHERE donor_id=?", (donation_date, donor_id))

def add_recipient(recipient_id, name, blood_type, required_units):
    today = datetime.now().strftime("%Y-%m-%d")
    execute("INSERT INTO recipients VALUES (?,?,?,?,?)",
            (recipient_id, name, blood_type, required_units, today))

def get_inventory():
    rows = execute("SELECT blood_type, donation_date, units FROM inventory")
    inv = defaultdict(list)
    for bt, d, u in rows:
        inv[bt].append((datetime.strptime(d, "%Y-%m-%d"), u))
    for bt in inv:
        inv[bt].sort(key=lambda x: x[0])
    return inv

def allocate(blood_type, needed):
    inv = get_inventory()
    batches = inv.get(blood_type, [])
    allocated = []
    remaining = needed
    for i, (date, units) in enumerate(batches):
        if remaining <= 0:
            break
        take = min(units, remaining)
        allocated.append((date, take))
        remaining -= take
        new_units = units - take
        if new_units == 0:
            execute("DELETE FROM inventory WHERE blood_type=? AND donation_date=?",
                    (blood_type, date.strftime("%Y-%m-%d")))
        else:
            execute("UPDATE inventory SET units=? WHERE blood_type=? AND donation_date=?",
                    (new_units, blood_type, date.strftime("%Y-%m-%d")))
    return allocated if remaining == 0 else None

def process_transfusion(recipient_id):
    rec = execute("SELECT name, blood_type, required_units FROM recipients WHERE recipient_id=?",
                  (recipient_id,))[0]
    name, r_bt, needed = rec
    compatible_types = [bt for bt in COMPATIBILITY if r_bt in COMPATIBILITY[bt]]
    for bt in compatible_types:
        if allocate(bt, needed):
            messagebox.showinfo("Success",
                                f"{needed} units of {bt} allocated to {name}.")
            return True
    messagebox.showwarning("Failed",
                           f"Insufficient compatible blood for {name}.")
    return False

# -------------------------------------------------
# Excel / PDF handling (same as previous version)
# -------------------------------------------------
def export_inventory_to_excel(filepath):
    inv = get_inventory()
    data = []
    for bt, batches in inv.items():
        for d, u in batches:
            data.append({"Blood Type": bt,
                         "Donation Date": d.strftime("%Y-%m-%d"),
                         "Units": u})
    pd.DataFrame(data).to_excel(filepath, index=False)
    messagebox.showinfo("Exported", f"Inventory saved to {filepath}")

def import_excel_to_db(filepath):
    df = pd.read_excel(filepath, engine="openpyxl")
    for _, row in df.iterrows():
        bt = str(row["Blood Type"]).strip().upper()
        date = pd.to_datetime(row["Donation Date"]).strftime("%Y-%m-%d")
        units = int(row["Units"])
        execute("""INSERT OR REPLACE INTO inventory (blood_type, donation_date, units)
                   VALUES (?,?,COALESCE((SELECT units FROM inventory WHERE blood_type=? AND donation_date=?),0)+?)""",
                (bt, date, bt, date, units))
    messagebox.showinfo("Imported", f"Data from {filepath} loaded.")

def generate_pdf_report(filepath):
    inv = get_inventory()
    # Table data
    table_data = [["Blood Type", "Donation Date", "Units"]]
    for bt, batches in inv.items():
        for d, u in batches:
            table_data.append([bt, d.strftime("%Y-%m-%d"), str(u)])

    c = canvas.Canvas(filepath, pagesize=A4)
    width, height = A4
    y = height - 50
    c.setFont("Helvetica-Bold", 20)
    c.drawString(40, y, PDF_TITLE)
    y -= 30

    # Table
    style = TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
        ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold")
    ])
    tbl = Table(table_data, colWidths=[120, 150, 80])
    tbl.setStyle(style)
    tbl.wrapOn(c, width, height)
    tbl.drawOn(c, 40, y - tbl._height)
    y -= tbl._height + 30

    # Forecast chart (generated later)
    fig, ax = plot_forecast()
    chart_path = "temp_forecast.png"
    fig.savefig(chart_path, bbox_inches="tight")
    plt.close(fig)
    c.drawImage(chart_path, 40, y-200, width=500, preserveAspectRatio=True)
    c.showPage()
    c.save()
    messagebox.showinfo("PDF Created", f"Report saved to {filepath}")

# -------------------------------------------------
# Demand‑forecast model
# -------------------------------------------------
def _historical_demand():
    """Return a DataFrame with columns: blood_type, day_offset, units_requested."""
    rows = execute("SELECT blood_type, required_units, request_date FROM recipients")
    data = []
    today = datetime.now()
    for bt, units, date_str in rows:
        day_offset = (today - datetime.strptime(date_str, "%Y-%m-%d")).days
        data.append({"blood_type": bt, "day_offset": day_offset, "units": units})
    return pd.DataFrame(data)

def train_demand_model():
    """Train a separate linear regression for each blood type."""
    df = _historical_demand()
    models = {}
    for bt in df["blood_type"].unique():
        sub = df[df["blood_type"] == bt]
        X = sub[["day_offset"]].values
        y = sub["units"].values
        if len(X) < 2:   # not enough data – fallback to mean
            pred = np.mean(y) if len(y) > 0 else 0
            models[bt] = lambda _: pred
            continue
        reg = LinearRegression()
        reg.fit(X, y)
        models[bt] = lambda days, r=reg: max(0, r.predict([[days]])[0])
    return models

def predict_demand(models, days_ahead=FORECAST_DAYS):
    """Return dict blood_type → predicted units for the next *days_ahead* days."""
    preds = {}
    for bt, func in models.items():
        preds[bt] = func(days_ahead)
    return preds

def plot_forecast():
    """Create a Matplotlib figure that shows current stock + forecast."""
    inv = get_inventory()
    current = {bt: sum(u for _, u in batches) for bt, batches in inv.items()}
    models = train_demand_model()
    forecast = predict_demand(models)

    blood = sorted(set(current) | set(forecast))
    stock_vals = [current.get(bt, 0) for bt in blood]
    forecast_vals = [forecast.get(bt, 0) for bt in blood]

    fig, ax = plt.subplots(figsize=(8, 4))
    x = np.arange(len(blood))
    width = 0.35
    ax.bar(x - width/2, stock_vals, width, label="Current Stock",
           color=[_bar_colour(v) for v in stock_vals])
    ax.bar(x + width/2, forecast_vals, width, label=f"Forecast ({FORECAST_DAYS} d)",
           color="#2196f3")
    ax.set_xticks(x)
    ax.set_xticklabels(blood)
    ax.set_ylabel("Units")
    ax.set_title("Stock vs. 30‑Day Demand Forecast")
    ax.legend()
    return fig, ax

def _bar_colour(units):
    if units >= THRESHOLDS["high"]:
        return "#4caf50"
    elif units >= THRESHOLDS["medium"]:
        return "#ff9800"
    else:
        return "#f44336"

# -------------------------------------------------
# GUI – integrates forecast chart
# -------------------------------------------------
class BloodApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🩸 Blood Management System – Forecast Edition")
        self.geometry("1080x780")
        self.configure(bg="#fafafa")
        self._create_menu()
        self._create_dashboard()
        self._create_log()
        self.refresh_dashboard()

    # ----- Menus -----
    def _create_menu(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        donor = tk.Menu(menubar, tearoff=0)
        donor.add_command(label="Add Donor", command=self.add_donor_dialog)
        donor.add_command(label="Record Donation", command=self.record_donation_dialog)
        menubar.add_cascade(label="Donors", menu=donor)

        rec = tk.Menu(menubar, tearoff=0)
        rec.add_command(label="Add Recipient", command=self.add_recipient_dialog)
        rec.add_command(label="Process Transfusion", command=self.process_transfusion_dialog)
        menubar.add_cascade(label="Recipients", menu=rec)

        rep = tk.Menu(menubar, tearoff=0)
        rep.add_command(label="Export → Excel", command=self.export_excel_dialog)
        rep.add_command(label="Import ← Excel", command=self.import_excel_dialog)
        rep.add_separator()
        rep.add_command(label="Generate PDF Report", command=self.pdf_report_dialog)
        menubar.add_cascade(label="Reports", menu=rep)

    # ----- Dashboard (stock + forecast) -----
    def _create_dashboard(self):
        dash = ttk.LabelFrame(self, text="Stock & Forecast Dashboard", padding=10)
        dash.pack(fill="both", expand=True, padx=12, pady=12)

        self.fig, self.ax = plt.subplots(figsize=(9, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=dash)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def refresh_dashboard(self):
        fig, ax = plot_forecast()
        self.fig.clf()
        self.ax = self.fig.add_subplot(111)
        # copy the generated axes into the displayed figure
        for artist in fig.axes[0].get_children():
            artist.remove()
            self.ax.add_artist(artist)
        self.canvas.draw()

    # ----- Log -----
    def _create_log(self):
        log_frame = ttk.LabelFrame(self, text="Activity Log", padding=5)
        log_frame.pack(fill="x", padx=12, pady=(0,12))
        self.log = tk.Text(log_frame, height=6, state="disabled", bg="#ffffff")
        self.log.pack(fill="x", padx=5, pady=5)

    def _log(self, msg):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log.configure(state="normal")
        self.log.insert("end", f"[{ts}] {msg}\n")
        self.log.configure(state="disabled")
        self.log.see("end")

    # ----- Simple form helper -----
    def _simple_form(self, master, fields):
        entries = {}
        for i, (lbl, key) in enumerate(fields):
            ttk.Label(master, text=lbl).grid(row=i, column=0, sticky="e", pady=2)
            ent = ttk.Entry(master)
            ent.grid(row=i, column=1, pady=2, padx=5)
            entries[key] = ent
        master.result = entries
        return master

    # ----- Dialogs (add donor, donation, recipient) -----
    def add_donor_dialog(self):
        dlg = simpledialog.Dialog(self, title="Add New Donor")
        dlg.body = lambda m: self._simple_form(m,
            [("Donor ID", "id"), ("Name", "name"), ("Blood Type", "bt")])
        dlg.apply = lambda: self._save_new_donor(dlg.result)

    def _save_new_donor(self, f):
        did = f["id"].get().strip()
        name = f["name"].get().strip()
        bt = f["bt"].get().strip().upper()
        if not (did and name and bt):
            messagebox.showerror("Error", "All fields required.")
            return
        add_donor(did, name, bt)
        self._log(f"Added donor {did} – {name} ({bt})")
        self.refresh_dashboard()

    def record_donation_dialog(self):
        dlg = simpledialog.Dialog(self, title="Record Donation")
        dlg.body = lambda m: self._simple_form(m,
            [("Donor ID", "id"), ("Units", "units"), ("Date (YYYY‑MM‑DD)", "date")])
        dlg.apply = lambda: self._save_donation(dlg.result)

    def _save_donation(self, f):
        did = f["id"].get().strip()
        units = f["units"].get().strip()
        date = f["date"].get().strip()
        try:
            units = int(units)
            datetime.strptime(date, "%Y-%m-%d")
        except Exception:
            messagebox.showerror("Error", "Invalid units or date.")
            return
        record_donation(did, units, date)
        self._log(f"Donation: {units} units from {did} on {date}")
        self.refresh_dashboard()

    def add_recipient_dialog(self):
        dlg = simpledialog.Dialog(self, title="Add Recipient")
        dlg.body = lambda m: self._simple_form(m,
            [("Recipient ID", "id"), ("Name", "name"),
             ("Blood Type", "bt"), ("Required Units", "units")])
        dlg.apply = lambda: self._save_new_recipient(dlg.result)

    def _save_new_recipient(self, f):
        rid = f["id"].get().strip()
        name = f["name"].get().strip()
        bt = f["bt"].get().strip().upper()
        units = f["units"].get().strip()
        try:
            units = int(units)
        except Exception:
            messagebox.showerror("Error", "Units must be integer.")
            return
        add_recipient(rid, name, bt, units)
        self._log(f"Added recipient {rid} – {name} ({bt}) needs {units}")
        self.refresh_dashboard()

    def process_transfusion_dialog(self):
        rid = simpledialog.askstring("Transfusion", "Recipient ID:")
        if rid and process_transfusion(rid.strip()):
            self._log(f"Transfusion processed for {rid}")

    # ----- Report dialogs -----
    def export_excel_dialog(self):
        path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                           filetypes=[("Excel files", "*.xlsx")],
                                           title="Save inventory as Excel")
        if path:
            export_inventory_to_excel(path)

    def import_excel_dialog(self):
        path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")],
                                          title="Import inventory from Excel")
        if path:
            import_excel_to_db(path)
            self.refresh_dashboard()

    def pdf_report_dialog(self):
        path = filedialog.asksaveasfilename(defaultextension=".pdf",
                                           filetypes=[("PDF files", "*.pdf")],
                                           title="Save PDF report")
        if path:
            generate_pdf_report(path)

# -------------------------------------------------
# Application entry point
# -------------------------------------------------
if __name__ == "__main__":
    init_db()
    app = BloodApp()
    app.mainloop()
