# player_box[['first_name', 'last_name', 'team_code', 'season', 'player_id', "pts", "fga", "fga3", "fgm", "fgm3", "fta", "ftm", "ast", "blk", "stl", "dreb", "oreb", "reb", "pf", "tf", "tov", "mins_played"]]

# X_num = X[num_attribs]
# X_num = num_pipeline.fit_transform(X_num)
#
# for cat in cat_attribs:
#     print(cat)
#     b = cat_pipeline.fit_transform(X[cat])

# X_cat = cat_pipeline.fit_transform(X_cat)


player_box = pd.read_csv("./data/player_box.csv")
player_info = pd.read_csv("./data/player_info.csv")


class Draft():
    def __init__(self):
        self.data = {}
        for year in range(2014, 2019):
            self.data[year] = pd.read_csv('./data/{0}.csv'.format(year))

    def drafted(self, name, year):
        keys = self.data.keys()
        if year in keys:
            dataset = self.data[year]
            for player in dataset.Player:
                if name == player:
                    return 1
        return 0


draft = Draft()

player_info[["grade_level", "division", "first_name", "last_name", "height_in", "season", "school", "conference_id",
             "player_id", "position"]]

player_box = player_box[player_box['player_id'] != -101]
player_box = player_box[~player_box['player_id'].isnull()]
player_box = player_box[player_box['season'] != None]
player_box = player_box[player_box['season'] != 2018]

player_info = player_info[player_info['player_id'] != -101]
player_info = player_info[~player_info['player_id'].isnull()]
player_info = player_info[player_info['season'] != None]
player_info = player_info[player_info['season'] != 2018]
player_info = player_info[~player_info['first_name'].isnull()]

player_box["player_id_AND_season"] = player_box["player_id"].map(int).map(str) + "_AND_" + player_box["season"].map(
    int).map(str)

player_info["player_id_AND_season"] = player_info["player_id"].map(int).map(str) + "_AND_" + player_info["season"].map(
    int).map(str)

player_stats = pd.merge(player_box, player_info, on='player_id_AND_season', how='outer')

player_stats = player_stats[
    ['pts', 'fga', 'fga3', 'fgm', 'fgm3', 'fta', 'ftm', 'ast', 'blk', 'stl', 'dreb', 'oreb', 'reb', 'pf', 'tf', 'tov',
     'mins_played', 'grade_level', 'division', 'first_name', 'last_name', 'height_in',

     'school', 'conference', 'position', "season_x"]]

player_stats

len(player_stats[~player_stats['pts'].isnull()])

working_dataset = (player_stats[~player_stats['pts'].isnull()])
list(working_dataset)

working_dataset = working_dataset[
    ["first_name", "last_name", 'pts', 'fga', 'fga3', 'fgm', 'fgm3', 'fta', 'ftm', 'ast', 'blk', 'stl', 'dreb', 'oreb',
     'reb', 'pf', 'tf', 'tov', 'mins_played', 'grade_level', 'division', "height_in", "season_x"]]

working_dataset = working_dataset.dropna()

list(working_dataset)

Y = np.zeros((working_dataset.shape[0], 1))

iter = working_dataset.iterrows()
for i, row in enumerate(iter):
    name = str(row[1].first_name) + ' ' + str(row[1].last_name)
    # print(name)
    if name != 'Opponent Stats Do Not Modify' and draft.drafted(name, row[1]['season_x'] + 1):
        Y[i] = [1]

list(working_dataset)