from django.db import models
import requests
from collections import Counter
from datetime import datetime, timedelta

url = "https://api.lotterywest.wa.gov.au/api/v1/games/"
date_fmt = "%Y-%m-%d"

class DrawResults(models.Model):
    numbers = []
    games = {}

    def get_all_results(self):
        try:
            response = requests.get(url).json()['data']
            return response
        except Exception as e:
            print("Error gathering data, try again later")
            print(str(e))

    def get_results(self, games=[], days_ago=0):
        self.numbers = []
        for game in games:
            response = self.get_all_results()[game]['results']
            for result in response:
                if days_ago > 0:
                    draw_date = datetime.strptime(result["draw_date"], date_fmt)
                    if (datetime.today() - timedelta(days=days_ago)) > draw_date:
                        continue
                winninig_numbers = result['winning_numbers_display'].replace(" ", "").split(",")
                self.numbers = self.numbers + winninig_numbers
        return dict(Counter(self.numbers))

    def get_games(self):
        self.games[0] = "All games"
        data = self.get_all_results()
        for key, value in data.items():
            try:
                self.games[key] = value['title']
            except:
                pass
        return self.games
