import time
import pandas as pd


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTH_DATA = ['all', 'january', 'february', 'march', 'april', 'may', 'june']

DAY_DATA = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


def get_filters(city, month, day):
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('\nName the city you want to explore data from: Chicago, New York City or Washington!>>').lower()
        if city not in CITY_DATA:
            print('\nInvalid input, please try again.\n')
            continue
        else:
            break

    # get user input for month (january, february ,... june or all)
    while True:
        month = input('\nFilter on months? January, February, ... June or all:>>').lower()
        if month not in MONTH_DATA:
            print('\nInvalid input, please try again.\n')
            continue
        else:
            break

    # get user input for day (monday, tuesday, ... sunday or all)
    while True:
        day = input('\nFilter on day? Monday, Tuesday, ... Sunday or all:>>').lower()
        if day not in DAY_DATA:
            print('\nInvalid input, please try again.\n')
            continue
        else:
            break

    print('\nYour selected City: ' ,city.upper())
    print('You filter on Month: ' ,month.upper())
    print('You filter on Day: ' ,day.upper() + '\n\n')
    print('-+-'*40)
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
    # convert Start Time to DateTime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extraxt month from Start Time and create new column month
    df['month'] = df['Start Time'].dt.month
    # extract day name from Start Time and create new column day_of_week
    df['day_of_week'] = df['Start Time'].dt.day_name()
    # extract month name from Start Time and create new column month_of_year
    df['month_of_year'] = df['Start Time'].dt.month_name()


    # if month is not equal to all, use month list and its index to filter data
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) +1
        df = df[df['month'] == month]

    # if day is not equal to all, use day_of_week which represents the day_name to filter data
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month

    common_month_of_year = df['month_of_year'].mode()[0]
    print('Most Frequent Start Month:',common_month_of_year)


    # display the most common day of week
    common_day_of_week = df['day_of_week'].mode()[0]
    print('Most Frequent Start Day:',common_day_of_week)


    # display the most common start hour
    # extract hour from Start Tiem and create new column hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print('Most Frequent Start Hour from 0 to 23:',common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-+-'*40)



def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start = df['Start Station'].mode()[0]
    print('Most commonly used Start Station:', common_start)

    # display most commonly used end station
    common_end = df['End Station'].mode()[0]
    print('Most commonly used End Station:', common_end)

    # display most frequent combination of start station and end station trip
    # creating a new column as combination of start station and end station trip
    df['combination'] = df['Start Station'] + ' to ' + df['End Station']
    common_combination = df['combination'].mode()[0]
    print('Most frequent combination of Start Station and End Station Trip: ',common_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-+-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    # print(total_travel_time) in seconds
    # time calculation for better reading, convertong tons of seconds into e readable format
    total_travel_time = (str(int(total_travel_time//86400)) +
                         'd ' +
                         str(int((total_travel_time % 86400)//3600)) +
                         'h ' +
                         str(int(((total_travel_time % 86400) % 3600)//60)) +
                         'm ' +
                         str(int(((total_travel_time % 86400) % 3600) % 60)) +
                         's')
    print("The total travel time is: " + str(total_travel_time))


    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    mean_travel_time = (str(int(mean_travel_time//60)) + 'min ' +  str(int(mean_travel_time % 60)) + 'sec')
    print("The mean travel time is: " + str(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-+-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("The user types are distributed as follow: \n" + str(user_types))

    # Display counts of gender
    if 'Gender' in df:
        gender = df['Gender'].value_counts()
        # there are non-values in the gender column, which can be found with a boolean exprssion using isna method
        Not_specified = df['Gender'].isna().sum()
        print('\nThe gender of users are distributed as follow: \nNot Specified ' + str(Not_specified) + "\n" + str(gender))

    else:
        # not all DFs have gender information
        print("There is no gender information for this city.")


    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest_birth = str(int(df['Birth Year'].min()))
        most_recent_birth = str(int(df['Birth Year'].max()))
        most_common_birth = str(int(df['Birth Year'].mode()[0]))

        print('\nEarliest year of birth: ' + str(earliest_birth))
        print('Most recent year of birth: ' + str (most_recent_birth))
        print('Most common year of birth: ' + str (most_common_birth))
    else:
        # not all DFs have Year of Birth information
        print('There is no birth year information for this city.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-+-'*40)

def display_raw_data(df):
    """Displays raw data on user request.
    Args:
        (DataFrame) df - Pandas DataFrame containing city data filtered by month and day
    """
    # displays the first 10 rows with start_index = 0 and end_index = 10
    next = 0
    print(df.iloc[next:10])
    # displays next 10 rows, whilst start_index icrement by 10 and end_index = start_index +10. As long as user types yes.
    while True:
        view_raw_data = input('\nEnter yes, if you like to see additional ten rows of raw data.>>')
        if view_raw_data.lower() != 'yes':
            return
        next = next + 10
        print(df.iloc[next:next+10])



def main():
    city = ""
    month = ""
    day = ""
    while True:
        city, month, day = get_filters(city, month, day)
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # asking for the first 10 rows of raw data to invoke display_raw_data-function
        while True:
            view_raw_data = input('\nEnter yes, if you like to see first ten rows of raw data!>>')
            if view_raw_data.lower() != 'yes':
                break
            display_raw_data(df)
            break

        restart = input('\nWould you like to restart? Enter yes or no.>>')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
