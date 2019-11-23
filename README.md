# mpd-wilson
Stickers for mpd based on Wilson score confidence interval.

The script sets three types of stickers: *likes*, *dislikes* and *Wilson rating*.

Wilson rating means "lower bound of Wilson score confidence interval for a Bernoulli parameter" and is a better way of computing a rating score than "likes - dislikes" or "likes / (likes + dislikes)". Explanation and justification can be found here: https://www.evanmiller.org/how-not-to-sort-by-average-rating.html

# Usage
`python rate.py [-h] [-l | -ul | -d | -ud] [-v]
`

* `-h`: automatically generated help message for usage.
* `-l`, `-ul`, `-d`, `-ud` are *like*, *unlike*, *dislike* and *undislike* respectively. 
* `-v`: verbose mode. Prints the sticker values before and after the update.

# TODO

* Add ability to create a playlist with top rated songs.
* Add ability to check rating without changing it.
* Add option to set up notifications on rating check (for shortcuts).
* Move TODO list to issues.