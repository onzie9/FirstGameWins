I asked myself the question "what is the minimum number of (NHL) hockey teams that have to lose their first game of a season if there are n teams and all teams play at least once within k days?" The answer was suprisingly interesting. I wanted to apply the idea to actual NHL data, so that's what I wrote up here.

The general idea here is that if we have unlimited days at the start of a season, we can grow the number of teams exponentially with only one team having to lose their first game on the first day. Also in the NHL, teams can't play 3 days in a row, so I took that into consideration. The recurrence relation ends up being A(n) = A(n-1) + 2A(n-3) with seeds 2, 4, 6. From there, we can look at the number of days we actually have, and partition the teams accordingly to get the answer to the question.

UPDATE:
After this initial work, I realized that there is an easier version of the question to understand that has the same answer: What is the theoretical maximum number of season-opening games played in a team's home arena?  All the math is identical, but we instead think of "losing" as "our season opener was played as an away game."
