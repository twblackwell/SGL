import requests
import pprint
import json
import sys
import csv
import time


#method to call ballchasing api's GET /replays/{id} ie: EACH game's data
def apiCallByReplayId(replayId):

    url = 'https://ballchasing.com/api/replays/' + replayId
    auth = {'Authorization': 'vA9akDv9RQ4TlOGMREPJpbXmFsvOKxkWRr3SYFXM'}
    r = requests.get(url, headers = auth)
    data = r.json()
    
    return data
#END apiCallByReplayId


#method to call ballchasing api's GET /replays/ returning list of game info
def apiCallReplays(steamID64arg, after, before):

    url = 'https://ballchasing.com/api/replays/'
    auth = {'Authorization': '6LKHeGEtGRRIuLVdAk9xkMia5rKj3llZffKJyJYM'}
    argsdict = {'uploader': steamID64arg,
            'created-after': after,
            'created-before': before}
    print(argsdict)
    
    #r = requests.get(url, headers = auth)
    #data =r.json()
    #print(data['blue']['players'][0]['id']['id'])
    #return data
#END apiCallByReplayId

#method to abstract out the player data for each team
def parsePlayerData(playerList):
    pass

#method to abstract out the team data
def parseTeamData(teamDict):
    pass

def welcome():

    print('Hi SGL data collector, welcome! Mint City is the Best! Charlotte Til I Die!')
    print("""
                                       .
				     wWWWw
                                 mWWWw   wWWW;
                            .mWWWW’    ,-,,’;WWWWw.
                        .mWWW’’  _____^______  ‘’WWWWm.
		    .mWWWM’     /MMMMMMMMMMMMM\    ‘WWWWm.
                 .mWWWM’’      (W(  )MWMMW(  )M)       ‘WWWWm.
             .mWWWWM’           \WmmW-----WmmW/          ‘’WWWMm.
	     WMM’	          ‘’       ‘’                 WMM
             WMM  MMMMMMMMMMMM  MMMMMMMMMMMMM   MMMMM         WMM
             WMM  MMMMMMMMMMMM  MMMMMMMMMMMMM   MMMMM         WMM
             MMM  MMMMM   MMMM  MMMMM           MMMMM         WMM
             MMM  ‘MMMMM.       MMMMM           MMMMM         MMM
             MMM    ‘MMMMMm.    MMMMM  MMMMMM   MMMMM         MMM
             MMM        ‘MMMMM  MMMMM  MMMMMM   MMMMM         MMM
             MMM  MMMMM   MMMM  MMMMM    MMMM   MMMMM         MMM
             MMM  WWWWWWWWWWWW  WWWWWWWWWWWWW   WWWWWWWWWWWW  MMM
             MMM  WWWWWWWWWWWW  WWWWWWWWWWWWW   WWWWWWWWWWWW  MMM
             WWW  ______   ______   ______   ______   ______  MMM
             MMM  MMMMMM   MMMMMM   MMMMMM   MMMMMM   MMMMMM  MMM
             WWW   ‘WWWW   MMMMMM   MMMMMM   MMMMMM   WWWW’   MMM
             MMMm.    ‘M   M CAN!   M USA!   M MEX!    W’   .mWWW
               ‘TWWWMm     MWWWWM   MWMMMW   MMMMMM     ‘MMMM’
                   ‘TMMMW.   ‘TWM   MMMMMM   MMT’   ;MMMMM’ 
                      ‘TMMMW.   ‘   MMMMMM  ‘   .;MMMM’
                          ‘TMMMM;.  ‘’MT’’  ./MMMM’’ 
                              ‘TMMMM;.  .;WMMMM’ 
                                  ‘TMMMMMMT’
                                     ‘TT’

        """)
    if len(sys.argv) == 1:
        print('You called the script without game id, player id, or date ranges.'+
              '\nOpening cmd ln MENU:')
        time.sleep(.5)
        print('.')
        time.sleep(.5)
        print('.')

        matchIDs = getCmdMatchIds()
        if len(matchIDs) == 0:
            playerId = getCmdSteamName()
            print('\nrecieved player id ' + playerId)
        
    print(len(sys.argv))

