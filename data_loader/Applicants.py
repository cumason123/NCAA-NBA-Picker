import pandas as pd
class Applicants():
  def __init__(self):
    self.data = {}
    for year in range(2014, 2019):
      self.data[year] = pd.read_csv('./data_loader/data/early_applicants/csv/{0}.csv'.format(year))
      
  def __contains__(self, value):
    """
    Returns a 1 if that player was an early applicant, 0 otherwise

    @param name: full capitalized string representing first and last name
    @param year: number representing the year of the season the player applied to the nba
    """
    name, year, dataset = value

    keys = self.data.keys()
    if year in keys:
      dataset = self.data[year]
      for player in dataset.Player:
        if name == player:
          return 1
    return 0

  def join(self, dataset):
    """
    Adds a column onto a given dataset indicating 1 if that player
    was drafted into the nba and 0 if that player was not
    """
    column = {'applied': []}

    for player in dataset.Player:
      name = ' '.join(player.first_name, player.last_name)

      if (name, player.season, dataset) in self:
        column['applied'].append(1)

      else:
        column['applied'].append(0)

    return datasets + pd.DataFrame(data=column)
