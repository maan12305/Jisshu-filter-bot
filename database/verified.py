import pymongo
from info import DATABASE_NAME, DATABASE_URI
from datetime import datetime, timedelta
import pytz
from info import DATABASE_URI, DATABASE_NAME
import motor.motor_asyncio
from pymongo.errors import DuplicateKeyError

import logging
import asyncio

logger = logging.getLogger(_name_)
logger.setLevel(logging.ERROR)



class anshalllist:
    def init(self):
        client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URI)
        db = client[DATABASE_NAME]    
        self.totalverified = db["total_verified"]
      

async def total_verified(self):
        # Get current date and time
        current_datetime = datetime.now(pytz.timezone("Asia/Kolkata"))

        # Get current date
        current_date = datetime.combine(current_datetime.date(), datetime.min.time())

        # Extract current month, year, and day
        current_month = current_date.month
        current_year = current_date.year
        current_day = current_date.day

        # Check if the file exists in the collection
        total_verified = await self.totalverified.find_one({"TOTAL_VERIFIED": "ANSH"})

        if total_verified:
            last_verified_datetime = total_verified.get("last_verified")  # Get last forwarded datetime
            last_verified_date = datetime.combine(last_verified_datetime.date(), datetime.min.time())  # Convert to datetime object

            # Extract last forwarded month, year, and day
            last_verified_month = last_verified_date.month
            last_verified_year = last_verified_date.year
            last_verified_day = last_verified_date.day

            # Calculate the difference in months
            month_difference = (current_year - last_verified_year) * 12 + current_month - last_verified_month

            # Update counts for the current month, year, and total
            if current_month == last_verified_month and current_year == last_verified_year:
                await self.totalverified.update_one(
                    {"TOTAL_VERIFIED": "ANSH"},
                    {"$inc": {"this_month": 1, "this_year": 1, "total_verified": 1}},
                    upsert=False
                )
            elif current_year == last_verified_year:
                await self.totalverified.update_one(
                    {"TOTAL_VERIFIED": "ANSH"},
                    {"$set": {"this_month": 1}, "$inc": {"this_year": 1, "total_verified": 1}},
                    upsert=False
                )
            else:
                await self.totalverified.update_one(
                    {"TOTAL_VERIFIED": "ANSH"},
                    {"$set": {"this_month": 1, "this_year": 1}, "$inc": {"total_verified": 1}},
                    upsert=False
                )

            # If the last forwarded date is the current date, update the forward count for today and the last forwarded date
            if last_verified_date.date() == current_date.date():
                await self.totalverified.update_one(
                    {"TOTAL_VERIFIED": "ANSH"},
                    {"$inc": {"verified_count_today": 1}, "$set": {"last_verified": current_date}},
                    upsert=False
                )
            elif (current_date - last_verified_date).days == 1:  # If there's a gap of 1 day
                await self.totalverified.update_one(
                    {"TOTAL_VERIFIED": "ANSH"},
                    {"$set": {
                        "verified_count_yesterday": total_verified.get("verified_count_today", 0),
                        "verified_count_today": 1,
                        "last_verified": current_date
                    }},
                    upsert=False
                )
            else:  # Reset today's count if there's a gap of more than 1 day
                await self.totalverified.update_one(
                  {"TOTAL_VERIFIED": "ANSH"},
                    {"$set": {
                        "verified_count_today": 1,
                        "verified_count_yesterday": 0,
                        "last_verified": current_date
                    }},
                    upsert=False
                )

            # Check if last month's count needs to be updated
            if month_difference == 1:
                # If there's a gap of 1 month, update last month's count
                await self.totalverified.update_one(
                    {"TOTAL_VERIFIED": "ANSH"},
                    {"$set": {"last_month_count": total_verified.get("this_month", 0)}},
                    upsert=False
                )            
        else:
            # If the file doesn't exist, add it to the collection with forward count for today
            await self.totalverified.insert_one(
                {
                    "TOTAL_VERIFIED": "ANSH", 
                    "verified_count_today": 1,
                    "verified_count_yesterday": 0,
                    "this_month": 1,
                    "last_month_count": 0,
                    "this_year": 1,
                    "total_verified": 1,
                    "last_verified": current_date
                }
            )
        
ansh = anshalllist()
