import pandas as pd
class Applicants():
  def __init__(self):
    self.data = {}
    for year in range(2014, 2018):
      csvfile = './data_loader/data/early_applicants/csv/{0}.csv'.format(year)
      self.data[year] = pd.read_csv(csvfile)
    self.data = pd.concat(self.data).drop_duplicates().reset_index(drop=True)
      
  def __contains__(self, value):
    """
    Returns a 1 if that player was an early applicant, 0 otherwise

    @param name: full capitalized string representing first and last name
    @param year: number representing the year of the season the player applied to the nba
    """
    if len(value) == 2:
      name, year = value
    else:
      raise(ValueError('Expected (name, year) or (name, year, dataset), found tuple of len {0}'.format(len(value))))

    for i, player in self.data.iterrows():
      dataset_player = ' '.join((player['first_name'], player['last_name']))
      if name == dataset_player:
        return True
    return False

  def join(self, dataset):
    """
    Adds a column onto a given dataset indicating 1 if that player
    was drafted into the nba and 0 if that player was not
    """
    a = dataset.merge(self.data, on=['first_name','last_name'], how='inner')
    return a
