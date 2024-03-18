#Romina Dehghani Mohammadi  2020510096
#Serkan Durmaz  2019510030
#Group 35
import csv
import json

#Reading file and storing in the dictionary and sorting
def read_csv_to_sorted_dict(filename):
    data_dict = {}
    
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        headers = next(csv_reader)  #Reading the header row
        Columns=headers[0].split(";")  #Stroring the first row for name of columns
        for row in csv_reader:
            row_split=row[0].split(";")
            key = row_split[0]  #Assuming the first column is the key
            #Storing the row data in the dictionary
            data_dict[int(key)] = {"id": row_split[0], "name": row_split[1], "lastname": row_split[2], "email": row_split[3],
                               "grade": row_split[4]}       
           
    #Sorting the dictionary by keys
    sorted_dict = dict(sorted(data_dict.items()))
    
    return sorted_dict,Columns

#Controling
def checking_query(querySp, Columns, operators):
    
    #Splitting the query column names
    checkColumnNames = querySp[1].split(",")
    checkNames = True
    checkOperators = False
    checkCondition= False
    
    #Checking if all column names are valid
    for name in checkColumnNames:
        if name not in Columns:
            checkNames = False
            break
    if(querySp[0].upper()=="SELECT"):
        if querySp[8].upper()=="AND" or querySp[8].upper()=="OR":
            #Checking if both operators are valid
            if querySp[6] in operators and querySp[10] in operators:
                checkOperators = True
            if querySp[5] in Columns and querySp[9] in Columns:
                checkCondition = True
        #Checking if the operator is valid
        elif querySp[6] in operators:
            checkOperators = True 
            if querySp[5] in Columns:
                checkCondition = True
    else:
        if(len(querySp)-1<7):
            #Checking if the operator is valid
            if querySp[5] in operators:
                checkOperators=True
            if querySp[4] in Columns:
                checkCondition = True
        else:
            #Checking if both operators are valid
            if querySp[5] in operators and querySp[9] in operators:
                checkOperators=True
                
            if querySp[4] in Columns and querySp[8] in Columns:
                checkCondition = True
     
        
    return checkNames, checkOperators,checkCondition

#If there is one condition
def one_condition(querySp,table,Columns,condition,operator,columnName):
    
    newTable={}  #Creating a new table to store the filtered rows
    #Removing the unnecessary quotation marks from the condition
    condition=condition.replace("‘", "")
    condition=condition.replace("’", "")
    condition=condition.replace('"', "")
    condition=condition.replace("'", "")
    #Iterating for each row in the table
    for key in table.keys():
        #Checking the operator and condition to determine if it satisfies the condition (for all if and elif )      
        if(operator=="!=") and (table[key][columnName])!=condition and ((querySp[1].upper()=="ALL") or (querySp[0].upper()=="DELETE")):
            #Include all the columns in the new table
            newTable[key]=table[key]
        elif(operator=="!=") and (table[key][columnName])!=condition and (querySp[1].upper()!="ALL"):
            #Splitting the selected query column names
            selectedColumns=querySp[1].split(",")
            newTable[key]={}
            for count in selectedColumns:
                #Only include the selected columns in the new table
                newTable[key].update({count:table[key][count]})
                    
        elif(operator=="=") and (table[key][columnName])==condition and ((querySp[1].upper()=="ALL") or (querySp[0].upper()=="DELETE")):
            #Include all the columns in the new table
            newTable[key]=table[key]
        elif(operator=="=") and (table[key][columnName])==condition and (querySp[1].upper()!="ALL"):
            #Splitting the selected query column names
            selectedColumns=querySp[1].split(",")
            newTable[key]={}
            for count in selectedColumns:
                #Only include the selected columns in the new table
                newTable[key].update({count:table[key][count]})
            
        elif(operator=="<") and (int(table[key][columnName])<int(condition)) and ((querySp[1].upper()=="ALL") or (querySp[0].upper()=="DELETE")):
            #Include all the columns in the new table
            newTable[key]=table[key]
        elif(operator=="<") and (int(table[key][columnName])<int(condition)) and (querySp[1].upper()!="ALL"):
            #Splitting the selected query column names
            selectedColumns=querySp[1].split(",")
            newTable[key]={}
            for count in selectedColumns:
                #Only include the selected columns in the new table
                newTable[key].update({count:table[key][count]})
                        
        elif(operator==">") and (int(table[key][columnName])>int(condition)) and ((querySp[1].upper()=="ALL") or (querySp[0].upper()=="DELETE")):
            #Include all the columns in the new table
            newTable[key]=table[key]
        elif(operator==">") and (int(table[key][columnName])>int(condition)) and (querySp[1].upper()!="ALL"):
            #Splitting the selected query column names
            selectedColumns=querySp[1].split(",")
            newTable[key]={}
            for count in selectedColumns:
                #Only include the selected columns in the new table
                newTable[key].update({count:table[key][count]})
                    
        elif((operator=="<=") or (operator=="!>")) and (int(table[key][columnName])<=int(condition)) and ((querySp[1].upper()=="ALL") or (querySp[0].upper()=="DELETE")):
            #Include all the columns in the new table
            newTable[key]=table[key]
        elif((operator=="<=") or (operator=="!>")) and (int(table[key][columnName])<=int(condition)) and (querySp[1].upper()!="ALL"):
            #Splitting the selected query column names
            selectedColumns=querySp[1].split(",")
            newTable[key]={}
            for count in selectedColumns:
                #Only include the selected columns in the new table
                newTable[key].update({count:table[key][count]})
                    
        elif((operator==">=") or (operator=="!<")) and (int(table[key][columnName])>=int(condition)) and ((querySp[1].upper()=="ALL") or (querySp[0].upper()=="DELETE")):
            #Include all the columns in the new table
            newTable[key]=table[key]
        elif((operator==">=") or (operator=="!<")) and (int(table[key][columnName])>=int(condition)) and (querySp[1].upper()!="ALL"):
            #Splitting the selected query column names
            selectedColumns=querySp[1].split(",")
            newTable[key]={}
            for count in selectedColumns:
                #Only include the selected columns in the new table
                newTable[key].update({count:table[key][count]})
            
    return newTable   

