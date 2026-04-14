# Develoment Journal 

## 12/04/2026

In order to begin with a competent portfolio, I came with the idea to make a app that can scrap Telegram JobFinding chanels and make statistics over them, in order to put them in a dashboard and make a newsletter that make you a weekly summary of the job market.

after some thought, most abstrac dataflow would be this 

[Ingesting] -> [Processing] -> [Storing] -> [Serving]

for this fist day I would like to focus in the [ingesting] part, so today's goal is to being able to read messages for a random telegram chat and storagin them raw in a SQL database 

a mayor issue with 'that' is that i want the backend of the app to be storaged in my homelab, the best way to make this happend is using docker containers, which i have no prior experience with, so that's it.

To begin with the docker part, for today i'm going to ount tho separated containers, one for 'app' witch is the Pyton script with Telethon and another Oner for the SQL database (PostgreSQL)


## 13/04/2026

After a LOT of reading a documentating code i reach the first iteration, it basically scraps a certain amount of messages from a Telegram chat and stores them in a SQL database.

I'm pretty proud of this first iteration, it's not much but it's a start.

But crearly there's A LOT  coming up, i have to make a way to cleanease the data, separate a non-ofer from a ofer and being capable of stract the most important information from the ofers (like the job title, the company, the salary, the location, etc.) and vier how to alocate that in the database schema 

But right now, I'm going to update the README.md file to include the information of this first iteration. 
