import random
import time
from datetime import datetime
from pathlib import Path
import pandas as pd

# 1. Locate the data folder
project_dir = Path(__file__).resolve().parent.parent
data_dir = project_dir / "data"
data_dir.mkdir(parents=True, exist_ok=True)

users_file = data_dir / "users.csv"

# 2. Define available user details
countries = ["india", "canada", "usa", "uk", "japan"]

channels = [
    "organic",
    "Google ads",
    "reffrell",
    "Social media"
]

# 3. Read existing users
if users_file.exists():
    users_df = pd.read_csv(
        users_file,
        dtype={"user_id": str}
    )

    # Add this column if older users do not have timestamps
    if "created_at" not in users_df.columns:
        users_df["created_at"] = pd.NA

    # Find the highest existing user ID number
    id_numbers = (
        users_df["user_id"]
        .dropna()
        .astype(str)
        .str.extract(r"(\d+)$")[0]
    )

    max_id = pd.to_numeric(
        id_numbers,
        errors="coerce"
    ).max()

    next_id = int(max_id) + 1 if pd.notna(max_id) else 1

else:
    users_df = pd.DataFrame(
        columns=["user_id", "country", "channel", "created_at"]
    )
    next_id = 1

# 4. Generate a random number of new users
new_user_count = random.randint(80, 130)

# 5. Record the date and time of this batch
run_time = datetime.now()

new_users = []
while True:
# 6. Create the new user records
        for i in range(next_id, next_id + new_user_count):

            user = {
                "user_id": f"U{i:03d}",
                "country": random.choice(countries),
                "channel": random.choice(channels),
                "created_at": run_time.strftime("%Y-%m-%d %H:%M:%S")
            }

            new_users.append(user)

        # 7. Convert new users into a DataFrame
        new_users_df = pd.DataFrame(new_users)

        # 8. Append the new records to the existing users
        all_users_df = pd.concat(
            [users_df, new_users_df],
            ignore_index=True
        )

        # 9. Save the complete users history
        all_users_df.to_csv(
            users_file,
            index=False,
            encoding="utf-8-sig"
        )

        # 10. Save a separate file for this batch
        batch_file = data_dir / (
            f"new_users_{run_time:%Y-%m-%d_%H-%M-%S}.csv"
        )

        new_users_df.to_csv(
            batch_file,
            index=False,
            encoding="utf-8-sig"
        )

        # 11. Display the result
        print("New users created:", new_user_count)
        print("First new user:", new_users_df["user_id"].iloc[0])
        print("Last new user:", new_users_df["user_id"].iloc[-1])
        print("Creation date and time:", run_time)
        print("Updated users file:", users_file)
        print("New users report:", batch_file)
        time.sleep(10)