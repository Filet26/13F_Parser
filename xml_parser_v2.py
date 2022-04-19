# Author    : Desmond Ho
# Date      : March 10, 2022
# Language  : Python
# Libraries : xmltodict, pprint, pandas, tabulate
# Warning   : works on SEC 13F filings @ fintel.io
from email import header
from enum import unique
from operator import attrgetter
import xmltodict
import pprint
import pandas
import time
from tabulate import tabulate

# =================GreenLight Capital ==================

Filename = 'Filings/Greenlight_13F.xml'

#  ===============Pershing Square=======================

# Filename = 'Filings/Pershing_Sqr_13F.xml'

# ==================Vanguard============================

# Filename = 'Filings/Vanguard_13F.xml'

# ==================Renaissance Technologies=============

# Filename = 'Filings/RenTech_13F.xml'



def parse_file(filename: str) -> dict:  
    """_parses XML files to a dictionary_

    Args:
        filename (str): _filename, or path to file name (relative)_

    Returns:
        dict: _a dictionary of holdings_
    """    
    # Open the file and read the contents
    with open(filename, 'r', encoding='utf-8') as file:
        my_xml = file.read()
    # parse the file
    my_dict = xmltodict.parse(my_xml)

    return my_dict


def Compile_Holdings(raw_dict: dict):
    """_summary_

    Args:
        raw_dict (dict): _dictionary of holdings, formmated from parse_file function_

    Returns:
        _type_: _description_
    """    
    
    allHoldings = []
    for i in raw_dict["informationTable"]["infoTable"]:
        try:
             optionType = i["putCall"]
        except:
            optionType = "Equity"
        allHoldings.append(Holding(i["nameOfIssuer"], i["titleOfClass"], i["cusip"], i["value"], \
                                    i["shrsOrPrnAmt"], i["investmentDiscretion"],i["votingAuthority"] , optionType))
    allHoldings.sort(key=lambda x: x.value, reverse=True)
    return allHoldings



class Firm:
    def __init__(self, name: str = "Default Capital LLC", list_of_holdings: list = None) -> None:
        self.name = name
        self.list_of_holdings = list_of_holdings

        

    def total_firm_Stats(self) -> str:
        """_returns a string with stats about the firm, including holdings and market values_

        Returns:
            _type_: _description_
        """        
        # information about the holdings
        total_mkt_vals = [self.list_of_holdings[i].value for i in range(len(self.list_of_holdings))]
        unique_holdings = []
        for i in self.list_of_holdings:
            if i.CUSIP not in unique_holdings:
                unique_holdings.append(i.CUSIP)

        return f"Total Firm AUM:  {sum(total_mkt_vals)}\nUnique Positions: {len(unique_holdings)}\nTotal Positions: {len(total_mkt_vals)}"

    def top_holding(self) -> str:
        # get the CUSIP of the stock
        self.list_of_holdings.sort(key=lambda x: x.value, reverse=True)
        return self.list_of_holdings[0]


    def printTable(self, write_to_file: str, Rows: str = None):
        """_prints a nicely formated table of the firms holdings, using tabulate
            there is an option to filter by a key, eg. Company name, holding value, CUSIP_

        Args:
            list_of_holdings (list): _formatted list of holdings_
            CUSIP (int, optional): _the CUSIP number for the company_. Defaults to None.
        """    
        data = []
        total_mkt_vals = [self.list_of_holdings[i].value for i in range(len(self.list_of_holdings))]
        headers = ["Company Name", "Share Class", "CUSIP", "Market Value", \
                        "Shares","Per Share","% of Portfolio", "Discretion", "Sole Voting", "Instrument"]
        for stock in self.list_of_holdings:
                data.append([stock.name, stock.shrClass, stock.CUSIP, stock.value, stock.shares, round(stock.value/stock.shares, 2), \
                (round((stock.value/sum(total_mkt_vals)*100), 2)), stock.discretion, stock.voting, stock.optionType])
        if Rows == None:
            if write_to_file == "y":
                with open("file123.txt", "w") as f:
                    f.write(tabulate(data, headers, tablefmt='pretty'))
            else:
                print(tabulate(data, headers, tablefmt='pretty'))
        elif int(Rows) != None:
            print(write_to_file[0])
            if write_to_file[0].lower() == "y":
                with open("file123.txt", "w") as f:
                    f.write(tabulate(data, headers, tablefmt='pretty'))
            else:
                print(tabulate(data[:Rows], headers, tablefmt='pretty'))
     






class Holding:
    def __init__(self, name=None, shrClass=None, CUSIP=None, \
    value=None, shares=None, discretion=None, voting=None, optionType=None) -> None:
        """_Class for individual stock holdings_

        Args:
            Bunch of them LMAO
            shares (dict): _the amount of shares held, this function
            only displays SOLE ownership too fucking bad eh?_

            voting (dict): _Also shows SOLE voting powers, lmao_

        Returns:
            None
        """    ''''''
        self.name = name
        self.shrClass = shrClass
        self.CUSIP = CUSIP
        self.value = int(value) * 1000
        # format
        self.shares = int(shares["sshPrnamt"])
        self.discretion = discretion
        # format
        self.voting = voting["Sole"]
        self.optionType = optionType 



    # prints all info for stock
    def __str__(self)-> str:
        """dunder method for print, will print out all the information about the stock

        Returns:
            _str_: _formmated string_
        """        ''''''
        string = f"Company Name: {self.name:>21}\nShare Class:  {self.shrClass:>14}\nCUSIP:"\
        f"{self.CUSIP:>20}\nMaket Value:  {self.value:>9}\nShares:       {self.shares:>8}\nPer Share (USD): "\
        f"{round(self.value/self.shares, 2):>1}\nDiscretion: {self.discretion:>8}\nVoting Rights: {self.voting:>7}\nOption (Type): {self.optionType:>8}\n"
        return string



def main():
    start_time = time.time()
    # list of holdings
    List_Holdings = Compile_Holdings(parse_file(Filename))
    # Firm class
    Greenlight = Firm("Greenlight", List_Holdings)
    Greenlight.printTable("y", 100)
    print(Greenlight.total_firm_Stats())
    print(75*"=")
    print(Greenlight.top_holding())
    print(f"===========================================================================\n"\
    f"Process finished --- {round((time.time() - start_time), 2)} seconds ---")
    print("===========================================================================")

if __name__ == "__main__":
    '''yea main big boi funcy'''
    main()





