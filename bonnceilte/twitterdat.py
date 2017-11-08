import pandas as pd
from os import path
from TwitterSearch import TwitterSearch, TwitterSearchOrder, TwitterSearchException


def get_creds(configfile="twitterconfig.txt"):
    """
    This function loads the API credentials from a given textfile
    in the dat directory.
    """
    dat_dir = path.dirname(path.dirname(path.abspath(__file__)))
    dat_dir += "/dat/"

    with open(dat_dir + configfile) as conf:
        creds = conf.readlines()
        creds = [c.strip() for c in creds]

    return creds


def get_tweets(kwlists, outfile):
    """
    This function takes a list of keyword lists and makes twitter searches
    for the set of keywords in each list. It returns the date and id of each
    tweet matching the search and saves it in a csv file or appends it to a
    csv file after searching for duplicates.
    """

    # set up a pandas dataframe for the twitter data,
    # include columns for each of the keywords searched
    kws = [kw for kwl in kwlists for kw in kwl]
    dfcols = ["id", "date"] + kws
    twitdf = pd.DataFrame(columns=dfcols)

    try:

        # set up the search with my API credentials
        creds = get_creds()
        ts = TwitterSearch(
                consumer_key = creds[0],
                consumer_secret = creds[1],
                access_token = creds[2],
                access_token_secret = creds[3]
             )


        # search through the twitter search terms
        for kwl in kwlists:

            tso = TwitterSearchOrder()
            tso.set_keywords(kwl)
            tso.set_include_entities(False)

            rowlist = []
            for i, tweet in enumerate(ts.search_tweets(tso)["content"]["statuses"]):

                # add a row to the dataframe for each tweet found
                tweetdate = pd.to_datetime(tweet["created_at"],
                                           infer_datetime_format=True)
                dfrow = {"id": tweet["id"],
                         "date": tweetdate}
                dfrow.update({k:1 for k in kwl})

                rowlist.append(dfrow)

            newdf = pd.DataFrame(rowlist)
            twitdf = pd.concat([twitdf, newdf])

    except TwitterSearchException as e: # take care of all those ugly errors if there are some
        print(e)

    # now merge the dataframe to any existing twitter date if outfile exists,
    # taking care not to have any double tweets

    # first make the output file point to the twitter data directory
    dat_dir = path.dirname(path.dirname(path.abspath(__file__)))
    dat_dir += "/dat/twitter/"
    outfile = dat_dir + outfile

    if path.isfile(outfile):
        oldf = pd.read_csv(outfile)
        newdf = pd.merge(oldf, twitdf, how='outer')
    else:
        twitdf.to_csv(outfile)


if __name__ == "__main__":

    kwlists = [["bitcoin"], ["BTC"]]
    get_tweets(kwlists, "bitcoin_btc.dat")
