# Read Reddit (and Hacker News)

I check Reddit more often than it updates, therefore I end
up seeing the same titles over and over again (yeah, it's
a really bad addiction). When 90% of these links are noise,
my day is ruined.

I'm taking steps towards mitigating the negative
effects of reading Reddit:

 * I need to setup a stream, such that I see only each post
   once.
 * I'm not against the South-Asian-African-Arabian
   livelihood or lifestyle, but I really do not give a shit
   about the ad-funded web turdlettes these guys shovel into
   every subreddit at constant rate. Asian web turdlettes are
   a bit too stale and brown for my taste even if I was
   otherwise interested about reddit & new posts. 

## What's wrong with programming subreddits as-it?

 * Elm, Go, Haskell, Kotlin, Rust, Swift, Typescript, fanposts.
 * Java "this thing isn't crap" or "who cares about verbosity?" fanposts.
 * Self-promotion spam (lol).
 * Dynamic vs. static anything debates. (protip: Anti-dynamic sucks)
 * Tabs vs. spaces debates. (protip: Tabs suck)
 * People posting their stuff to wrong subreddit.

## Why read reddit at all?

Sometimes there are golden nuggets in between that I cannot
really afford to miss. There are the funny things like the
TempleOS and the cool things such as the demofox.org
blogposts. 

I also read hacker news, but it's going to require much
stronger filtering. They have the problem of self-importance,
negativity and alarmed tone in the posts. I think over the
short while a simple domain filtering will help on that, but
I need to come up with something better eventually.

## What does this script do?

This thing fetches stuff from Reddit and Hacker News
bundles at a time. After printing them it puts a bookmark
that tells where to continue from the next time.

While fetching the posts, it's doing some filtering to check
the quality of the posts. For now it's only checking against
blacklisted domains.

To add some filtering, this thing dumps the post titles into
`uncategorized.list`. From there you can dump them into `spam.list`
`worthless.list`, `interesting.list`, `important.list`.

The files are fed to a naive bayes classifier, and it will color
the titles depending on the classification result.

When I will no longer get false positives, I will hide the spam titles
entirely.

Note: There's a feature that lets you create your own
categories now. On 'categories' you need at least 4
categories. This is due to how the lists are treated for
now, and it may be relaxed later.

Note: From now on, the stuff on the spam.list is immediately
ignored and written into "spam_candinates.list". From there you
can read them and move the appropriate ones into actual spam.
