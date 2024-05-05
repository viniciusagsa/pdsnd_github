import time
import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None)  

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv',
              'all': 'all' }

FILTER = ['month', 'day', 'all']

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'all']

DAYS = {6: 'Sunday',
        0: 'Monday',
        1: 'Tuesday',
        2: 'Wednesday',
        3: 'Thursday',
        4: 'Friday',
        5: 'Saturday'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')

    # get user input for city (chicago, new york city, washington)
    while True:
        city = input('Would you like to see data for Chicago, New York, Washington or all at once? \nType "All" to visualize data from the three cities.\n').lower().strip()
        if city in CITY_DATA:
                break
        else:
            print('\nThere was a misspell! Check if your answer is any of "Chicago", "New York", "Washington" or "All".\n')

    if city == 'all':
        print(f'Sure! Let\'s see the data from the three cities.\n')
    else:
        print(f'Sure! Let\'s filter by {city.title()}\n')


    # get use input to filter by selected timeframe
    while True:
        filter_type = input('Would you like to filter data by month, day or none at all? \nType "all" for no time filter.\n').strip().lower()
        if filter_type in FILTER:
            break
        else:
            print('Hummmm.... Coundn\'t understand that. Please check if our answer is any of "Month", "Day" or "None".')


    if filter_type == 'month':
        # get user input for month (all, january, february, ... , june)
        while True:
            month = input('Which month? January, February, March, April, May, June or all?.\n').lower().strip()
            if month in MONTHS:
                day = None
                break
            else:
                print('I think there was a misspell or the month is out of range.\nPlease type "January", "February", "March", "April", "May", "June" or "All".\n')

        print(f'Ok! Les\'s filter by {month.title()}!\n')

    elif filter_type == 'day':
        # get user input for day of week (all, monday, tuesday, ... sunday)
        while True:
            day = input('Which day of the week? Please type your answer as an integer (e.g., 0 = Monday, 1 = Tuesday...) or "all".\n').strip().lower()
            if day in ['0','1','2','3','4','5','6', "all"]:
                month = None
                break
            else:
                print('Please check for a typpo or if your answer is out of range (ans <= 6) or is "All".\n')
        if day != 'all':
            print(f'Ok!! Let\'s filter by {DAYS[int(day)]}')
    else:
        month, day = None, None
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or None to apply no month filter
        (str) day - name of the day of week to filter by, or None to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    if city == 'all':
        df1 = pd.read_csv(CITY_DATA['chicago'])

        df2 = pd.read_csv(CITY_DATA['new york'])

        df3 = pd.read_csv(CITY_DATA['washington'])

        df = pd.concat([df1, df2, df3])
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        df['End Time'] = pd.to_datetime(df['End Time'])

    else:
        df = pd.read_csv(CITY_DATA[city])
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        df['End Time'] = pd.to_datetime(df['End Time'])

    if month:
        if month != 'all':
            df = df[df['Start Time'].dt.month_name() == month.title()]

    if day:
        if day != 'all':
            df = df[df['Start Time'].dt.weekday == int(day)]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    mode_month = df['Start Time'].dt.month_name().mode()[0]
    count_month = df['Start Time'].dt.month_name().value_counts()[0]
    print(f'Most Common Month: {mode_month}.\nCounts: {count_month}')

    # display the most common day of week
    mode_day_of_week = df['Start Time'].dt.day_name().mode()[0]
    count_day_of_week = df['Start Time'].dt.day_name().value_counts()[0]
    print(f'Most Common day of week: {mode_day_of_week}.\nCounts: {count_day_of_week}')
    
    # display the most common start hour
    mode_start_hour = df['Start Time'].dt.hour.mode()[0]
    count_start_hour = df['Start Time'].dt.hour.value_counts()[mode_start_hour]
    print(f'Most Common start hour: {mode_start_hour}.\nCounts: {count_start_hour}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    mode_start_station = df['Start Station'].mode()[0]
    count_start_station = df['Start Station'].value_counts()[0]
    print(f'Most Common start station: {mode_start_station}.\nCounts: {count_start_station}')

    # display most commonly used end station
    mode_end_station = df['End Station'].mode()[0]
    count_end_station = df['End Station'].value_counts()[0]
    print(f'Most Common End station: {mode_end_station}.\nCounts: {count_end_station}')

    # display most frequent combination of start station and end station trip
    mode_station_comb = df[['Start Station','End Station']].mode()
    count_station_comb = df[['Start Station','End Station']].value_counts()[0]
    print(f'Most Common combination of start station and end Station: \n{mode_station_comb["Start Station"][0]} --> {mode_station_comb["End Station"][0]}.\nCounts: {count_station_comb}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_trip_duration = df['Trip Duration'].sum()
    print(f'Total Duration: {total_trip_duration} seconds or...\n\t\t{total_trip_duration / 60:.2f} minutes or...\n\t\t{total_trip_duration / 3600:.2f} hours.\n')

    # display mean travel time
    mean_trip_duration = df['Trip Duration'].mean()
    print(f'Mean Duration: {mean_trip_duration} seconds or...\n\t\t{mean_trip_duration / 60:.2f} minutes.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Counts of user types:')
    print(df['User Type'].value_counts().to_string())

    # Display counts of gender
    if 'Gender' in df.columns:
        print('\nCounts of user gender:')
        print(df['Gender'].value_counts().to_string())
    else:
        print('\nThere is no Gender classification data.')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_year = df['Birth Year'].min()
        recent_year = df['Birth Year'].max()
        common_year = df['Birth Year'].mode()[0]
    
        print(f"""
Earliest Birth Year: {earliest_year}
Most Recent Birth Year: {recent_year}
Most Common Birth Year: {common_year}
""")
    else:
        print('\nThere is no Birth Year data.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """"Display 5 rows of data as many times the user wants."""

    show_rows = input('\nDo you want to see 5 rows of data? Enter yes or no.\n').lower().strip()
    if show_rows == 'yes':
        start_loc = 0
        next_rows = 'yes'
        while next_rows == 'yes':
            print(df.iloc[start_loc:start_loc + 5])
            start_loc +=5
            next_rows = input('\nDo you want to see the next 5 rows of data?\n').lower().strip()

    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
