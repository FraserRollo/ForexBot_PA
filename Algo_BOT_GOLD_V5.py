import pandas as pd

import oandapyV20

import oandapyV20.endpoints.instruments as instruments

import numpy as np

import time

import datetime

import os

from pathlib import Path

from matplotlib import pyplot as pltpip 

import csv



#path = str(Path(__file__).parent.absolute())

#path = input('Enter Path:') # D:#Code\Example\Pythonic Fx\WinPython\Forex OHLC

#print(path)

path = 'C:/Users/Administrator/Desktop/PythonBOT'

path=path.replace("\\","\\\\")

path=path[:path.find("PythonBOT")]

MT4link = 'C:/Users/Administrator/AppData/Roaming/MetaQuotes/Terminal/B591EFE97FF0D3AA8CB011E036154D17/MQL4/Files'#('Enter MT4 files folder, replace \ with /')





def DataDownloader(witPair):

    

    fx_pairs=(witPair)

    fx_pairs=fx_pairs.replace(' ','')



    counter1=(len(fx_pairs)-1)

    while counter1>0:

        string=fx_pairs[-6:]

        print(string)

        fx_pairs=fx_pairs[0:-6]

        pd.set_option('display.max_rows', 500)

        pd.set_option('display.max_columns', 500)

        pd.set_option('display.width', 1000)



        client = oandapyV20.API(access_token='7ef82c65e4c87de29202fc50287ae7a6-f665870decef9174b416a4e822b12efa',#insert new access token, will be expired

                                headers={"Accept-Datetime-Format":"Unix"})



        params = {

          "count": 201,

          "granularity": "M1"   #TIME DOMAIN TO RECIVE DATA

        }



        print ('Downloading ohlc data for '+string+'!')

        print('...')

        



        r = instruments.InstrumentsCandles(instrument=string[0:3]+'_'+string[3:6] , params=params)



        client.request(r)

        df=pd.DataFrame(r.response['candles'])

        #print(df)

        length=(len(df))-1

        low= np.asarray([])

        high= np.asarray([])

        close= np.asarray([])

        openn= np.asarray([])

        while length>0:

            specific_candle=pd.DataFrame(r.response['candles'][length])

            #print(specific_candle)

            obtain_low=specific_candle.tail(2)

            obtain_low=obtain_low.head(1)

            obtain_low=(obtain_low.mid.values)

            #print(obtain_low)

            obtain_close=specific_candle.head(1)

            obtain_close=obtain_close.mid.values

            obtain_high=specific_candle.head(2)

            obtain_high=obtain_high.tail(1)

            obtain_high=(obtain_high.mid.values)

            obtain_open=specific_candle.tail(1)

            obtain_open=obtain_open.mid.values

            #print(obtain_high)

            low=np.insert(low,0,float(obtain_low))

            high=np.insert(high,0,float(obtain_high))

            close=np.insert(close,0,float(obtain_close))

            openn=np.insert(openn,0,float(obtain_open))

            kopen= pd.DataFrame(columns=['open'], data=openn)

            khigh= pd.DataFrame(columns=['high'], data=high)

            klow=pd.DataFrame(columns=['low'], data=low)

            kclose=pd.DataFrame(columns=['close'], data=close)

            klines=pd.concat([kopen,khigh,klow,kclose,df], axis=1)



            length=length-1



        klines.mid=klines.mid.shift(-1)

        klines.complete=klines.complete.shift(-1)

        klines.time=klines.time.shift(-1)

        klines.volume=klines.volume.shift(-1)

        klines=klines.drop(columns=['mid'])

        klines.drop(klines.tail(1).index,inplace=True)

        print (klines.head(5))

        print(klines.tail(5))

        if os.name == 'nt':

            print(path+'PythonBOT\\Data\\'+string+'.csv')

            klines.to_csv((path+'PythonBOT\\Data\\'+string+'.csv')) #if using windows do not change

        else:

            klines.to_csv((r'/home/q/Dropbox/Dracula Blood Money Algo/H1OHLC/'+string+'.csv'))#if using linux/mac change directory 



