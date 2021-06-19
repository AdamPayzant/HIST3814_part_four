# Part 4 Log

Edward Adam Payzant, 
SN: 101082175

Following "Going Further" Sequence

## Take 1

**NOTE:** I had a revalation down the line, so everything in take 1 is more of the process, rather than actual results.

### Data Collection

Because I'm picking a not suggested data set, I first had to track down a large enough data set for this project.
After some googling, I found the Ancestry "All Civil War Records" which could be filtered to just include Canadian residents.
Annoyingly, this requires an account to access, so this makes building my webscraper all the more painful.

Providing log-in information per-request didn't work, so I ended up having to create a new session.
This also means that I need to capture the log-in post request to mimic in my own scraper.
This was just a matter of toggling firefox dev tools, enable persistant network monitor, then log in.
The payload just ended up being "username" and "password" as is standard, but my experience with web requests is to expect anything but standard.
Despite how easy sounds, I couldn't get this to work and decided to go in another direction.

I briefly looked into using HTML+JS to try and embed it in another page, preserving browser cookies, but this also seemed to fail.
Annoyingly professionally made websites have some kind of qualm with being embedded in other webpages.
I figured this was a lost cause, but after some more minor tweaking, I gave up and went back to python.

When I first looked into the webscraping, [I found this github repo](https://github.com/mjhea0/ancestry-scraper) but it failed when just cloned.
I did some minor updating (changing links, refactoring a bit, etc) but it seemed to still fail.
That said, selenium was a good call, and so I went down my own, inspired path to implement it myself.
It's worth noting selenium won't work in a notebook, so everything from here will be restricted to python scripts.
First things first, it looks like ancestry has moved the sign in to an iframe, so I need to set the driver's frame to that instead.
Once I made that change, I can now log in (wooooooo).
Of course everything couldn't be just smooth sailing, and I couldn't get selenium to recognize HTML.
Rather than fighting it, I decided to just throw in beautiful soup.
After some minor tweaking and edge case "handling" for bs4, I can now finally pull all the data.

Now lets actually store it.
This is pretty straightforward, just shove the data in a dataframe, and run `to_csv()`.
I also decided to scrape Canadian Born volunteers as well, but that was just a copy and paste then changing a couple of values.

Alright, everything's finally ready to run, and of course there are new problems.
It looks like Ancestry will only let you view up to page 100, with every page after telling to refine the search.
Even manually, it won't work.
This is a pretty severe roadblock, and there's not an easy way to get around it.
I may be able to collect more data if I play with the filters, but I've spent too long on this webscraper and if I spend any more time all I'll have to show is the data set.4

Loading the data into a spreedsheet program, it looks like the residence and birth data got mixed somehow.
Turns out I forgot to change function names when I copied the loop.

For the time being, onto data cleaning!

### Data Cleaning

Alright, so once again looking at the data as a spreedsheet, I notice another problem.
The residence data generally doesn't have a town associated, only "Canada" and maybe their province associated.
That's okay, it's why I also collected the birth data.
It's not as accurate as I'd want, as it includes Canadians who immigrated to the US for unrelated reasons, but it includes Candians who never moved back (as most of the records are pension records made several years after the war).

So, first things first lets get some basic regex cleaning.
First lets remove that first column my script will accidently write.
This is pretty easily done with `^(\d+)?,` and just replace with nothing.
Next, let's remove the "abt"'s and birth years from the place of birth.
These two don't really have any regex, but the search commands were `,abt` and `,"abt`.
Turns out there were no names containing "abt" so that's nice at least.
Now let's remove the birth dates.
So, I started with this command ([found on stack overflow](https://stackoverflow.com/questions/2655476/regex-to-match-month-name-followed-by-year)):
```,(\b\d{1,2}\D{0,3})?\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|(Nov|Dec)(?:ember)?)\D?(\d{1,2}\D?)?\D?((19[7-9]\d|20\d{2})|\d{2})```.
Then I added a comma to the start, replaced with it just a comma.
Then I repeated, adding a quatiation mark after the comma.
And that's the regex done.

Now that I'm done with the regex, lets deal with the typos and inconsistencies.
I'll just load this up in Open Refine.
For once something finally went my way.
I was able to do some cluster and clean up all the typos and formatting errors.

In the data, we have a lot of people with their place of birth listed as just "Canada".
Right now, we want to be looking at the province and city of birth, so lets make a copy of the data and remove any line that matches `.*,Canada`.
There we go, now we have a list of people with at least a listed province.

With that all the data cleaning is done, I have just 527 entries compared to the Ancestry query of 81,732.
This is when I realized I'm a fool and could just list the provinces as the place of birth, rather than all of Canada.
Onto take 2 of this process.

## Take 2

### Data Collection

So this is pretty much the same, but now I'm just pulling the place of birth per province.
It just took some light modification and it was ready to go.
Taking significantly longer to scrape, the data was finally ready to go.

### Data Cleaning

Repeating the cleaning steps from last time I:
    * remove the index column
    * remove the `,abt` and `,"abt`
    * Remove the dates
With that repeat regex done I noticed a new issue.
Because I didn't specify the Provinces as Canadian, towns like "Brunswick, Georgia" slipped in.
I took the lazy approach here and just addressed it with removing any matches for `&.*<State>.*"?\n`.
I got too ambitious and this would take far more time than I have to give to fix all this, so I patched out the obvious ones but this data set could definitely use a second pass.

With the data prepped, let's run it through open refine.
I clustered all the data, cleaned it up, and downloaded it again.
Afterwards I gave it another pass through with some regex matching to remove the irrelevant entries I missed in the first pass.

Now all the data is vaguely ready to start presentation.

### Presentation


