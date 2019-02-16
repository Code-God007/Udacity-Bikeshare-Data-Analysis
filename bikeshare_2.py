import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city_input=''
    while city_input.lower() not in CITY_DATA:
        city_input = input("Would you like to see data for Chicago, New York, or Washington?\n")
        if city_input.lower()=='chicago':
            city = 'chicago'
            break
        elif city_input.lower()=='new york':
            city = 'new york city'
            break
        elif city_input.lower()=='washington':
            city = 'washington'
            break
        else:
            print("Please enter a valid city from one of the following : Chicago, New York, or Washington.")
    # get user input for month (all, january, february, ... , june)
    month=''
    months = ['january', 'february','march','april','may','june']
    while month.lower() not in months:
        month = input("\nEnter a month from the following : January, February, March, April, May, or June\n").lower()
        if month.lower() not in months:
            print("\nPlease enter a valid month between January to June\n")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day=''
    days = {'all':0,'monday':1, 'tuesday':2, 'wednesday':3, 'thursday':4, 'friday':5, 'saturday':6, 'sunday':7}
    while day.lower() not in days.keys():
        day = input('\nEnter a day from the following : Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday\n').lower()
        if day.lower() not in days.keys():
            print("\nPlease enter a valid day  as an integer from Monday-0 to Sunday-7\n")

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    return df
def pop_month(df):
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    index = int(df['Start Time'].dt.month.mode())
    most_pop_month = months[index-1]
    return most_pop_month

def pop_day(df):
    days = ['Sunday','Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    index = int(df['Start Time'].dt.dayofweek.mode())
    most_pop_day = days[index]
    return most_pop_day

def pop_hour(df):
    most_pop_hr = int(df['Start Time'].dt.hour.mode())
    if most_pop_hr == 0:
        am_pm = 'am'
        pop_hr_readable  = 12
    elif 1 <= most_pop_hr < 13:
        am_pm = 'am'
        pop_hr_readable = most_pop_hr
    elif 13 <= most_pop_hr <24:
        am_pm = 'pm'
        pop_hr_readable = most_pop_hr - 12
    return [pop_hr_readable,am_pm]
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common
    most_common_month = pop_month(df)
    print("Most Common Month : {}".format(most_common_month))
    # display the most common day of week
    most_common_day = pop_day(df)
    print("Most Common Day : {}".format(most_common_day))
    # display the most common start hour
    most_common_hr = pop_hour(df)
    print("Most Common Hour : {}{}".format(most_common_hr[0],most_common_hr[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].value_counts().index[0]
    print("The most common Start Station is : {}".format(common_start_station))
    # display most commonly used end station
    common_end_station = df['End Station'].value_counts().index[0]
    print("The most common End Station is : {}".format(common_end_station))
    # display most frequent combination of start station and end station trip
    most_common_pair = df.groupby(['Start Station','End Station']).max().index[0]
    print("The most common combination of start station and end station is : {}".format(most_common_pair))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def convert_time(sec):
    day = sec // (24*3600)
    sec %= (24*3600)
    hour =sec //3600
    sec %=3600
    minutes = sec //60
    sec %=60
    return ([day,hour,minutes,sec])


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    res = convert_time(total_travel_time)
    print("The total travel time is : {} days {} hours {} minutes {} seconds".format(res[0],res[1],res[2],res[3]))
    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    res1 = convert_time(mean_travel_time)
    print("The mean travel time is : {} days {} hours {} minutes {} seconds".format(res1[0],res1[1],res1[2],res[3]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    try:
        print('\nCalculating User Stats...\n')
        start_time = time.time()

        # Display counts of user types
        user_type = df.groupby("User Type").size()
        print("Total count of each User Type is : {}".format(user_type))

        # Display counts of gender
        gender_count = df.groupby("Gender").size()
        print("Total gender count is : {}".format(gender_count))

        # Display earliest, most recent, and most common year of birth
        earliest_year = df['Birth Year'].sort_values(ascending = False).dropna().iloc[-1]
        most_recent_birthyear = df['Birth Year'].sort_values(ascending = False).iloc[0]
        most_common_year_of_birth = df['Birth Year'].value_counts().index[0]


        print("The earliest Birth Year : {}".format(int(earliest_year)))
        print("The most recent Birth Year : {}".format(int(most_recent_birthyear)))
        print("The most common year of Birth is : {}".format(int(most_common_year_of_birth)))

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
    except:
        print("Details of the Users are not availiable for this city.\n")

def raw_data(df):
    count = 0
    while True:
        print(df[count : count+5])
        response = input("Do you want to see more?Yes or no.\n").lower()
        if response != 'yes':
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        answer = input('\nDo you want to see raw_data ?Yes or No.\n')
        if answer == 'yes':
            raw_data(df)


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
