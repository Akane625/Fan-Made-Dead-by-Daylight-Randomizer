import tkinter as tk
import pandas as pd
import random

# ==========================================
# LOAD DATA
# ==========================================

df = pd.read_csv("Killer Perks Dataset.csv")

all_killers = sorted(df["killer"].dropna().unique())

# ==========================================
# MAIN WINDOW
# ==========================================

root = tk.Tk()
root.title("Dead by Daylight Randomizer")
root.geometry("500x350")
root.resizable(False, False)

# ==========================================
# VARIABLES
# ==========================================

killer_vars = {killer: tk.BooleanVar(value=True) for killer in all_killers}

# ==========================================
# FUNCTIONS
# ==========================================

def update_filter_label():
    selected = sum(var.get() for var in killer_vars.values())
    filter_label.config(text=f"Selected Killers: {selected}/{len(all_killers)}")


def generate_build():
    selected_killers = [k for k, v in killer_vars.items() if v.get()]

    if not selected_killers:
        result_label.config(text="Please select at least one killer.")
        return

    killer = random.choice(selected_killers)

    perk_pool = df.loc[
        df["killer"].isna() | df["killer"].isin(selected_killers), "perk"
    ].dropna().tolist()

    if len(perk_pool) < 4:
        result_label.config(text="Not enough perks available.")
        return

    selected_perks = random.sample(perk_pool, 4)

    output = f"Killer: {killer}\n\n" + "\n".join(
        f"Perk {i}: {perk}" for i, perk in enumerate(selected_perks, 1)
    )
    result_label.config(text=output)


def open_filter_window():
    window = tk.Toplevel(root)
    window.title("Owned Killer Filter")
    window.geometry("800x300")

    content = tk.Frame(window)
    content.pack(fill="both", expand=True)

    # ---- Left side: checkbox grid ----
    left = tk.Frame(content)
    left.pack(side="left", fill="both", expand=True)

    columns = 5
    for i, killer in enumerate(all_killers):
        tk.Checkbutton(
            left,
            text=killer,
            variable=killer_vars[killer],
            command=update_filter_label
        ).grid(row=i // columns, column=i % columns, sticky="w", padx=10, pady=3)

    # ---- Right side: action buttons ----
    right = tk.Frame(content)
    right.pack(side="right", fill="y", padx=4, pady=10)

    def set_all(value):
        for var in killer_vars.values():
            var.set(value)
        update_filter_label()

    for text, cmd in [
        ("Select All", lambda: set_all(True)),
        ("Deselect All", lambda: set_all(False)),
        ("Save & Close", window.destroy),
    ]:
        tk.Button(right, text=text, width=18, command=cmd).pack(pady=8)


# ==========================================
# LAYOUT
# ==========================================

tk.Label(root, text="Dead by Daylight Randomizer", font=("Arial", 18, "bold")).pack(pady=15)

filter_label = tk.Label(root, font=("Arial", 11))
filter_label.pack()
update_filter_label()

button_frame = tk.Frame(root)
button_frame.pack(pady=15)

tk.Button(button_frame, text="Edit Killer Filter", width=18, command=open_filter_window) \
    .grid(row=0, column=0, padx=10)
tk.Button(button_frame, text="Generate Build", width=18, command=generate_build) \
    .grid(row=0, column=1, padx=10)

result_frame = tk.LabelFrame(root, text="Generated Build", padx=15, pady=15)
result_frame.pack(fill="both", expand=True, padx=20, pady=15)

result_label = tk.Label(
    result_frame,
    text="Click Generate Build!",
    justify="left",
    anchor="nw",
    font=("Consolas", 11)
)
result_label.pack(anchor="nw")

# ==========================================
# START
# ==========================================

root.mainloop()
