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

## 14/04/2026

today i did't did nothing, i mean, i just will star working after mmidnight, but what concerns about "what i did in the 14th day of april" no pal i didn't did nothing, i readed LN all day since my internet provider decided to fuck me, and also i did college work, so ok

"tomorow" (today past midnight) i'll have a website where to test, that include integrate the fist API so

and also i'll have resolved the first step in prossesing the data 

*btw i just did this entry in the journal just for not losing that green dot in my github*

## 15/04/2026

i dedicated into introducing me to react, because i think is the best approach to the fonrtend part of the project 
learning concepts like single page applications and components (functions than return html) show me why this is considered advance frontend.

### Iteration 1.5
Ok, for the 1.5 iteration I want to add ract to my stack, thats because is the best frontend tool that would help me with the graphs and chart i'm willing to use, also if a next iteration i decide to do a movile feature, it would save a lot of work

## 16/04/2026

Ok, personal info dump: i have other things to do, like tomorow i have a Fourier's analysis exam and the day after my band have a gig, but screw it, this data extraction have to be done, and i'm pretty sure i can do it in a day or two, so let's do it 

right now une of my aideas is use the Kor library

## 19/04/26

Due i didn't did nothing