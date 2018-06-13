import time
from datetime import datetime
import calendar
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'resources/chicago.csv',
              'new york city': 'resources/new_york_city.csv',
              'washington': 'resources/washington.csv' }

filter_type = ''
month = ''
day = ''

"""
Returns:
    (str) city - name of the city to analyze
    (str) month - name of the month to filter by, or "all" to apply no month filter
    (str) day - name of the day of week to filter by, or "all" to apply no day filter
"""
def get_filters():

    print('Hello! Let\'s explore some US bikeshare data!')
    valid_cities = ['chicago', 'new york city', 'washington']
    valid_filters = ['month', 'day', 'both', 'none']
    valid_months = ['january', 'february', 'march', 'april', 'may', 'june']
    valid_days = ['1', '2', '3', '4', '5', '6', '0']

    global filter_type
    global month
    global day

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('\nWould you like to see data for Chicago, New York City, or Washington?\n').lower()
    while city not in valid_cities:
        print('\nHmmmm we don\'t seem to have data for the city that you\'re looking for. Please try again')
        city = input('\nWould you like to see data for Chicago, New York, or Washington?\n').lower()

    # ask the user how they would like to filter the data
    filter_type = input('\nWould you like to filter the data by month, day, both, or not at all? Type "none" for no time filter.\n').lower()
    while filter_type not in valid_filters:
        print('\nSorry, I don\'t understand that filter type. Please try again')
        filter_type = input('\nWould you like to filter the data by month, day, both or not at all? Type "none" for no time filter.\n').lower()

    if filter_type == 'month' or filter_type == 'both':
        # get user input for month (all, january, february, ... , june)
        month = input('\nWhich month would you like to filter on? January, February, March, April, May, or June\n').lower()
        while month not in valid_months:
            print('\nHmmmm we don\'t seem to have data for the month that you\'re looking for. Please try again')
            month = input('\nWhich month would you like to filter on? January, February, March, April, May, or June\n').lower()


    if filter_type == 'day' or filter_type == 'both':
        # get user input for day of week (all, monday, tuesday, ... sunday)
        day = input('\nWhich day of the week would you like to filter on? Please type your response as an integer (e.g., 0=Monday).\n').lower()
        while day not in valid_days:
            print('\nHmmmm we don\'t seem to have data for the day that you\'re looking for. Please try again')
            day = input('\nWhich day of the week would you like to filter on? Please type your response as an integer (e.g., 0=Monday).\n').lower()


    print('-'*40)
    return city, month, day

"""
Loads data for the specified city and filters by month and day if applicable.

Args:
    (str) city - name of the city to analyze
    (str) month - name of the month to filter by, or "all" to apply no month filter
    (str) day - name of the day of week to filter by, or "all" to apply no day filter
Returns:
    df - Pandas DataFrame containing city data filtered by month and day
"""
def load_data(city, month, day):

    #read the file
    df = pd.read_csv(CITY_DATA[city])

    #filter the data
    # convert the Start Time and End Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])       #this will actually be used later

    if filter_type == 'month' or filter_type == 'both':
        df = df.loc[(df['Start Time'].dt.month == datetime.strptime(month, '%B').month)]

    if filter_type == 'day' or filter_type == 'both':
        df = df.loc[(df['Start Time'].dt.dayofweek == int(day))]

    return df

"""Displays statistics on the most frequent times of travel."""
def time_stats(df):

    print('the filter type is ' + filter_type)
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if filter_type == 'month' or filter_type == 'both':
        print('Most common month: ' + month.title() + '(Obviously)\n')
    else:
        df['month'] = df['Start Time'].dt.month
        print('The most common month is: ', calendar.month_name[df['month'].mode()[0]].title())

    # display the most common day of week
    if filter_type == 'day' or filter_type == 'both':
        print('Most common day: ' + calendar.day_name[int(day)].title() + '(Obviously)\n')
    else:
        df['day'] = df['Start Time'].dt.dayofweek
        print('The most common day is: ', calendar.day_name[df['day'].mode()[0]].title())

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print('The most popular Start hour: ', df['hour'].mode()[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

"""Displays statistics on the most popular stations and trip."""
def station_stats(df):

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most commonly used start station: ', df['Start Station'].mode()[0].title())

    # display most commonly used end station
    print('The most commonly used end station: ', df['End Station'].mode()[0].title())

    # display most frequent combination of start station and end station trip
    df["Trip"] = df["Start Station"] + ' - ' + df["End Station"]
    print('The most frequent combination of start station and end station trip: ', df['Trip'].mode()[0].title())


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df["Trip Time"] = df["End Time"] - df["Start Time"]
    total_time = df["Trip Time"].sum()
    print('The total travel time: ', total_time)

    # display mean travel time
    print('The average travel time: ', df['Trip Time'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('User type counts:\n', user_types)

    # Display counts of gender
    try:
        user_gender = df['Gender'].value_counts()
        print('\nUser gender counts:\n', user_gender)
    except KeyError as e:
        #logging e for debugging
        print('\nUser gender data is not available\n')

    # Display earliest, most recent, and most common year of birth
    try:
        print('\nEarliest birth year:', df['Birth Year'].min())
        print('\nMost recent birth year:', df['Birth Year'].max())
        print('\nMost common birth year:', df['Birth Year'].mode()[0])
    except KeyError as e:
        print('\nUser birth year data is not available\n')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def individual_trip_stats(df):
    """Displays statistics on bikeshare individual trips."""

    response = input('\nWould you like to raw, individual trip data? Type \'yes\' or \'no\'.\n')
    if response.lower() == 'yes':
        
        # Print 5 lines of raw data
        for index, row in df.iterrows():
            print(row, '\n\n')

            if index % 5 == 0 and index != 0:

                print_more = input('\nWould you like to see more rows.\n')
                
                if print_more.lower() != 'yes':
                    break
                print('-'*40)

def printBannerMessage():
    with open('resources/ascii_art.txt', 'r') as f:
        for line in f:
            print(line.rstrip())

def main():

    printBannerMessage()

    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        individual_trip_stats(df)

        restart = input('\nWould you like to restart? Enter yes or any other characters to quit.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
