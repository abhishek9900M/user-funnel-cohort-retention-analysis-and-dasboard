import random
import random
from calendar import day_abbr
from pathlib import Path
import pandas as pd
from datetime import datetime , timedelta

from numpy.testing import print_coercion_tables

app_name = "Shopping_Analysis"
no_users = 1000
users = []
events = ["signup", "purchase","app_visit"]
countries = ["india","canada","usa","uk","japan"]
channels = ["organic","Google ads","reffrell","Social media"]
event_time = datetime.now()
for i in range(1,1001):
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
'''df2.to_csv(data_dir / "Event.csv", index=False)
'''
start_date = datetime.now().replace(
    hour=10, minute=0, second=0, microsecond=0
)
events = []
state = {u["user_id"]: {"signed_up": False, "activated": False} for u in users}
for i in range(1, 1001):
    user_id= f"U{i:03d}"
    event_time = start_date + timedelta(
        minutes=random.randint(0, 600)
    )

    events.append({
        "user_id": user_id,
        "event_name": "app_visit" ,
      "event_timestamp": event_time })


    if random.random() < 0.86:
        event_time = event_time + timedelta(minutes=3)
        events.append({"user_id": user_id,
                     "event_name":"signup",
                    "event_timestamp": event_time })
        if random.random() < 0.50:
            event_time = event_time + timedelta(minutes=2)
            events.append({
                "user_id": user_id,
                "event_name": "search_used",
                "event_timestamp": event_time
            })

        if random.random() < 0.70:
            event_time = event_time + timedelta(minutes=4)
            events.append({
                "user_id": user_id,
                "event_name":"activation",
                "event_timestamp": event_time })
            if random.random() < 0.30:
                event_time = event_time + timedelta(minutes=5)
                events.append({
                    "user_id": user_id,
                    "event_name": "wishlist_used",
                    "event_timestamp": event_time
                })
            if random.random() < 0.60:
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
    returning_ids = random.sample(all_ids, int( 1000* return_rate))
    for user_id in returning_ids:
        s = state[user_id]
        event_time = start_date + timedelta(days=i)
        events.append({
            "user_id": user_id,
            "event_name": "app_visit",
            "event_timestamp": event_time})



        # signup only if not signed up yet, and very low chance
        if not s["signed_up"] and random.random() < 0.07:
            event_time += timedelta(minutes=3)
            events.append({"user_id": user_id,
                           "event_name": "signup",
                           "event_timestamp": event_time})
            s["signed_up"] = True

        if random.random() < 0.66:
            event_time += timedelta(minutes=2)
            events.append({
                "user_id": user_id,
                "event_name": "search_used",
                "event_timestamp": event_time
            })

        # activation only after signup
        if  random.random() < 0.70:
            event_time += timedelta(minutes=4)
            events.append({
                "user_id": user_id,
                "event_name": "activation",
                "event_timestamp": event_time})
            s["activated"] = True

            if random.random() < 0.40:
                event_time = event_time + timedelta(minutes=5)
                events.append({
                    "user_id": user_id,
                    "event_name": "wishlist_used",
                    "event_timestamp": event_time
                })
            if random.random() <0.36:
                event_time = event_time + timedelta(minutes=4)
                events.append({
                    "user_id": user_id,
                    "event_name":"purchase",
                    "event_timestamp": event_time
                })




'''print(events[:5])'''
print(len(events),"events")
'''print("visits:",sum(1 for e in events if e["event_name"] == "app_visit"))
print("signups:",sum(1 for e in events if e["event_name"] == "signup"))
print("activated:", sum(1 for e in events if e["event_name"] == "activation"))
print("purchased:", sum(1 for e in events if e["event_name"] == "purchase"))'''
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

events_df = pd.DataFrame(events)
events_df.to_csv(data_dir / "events.csv", index=False)
events_df.to_excel(data_dir / "events.xlsx", index=False, engine= "openpyxl")

'''print(events_df.head(10))
'''
'''events_df = pd.read_csv(data_dir /  "events.csv")
print(events_df.head())
print("Rows & Columns:",events_df.shape)
print("Events_Type:",events_df["event_name"].unique())'''

'''Total_visits=(events_df["event_name"] == "app_visit").sum()
print("Total_visits",Total_visits)
Total_signup=(events_df["event_name"] == "signup").sum()
print("Total_signup",Total_signup)
Total_activation=(events_df["event_name"] == "activated").sum()
print("Total_activation",Total_activation)
total_search = (events_df["event_name"] == "search_used").sum()
total_wishlist_used = (events_df["event_name"] == "wishlist_used").sum()
total_purchase = (events_df["event_name"] == "purchase").sum()'''



funnel_df = pd.DataFrame([
        {"stage":"app_visit","users": total_visits,"Conversion Rate":"100%"},
        {"stage": "search", "users": total_search,"Conversion Rate":f"{round((total_search/total_visits)*100,2)}%"},
        {"stage": "signup", "users": total_signups,"Conversion Rate":f"{round((total_signups/no_users)*100,2)}%"},
        {"stage": "activation", "users": total_activation,"Conversion Rate":f"{round((total_activation/total_visits)*100,2)}%"},
        {"stage": "wishlist_used", "users": total_wishlist_used,"Conversion Rate":f"{round((total_wishlist_used/total_activation)*100,2)}%"},
        {"stage": "purchase", "users": total_purchase,"Conversion Rate":f"{round((total_purchase/total_activation)*100,2)}%"}
])
print(funnel_df.head(10))

events_df["event_timestamp"] = pd.to_datetime(events_df["event_timestamp"])
events_df["event_date"] = pd.to_datetime(events_df["event_timestamp"]).dt.date
#group by userid and min date = first visit
first_visit = events_df[events_df["event_name"]=="app_visit"].groupby("user_id")["event_date"].min()
print(first_visit.count())

visits_df = events_df[events_df["event_name"] == "app_visit"].copy()

visits_df["event_date"] = pd.to_datetime(visits_df["event_date"])

start_date = visits_df["event_date"].min().normalize()

for day in range(30):
    current_date = start_date + pd.Timedelta(days=day)

    daily_visits = visits_df[
        visits_df["event_date"].dt.normalize() == current_date ]

    print(f"Day {day + 1}: {current_date:%d-%b-%Y}")
    print("Total visits:", len(daily_visits))
    print("-------------------")
#print(first_visit.head(2))




# Find users present on both days
'''returned_user_ids = day1_user_ids & day2_user_ids

print("Day 1 users:", len(day1_user_ids))
print("Day 2 visitors:", len(day2_user_ids))


print("Returning users:", len(returned_user_ids))
if len(returned_user_ids)>0:
    retention_rate = len(returned_user_ids) / len(day1_user_ids) * 100
    print(round(retention_rate,2),"%")

else:
    retention_rate = 0'''







'''day0_date = first_visit.min()

day0_users = events_df[(events_df["event_name"]=="app_visit") & (events_df["event_date"]==day0_date)]["user_id"].nunique()


day1_date = day0_date + timedelta(days=1)

day1_user = events_df[(events_df["event_name"]=="app_visit")&(events_df["event_date"]==day1_date)]["user_id"].nunique()
print("day0",day0_users)
print("day1 ",day1_user)


returned_user = day1_user & day0_users
print("return users : ", returned_user)
print("Return users :",len(returned_user))'''



'''current_time = datetime.now()
later_time = current_time + timedelta(minutes=2)
print(current_time)
print(later_time)
'''
'''current_time = datetime.now()
later_time = current_time + timedelta(minutes=2)
print(current_time)
print(later_time)
'''









