import types.PoolKey


class TimeSeriesHelper():
    def __init__(self,token0: str, token1: str):
        self.poolData = PoolData(token0,token1)
        self.poolKey = self.poolData.poolKey 

    def getTimeFor(self, by: Filter,frequency: Frequency, timeInterval: TimeInterval) -> TimeData: 
    
    def getPriceSeries(self,frequency: Frequency, timeInterval: TimeInterval) -> pd.Series:
    



    
