from UniswapData import *
from pandas import pd.DataFrame
from pandas import pd.Series



class Snapshot(pd.Series):
    def __init__(self,time: TimeData):
        self.time TimeData
        
    def time(self):
        return self.time

class CrossSectionalHelper:
    def __init__(self, token0: str, token1: str):
        self.aggDataEndpoint = UniswapData(token0=token0,token1=token1)


    def calculateValue(time:TimeData) -> float:

        '''
        At the given time
        1. fetches total liquidity of the pool
        2. fetches the sqrtPrice or price and if not squarted sqaare ir
        3. sqrLiquidity multiply it by sqrtPrice and then by 2 
        4. return value
        '''
    
    def fetchLiquidityProvidersLPShare(time:TimeData)-> Snapshot:
        '''
        At the given time:
        1. fetches the balance of the lp token for all active LP'S on the pool
        2. 
        '''
    def calculateLiquidityProvidersPositionValue(balances:FixedSeries) -> Snapshot:
        '''
        At the given time: divides the balances 
        1. queries the totalSupply of the pool
        2. qeureis the value of teh pool at the (calculateValue) 
        2. divides the balances each lp over the balance
        3. multiples the result by the value
        4. return the series with this calculations

        '''


    
    

