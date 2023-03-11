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
    city= None
    month= None
    day= None
    while str(city).lower() not in CITY_DATA:
        city=str(input('Which city are you interested in?: ')).title()
        if str(city).lower() not in CITY_DATA:
            print('That\'s not a valid entry! Please enter: New York City, Washington, or Chicago.')
    print(city, 'found! Loading data..')
    while str(month).lower() not in ('all', 'january', 'february', 'march', 'april', 'may', 'june'):
        month=str(input('Please specify month or enter \'all\' to leave month unspecified:')).title()
        if str(month).lower() not in ('all', 'january', 'february', 'march', 'april', 'may', 'june'):
            print('That\'s not a valid entry! Please enter "all" or any month from January to June!')
    print('Loading {} data in {}...'.format(month, city))
    while str(day).lower() not in ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
        day=str(input('Which day of the week? Enter \'all\' to unspecify:')).title()
        if str(day).lower() not in ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
            print('That\'s not a valid entry! Please enter "all" or any day of the week!')
    print('Loading data for {} day(s) of week in {} month(s) in the city of \n {}...'.format(day, month, city))
    print('-'*40)
    city=city.lower()
    month=month.title()
    day=day.title()

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
        
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month_name()
    df['Day'] = df['Start Time'].dt.day_name()  

    if day != 'All':    
        df = df[df['Day'] == day]          

    if month != 'All':
        df = df[df['Month'] == month]

    df = df.dropna()
   
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    common_month = df['Month'].mode()
    print('Most common travel month: ',common_month[0])
    common_dayofweek = df['Day'].mode()
    print('Most common travel day of week: ',common_dayofweek[0])
    df['Hour'] = df['Start Time'].dt.hour    # TO DO: display the most common day of week
    common_hour = df['Hour'].mode()
    print('Most common hour of travel: ',common_hour[0])
    # TO DO: display the most common start hour
    print("\nThis took %s seconds." % round((time.time() - start_time),3))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    common_startstation = df['Start Station'].mode()
    print('Most common Start Station: ',common_startstation[0])# TO DO: display most commonly used start station
    common_endstation = df['End Station'].mode()
    print('Most common End Station: ',common_endstation[0])
    
    df['Start Stop'] = df['Start Station'] + ' & \n' + df['End Station']
    common_startstop = df['Start Stop'].mode()
    print('Most common Station Combo: ',common_startstop[0])
    # TO DO: display most commonly used end station
    # TO DO: display most frequent combination of start station and end station trip
    print("\nThis took %s seconds." % round((time.time() - start_time),3))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_time = int(df['Trip Duration'].sum())
    print('Total travel time in seconds: ',total_time)# TO DO: display total travel time
    mean_time = int(df['Trip Duration'].mean())
    print('Mean travel time in seconds: ',mean_time)
    # TO DO: display mean travel time
    print("\nThis took %s seconds." % round((time.time() - start_time),3))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    user_counts = df['User Type'].value_counts()
    print('User Type Counts: ',user_counts)
    try:
        gender_counts = df['Gender'].value_counts()
        print('Gender Counts: ',gender_counts)
        min_birth = int(df['Birth Year'].min())
        print('Earliest Birth Year: ',min_birth)
        max_birth = int(df['Birth Year'].max())
        print('Most Recent Birth Year: ',max_birth)
        common_birth = df['Birth Year'].mode()
        print('Most Common Birth Year: ',int(common_birth[0]))
    except:
        print('No gender or birth year data available.')
    print("\nThis took %s seconds." % round((time.time() - start_time),3))
    print('-'*40)
    
def raw_data(df):
    x = 0
    display = str(input('Would you like to display raw data?')).lower()
    pd.set_option('display.max_columns',200)
    
    while display.lower() == 'yes':
            print(df.loc[x:x+4])
            display = str(input('Would you like to view more rows?')).lower()
            x += 5
            if display.lower() == 'no':
                break
            elif display != 'yes' and display != 'no':
                display = str(input('Invalid entry. Would you like to display raw data? (Yes or no)'))
        

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        while restart.lower() != 'yes' and restart.lower() != 'no':
            print ('Invalid Entry. Please try again!')
            restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() == 'no':
            break
    
if __name__ == "__main__":
	main()
    