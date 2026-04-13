# Develoment Journal 

## 12/04/2026

In order to begin with a competent portfolio, I came with the idea to make a app that can scrap Telegram JobFinding chanels and make statistics over them, in order to put them in a dashboard and make a newsletter that make you a weekly summary of the job market.

after some thought, most abstrac dataflow would be this 

[Ingesting] -> [Processing] -> [Storing] -> [Serving]

for this fist day I would like to focus in the [ingesting] part, so today's goal is to being able to read messages for a random telegram chat and storagin them raw in a SQL database 

a mayor issue with 'that' is that i want the backend of the app to be storaged in my homelab, the best way to make this happend is using docker containers, which i have no prior experience with, so that's it.

To begin with the docker part, for today i'm going to ount tho separated containers, one for 'app' witch is the Pyton script with Telethon and another Oner for the SQL database (PostgreSQL)

