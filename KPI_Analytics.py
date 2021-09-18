import pathlib
import pandas
import numpy as np
import calendar
import datetime

#Set first week of the month
calendar.setfirstweekday(calendar.FRIDAY)

#Set the precision for all the float values of Panda Series
pandas.set_option("display.precision", 2)

#Analytics Class which 
#validates file on init
#parses the csv
#allows filtering the resulted panda series
#displaying filtered series
class KPI_Analytics:
    #path to the .csv file is stored in filepath
    def __init__(self):
      self.filepath = r"https://cdn.shopify.com/s/files/1/0424/9098/6654/files/data.csv?v=1631922030"
      self.filetype = pathlib.Path(self.filepath).suffix
      #validate filetype
      if ".csv" in self.filetype:
        self.parseAnalyticsData()
      else:
        print("Invalid File")
    
    #return the week number for a supplied date    
    def week_of_month(self,date):
      year = int(date.strftime("%Y"))
      month = int(date.strftime("%m"))
      day = int(date.strftime("%d"))
      x = np.array(calendar.monthcalendar(year, month))
      week_of_month = np.where(x==day)[0][0] + 1
      return(week_of_month)
    
    #parse the .csv file after validation    
    def parseAnalyticsData(self):
      data = pandas.read_csv(self.filepath, parse_dates=["date"])
      #create a new dataframe to store the calculated values
      self.kpis = pandas.DataFrame()
      
      #calculate all the KPI's and store it to the panda series
      self.kpis.loc[data.date != None, 'Date'] = data.date
      self.kpis.loc[data.date != None, 'Week'] = data.loc[:,'date'].apply(lambda x: self.week_of_month(x))
      self.kpis.loc[data.total_sessions > 0, 'Sessions'] = data.total_sessions
      self.kpis.loc[data.total_sessions> 0, 'App_Sessions%'] = (data.app_sessions/data.total_sessions) * 100
      self.kpis.loc[data.total_sessions> 0, 'CvR_Overall'] = (data.total_orders/data.total_sessions) * 100
      self.kpis.loc[data.app_sessions> 0, 'CvR_App'] = (data.app_orders/data.app_sessions) * 100
      self.kpis.loc[data.web_sessions> 0, 'CvR_Web'] = (data.web_orders/data.web_sessions) * 100
      self.kpis.loc[data.total_orders> 0, 'Orders'] = data.total_orders
      self.kpis.loc[data.total_orders> 0, 'App_Orders%'] = (data.app_orders/data.total_orders) * 100
      self.kpis.loc[data.total_revenue> 0, 'CIR_Overall'] = (data.total_cost/data.total_revenue) * 100
      self.kpis.loc[data.app_revenue> 0, 'CIR_App'] = (data.app_cost/data.app_revenue) * 100
      self.kpis.loc[(data.total_revenue-data.app_revenue)> 0, 'CIR_Web'] = (data.web_cost/(data.total_revenue-data.app_revenue)) * 100
      self.kpis.loc[data.total_orders> 0, 'AOV_Overall'] = data.total_revenue/data.total_orders
      self.kpis.loc[data.app_orders> 0, 'AOV_App'] = data.app_revenue/data.app_orders
      self.kpis.loc[data.web_orders> 0, 'AOV_Web'] = (data.total_revenue-data.app_revenue)/data.web_orders
      self.kpis.loc[data.total_sessions> 0, 'CostPerVisit'] = data.total_cost/data.total_sessions
      print(self.kpis.to_string(index=False))
      self.filterKPIFields()
    
    #render filterable fields and validate the input  
    def filterKPIFields(self):
      filterby = input("Filter by [Date,Week,Platform] :")
      if(filterby == "Date"):
        date_from = input("Please enter date from (YYYY-MM-DD):")
        date_to = input("Please enter date to (YYYY-MM-DD):")
        year, month, day = date_from.split('-')
        isValidDate = True
        try:
            datetime.datetime(int(year), int(month), int(day))
        except ValueError:
            isValidDate = False
        if(isValidDate):
            self.filterKPIData(filterby,date_from,date_to)
        else:
            print("Date is not valid.")
            self.filterKPIFields()
      elif(filterby == "Week"):
        week = int(input("Please enter week:"))
        if(week > 0):
          self.filterKPIData(filterby,week)
        else:
          print("Week is not valid.")
          self.filterKPIFields()
      elif(filterby == "Platform"):
        platform = input("Please enter Platform (App/Web):")
        if(platform == "App" or platform == "Web"):
          self.filterKPIData(filterby,platform)
        else:
          print("Platform is not valid.")
          self.filterKPIFields()
      else:
        print("Filter by field doesn't exist")
        self.filterKPIFields()
    
    #filter the panda series after validating the filter fields and their value
    def filterKPIData(self,column,value1,value2=None):
      #filter by Week column using the week number
      if(column == "Week"):
        filtered = self.kpis[self.kpis[column] == value1]
     
      #filter by Platform, only the columns related to the filtered platform will be rendered
      if(column == "Platform"):
        if(value1 == "App"):
          filtered = self.kpis[['Date', 'Week', 'Sessions', 'App_Sessions%', 'CvR_App', 'App_Orders%', 'CIR_App', 'AOV_App']]
        elif(value1 == "Web"):
          filtered = self.kpis[['Date', 'Week', 'Sessions', 'CvR_Web', 'CIR_Web', 'AOV_Web']]
          
      #filter by Date, in case of from and to date, the rows between the two dates will be rendered
      #in case of only from date, all the rows starting from date will be rendered
      if(column == "Date"):
        if(value2 != None and value2):
          filtered = self.kpis[(self.kpis[column] >= value1) & (self.kpis[column] <= value2)]
        else:
          filtered = self.kpis[(self.kpis[column] >= value1)]
      
      #output the filtered records    
      if filtered.empty:
        print('No matched records')
        self.filterKPIFields()
      else:
        print(filtered.to_string(index=False))
        self.filterKPIFields()

process = KPI_Analytics();