#If there are two conditions
def two_condition(querySp,first_condition_table,second_condition_table):
    #Creating a new table for storing the result
    result_table={}
    if querySp[8].upper()=="AND":
        #Condition for "AND" operator
        for element1 in first_condition_table:
            for element2 in second_condition_table:
                if (element1 == element2):
                    #Adding the matching elements to the result table
                    result_table[element1]={}
                    result_table[element1].update(first_condition_table[element1])
    elif querySp[8].upper()=="OR":
        #Condition for "OR" operator
        for element1 in first_condition_table:
            if element1 not in result_table:
                #Adding non-repeating elements from the first condition table to the result table
                result_table[element1]={}
                result_table[element1].update(first_condition_table[element1])
            
        for element2 in second_condition_table:
            if element2 not in result_table:
                #Adding non-repeating elements from the second condition table to the result table
                result_table[element2]={}
                result_table[element2].update(second_condition_table[element2])
   
    return result_table

#Checking conditions for deleting
def delete(querySp,first_condition_table,second_condition_table,table):
    #Creating a new table to store the result
    result_table={}
    if querySp[7].upper()=="AND":
        #Condition for "AND" operator
        for element in table:
            #Checking if the element exists in both condition tables
            if (element in first_condition_table)and(element in second_condition_table):
                #Adding the element to the result table
                result_table[element]={}
                result_table[element].update(table[element])                       
      
    elif querySp[7].upper()=="OR":
        #Condition for "OR" operator
        for element in table:
            #Checking if the element exists either in the first table or in the second table or in both tables
            if (element in first_condition_table) or (element  in second_condition_table):
                #Adding the element to the result table
                result_table[element]={}
                result_table[element].update(table[element])
            
   
    return result_table
    
