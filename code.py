import numpy as np

# Reading Inputs from the input.txt file 
with open('input.txt','r') as file:
    list_=file.readline().strip()
    passengers=int(file.readline().strip())

# Condition for no input
if len(list_) == 0:
    print('\n','No input list is found!!'.center(100))
    exit()

print(f'\nInputed list of segments in form of Column X Row: {list_} \n\nInputted number of Passengers: {passengers}')

# Converting 1-D list into 2-D list of 2 columns 
list_ = list_.split(',')
list_ = np.reshape(list_, (-1, 2)).astype('int')

max_row_cnt, cnt_col, total, ais, midd, wind = -1, 0, 0, 0, 0, 0
column_list = list()

# Loop to find number of aisle, middle, window and total seats available
for i in range(len(list_)):

    max_row_cnt = max(max_row_cnt, list_[i, 1])
    total += list_[i, 0]*list_[i, 1]
    column_list.append(list_[i, 0]) # Store the number of columns of each section 
    cnt_col += list_[i, 0]

    if i == 0 or i == len(list_)-1:
        wind += list_[i, 1]
        ais += list_[i, 1]
    else:
        ais += 2*list_[i, 1]

# Finding the starting value for each type of seat
ais_start, wind_start, midd_start = 1, ais+1, ais+wind+1

output = np.full((max_row_cnt, cnt_col), 0, int)


for i in range(len(output)):

    start_ptr, seg_ptr = 0, 0 # Pointers used to find the segment and column number in that particular segment 

    for j in range(len(output[i])):

        # Incrementing segment if we reach the end of column in that particular segment 
        # and setting the value of reference pointer i.e. start_pointer equal to j

        if j-start_ptr >= column_list[seg_ptr]:
            start_ptr = j
            seg_ptr = (seg_ptr+1)

        # Condition to check that if particular segment has a seat or not
        if list_[seg_ptr, 1] <= i: 
            output[i, j] = -1
            continue

        c_num = j-start_ptr # Finding the column number in the segment

        # Condition to check for first section of seat
        if seg_ptr == 0:

            if c_num == 0:
                if wind_start <= passengers:
                    output[i, j] = wind_start
                    wind_start += 1

            elif c_num == column_list[seg_ptr]-1:
                if ais_start <= passengers:
                    output[i, j] = ais_start
                    ais_start += 1
            else:
                if midd_start <= passengers:
                    output[i, j] = midd_start
                    midd_start += 1

        # Condition to check for last section of seat
        elif seg_ptr == len(column_list)-1:

            if c_num == column_list[seg_ptr]-1:
                if wind_start <= passengers:
                    output[i, j] = wind_start
                    wind_start += 1
            elif c_num == 0:
                if ais_start <= passengers:
                    output[i, j] = ais_start
                    ais_start += 1
            else:
                if midd_start <= passengers:
                    output[i, j] = midd_start
                    midd_start += 1

        # Condition to check for middle sections
        else:
            if c_num == 0 or c_num == column_list[seg_ptr]-1:
                if ais_start <= passengers:
                    output[i, j] = ais_start
                    ais_start += 1
            else:
                if midd_start <= passengers:
                    output[i, j] = midd_start
                    midd_start += 1


output = output.astype('str')

for i in range(len(output)):
    for j in range(len(output[i])):

        # -1 represents that seat is not there
        if output[i, j] == '-1':
            output[i, j] = ' '
        
        # 0 represents seat is available & empty
        elif output[i, j] == '0':
            output[i, j] = '--'

if total < passengers:
    print(f'\n\nNumber of passengers EXCEED the total capacity ({total}) of flight!!\n\n')
else:
    print("\n\n")

# Loop to print the seating arrangement in tabular format 
for i in range(len(output)):
    
    start_ptr, seg_ptr = 0, 0
    
    for j in range(len(output[i])):

        if column_list[seg_ptr] == j-start_ptr:
            print("{:<3}".format("|"), end="")
            seg_ptr += 1
            start_ptr = j

        print("{:<3}".format(output[i, j]), end=" ")
    print()
