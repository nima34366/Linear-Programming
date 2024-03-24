import pandas as pd
import sys
from fractions import Fraction
import numpy as np
MAXI = True

def float_to_mixed_number(value):
    # Convert the float to a Fraction with a limited denominator
    fraction = Fraction(value).limit_denominator()
    # The integer part of the mixed number
    integer_part = int(fraction)
    # The fractional part of the mixed number
    fractional_part = fraction - integer_part
    if integer_part and fractional_part:
        return f"{integer_part} {fractional_part}"
    if integer_part and not fractional_part:
        return  f"{integer_part}"
    if not integer_part and fractional_part:
        return  f"{fractional_part}"
    
# def print_mat(mat,columns,rows):
#     data = dict()
#     for col in range(len(columns)):
#         data[columns[col]] = [float_to_mixed_number(row[col]) for row in mat]

#     df = pd.DataFrame(data, index = rows[:])   
#     print(df)    
 
def print_mat(mat,columns,rows):
    data = dict()
    for col in range(len(columns)):
        data[columns[col]] = [row[col] for row in mat]

    df = pd.DataFrame(data, index = rows[:])   
    print(df)  

def is_feasible(data,columns,basic):

    for var_ind in range(1,len(basic)):
        ind = columns.index(basic[var_ind])
        column_data = []
        for row_ind in range(len(data)):
            column_data.append(data[row_ind][ind]) 
            if basic[row_ind] != columns[ind] and data[row_ind][ind]!=0:     
                return False,"pivot_issue"

    for row in data[1:]:
        # print(row)
        if row[-1]<0:
           return False,"neg_solution"
            
    return True,"ok"

def is_optimal(data):
    global MAX       
    for ind in range(1,len(data[0])-1):
        # print(data[0][ind])

        if MAXI:
            if data[0][ind]<0:
                return False    
        else:
            if data[0][ind]>0:
                return False  
    return True

def do_it_maxi(data, columns, basic, EV = None):
    global MAX
    #Entering Variable
    if EV==None:
        EV = 1
        for i in range(1,len(data[0])-1):
            if (data[0][i])<data[0][EV]:
                EV = i
        print("Entering Variable is",columns[EV])
    
    else:
        print("Entering Variable is",columns[EV])

    #Leaving Variable
    LV=-1
    min_ratio = float('inf')

    ratio_col = []

    for r in range(1,len(data)):
        if data[r][EV] == 0:
            continue
        ratio = data[r][-1]/data[r][EV]
        ratio_col.append(ratio)
        if ratio>0 and ratio<min_ratio:
            min_ratio = ratio
            LV = r
    print("Leaving Variable is",basic[LV])
    print("Ratio column is",ratio_col)
    if min_ratio == float('inf'):
        print("All ratios are negative. No feasible solution")
        sys.exit(1)    
    #Change basic variable
    basic[LV] = columns[EV]

    #Make the column pivot vector
    data[LV] = [i/data[LV][EV] for i in data[LV]]

    for row_ind in range(len(data)):
        if row_ind == LV:
            continue
        mul_fac = data[row_ind][EV]/data[LV][EV]
        # print(mul_fac)
        for column_ind in range(len(data[row_ind])):
            data[row_ind][column_ind] = data[row_ind][column_ind] - mul_fac*data[LV][column_ind]   
            

def do_it_mini(data, columns, basic, EV = None):
    #Entering Variable
    if EV==None:
        EV = 1
        for i in range(1,len(data[0])-1):
            if (data[0][i])>data[0][EV]:
                EV = i
        print("Entering Variable is",columns[EV])

    else:
        print("Entering Variable is",columns[EV])

    #Leaving Variable
    LV=-1
    min_ratio = float('inf')
    ratio_col = []
    for r in range(1,len(data)):
        if data[r][EV] == 0:
            continue
        ratio = data[r][-1]/data[r][EV]
        ratio_col.append(ratio)
        if ratio>0 and ratio<min_ratio:
            min_ratio = ratio
            LV = r

    print("Leaving Variable is",basic[LV])
    print("Ratio column is",ratio_col)
    if min_ratio == float('inf'):
        print("All ratios are negative. No feasible solution") 
        sys.exit(1)       

    #Change basic variable
    basic[LV] = columns[EV]

    #Make the column pivot vector
    data[LV] = [i/data[LV][EV] for i in data[LV]]

    for row_ind in range(len(data)):
        if row_ind == LV:
            continue
        mul_fac = data[row_ind][EV]/data[LV][EV]
        for column_ind in range(len(data[row_ind])):
            data[row_ind][column_ind] = data[row_ind][column_ind] - mul_fac*data[LV][column_ind]   

