# using excel sheet
import xlrd # reading excel
loc = ("covid19 for python.xlsx")
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)


#defining variables for accessing the excel sheet columns. 
# county = 0, median household income = 1, population = 2, COVID-19 cases = 3
colcounty = 0
coli = 1
colp = 2
colcase = 3
'''for i in range(sheet.nrows):  #for printing out the entire column 
    print(sheet.cell_value(i,colcase))  '''

#high income factor 
#HIGHINCOMETHRESH = 68703
MAXINCOME = 89881 #max household income is found from the spreadsheet out of public data
def probH(ithresh):
    highincomepop = 0 # high income population 
    totalpop = 0
    for i in range(sheet.nrows-1):
        rownum = i + 1
        if sheet.cell_value(rownum,coli) > ithresh:
            highincomepop += sheet.cell_value(rownum, colp)
        totalpop += sheet.cell_value(rownum, colp)
    probH= highincomepop/totalpop # P(H)
    # print("high income population: ", highincomepop)
    # print("total population: ", totalpop)
    return probH

def probnotH(probH): 
    return 1 - probH

#note the divisor should be the total population not the total COVID-19 cases 
def probCgivenH(ithresh): 
    highincomecovidpop = 0 # high income population that have tested postitive for COVId-19 
    totalpop = 0 # total COVID-19 positive cases in WA
    for i in range(sheet.nrows-1):
        rownum = i + 1
        if sheet.cell_value(rownum,coli) > ithresh:
            highincomecovidpop += sheet.cell_value(rownum, colcase)
        totalpop += sheet.cell_value(rownum, colp)
    return highincomecovidpop/totalpop 

def probCgivennotH(ithresh): 
    lowincomecovidpop = 0 # high income population that have tested postitive for COVId-19 
    totalpop = 0 # total COVID-19 positive cases in WA
    for i in range(sheet.nrows-1):
        rownum = i + 1
        if sheet.cell_value(rownum,coli) < ithresh:
            lowincomecovidpop += sheet.cell_value(rownum, colcase)
        totalpop += sheet.cell_value(rownum, colp)
    return lowincomecovidpop/totalpop 

def probHgivenC(ithresh):
    num = probCgivenH(ithresh) * probH(ithresh)
    den = num + (probCgivennotH(ithresh) * probnotH(probH(ithresh)))
    return num/den

# main, second part of the project for variable income threshold which is determined by incrementing the percentage by 5 and multiplying that 
# by the highest median income. This code prints 20 data points. 
for i in range(0,20):
    ratio = (i + 1)* 0.05
    incomethresh = ratio*MAXINCOME
    #print(incomethresh)
    print(1 - probHgivenC(incomethresh)) 
    

print("P(C|H) = ", probCgivenH(68703))
print("P(C|not H) = ", probCgivennotH(68703))
print("P(H|C) = ", probHgivenC(68703))
