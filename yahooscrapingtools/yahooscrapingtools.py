import os
import json
import datetime
from yahoo_oauth import OAuth2
import yahoo_fantasy_api as yfa
from .leagueutils import LeagueUtils


def get_year():
    today = datetime.datetime.now()
    if today.month < 8:
        today = today.replace(year=today.year - 1)
    return int(today.year)


CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')


class YahooScrapingTools:

    game = None
    sc = None
    last_league = None
    logged_in = False

    def __init__(self, creds=None):
        if creds:
            try:
                a, b = self._load_creds(creds)
                self.consumer_key, self.consumer_secret = a, b
            except ValueError:
                raise
        else:
            self.consumer_key, self.consumer_secret = CONSUMER_KEY, CONSUMER_SECRET

    def _set_last_league(self, lid):
        self.last_league = lid

    @staticmethod
    def _load_creds(creds):
        if isinstance(creds, str):
            try:
                with open(os.path.join(os.getcwd(), creds), 'rb') as file:
                    dcreds = json.load(file)
            except FileNotFoundError:
                dcreds = json.loads(creds)
        elif isinstance(creds, dict):
            dcreds = creds
        else:
            raise ValueError
        return dcreds['consumer_key'], dcreds['consumer_secret']

    def _get_session(self):
        return OAuth2(self.consumer_key, self.consumer_secret)

    def login(self):
        self.sc = self._get_session()
        self.game = yfa.Game(self.sc, 'nba')

    def get_leagues(self, year=None):
        if self.game:
            if year:
                if isinstance(year, bool):
                    year = get_year()
                league = self.game.league_ids(year=year)[0]
                self._set_last_league(league)
                return league
            else:
                return self.game.league_ids()

    def get_scoreboards(self, league=None, week=None):
        if not league:
            league = self.last_league
        if league:
            util = LeagueUtils(self.sc, league)
            return util.get_scoreboard(week)

    def get_teams(self, league=None):
        if not league:
            league = self.last_league
        if league:
            util = LeagueUtils(self.sc, league)
            res = util.get_teams()
            return {team['team_key']: team['name'] for team in res}


if __name__ == '__main__':
    test = YahooScrapingTools()
    test.login()
    t = test.get_leagues(2019)
    s = test.get_scoreboards(week=1)
    # for l in t:
    #     print(l)
    print(t)
    print(s)
    print('boop')