def make_it_feasible(mat,columns,basic):
    print("Check for minimum distortion")
    #Check Maximum Negative Value
    LV = None
    max_neg = 0
    for row_ind in range(1,len(mat)):
        # print(row)
        if mat[row_ind][-1]<0 and mat[row_ind][-1]<max_neg:
           LV = row_ind
           max_neg = mat[row_ind][-1]

    print("Leaving Variable is",basic[LV])
    #Get the abs ratio
    EV = float('inf')
    min_distortion = float('inf')       
    ratios = []
    for col_ind in range(1,len(mat[0])-1):
        try:
            ratio = abs(mat[0][col_ind])/abs(mat[LV][col_ind])
            if ratio>0 and ratio<min_distortion and data[LV][col_ind]<0:
                min_distortion = ratio
                EV = col_ind
            ratios.append(ratio)
            # print(ratio, min_distortion)
        except:
            ratios.append("inf")
            pass
    
    print("Entering Variable is",columns[EV]) 
    print("Ratio row is ",ratios) 

    #Change basic variable
    basic[LV] = columns[EV]

    #Make the column pivot vector
    data[LV] = [i/data[LV][EV] for i in data[LV]]

    for row_ind in range(len(data)):
        if row_ind == LV:
            continue
        mul_fac = data[row_ind][EV]/data[LV][EV]
        for column_ind in range(len(data[row_ind])):
            data[row_ind][column_ind] = data[row_ind][column_ind] - mul_fac*data[LV][column_ind]   

def make_it_feasible2(mat,columns,basic):

    for var_ind in range(1,len(basic)):
        ind = columns.index(basic[var_ind])
        column_data = []
        for row_ind in range(len(mat)):
            column_data.append(mat[row_ind][ind]) 
            if basic[row_ind] != columns[ind] and mat[row_ind][ind]!=0:
                mat[row_ind] = [mat[row_ind][col_ind]-mat[var_ind][col_ind]* mat[row_ind][ind]  for col_ind in range(len(columns)) ]

def multiple_solutions(mat, columns, basic):
    for i in columns:
        if i not in basic:
            if mat[0][columns.index(i)] == 0:
                print("Multiple solutions due to ", i)
                return columns.index(i)
    return None

def get_max_frac_index(sols):
    fracs = []
    for i in sols:
        if i>=0:
            fracs.append(i - int(i))
        else:
            fracs.append(i - int(i) + 1)
    print('Solution column fractions are',fracs)    
    return fracs.index(max(fracs)) + 1

def get_frac_row(index, mat):
    row = mat[index].copy()
    for i in range(len(row)):
        if row[i] >= 0:
            row[i] = row[i] - int(row[i])
        else:
            row[i] = row[i] - int(row[i]) + 1
    row = -row
    print("Fraction row is",row)
    return np.expand_dims(row, axis=0)


def integerize(mat, columns, basic):
    global g
    mat = np.array(mat)
    print('before vstacck')
    print(mat)
    mat = np.vstack((mat,get_frac_row(get_max_frac_index(mat[1:,-1]), mat)))
    print('after vstacck')
    print(mat)
    new_column = np.zeros(len(basic)+1)
    new_column[-1] = 1
    new_column = np.expand_dims(new_column, axis=-1)
    columns.append(f'G{g}')
    columns[-1], columns[-2] = columns[-2], columns[-1]
    basic.append(f'G{g}')
    g+=1
    mat = np.hstack((mat, new_column))
    mat[:, [-2, -1]] = mat[:, [-1, -2]]
    print_mat(mat, columns, basic)
    return mat.tolist(), columns, basic
    

data = ['1 -1	-1	0	0	0',
'0 3	2	1	0	5',
'0 0	1	0	1	2',
]
columns = "Z X1	X2	S1	S2	Solution".split()
rows = "Z S1 S2 ".split()
MAXI = True


data = [list(map(float,i.split())) for i in data]
print("################### INITIAL TABULATION ###################")
count = 0
g = 1

while(True):
    if count!=0:
        print("################### ITERATION",count,"###################")
    print_mat(data,columns,rows)

    if is_feasible(data, columns, rows)[0]:
        if is_optimal(data):
            print("Feasible, Optimal")
            if multiple_solutions(data, columns, rows) != None:
                if input("Multiple solutions exist. Continue? (y/n): ") == "y":
                    if MAXI:
                        do_it_maxi(data, columns, rows, multiple_solutions(data, columns, rows))
                        continue
                    else:
                        do_it_mini(data, columns, rows, multiple_solutions(data, columns, rows)) 
                        continue
            if input("Do you want to integerize the solution? (y/n): ") == "y":
                data, columns, rows = integerize(data, columns, rows)
            else: 
                sys.exit(0)
        else:
            print("Feasible, Not optimal")
            if MAXI:
                do_it_maxi(data, columns, rows)
            else:
                do_it_mini(data, columns, rows)  
    else:
        status =  is_feasible(data, columns, rows)[1]
        print("Not Feasible", is_feasible(data, columns, rows)[1] )
        if status == "neg_solution":
            make_it_feasible(data,columns,rows)
        elif status == "pivot_issue":    
            make_it_feasible2(data,columns,rows)   
        else:
            print("Unknown Error")
            sys.exit(0)    
    print("\n")
    count+=1

# print(rows)