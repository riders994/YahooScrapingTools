import yahoo_fantasy_api as yfa


class LeagueUtils:

    def __init__(self, sc, lid):
        self.lid = lid
        self.sc = sc
        self.league = yfa.League(self.sc, league_id=lid)
        self.handler = yfa.yhandler.YHandler(sc)

    def get_teams(self):
        return self.league.teams()

    def get_scoreboard(self, week=None):
        dump = self.handler.get_scoreboard_raw(self.lid, week)
        res = dump['fantasy_content']['league'][1]['scoreboard']
        return res['0']['matchups']


if __name__ == '__main__':
    pass
