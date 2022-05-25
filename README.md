# RandPokeTeamBot
Code for the Twitter bot called @RandPokeTeamBot (the account is now now non-existant). This bot used to randomly generate a team of six Pokemon, along with ball caught in, gender, moveset, abilities, levels, and other information like forms. The goal is to make each Pokemon legally possible based on the stats given; only Pokemon that can have a certain ability will be able to randomly receive it, for example. This was achieved for every stat except for movesets, which are incredibly complicated and depend entirely on the path a Pokemon takes through the 25+yr set of games.

Users replying to the bot with "team me" receive and additional customized team.

This solution utilizes a Postgres DB to store all the above Pokemon data, and more. I opted to only have different forms in the database (that could be randomly selected) if those forms are available "out of battle". However in a next version, I may have valid in-battle forms, including a max of one mega-evolved Pokemon per team.

In the future, I also plan to turn this into a one-Pokemon generator and add a lot more complicated information, including a generated path through the games, and a resulting moveset from that path.

Previous (and future?) location: twitter.com/randpoketeambot
