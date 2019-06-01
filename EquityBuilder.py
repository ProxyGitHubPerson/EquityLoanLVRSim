import pandas as pd
import numpy as np
import datetime
from datetime import date
from collections import OrderedDict
from dateutil.relativedelta import *

####################

def amortize(principal, interest_rate, years, addl_principal = 0 , annual_payments=12, start_date=date.today()):

    pmt = -round(np.pmt(interest_rate/annual_payments, years*annual_payments, principal), 2)
    # initialize the variables to keep track of the periods and running balances
    p = 1
    beg_balance = principal
    end_balance = principal

    while end_balance > 0:

        # Recalculate the interest based on the current balance
        interest = round(((interest_rate/annual_payments) * beg_balance), 2)

        # Determine payment based on whether or not this period will pay off the loan
        pmt = min(pmt, beg_balance + interest)
        principal = pmt - interest

        # Ensure additional payment gets adjusted if the loan is being paid off
        addl_principal = min(addl_principal, beg_balance - principal)
        end_balance = beg_balance - (principal + addl_principal)

        yield OrderedDict([('Month',start_date),
                           ('Period', p),
                           ('Begin Balance', beg_balance),
                           ('Payment', pmt),
                           ('Principal', principal),
                           ('Interest', interest),
                           ('Additional_Payment', addl_principal),
                           ('End Balance', end_balance)])

        # Increment the counter, balance and date
        p += 1
        start_date += relativedelta(months=1)
        beg_balance = end_balance

def run_simulation(df,equityAmt,interest_Rate_Sim,LVRPercentage,LVRTitle):
    
    totalbreachlist = []
    totalresultlist = []


    for row in df.itertuples():

        date = row[1]
        initialPrice = row[2]
        numShares = equityAmt / initialPrice
        
        LVRPrincipal = []
    
        for lvrLevel in LVRPercentage:
            principalamt = pd.DataFrame(amortize(
            principal = equityAmt * lvrLevel
            , addl_principal = equityAmt * 0.02/12
            , interest_rate =  interest_Rate_Sim
            , years = 15))
            LVRPrincipal.append(principalamt['End Balance'])
            
        LVRPrincipalStack = dict(zip(LVRTitle,LVRPrincipal))
            
        dfLVRSim = df[df['Date'] >= date].copy()
        dfLVRSim['DateForCheck'] = date
        dfLVRSim = dfLVRSim.head(180) #Grabs next 180 months
        dfLVRSim['EquityVal'] = dfLVRSim['Price'] * numShares
        dfLVRSim.reset_index(inplace = True)
        
        for LVRTitleItem, LVRPrincipalList in LVRPrincipalStack.items(): 
            dfLVRSim[LVRTitleItem] = LVRPrincipalList
                        
        totalresultlist.append(dfLVRSim)
    
    totalresultlist = pd.concat(totalresultlist)
    totalresultlist.to_csv("""totalresult.csv""")
    
    for LVRTitleItem in LVRPrincipalStack.keys():
        breach = totalresultlist[totalresultlist[LVRTitleItem] >= totalresultlist['EquityVal']]['EquityVal'].count()
        title = LVRTitleItem
        print(title)
        print(breach)

####################
        
df = pd.read_csv("""MSCI World.csv""")
df['Date'] = pd.to_datetime(df['Date'],format = "%d/%m/%Y")
df['Price'].astype(float)

equityAmt = 100000
LVRPercentage = [0.4,0.5,0.60,0.65,0.7,0.75]
LVRTitle = ['LVR40','LVR50','LVR60','LVR65','LVR70','LVR75']
interest_Rate_Sim = 0.05

run_simulation(df,equityAmt,interest_Rate_Sim,LVRPercentage,LVRTitle)

