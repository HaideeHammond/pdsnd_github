import time
import pandas as pd
import numpy as np

CITY_DATA = ['chicago', 'new york city', 'washington']

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']

DAYS_OF_THE_WEEK = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or 'all' to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    city = ''
    month = ''
    day = ''
    print('Hello! Let\'s explore some US bikeshare data!')

    while city not in CITY_DATA:
        city = input('What city\'s data are you interested in, Chicago, Washington or New York City? ')
        city = city.lower()

    time_filter = input('Do you want to filter by day or month? ')
    if time_filter == 'day' or time_filter == 'Day':
        while day not in DAYS_OF_THE_WEEK:
            day = input('What day of the week are you interested in? : ')
            day = day.lower()
            month = 'all'
    elif time_filter == 'month' or time_filter == 'Month':
        while month not in MONTHS:
            month = input('What month are you interested in? : ')
            month = month.lower()
            day = 'all'
    else:
        raise Exception("option not allowed, sorry")

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
    city = city.lower()
    if city not in CITY_DATA:
        raise Exception("Only available cities are Chicago, Washington and New York City. The value of the city was: {}".format(city))
    if city == 'new york city':
        city = 'new_york_city'
    filename = "{}.csv".format(city)
    df = pd.read_csv(filename)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month using int instead of strings unless 0
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = MONTHS.index(month) + 1
        df = df[df['month'] == month]

    # filter by day of week using their strings unless "all"
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    return df

def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # There is no point to show mode of a value we have folter for:
    if month == 'all':
        popular_month = df['month'].mode()[0]
        print('Most Popular Month:', popular_month)
        popular_day = df['day_of_week'].mode()[0]
        print('Most Popular Day: ', popular_day)

    if day == 'all':
        df['hour'] = df['Start Time'].dt.hour
        popular_hour = df['hour'].mode()[0]
        print('Most Popular Start Hour: ', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    popular_start_station = df['Start Station'].mode()[0]
    print('Most Popular Start Station: ', popular_start_station)

    popular_end_station = df['End Station'].mode()[0]
    print('Most Popular End Station: ', popular_end_station)

    df['Trip'] = df['Start Station'] + ' to ' + df['End Station']
    popular_trip = df['Trip'].mode()[0]
    print('Most Popular Trip: ', popular_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_trip_time = df['Trip Duration'].sum(axis = 0)
    print('Total travel time: ', total_trip_time)

    mean_trip_time = df['Trip Duration'].mean()
    print('Mean travel time: ', mean_trip_time)

    print("\nThis took %s seconds." % (time.time() - mean_trip_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_count = df['User Type'].value_counts()
    print('This is our customer type distribution: ', user_count)

    #if df['Gender'] is not None:
    if 'Gender' in df.columns:
        gender_count = df['Gender'].value_counts()
        print('This is the gender distribution: ', gender_count)

    if 'Birth Year' in df.columns:
        min_birth = df['Birth Year'].min()
        max_birth = df['Birth Year'].max()
        common_birth = df['Birth Year'].mode()[0]
        print('Our youngest user was born in: ', max_birth)
        print('Our oldest user was born in: ', min_birth)
        print('The most common year of birth is: ', common_birth)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    user_response = input('Do you want to see some raw data? (enter "yes" or "no")')
    count = 0
    while True:
        if user_response == 'yes':
            print(df.iloc[count:count + 5])
            count += 5
            user_response = input('Do you want to see some raw data? (enter "yes" or "no")')
        elif user_response == 'no':
            break
        else:
            print('I didn\'t get that response, please try again.\n')

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