def main():



    while True:

     try:



        DataDownloader('EURUSD''USDCAD''AUDUSD''USDJPY')

    



     except Exception as e: #break code on purpose, always force exceptions while scripts loop for long periods of time. Script can crash if internet connection is lost without exceptions.

         print(e)

         print('Timestamp: {:%Y-%b-%d %H:%M:%S}'.format(datetime.datetime.now()))

         print('Downloaded all candlestick data. sleeping for 30 min. zzz')

         #time.sleep(0)#adjust to 1800 for 30 min



         PairR = ['GBPUSD-g','EURUSD-g','XAUUSD-g','USDJPY-g','AUDUSD-g']

         PairT = ['EURUSD','USDCAD','USDJPY','AUDUSD']

        

        

         for num in range(0,len(PairT),1):



            arr = 'C:/Users/Administrator/Desktop/PythonBOT/Data/'+PairT[num]+'.csv'

            print(arr)

            df = pd.read_csv(arr,delimiter =',')

            Pair = str(PairT[num])

            close = np.array(df['close'])

            low = np.array(df['low'])

            high = np.array(df['high'])

            



            PIP = 0.0001

            BUFF = 0.001

            Multi = 10000

            Constraint1 = 0.0003

            Constraint2 = 0.0008



            if Pair == 'XAUUSD':

                BUFF = 0.4

                Multi = 10

                Constraint1 = 0.8

                Constraint2 = 1



            if Pair == 'USDJPY':

                BUFF = 0.02

                Multi = 100*(100/close[len(close)-1])

                Constraint1 = 0.03

                Constraint2 = 0.08




            # plt.plot(rsi(df))

            # plt.show()


            ######################################################################################################

            #   IDENTIFY LEGS



            NoL = 2



            # BUY LEGS 

            # Sell Legs



            sellLEGS = close[1:]-close[0:len(close)-1]

            sellLEGS = np.where(sellLEGS > 0,1,sellLEGS)

            sellLEGS = np.where(sellLEGS < 0,0,sellLEGS)

            sellLEGS = np.where(sellLEGS==0)

            sellLEGS1 = sellLEGS[0]



            ase = np.array(np.diff(sellLEGS,axis = -1))

            as1 = np.array(ase[0])



            idxs = np.where(as1>1)

            bs = np.array(idxs[0])

            bs = bs+1

        

            if len(bs)>=1:

                cs = []

                cs.append(bs[0])

                for i in range(0,len(bs)-1,1):

                    #c.append(b[0])

                    cs.append(bs[i+1]-bs[i])

                cs = np.array(cs)

                ds = np.cumsum(cs)



                es = np.where(cs == NoL)

                startPOSs = ds[es[0]]-1

                startPOSs = sellLEGS1[startPOSs]



                FdsL = np.array(startPOSs)

                FdsL = FdsL 



                RangeS = []



                for i in range(0,len(FdsL),1):

                    RangeS.append(max(high[FdsL[i]:FdsL[i]+2])-min(low[FdsL[i]:FdsL[i]+2]))



                RangeS = np.array(RangeS) 

                RangeSI = np.where(RangeS<10000)

                RangeSI = RangeSI[0]

                

                if len(RangeSI) >= 1:

                

                    if startPOSs[RangeSI[len(RangeSI)-1]] < len(close)-5:



                        for k in range(0,len(RangeSI),1):



                            if startPOSs[RangeSI[k]] > 1:

                            

                                SL = (max(high[startPOSs[RangeSI[k]]:startPOSs[RangeSI[k]]+2]))

                                NBL = (high[int(startPOSs[RangeSI[k]])+2:int(startPOSs[RangeSI[k]]+5)])

                                pos3 = np.where(NBL== max(NBL))

                                pos3 = pos3[0]

                                print('Stage 1 - BUY '+PairT[num])

                            

                        



                                if (max(NBL) > SL) and (SL+(BUFF) > max(NBL)):

                                    #NSL2 = (low[startPOSs[RangeSI[k]]+2+pos3[0]+1:startPOSs[RangeSI[k]]+2+pos3[0]+1+4])

                                    NSL2 = (low[startPOSs[RangeSI[k]]+2+pos3[0]+1:])



                                    if startPOSs[RangeSI[k]]+2+pos3[0]+1 < len(close)-4:

                                        NSL2 = (low[startPOSs[RangeSI[k]]+2+pos3[0]+1:startPOSs[RangeSI[k]]+2+pos3[0]+1+4])



                                    pos4 =  np.where(NSL2 == min(NSL2))

                                    pos4 = pos4[0]

                                    print('Stage 2 - BUY '+PairT[num])

                                    

                        

                            

                                    if (min(NSL2) < SL-(RangeS[RangeSI[k]]/2)) and (min(NSL2) > SL-RangeS[RangeSI[k]]):

                                        #FBL = high[int(startPOSs[RangeSI[k]])+2+pos3[0]+1+pos4[0]+1:int(startPOSs[RangeSI[k]]+2+pos3[0]+1+pos4[0]+1+6)]

                                        print('Stage 3 - BUY '+PairT[num])

                                        FBL = high[int(startPOSs[RangeSI[k]])+2+pos3[0]+1+pos4[0]+1:]



                                        if int(startPOSs[RangeSI[k]])+2+pos3[0]+1+pos4[0]+1 < len(close)-5:

                                            FBL = high[int(startPOSs[RangeSI[k]])+2+pos3[0]+1+pos4[0]+1:int(startPOSs[RangeSI[k]])+2+pos3[0]+1+pos4[0]+1+6]



                                        if len(FBL)>=1:



                                            fbp = np.where(FBL > max(NBL))

                                            fbp = fbp[0]



                                            if len(fbp) >= 1:

                                                if int(startPOSs[RangeSI[k]])+2+pos3[0]+1+pos4[0]+1+fbp[0]+1 > len(close)-1:



                                                    if max(FBL) > max(NBL):

                                                        print('Stage 4 - BUY '+PairT[num])
                                                        ps2 = np.where(FBL>max(NBL))[0]
                                                        poss2 = ps2[0]                                                       



                                                        if min(low[int(startPOSs[RangeSI[k]])+2:int(startPOSs[RangeSI[k]])+2+pos3[0]+1+pos4[0]+1+6]) >= (min(low[startPOSs[RangeSI[k]]:startPOSs[RangeSI[k]]+2])):



                                                            if low[len(close)-1] >=  (min(low[startPOSs[RangeSI[k]]:startPOSs[RangeSI[k]]+2])):



                                                                if ((close[len(close)-1]-(min(low[startPOSs[RangeSI[k]]:startPOSs[RangeSI[k]]+2])))) > Constraint1 and ((close[len(close)-1]-(min(low[startPOSs[RangeSI[k]]:startPOSs[RangeSI[k]]+2])))) < Constraint2:

                                                                    if pos3[0] + pos4[0] + poss2 < 3: #if  (close[len(close)-1]-(min(low[startPOSs[RangeSI[k]]:startPOSs[RangeSI[k]]+2]))) <= (2.5*PIP):

                                                                        TP1 = close[len(close)-1] + ((close[len(close)-1]-(min(low[startPOSs[RangeSI[k]]:startPOSs[RangeSI[k]]+2])))*1.5)    #-(((max(high[startPOS[RangeBI[k]]:startPOS[RangeBI[k]]+2]))-close[len(close)-1])*3)
                                                                        TP2 = close[len(close)-1] + ((close[len(close)-1]-(min(low[startPOSs[RangeSI[k]]:startPOSs[RangeSI[k]]+2])))*2) 
                                                                        TP3 = close[len(close)-1] + ((close[len(close)-1]-(min(low[startPOSs[RangeSI[k]]:startPOSs[RangeSI[k]]+2])))*3) 
                                                                        SL = (min(low[startPOSs[RangeSI[k]]:startPOSs[RangeSI[k]]+2]))#+((close[len(close)-1]-(min(low[startPOSs[RangeSI[k]]:startPOSs[RangeSI[k]]+2])))*0.1)
                                                                        SLinPIP = ((close[len(close)-1]-(min(low[startPOSs[RangeSI[k]]:startPOSs[RangeSI[k]]+2]))))*Multi



                                                                        signal = str('OP_BUY')

                                                                        place_order = pd.DataFrame({'': [Pair+','+signal+','+str(SL)+','+str(TP1)+','+str(TP2)+','+str(TP3)+','+str(SLinPIP),',,,']})

                                                                        place_order = place_order.to_csv(MT4link+"/LastSignal.csv", header=None, index=None, mode='w', sep=' ',quoting=csv.QUOTE_NONE, quotechar=",")

                                                                    

                                                                        print(Pair+ ' has opened a BUY postion ')

                                                                        time.sleep(200)

                                                                        main()



     except Exception as e: #break code on purpose, always force exceptions while scripts loop for long periods of time. Script can crash if internet connection is lost without exceptions.

        print(e)

        print('Timestamp: {:%Y-%b-%d %H:%M:%S}'.format(datetime.datetime.now()))

        print('Downloaded all candlestick data. sleeping for 30 min. zzz')

        time.sleep(1)#adjust to 1800 for 30 min



main()