def main():
    filename = 'students.csv'  #Setting the filename
    #Reading the CSV file into a sorted dictionary and obtain the column names
    table,Columns = read_csv_to_sorted_dict(filename)
    operators = ["!=", "=","<",">","<=",">=","!<","!>", "AND", "OR"]  #List of operators
    query=input()  #Taking an input from the user
    
    while(query.upper()!="EXIT"):
        querySp=query.split(" ")  #Spliting the query
        result={}  #Creating a dictionary for storing the result
        SELECT_dict={}  #Creating a dictionary for the SELECT query
        before_query=querySp[0]  #keeping query for select
        #Checking
        if(querySp[0].upper()=="SELECT"and querySp[2].upper()=="FROM" and  querySp[3].upper()=="STUDENTS" and  querySp[4].upper()=="WHERE"and querySp[len(querySp) -3].upper()=="ORDER" and querySp[len(querySp) -2].upper()=="BY" and (querySp[len(querySp) -1].upper()=="ASC" or querySp[len(querySp) -1].upper()=="DSC") ):
            checkNames,checkOperators,checkCondition= checking_query(querySp, Columns, operators)
            if(checkNames and checkOperators and checkCondition):            
                if(querySp[8].upper()=="OR"or querySp[8].upper()=="AND"):
                    first_condition_table = one_condition(querySp,table,Columns,querySp[7],querySp[6],querySp[5])
                    second_condition_table = one_condition(querySp,table,Columns,querySp[11],querySp[10],querySp[9])
                    result = two_condition(querySp,first_condition_table,second_condition_table)
                    if ((querySp[len(querySp)-1]).upper()=="ASC"):
                        #Sorting the dictionary by keys
                        SELECT_dict = dict(sorted(result.items()))
                    else:
                        #Sorting the dictionary by key in descending order
                        SELECT_dict = dict(sorted(result.items(),reverse = True))
                        
                    print(SELECT_dict)
                else:
                    result = one_condition(querySp,table,Columns,querySp[7],querySp[6],querySp[5])
                    if ((querySp[len(querySp)-1]).upper()=="ASC"):
                        #Sorting the dictionary by keys
                        SELECT_dict = dict(sorted(result.items()))
                    else:
                        #Sorting the dictionary by key in descending order
                        SELECT_dict = dict(sorted(result.items(),reverse = True))
                        
                    print(SELECT_dict)
                    
            else:  #If entering the wrong columnames or wrong operators
                print("Sorry wrong columnames or wrong operators try againn!!")
        #Checking        
        elif(querySp[0].upper()=="INSERT" and querySp[1].upper()=="INTO" and  querySp[2].upper()=="STUDENTS"):
            #Deleting unnecessary chars
            values = querySp[3].split("(")
            flag=False
            if(values[0].upper()=="VALUES"):  #Checking
                flag=True             
            values = values[1].split(")")
            values = values[0].split(",")
            if (flag and len(values)==5):     
                #Insert table
                table[int(values[0])] = {"id": values[0], "name": values[1], "lastname": values[2], "email": values[3],
                               "grade": values[4]}
                print(table)
                print("Insert is done. If you want to see the file, type exit.")
            else:  #If entering the wrong command or missing data
                print("wrong command or missing data please try againn!!")
        #Checking
        elif(querySp[0].upper()=="DELETE"and querySp[1].upper()=="FROM" and  querySp[2].upper()=="STUDENTS" and  querySp[3].upper()=="WHERE"):
            checkNames,checkOperators,checkCondition= checking_query(querySp, Columns, operators)
            if(checkOperators and checkCondition):
                if(len(querySp)-1<7):  #One condition
                    #Must to delete
                    result = one_condition(querySp,table,Columns,querySp[6],querySp[5],querySp[4])
                    for key in result:
                        if key in table:
                            del table[key]  #Deleting
                    print(table)
                    print("Delete is done. If you want to see the file, type exit.")         
                elif querySp[7].upper()=="OR" or querySp[7].upper()=="AND":  #Two condition
                    #Must to delete
                    result1 = one_condition(querySp,table,Columns,querySp[6],querySp[5],querySp[4])
                    result2 = one_condition(querySp,table,Columns,querySp[10],querySp[9],querySp[8])
                    result = delete(querySp, result1, result2,table)
                    for key in result:
                        if key in table:
                            del table[key]  #Deleting
                    print(table)   
                    print("Delete is done. If you want to see the file, type exit.")
                else:  #If entering the wrong command or missing data
                    print("wrong command or missing data please try againn!!")
            else:  #If entering the wrong operators
                print("Sorry wrong operators or wrong condition try againn!!")
        else:  #If entering the wrong command
            print("There is no such command please type another command")              
        query = input("Give new command or EXIT: ")
        if(query.upper()=="EXIT"):
            with open('result.json', 'w') as fp:
                if(before_query.upper()=="SELECT"):  #If the comment is select we write select dictionary in json
                    json.dump(SELECT_dict,fp,indent=4)
                else:  #We write table dictionary in json
                    json.dump(table,fp,indent=4)      
            fp.close()
                    
main()