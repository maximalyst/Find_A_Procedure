# Find A Procedure tool

The goal of this package is to parse and provide data for a future web tool for CFIs, students, or anyone who wants to asks, "What procedures have these characteristics?" This started when I first learned about back course approaches, and found a list only after some searching. Then I wanted to know which approaches might have Outer, Middle or Inner markers, but I couldn't find that at all (Seems they're mostly gone now anyway).

A post on reddit seemed to indicate some demand for a tool like this, so here we are.

The FAA posts the Coded Instrument Flight Procedures [here](https://www.faa.gov/air_traffic/flight_info/aeronav/digital_products/cifp) in ARINC 424 v18 form. The code in this repository is meant to parse this data for use on the web tool by creating a SQLite database from the raw data. Unfortunately the specification is proprietary, so I will not post it within this repo.

Initially I'm just getting a minimum viable product to input into the web tool--there's much more information in the CIFP than I'm bothering to parse. I mainly want to ask the basic questions like "Where in the US or Canada can I find [xxx] type of procedure?"

I'm happy to get tips on coding style etc.--I'm also using this as an excuse to get better at both Python and SQL. Feel free to take a look, fork, edit, etc. as allowed within the license file.

If you find it useful, I'd also appreciate a value for value contribution to the tip jar--hit me up @bransmit246 on Venmo.