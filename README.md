This is Kat Gorski's submission for the data science internship code challenge
for the internship program at bit.ly. If you wish to contact me, my email
is kat.gorski@gmail.com and my cell phone number is 201.410.0600. 

These scripts were written for Python 3.4.3 and run on a system running
Ubuntu Linux 15.10, from the command line. 

For these scripts to function, the unzipped decode files must reside in the same
directory as the scripts. 

Due to limitations in processing power on my personal computer, these scripts 
only use the first 500,000 decode events from each of the six decode files. 
Decode time was not a consideration in this analysis, rather, I focus on
providing scripts to explore what sort of audience a link draws, including a
script to check conditional probabilities that a user from a given country
engages with an individual link or with a more general domain, and a very very
simple naive Bayes classifier to classify a user into a country based on my
limited set of data. In addition, there are summary statistics that can be
generated from the decode files indicating which links and domains get the
most traffic through bit.ly decodes. 

Note that all analyses with the newly organized data from these scripts are on
UNIQUE users, not the total number of engagements with a link.  

Unless otherwise noted, all scripts can be run with the command
    python3 SCRIPT_NAME
Assuming the files specified in the descriptions are present in the working
directory with the scripts, along with the decodes_func.py script. If the
scripts are run in the order presented here, there should be no problems with
missing files. 

The package contains the following scripts:

condense_decodes.sh
    A small bash script concatenate the first 500k lines of each decode file in
    the new file decode_cond. It is necessary to create this file in whichever
    method you prefer before moving forward, with however many lines you need.
    A decode_cond of any length will work with these scripts. This script also
    requires that all the decode files are already unzipped. 
    Run as bash condense_decodes.sh or make an executable. 

decodes_func.py
    Defines several functions used in several of the scripts presented in this
    package. Not meant to be run. 

create_user_db.py
    Requires a decode_cond file to be in the working directory. 
    Reorganizes the decode event information into a simplified user database
    from all decode files in a Python dictionary format, with the following
    variables: 
        'uid': bit.ly's user hash identifier.
        'c': the country code associated with the user.
        'nk': the repeat client identifier: 1 if a cookie exists for that user,
        0 otherwise.
        'a': the user browser agent
        'short_url': a list of short URLs the user engaged with, may include
        duplicates if a user clicked on a link more than once.
        'domain': a list of domain names associated with the short_urls visited,
        similarly to the short_url field, this may contain duplicates if a user
        engaged with a link more than once, OR if a user clicked on multiple
        links associated with a domain. 
    This information is written into the file user_db. This file is used
    downstream by calc_prob.py. 

get_top_domains.py
    Requires a decode_cond file to be in the working directory.
    Creates a list of domains with counts and generates summary statistics on the
    average number of times unique users engage with a link. This script takes no
    arguments and simply runs using the decode_cond file in the directory.

    There are three files that result from running this script: domain_counts, 
    short_url_counts, and summary_statistics.txt. The summary_statistics file
    provides some basic information on the average number of decodes, the variance,
    and the standard deviation for both short urls and the general domain. 
    Each line is in the format COUNT: (links, or, domains, here, comma, separated). 

    I was unable to have this script finish on my system even with my smaller
    dataset, but I have tested it with several even smaller sets and it should
    be able to work on something longer. Be aware that this is not the most optimal
    implementation of this script. Making sure that it counts unique visits is the
    bottleneck, as it moves through a hash every time to see if the link was
    already counted for for that particular user. The user count for my smaller
    data set is ~360k, which becomes significant. I also use Python's re module,
    and I am not sure how Python's implementation of regex behaves in terms of speed
    relative to Perl's regular expressions, which I work with on a regular basis.

    Lines 14, 18, and 33 are commented out. If you wish to run the file without
    moving through the whole dataset, uncommenting those lines will provide an
    idea of how this script runs and how the output is formatted. 

change_for_histogram.py
    Takes the resulting file from get_top_domains.py (either domain_counts or
    short_url_counts, it's indicated by the user) and formats them in a way that
    the histogram.py script from the bit.ly github can process it! Use as
        python3 change_for_histogram.py DATA | ./histogram_bitly.py
    The resulting histogram will be written to STDOUT. 

calc_prob.py
    Requires user_db file to be present in the working directory.
    Note: The subset of decode data I used did not have any given user click on
    more than one unique link, ie, each user I have listed only engaged with one
    link total. To simplify things, this script does not check for other possible
    domains. Obviously, if this was a full data set it would be otherwise. 
    If you do use these scripts on some other data set, the script see_mult.py
    will count the number of users who engage with more than one link (listed by
    the bitly hash, not the domain name).

    Run as:
        python3 calc_prob.py domain|link query country
    where domain|link indicates the type of query (the bit.ly link identifier or
    the domain that the link leads to), the query, a bit.ly link identifier or a
    domain name (a partial domain name is fine, ie, guardian.com will pick up
    www.guardian.com and other related URLs), and a two letter country code for
    which you want to see statistics. This will output a few statistics that will
    give you some information about what sort of engagements this link garners. 
    For an example, run as
        python3 calc_prob.py domain guardian.com GB

    If you need a reminder at the command line, you can use
        python3 calc_prob.py help
    to get a reminder of the command the script takes.

bayes_classifier.py
    A very simple, admittedly inefficient naive Bayes classifier to determine the
    country of a given user. In order to run bayesian_classifier.py, the following
    scripts need to be run:
        condense_decodes_test.sh
            Bash script to concantenate some of the decode data into the file
            decode_cond_alt.
            condense_decodes.sh takes the head of the original decode data, this
            takes the tails. It also requires that the unzipped decode files are
            present in the working directory.
        make_test_data.py
            Requires the file decode_cond_alt to run.
            make_test_data.py is very similar to create_user_db.py, but it uses
            the decode_cond_alt data instead. Creates the file user_db_test
            that contains data formatted in the same fashion as user_db,
            described above. 
    The data used to classify are:
        nk: repeat client
        g/short url: the short bit.ly link identifier
        domain: the domain name derived from the u key in the original decode file
        a/platform: the platform used to access the link. This script uses the
        full name of the platform, not whether or not a user is simply using a
        mobile platform. 
    The data will print to STDOUT in the following format:
        Actual country: CC, predicted country: CC
    where CC is the country code. 
    The last line of information written to STDOUT is the percent of records
    correctly indentified. Running the script as presented, I achieved 
    ~79% accuracy.