#Get the command args via MENU
def getCmdMatchIds():

    print("""Enter match IDs: 
    (enter as many as you\'d like, when done hit enter with blank line)
    (if none at all, hit enter with blank line to proceed to player ID args)
    """)
    blankEntered = False
    i = 1
    matchIDs = []
    while blankEntered == False:
        matchId = input('Enter match ' + str(i) + ' ID: ')
        i+=1
        if matchId == '':
            blankEntered = True;
            if len(matchIDs) > 0:
                print('\nRecieved ' + str(len(matchIDs))+ ' Match IDs: ')
                for match in matchIDs:
                    print(match + ", ", end='')
                print()
        else:
            matchIDs.append(matchId)
    return matchIDs


def getCmdSteamName():

    uploaderDict = {
        "patabread5": "76561198977461368",
        "patabread": "76561198977461368",
        "pata": "76561198977461368",
        "76561198977461368": "76561198977461368"
    }

    steamNames = uploaderDict.keys()
    steamIDs = uploaderDict.keys()
    idValue = None

    while idValue is None:
        playerNameOrIDinput = input('\nSteam name or player ID of who uploaded this weeks matches to Ballchaser.com: ')
        playerNameOrIDinput = playerNameOrIDinput.lower()

        holder = playerNameOrIDinput
    
        idValue = uploaderDict.get(playerNameOrIDinput)
        
        if idValue is None and holder != '':
            print('Sorry could not validate an ID for that input, try again or enter blank to end.')
        elif holder == '':
            print('Ending')
            return
    return(idValue)


