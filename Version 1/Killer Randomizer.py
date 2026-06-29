import random
import pandas as pd

df = pd.read_csv("Killer Perks Dataset.csv")

all_killers = df["killer"].dropna().unique().tolist()
owned_killers = set(all_killers)

while True:
    print("\n===== Killer Filter =====")
    for i, killer in enumerate(all_killers, start=1):
        mark = "✓" if killer in owned_killers else " "
        print(f"{i:2}. [{mark}] {killer}")
    
    print("\nCommands:")
    print(" number = toggle killer")
    print(" r      = random build")
    print(" q      = quit")

    choice = input("> ").strip().lower()

    if choice == "q":
        break

    elif choice == "r":
        if not owned_killers:
            print("No killers selected!")
            continue
        
        filtered_df = df[df["killer"].isin(owned_killers)]

        killer = random.choice(list(owned_killers))
        perks = random.sample(filtered_df["perk"].tolist(), 4)

        print(f"\nKiller: {killer}")
        for i, perk in enumerate(perks, start=1):
            print(f"Perk {i}: {perk}")

    elif choice.isdigit():
        index = int(choice) - 1
        if 0 <= index < len(all_killers):
            killer = all_killers[index]

            if killer in owned_killers:
                owned_killers.remove(killer)
            else:
                owned_killers.add(killer)
