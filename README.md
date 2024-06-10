<h1 align="center">Data Engineering</h1>

<p align="center">CinePlex Tracker</p>

## Introduction

This project aims to create a data pipeline with Python, AirFlow, Kafka Connect, ElasticSearch and mongoDB,
which allows users to search movies and subscribe for updates.



## API:
Query Movie: GET /movies/query <br />
Get Movie: GET /movies/{movie_id} <br />
Subscribe movie updates: POST /movies/{movie_id}/subs

## Schema
![](graph/schema.png)

## Architecture ##

![](graph/arch.png)


## Author
- [@harrison](https://github.com/harrison-yck)