def getReplayFile(replay_id):

    url = 'https://ballchasing.com/api/replays/' + replay_id
    auth = {'Authorization': 'vA9akDv9RQ4TlOGMREPJpbXmFsvOKxkWRr3SYFXM'}
    r = requests.get(url, headers=auth)
    # print(r.content)
    replay_json = r.json()
    # print(replay_json)
    cw = open('replay_data_' + replay_id + '.csv', 'w+')
    # cw = csv.writer(csv_file)
    header = "Date,Time,Venue,Teams,Results,Outcome," \
             "Players,Points,points,goals,assists,saves,shots" \
             "mvp,shooting_precentage,demos_inflicted,demos_taken," \
             "Boost/Min,bcpm,avg_amount,amount_collected,amount_stolen,amount_collected_big,amount_stolen_big," \
             "amount_collected_small,amount_stolen_small,count_collected_big,count_stolen_big,count_collected_small," \
             "count_stolen_small,amount_overfill,amount_overfill_stolen,amount_used_while_supersonic,time_zero_boost," \
             "percent_zero_boost,time_full_boost,percent_full_boost,time_boost_0_25,time_boost_25_50," \
             "time_boost_50_75,time_boost_75_100,percent_boost_0_25,percent_boost_25_50,percent_boost_50_75," \
             "percent_boost_75_100," \
             "avg_speed,total_distance,time_supersonic_speed,time_boost_speed,time_slow_speed," \
             "time_ground,time_low_air,time_high_air,time_powerslide,count_powerslide,avg_powerslide_duration," \
             "avg_speed_percentage,percent_slow_speed,percent_boost_speed,percent_supersonic_speed,percent_ground," \
             "percent_low_air,percent_high_air" \
             "avg_distance_to_ball,avg_distance_to_ball_possession,avg_distance_to_ball_no_possession," \
             "time_defensive_third,time_neutral_third,time_offensive_third,time_defensive_half,time_offensive_half," \
             "time_behind_ball,time_infront_ball,time_most_back,time_most_forward,goals_against_while_last_defender," \
             "time_closest_to_ball,time_farthest_from_ball,percent_defensive_third,percent_offensive_third," \
             "percent_neutral_third,percent_defensive_half,percent_offensive_half,percent_behind_ball," \
             "percent_infront_ball,percent_most_back,percent_most_forward,percent_closest_to_ball," \
             "percent_farthest_from_ball"
    cw.write(header + "\n")
    blue_rows = []
    orange_rows = []

    # get player names and data
    for player in range(0, len(replay_json["blue"]["players"])):
        blue_rows.append(replay_json["blue"]["players"][player]["name"])
        blue_rows.append(str(replay_json["blue"]["players"][player]["stats"]["core"].get("score")))
        blue_rows.append(str(replay_json["blue"]["players"][player]["stats"]["core"].get("goals")))
        blue_rows.append(str(replay_json["blue"]["players"][player]["stats"]["core"].get("assists")))
        blue_rows.append(str(replay_json["blue"]["players"][player]["stats"]["core"].get("saves")))
        blue_rows.append(str(replay_json["blue"]["players"][player]["stats"]["core"].get("shots")))
        blue_rows.append(str(replay_json["blue"]["players"][player]["stats"]["demo"].get("inflicted")))
        blue_rows.append(str(replay_json["blue"]["players"][player]["stats"]["demo"].get("taken")))
        for stat_category in replay_json["blue"]["players"][player]["stats"]:
            if stat_category != "core" and stat_category != "demo":
                for stat in replay_json["blue"]["players"][player]["stats"][stat_category]:
                    blue_rows.append(str(replay_json["blue"]["players"][player]["stats"][stat_category].get(stat)))
        if player != 0:
            blue_str = ',,,,,,' + ','.join(blue_rows) + "\n"
        else:
            if replay_json["blue"]["name"]:
                blue_str = str(replay_json["date"].split("T")[0].replace("-", "/")) + "," + str(replay_json["date"].split("T")[1]) + \
                             ",SGL Twitch," + replay_json["blue"]["name"] + ",,," + ','.join(blue_rows) + "\n"
            else:
                blue_str = str(replay_json["date"].split("T")[0]) + "," + str(replay_json["date"].split("T")[1]) + \
                             ",SGL Twitch,,,," + ','.join(blue_rows) + "\n"
        cw.write(blue_str)
        blue_rows = []

    for player in range(len(replay_json["orange"]["players"])):
        orange_rows.append(replay_json["orange"]["players"][player]["name"])
        orange_rows.append(str(replay_json["orange"]["players"][player]["stats"]["core"].get("score")))
        orange_rows.append(str(replay_json["orange"]["players"][player]["stats"]["core"].get("goals")))
        orange_rows.append(str(replay_json["orange"]["players"][player]["stats"]["core"].get("assists")))
        orange_rows.append(str(replay_json["orange"]["players"][player]["stats"]["core"].get("saves")))
        orange_rows.append(str(replay_json["orange"]["players"][player]["stats"]["core"].get("shots")))
        orange_rows.append(str(replay_json["orange"]["players"][player]["stats"]["demo"].get("inflicted")))
        orange_rows.append(str(replay_json["orange"]["players"][player]["stats"]["demo"].get("taken")))
        for stat_category in replay_json["orange"]["players"][player]["stats"]:
            if stat_category != "core" and stat_category != "demo":
                for stat in replay_json["orange"]["players"][player]["stats"][stat_category]:
                    orange_rows.append(str(replay_json["orange"]["players"][player]["stats"][stat_category].get(stat)))
        if player != 0:
            orange_str = ',,,,,,' + ','.join(orange_rows) + "\n"
        else:
            if replay_json["orange"]["name"]:
                orange_str = str(replay_json["date"].split("T")[0].replace("-", "/")) + "," + str(replay_json["date"].split("T")[1]) + \
                       ",SGL Twitch," + replay_json["orange"]["name"] + ",,," + ','.join(orange_rows) + "\n"
            else:
                orange_str = str(replay_json["date"].split("T")[0]) + "," + str(replay_json["date"].split("T")[1]) + \
                             ",SGL Twitch,,,," + ','.join(orange_rows) + "\n"
        cw.write(orange_str)
        orange_rows = []

    # blue_rows.append(stat)
    # for stat_category in replay_json["orange"]["players"]["stats"]:
    #     for stat in stat_category:
    #         orange_rows.append(stat)

    #
    #     str(replay_json["blue"]["name"]) + "," + \
    #     str(replay_json["blue"]["stats"]["core"]["score"]) + "," +\
    #     str(replay_json["blue"]["stats"]["core"]["shots"]) + "," + \
    #     str(replay_json["blue"]["stats"]["core"]["shots_against"]) + "," + \
    #     str(replay_json["blue"]["stats"]["core"]["goals"]) + "," + \
    #     str(replay_json["blue"]["stats"]["core"]["goals_against"]) + "," + \
    #     str(replay_json["blue"]["stats"]["core"]["saves"]) + "," + \
    #     str(replay_json["blue"]["stats"]["core"]["assists"]) + "," + \
    #     str(replay_json["blue"]["stats"]["core"]["goals"]) + "," + \
    #     str(replay_json["blue"]["stats"]["demo"]["inflicted"]) + "," + \
    #     str(replay_json["blue"]["stats"]["demo"]["taken"])
    # cw.write(blue_first + "\n")
    # for i in range(0, len(replay_json["blue"]["players"])):
    #     row = str(replay_json["blue"]["players"][i]["name"]) + "," + \
    #         str(replay_json["blue"]["players"][i]["stats"]["core"]["score"]) + "," + \
    #         str(replay_json["blue"]["players"][i]["stats"]["core"]["goals"]) + "," + \
    #         str(replay_json["blue"]["players"][i]["stats"]["core"]["assists"]) + "," + \
    #         str(replay_json["blue"]["players"][i]["stats"]["core"]["saves"]) + "," + \
    #         str(replay_json["blue"]["players"][i]["stats"]["core"]["shots"]) + "," + \
    #         str(replay_json["blue"]["players"][i]["stats"]["demo"]["inflicted"]) + "," + \
    #         str(replay_json["blue"]["players"][i]["stats"]["demo"]["taken"])
    #     cw.write(row + "\n")
    #
    # orange_first = str(replay_json["date"].split("T")[0]) + "," + str(
    #     replay_json["date"].split("T")[1]) + ",SGL Twitch," + \
    #         str(replay_json["orange"]["name"]) + "," + \
    #         str(replay_json["orange"]["stats"]["core"]["score"]) + "," + \
    #         str(replay_json["orange"]["stats"]["core"]["shots"]) + "," + \
    #         str(replay_json["orange"]["stats"]["core"]["shots_against"]) + "," + \
    #         str(replay_json["orange"]["stats"]["core"]["goals"]) + "," + \
    #         str(replay_json["orange"]["stats"]["core"]["goals_against"]) + "," + \
    #         str(replay_json["orange"]["stats"]["core"]["saves"]) + "," + \
    #         str(replay_json["orange"]["stats"]["core"]["assists"]) + "," + \
    #         str(replay_json["orange"]["stats"]["core"]["goals"]) + "," + \
    #         str(replay_json["orange"]["stats"]["demo"]["inflicted"]) + "," + \
    #         str(replay_json["orange"]["stats"]["demo"]["taken"])
    # cw.write(orange_first + "\n")
    # for i in range(0, len(replay_json["orange"]["players"])):
    #     row = str(replay_json["orange"]["players"][i]["name"]) + "," + \
    #         str(replay_json["orange"]["players"][i]["stats"]["core"]["score"]) + "," + \
    #         str(replay_json["orange"]["players"][i]["stats"]["core"]["goals"]) + "," + \
    #         str(replay_json["orange"]["players"][i]["stats"]["core"]["assists"]) + "," + \
    #         str(replay_json["orange"]["players"][i]["stats"]["core"]["saves"]) + "," + \
    #         str(replay_json["orange"]["players"][i]["stats"]["core"]["shots"]) + "," + \
    #         str(replay_json["orange"]["players"][i]["stats"]["demo"]["inflicted"]) + "," + \
    #         str(replay_json["orange"]["players"][i]["stats"]["demo"]["taken"])
    #     cw.write(row + "\n")

    cw.close()


