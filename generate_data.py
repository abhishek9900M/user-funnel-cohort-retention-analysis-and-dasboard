import random
import random
from calendar import day_abbr
from pathlib import Path
import pandas as pd
from datetime import datetime , timedelta

from numpy.testing import print_coercion_tables

app_name = "Shopping_Analysis"
no_users = 3000
users = []
events = ["signup", "purchase","app_visit"]
countries = ["India","Canada","USA","UK","japan","China","Korea","UAE","Canada"]
channels = ["Organic","Google ads","Refrell","Social Media"]
event_time = datetime.now()
for i in range(1,3001):
        user= {
            "user_id" : f"U{i:003d}"  ,
            "country": random.choice(countries),
            "channel":random.choice(channels),
        }

        users.append(user)


df = pd.DataFrame(users)
# print(df.head())

project_dir = Path(__file__).resolve().parent.parent
data_dir = project_dir / "data"
data_dir.mkdir(parents=True, exist_ok=True)

df.to_csv(data_dir / "users.csv", index=False)
df1 = pd.read_csv(data_dir / "users.csv")
df2 = pd.read_csv(data_dir / "events.csv")
'''df2.to_csv(data_dir / "Event.csv", index=False)
'''
start_date = datetime.now().replace(
    hour=10, minute=0, second=0, microsecond=0
)

events = []
state = {u["user_id"]: {"signed_up": False, "activated": False} for u in users}
for i in range(1, 3001):
    user_id= f"U{i:03d}"
    i=i+1
    event_time = start_date + timedelta(
        minutes=random.randint(0, 600)
    )

    events.append({
        "user_id": user_id,
        "event_name": "app_visit" ,
      "event_timestamp": event_time })


    if random.random() < 0.76:
        event_time = event_time + timedelta(minutes=3)
        events.append({"user_id": user_id,
                     "event_name":"signup",
                    "event_timestamp": event_time })
        if random.random() < 0.40:
            event_time = event_time + timedelta(minutes=2)
            events.append({
                "user_id": user_id,
                "event_name": "search_used",
                "event_timestamp": event_time
            })

        if random.random() < 0.60:
            event_time = event_time + timedelta(minutes=4)
            events.append({
                "user_id": user_id,
                "event_name":"activation",
                "event_timestamp": event_time })
            if random.random() < 0.20:
                event_time = event_time + timedelta(minutes=5)
                events.append({
                    "user_id": user_id,
                    "event_name": "wishlist_used",
                    "event_timestamp": event_time
                })
            if random.random() < 0.50:
                event_time = event_time + timedelta(minutes=4)
                events.append({
                    "user_id": user_id,
                    "event_name":"purchase",
                    "event_timestamp": event_time
                })

all_ids = list(state.keys())
        # Generate random return visits over the next 30 d
for i in range(1, 31):
    event_time = start_date + timedelta(days=i-1)
    return_rate = 0.67 if i == 1 else random.uniform(0.50, 0.66)
    returning_ids = random.sample(all_ids, int( 3000* return_rate))
    for user_id in returning_ids:
        s = state[user_id]
        event_time = start_date + timedelta(days=i)
        events.append({
            "user_id": user_id,
            "event_name": "app_visit",
            "event_timestamp": event_time})



        # signup only if not signed up yet, and very low chance
        if not s["signed_up"] and random.random() < 0.05:
            event_time += timedelta(minutes=3)
            events.append({"user_id": user_id,
                           "event_name": "signup",
                           "event_timestamp": event_time})
            s["signed_up"] = True

        if random.random() < 0.54:
            event_time += timedelta(minutes=2)
            events.append({
                "user_id": user_id,
                "event_name": "search_used",
                "event_timestamp": event_time
            })

        # activation only after signup
        if  random.random() < 0.60:
            event_time += timedelta(minutes=4)
            events.append({
                "user_id": user_id,
                "event_name": "activation",
                "event_timestamp": event_time})
            s["activated"] = True

            if random.random() < 0.39:
                event_time = event_time + timedelta(minutes=5)
                events.append({
                    "user_id": user_id,
                    "event_name": "wishlist_used",
                    "event_timestamp": event_time
                })
            if random.random() <0.26:
                event_time = event_time + timedelta(minutes=4)
                events.append({
                    "user_id": user_id,
                    "event_name":"purchase",
                    "event_timestamp": event_time
                })



print(len(events),"events")
total_visits = sum(1 for e in events if e["event_name"] == "app_visit")
total_signups = sum(1 for e in events if e["event_name"] == "signup")
total_activation  = sum(1 for e in events if e["event_name"] == "activation")
total_purchase = sum(1 for e in events if e["event_name"] == "purchase")
total_search = sum(1 for e in events if e["event_name"] == "search_used")
total_wishlist_used = sum(1 for e in events if e["event_name"] == "wishlist_used")


print("Signup Rate ",round((total_signups/no_users)*100,2),"%")
print("Search Rate ",round((total_search/total_visits)*100,2),"%")
print("Activation Rate ",round((total_activation/total_visits)*100,2),"%")
print("Purchase Rate",round((total_purchase/total_activation)*100,2),"%")
print("Whishlist Rate",round((total_wishlist_used/total_activation)*100,2),"%")



funnel_df = pd.DataFrame([
        {"stage":"app_visit","users": total_visits,"Conversion Rate":"100%"},
        {"stage": "search", "users": total_search,"Conversion Rate":f"{round((total_search/total_visits)*100,2)}%"},
        {"stage": "signup", "users": total_signups,"Conversion Rate":f"{round((total_signups/no_users)*100,2)}%"},
        {"stage": "activation", "users": total_activation,"Conversion Rate":f"{round((total_activation/total_visits)*100,2)}%"},
        {"stage": "wishlist_used", "users": total_wishlist_used,"Conversion Rate":f"{round((total_wishlist_used/total_activation)*100,2)}%"},
        {"stage": "purchase", "users": total_purchase,"Conversion Rate":f"{round((total_purchase/total_activation)*100,2)}%"}
])
print(funnel_df.head(10))
events_df = pd.DataFrame(events)
events_df["event_timestamp"] = pd.to_datetime(events_df["event_timestamp"])
events_df["event_date"] = pd.to_datetime(events_df["event_timestamp"]).dt.date
#group by userid and min date = first visit
first_visit = events_df[events_df["event_name"]=="app_visit"].groupby("user_id")["event_date"].min()
print(first_visit.count())


#this filter out the visits data and dates only , user id and dates are copied into the visits df.
visits_df = events_df[events_df["event_name"].isin(["app_visit", "signup"])].copy()
visits_df["event_date"] = pd.to_datetime(visits_df["event_date"])

start_date1 = visits_df["event_date"].min().normalize()

'''for day in range(30):
    current_date = start_date1 + pd.Timedelta(days=day)
    daily_visits = visits_df[visits_df["event_date"].dt.normalize() == current_date ]
    total_visits = (daily_visits["event_name"] == "app_visit").sum()
    total_signups = (daily_visits["event_name"] == "signup").sum()

    print(f"Day {day + 1}: {current_date:%d-%b-%Y}")
    print("Total visits:", total_visits)
    print("Total signups:", total_signups)
    print("-------------------")

'''


events_df.to_csv(data_dir / "events.csv", index=False)
events_df.to_excel(data_dir / "events.xlsx", index=False, engine= "openpyxl")





