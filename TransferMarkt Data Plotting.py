# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 09:54:19 2026

@author: Alex Sachar
"""

# The following script takes data from the accompanying list of HTML files and allows users to produce
# plots of a Premier League club's Expenditures, Income, Arrivals (signings), Departures (sold players), Net Balance (advise against using this metric),
# and points totals. The correct strings for calling a given team are listed as the Values in the local dict in
# the longhand function (line 109).

import numpy as np

import pandas as pd

from matplotlib import pyplot as plt  

# The following allows us to read the saved HTML files.

def save_html(html, path):
    with open(path, 'wb') as f:
        f.write(html)

def open_html(path):
    with open(path, 'rb') as f:
        return f.read()



# HTML files listed below, to be parsed through functions later on

# Transfer data from TransferMarkt.com:

url_list = ['tm92-93.html',
            'tm93-94.html',
            'tm94-95.html',
            'tm95-96.html',
            'tm96-97.html',
            'tm97-98.html',
            'tm98-99.html',
            'tm99-00.html',
            'tm00-01.html',
            'tm01-02.html',
            'tm02-03.html',
            'tm03-04.html',
            'tm04-05.html',
            'tm05-06.html',
            'tm06-07.html',
            'tm07-08.html',
            'tm08-09.html',
            'tm09-10.html',
            'tm10-11.html',
            'tm11-12.html',
            'tm12-13.html',
            'tm13-14.html',
            'tm14-15.html',
            'tm15-16.html',
            'tm16-17.html',
            'tm17-18.html',
            'tm18-19.html',
            'tm19-20.html',
            'tm20-21.html',
            'tm21-22.html',
            'tm22-23.html',
            'tm23-24.html',
            'tm24-25.html',
            'tm25-26.html']

# Premier League end-of-season tables from TransferMarkt.com

prem_url_list =  ['pl92-93.html','pl93-94.html','pl94-95.html',
'pl95-96.html',
'pl96-97.html',
'pl97-98.html',
'pl98-99.html',
'pl99-00.html',
'pl00-01.html',
'pl01-02.html',
'pl02-03.html',
'pl03-04.html',
'pl04-05.html',
'pl05-06.html',
'pl06-07.html',
'pl07-08.html',
'pl08-09.html',
'pl09-10.html',
'pl10-11.html',
'pl11-12.html',
'pl12-13.html',
'pl13-14.html',
'pl14-15.html',
'pl15-16.html',
'pl16-17.html',
'pl17-18.html',
'pl18-19.html',
'pl19-20.html',
'pl20-21.html',
'pl21-22.html',
'pl22-23.html',
'pl23-24.html',
'pl24-25.html',
'pl25-26.html']


# The following function uses a dict to equate the different references to
# teams so the data knows to match the correct team data from each. in url_list the team names often differ from those in prem_url_list
# , for example 'Arsenal' and 'Arsenal FC' are equated.

def longhand(team_name):
    teams = {
        'Man Utd': 'Manchester United',
        'Man City': 'Manchester City',
        'Arsenal': 'Arsenal FC',
        'Chelsea': 'Chelsea FC',
        'Liverpool': 'Liverpool FC',
        'Tottenham': 'Tottenham Hotspur',
        'Newcastle': 'Newcastle United',
        'Brighton': 'Brighton & Hove Albion',
        'Fulham': 'Fulham FC',
        'Bournemouth': 'AFC Bournemouth',
        'Brentford': 'Brentford FC',
        'Everton': 'Everton FC',
        'West Ham': 'West Ham United',
        'Wolves': 'Wolverhampton Wanderers',
        'Nottm Forest': 'Nottingham Forest',
        "Nott'm Forest": 'Nottingham Forest',
        'Leicester': 'Leicester City',
        'Southampton': 'Southampton FC',
        'Ipswich': 'Ipswich Town',
        'Crystal Palace': 'Crystal Palace',
        'Aston Villa': 'Aston Villa',
        'Burnley': 'Burnley FC',
        'Sunderland': 'Sunderland AFC',
        'Leeds': 'Leeds United',
        'Norwich': 'Norwich City',
        'Watford': 'Watford FC',
        'West Brom': 'West Bromwich Albion',
        'Stoke': 'Stoke City FC',
        'Swansea': 'Swansea City',
        'Cardiff': 'Cardiff City FC',
        'Huddersfield': 'Huddersfield Town',
        'Hull': 'Hull City',
        'Middlesbrough': 'Middlesbrough FC',
        'Sheffield Utd': 'Sheffield United',
        'Sheffield Wed': 'Sheffield Wednesday',
        'QPR': 'Queens Park Rangers',
        'Birmingham': 'Birmingham City',
        'Blackburn': 'Blackburn Rovers',
        'Blackpool': 'Blackpool FC',
        'Bolton': 'Bolton Wanderers',
        'Bradford': 'Bradford City AFC',
        'Charlton': 'Charlton Athletic FC',
        'Coventry': 'Coventry City FC',
        'Derby': 'Derby County',
        'Oldham': 'Oldham Athletic',
        'Portsmouth': 'Portsmouth FC',
        'Reading': 'Reading FC',
        'Swindon': 'Swindon Town',
        'Wigan': 'Wigan Athletic',
        'Wimbledon': 'Wimbledon',
        'Barnsley': 'Barnsley FC',
    }
    return teams.get(team_name)

    

from bs4 import BeautifulSoup

# List of seasons over which we are analysing data:

season_list = ['92/93','93/94','94/95','95/96','96/97','97/98','98/99','99/00','00/01','01/02','02/03','03/04','04/05','05/06','06/07','07/08','08/09','09/10','10/11','11/12','12/13','13/14','14/15','15/16','16/17','17/18','18/19','19/20','20/21','21/22','22/23','23/24','24/25','25/26']

# The following function takes a given unweighted, raw metric of a club and plots it by season.

def plot_club(team_of_interest, stat_of_interest, start_season, end_season):
    
    start_index = season_list.index(start_season) # Indicates the starting season from which we plot
    
    end_index = season_list.index(end_season) # Indicates the final season up to which we plot

    club_data = {'Season':season_list[start_index:end_index + 1], 
                            'Expenditure':[], 
                            'Income':[], 
                            'Net Balance':[], 
                            'Arrivals':[], 
                            'Departures':[],
                            'Points':[]}

    league_average_list = []

    # The following for loop goes through each season's transfer data table from TransferMarket.com
    # and extracts the chose metric data for each club. At the same time, it works out the league's average of that metric
    # for each season, and saves this to a list.
    
    for j in range(start_index,end_index+1):
        
        html = open_html(url_list[j])
    
        soup = BeautifulSoup(html, 'html.parser')
    
        rows = soup.select('#yw1 > table tr')
        
        
        html_2 = open_html(prem_url_list[j])
        
        soup_2 = BeautifulSoup(html_2, 'html.parser')
        
        rows_2 = soup_2.select('#yw1 > table > tbody > tr')
 
        
        # the following if statement accounts for the increased number of teams in the PL in the first 3 seasons
    
        if j in [0,1,2]:
            team_count = 22
        else:
            team_count = 20
        
        clubs_list = []
        
        clubs_list_2 =[]
        
        current_running_league_total = 0
        
        for i in range(1, team_count + 1):
            
            row = rows[i]
            
            name = row.select_one('.hauptlink a').text.strip()
            clubs_list.append(name)
            
            expenditure = row.select_one('.rechts.hauptlink.redtext').text.strip()
            
            income = row.select_one('.rechts.hauptlink.greentext').text.strip()
        
            try:
                net_balance = row.select_one('.hauptlink .redtext').text.strip()
            except:
                net_balance = row.select_one('.hauptlink .greentext').text.strip()
         
            arrivals = row.select('.zentriert a')[1].text.strip()
            
            departures = row.select('.zentriert a')[2].text.strip()
            
            # next part goes through points for that season
            
            row_2 = rows_2[i-1]
            
            name_2 = row_2.select_one('.hauptlink a').text.strip()
            
            clubs_list_2.append(longhand(name_2))

            points = int(row_2.select('td')[9].text.strip())
            
            if longhand(name_2) == team_of_interest:
                club_data['Points'].append(points)
            
            
            # the next part cleans and sets the data to the correct data type,
            # as the data is all saved as strings initially. Some of the data entries
            # have a 'm' at the end (for 'millions'), or a Euro symbol at the start.
            # For this reason we truncated the first and last entry of each. Some have
            # 'k' at the end (for 'thousands') hence we divide these entries by 1000 to
            # put them in terms of millions.
            
            
 
            try:
                if expenditure[-1] == 'k':
                    expenditure = float(expenditure[1:-1])/1000
                else:
                    expenditure = float(expenditure[1:-1])
            except:
                expenditure = 0
                
            try:
                if income[-1] == 'k':
                    income = float(income[1:-1])/1000
                else:
                    income = float(income[1:-1])
            except:
                income = 0
            
            try:
                if net_balance[-1] == 'k':
                    net_balance = float(net_balance[1:-1])/1000
                else:
                    net_balance = float(net_balance[1:-1])
            except:
                net_balance = 0
                
            try:
                arrivals = float(arrivals)
            except:
                arrivals = 0
                
            try:
                departures = float(departures)
            except:
                arrivals = 0
            
            # This next if statement saves our chosen club's metrics.
            
            if name == team_of_interest:
                club_data['Expenditure'].append(expenditure)
                club_data['Income'].append(income)
                club_data['Net Balance'].append(net_balance)
                club_data['Arrivals'].append(arrivals)
                club_data['Departures'].append(departures)
                
            
            # next bit is for working out the league average
            
            if stat_of_interest == 'Expenditure':
                #if expenditure != np.nan:
                    current_running_league_total += expenditure
            elif stat_of_interest == 'Income':
                #if income != np.nan:
                    current_running_league_total += income
            elif stat_of_interest == 'Net Balance':
                #if net_balance != np.nan:
                    current_running_league_total += net_balance
            elif stat_of_interest == 'Arrivals':
                #if arrivals != np.nan:
                    current_running_league_total += arrivals
            elif stat_of_interest == 'Departures':
                #if departures != np.nan:
                    current_running_league_total += departures
                
        
        # This next part accounts for when a team is not in the Premier League in a given
        # season, or there is an empty data entry (rare).
        
        if team_of_interest not in clubs_list:
            club_data['Expenditure'].append(0)
            club_data['Income'].append(0)
            club_data['Net Balance'].append(0)
            club_data['Arrivals'].append(0)
            club_data['Departures'].append(0)
            
        if team_of_interest not in clubs_list_2:
            club_data['Points'].append(0)
            
        league_average_list.append(current_running_league_total/team_count)
        
    team_df = pd.DataFrame(club_data)        
    
    
    
    plt.xlabel('Season', fontsize=18)
    plt.ylabel(stat_of_interest, fontsize=16)
    
    plt.xticks(fontsize=7, rotation=45)
    plt.tight_layout()
        
    plt.plot(team_df['Season'], team_df[stat_of_interest], marker='o', color ='grey', label=team_of_interest)
    
    plt.plot(team_df['Season'], league_average_list, color ='red', label= 'Premier League Average')
    
    plt.legend(loc="upper left")
    


# This next function does the exact same as the previous one, except this time gives each metric as a multiple
# of the league average that season. It then plots this against the league average and alongside a graph of
# that team's league finishes over time.

def plot_club_weighted(team_of_interest, stat_of_interest, start_season, end_season, graph_range, vline_season=None, vline_label=None):
    
    start_index = season_list.index(start_season)
    
    end_index = season_list.index(end_season)

    club_data = {'Season':season_list[start_index:end_index + 1], 
                            'Expenditure':[], 
                            'Income':[], 
                            'Net Balance':[], 
                            'Arrivals':[], 
                            'Departures':[],
                            'Final League Position':[]}

    league_average_list = []

    for j in range(start_index,end_index+1):
        
        html = open_html(url_list[j])
    
        soup = BeautifulSoup(html, 'html.parser')
    
        rows = soup.select('#yw1 > table tr')
        
        
        html_2 = open_html(prem_url_list[j])
        
        soup_2 = BeautifulSoup(html_2, 'html.parser')
        
        rows_2 = soup_2.select('#yw1 > table > tbody > tr')
        
        
        if j in [0,1,2]:
            team_count = 22
        else:
            team_count = 20
        
        clubs_list = []
        
        clubs_list_2 =[]
        
        current_running_league_total = 0
        
        for i in range(1, team_count + 1):
            
            row = rows[i]
            
            name = row.select_one('.hauptlink a').text.strip()
            clubs_list.append(name)
            
            expenditure = row.select_one('.rechts.hauptlink.redtext').text.strip()
            
            income = row.select_one('.rechts.hauptlink.greentext').text.strip()
        
            try:
                net_balance = row.select_one('.hauptlink .redtext').text.strip()
            except:
                net_balance = row.select_one('.hauptlink .greentext').text.strip()
         
            arrivals = row.select('.zentriert a')[1].text.strip()
            
            departures = row.select('.zentriert a')[2].text.strip()
            
            
            # next part goes through points for that season
            
            row_2 = rows_2[i-1]
            
            name_2 = row_2.select_one('.hauptlink a').text.strip()
            clubs_list_2.append(longhand(name_2))

            league_position = int(row_2.select('td')[0].text.strip())
            
            if longhand(name_2) == team_of_interest:
                club_data['Final League Position'].append(league_position*(-1))
            
            
            # the next part cleans and sets the data to the correct data type
            
 
            try:
                if expenditure[-1] == 'k':
                    expenditure = float(expenditure[1:-1])/1000
                else:
                    expenditure = float(expenditure[1:-1])
            except:
                expenditure = 0
                
            try:
                if income[-1] == 'k':
                    income = float(income[1:-1])/1000
                else:
                    income = float(income[1:-1])
            except:
                income = 0
            
            try:
                if net_balance[-1] == 'k':
                    net_balance = float(net_balance[1:-1])/1000
                else:
                    net_balance = float(net_balance[1:-1])
            except:
                net_balance = 0
                
            try:
                arrivals = float(arrivals)
            except:
                arrivals = 0
                
            try:
                departures = float(departures)
            except:
                arrivals = 0
            
            if name == team_of_interest:
                club_data['Expenditure'].append(expenditure)
                club_data['Income'].append(income)
                club_data['Net Balance'].append(net_balance)
                club_data['Arrivals'].append(arrivals)
                club_data['Departures'].append(departures)
                
            
            # next bit is for working out the league average
            
            if stat_of_interest == 'Expenditure':
                #if expenditure != np.nan:
                    current_running_league_total += expenditure
            elif stat_of_interest == 'Income':
                #if income != np.nan:
                    current_running_league_total += income
            elif stat_of_interest == 'Net Balance':
                #if net_balance != np.nan:
                    current_running_league_total += net_balance
            elif stat_of_interest == 'Arrivals':
                #if arrivals != np.nan:
                    current_running_league_total += arrivals
            elif stat_of_interest == 'Departures':
                #if departures != np.nan:
                    current_running_league_total += departures
                
            
        if team_of_interest not in clubs_list:
            club_data['Expenditure'].append(np.nan)
            club_data['Income'].append(np.nan)
            club_data['Net Balance'].append(np.nan)
            club_data['Arrivals'].append(np.nan)
            club_data['Departures'].append(np.nan)
            
        if team_of_interest not in clubs_list_2:
            club_data['Final League Position'].append(np.nan)
            
        league_average_list.append(current_running_league_total/team_count)
        
        # We've scraped, cleaned and saved the data for our team_of_interest,
        # now we can just divide it by the average for that webpage (season).
        
        club_data['Expenditure'][-1] = club_data['Expenditure'][-1]/league_average_list[-1]
        club_data['Income'][-1] = club_data['Income'][-1]/league_average_list[-1]
        club_data['Net Balance'][-1] = club_data['Net Balance'][-1]/league_average_list[-1]
        club_data['Arrivals'][-1] = club_data['Arrivals'][-1]/league_average_list[-1]
        club_data['Departures'][-1] = club_data['Departures'][-1]/league_average_list[-1]
        
    team_df = pd.DataFrame(club_data)        
    
    # The following plots this data neatly
    
    fig, (ax1, ax2) = plt.subplots(
    2, 1,
    figsize=(12, 8),
    sharex=True,
    gridspec_kw={'height_ratios': [1, 1]}
    )

    ax1.plot(
        team_df['Season'],
        team_df[stat_of_interest],
        marker='o',
        color='grey',
        label=team_of_interest
    )

    ax1.plot(
        team_df['Season'],
        [1] * len(team_df),
        color='red',
        linestyle='--',
        label='League Average ' + stat_of_interest
    )

    ax1.set_ylabel(stat_of_interest + ' (multiple of league Average)', fontsize=14)
    ax1.set_title(
        f'{team_of_interest}: {stat_of_interest} and League Position',
        fontsize=16
    )
    
    ax1.set_ylim(0, graph_range)
    
    
    ax1.grid(True, alpha=0.3)
    
   
    ax2.plot(
        team_df['Season'],
        team_df['Final League Position'],
        marker='o',
        color='blue',
        label='Final League Position'
    )
    
    ax2.set_ylabel('Final League Position', fontsize=14)
    ax2.set_xlabel('Season', fontsize=16)
    
    
    ax2.set_yticks(range(-20, 0))
    
    
    ax2.set_ylim(-20, 0)
    
    if vline_season is not None:

       if isinstance(vline_season, str):
           vline_season = [vline_season]

       if vline_label is None or isinstance(vline_label, str):
           vline_label = [vline_label] * len(vline_season)

       plotted_seasons = list(team_df['Season'])
       line_colours = ['green', 'purple', 'orange', 'brown', 'black']

       for k, (season, label) in enumerate(zip(vline_season, vline_label)):

           x_position = plotted_seasons.index(season)
           colour = line_colours[k % len(line_colours)]

           ax1.axvline(x=x_position, color=colour, linestyle=':', linewidth=2, label=label)
           ax2.axvline(x=x_position, color=colour, linestyle=':', linewidth=2)

    # Legends are drawn last so they include the vertical line labels.
    ax1.legend()
    ax2.legend()

    
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    
    plt.xticks(fontsize=8, rotation=45, ha='right')
    
    plt.tight_layout()
    plt.show()