def getReplayIDs(uploader, replay_date_before, replay_date_after):

    url = 'https://ballchasing.com/api/replays?uploader=' + uploader + '&replay-date-before=2020-' + \
          replay_date_before[0] + 'T' + replay_date_before[1] + ':00-06:00' + '&replay-date-after=2020-' + \
          replay_date_after[0] + 'T' + replay_date_after[1] + ':00-06:00&playlist=private&count=30'
    auth = {'Authorization': 'vA9akDv9RQ4TlOGMREPJpbXmFsvOKxkWRr3SYFXM'}
    r = requests.get(url, headers=auth)
    # print(url + "\t" + str(r.json()))

    data = r.json()

    return data


def main():

    # TODO: include support for multiple time zones lol
    # TODO: add columns to event page? thru player stats table?
    # TODO: do results/outcome data get updated automatically? where do they come from?
    # welcome()
    replay_date_after = input("Enter date and time matches started [MM-DD] [hh:mm] in 24-hour CT\n").split(" ")
    replay_date_before = input("Enter date and time matches ended [MM-DD] [hh:mm] in 24-hour CT\n").split(" ")
    replays = getReplayIDs("76561198240898984", replay_date_before, replay_date_after) # set to whoever is uploader
    # data = apiCallByReplayId('1ef2f98e-d7d9-45a3-b2dd-7e92a2da73b0')76561198156218146
    # print(replays)
    for replay in replays["list"]:
        print(replay["id"])
        getReplayFile(str(replay["id"]))

    # print(data['blue']['players'][0]['camera']['fov'])
    # apiCallReplays(76561198977461300, )


if __name__ == '__main__':
    main()

