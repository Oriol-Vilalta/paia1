import sys
import random

clauses = []
num_vars = 0
num_clauses = 0
num_attempts = 1

#This function opens and reads the file and stores all the data in global variables.
# The name of the file is received as first argument when executing. If there are no arguments, "example1.txt" is opened by default.
def read_file(argv):
    global num_vars, num_clauses
    if len(argv)>1:
        try:
            file = open(argv[1], 'r')
        except IOError:
            print("File specified in the arguments can't be openend.")
            exit(1)
    else:
        try:
            file = open("example1.txt", 'r')
        except IOError:
            print("Default file can't be opened.")
            exit(1)
    for line in file:
        if line.startswith("p cnf"):
            _, _, num_vars, num_clauses = line.split()
        elif not line.startswith("c"):
            clauses.append(line.split())
    file.close()

#This function checks if the input follows correctly the CNF Dimacs format.
def check_clauses():
    global num_vars, num_clauses
    try:
        num_vars = int(num_vars)
        num_clauses = int(num_clauses)
    except ValueError:
        print("Non-numeric value for number of variables or number of clauses.")
    if len(clauses) != num_clauses:
        print("Wrong number of clauses.")
        exit(1)
    for i in range(len(clauses)):
        for j in range(len(clauses[i])):
            try:
                value = int(clauses[i][j])
            except ValueError:
                print("Non-numeric value in a clause.")
            if abs(value) > num_vars or (value == 0 and j != len(clauses[i]) - 1) or (value != 0 and j == len(clauses[i]) - 1):
                print("Incorrect value in a clause.")
                exit(1)
            elif (value==0):
                clauses[i].pop(j)
            else:
                clauses[i][j] = value

#This function generates randomly a binary number. Every bit represents a variable.
#If the bit is 0, the corresponding variable is set to False. Otherwise, it's set to true.
def random_values():
    rand_int = random.randint(0, 2**num_vars-1)
    rand_bin = bin(rand_int)[2:].zfill(num_vars)
    rand_list = [*rand_bin]
    for i in range(1, num_vars+1):
        if int(rand_list[i-1]) == 0:
            rand_list[i-1] = -i
        else:
            rand_list[i-1] = i
    return rand_list

#This function checks how many clauses are satisfied by a certain assignation of values to the variables.
def num_of_satisfied_clauses(values):
    result = 0
    for clause in clauses:
        for value in clause:
            if values[abs(value)-1] == value:
                result+=1
                break
    return result

#This function determines which of the assignations of values appears less times in the formula.
#This is the chosen heuristics for the search.
def find_least_repeated(values):
    min_repetitions = -1
    least_repeated = -1
    for value in values:
        counter = 0
        for clause in clauses:
            if value in clause:
                counter+=1
        if min_repetitions < 0 or counter < min_repetitions:
            min_repetitions = counter
            least_repeated = value
    return least_repeated

#This function receives the random assignation and modifies the value returned by the previous function while a solution hasn't been found.
#A taboo search is done. The previously modified assignations can't be modified again unless others have been already modified as well.
#The attempt is considered a failure if the current approach satisifes less clauses than the previous one.
#Only a certain amount of total failures and consecutive failures are allowed before generating a new random set of values.
def modify(values):
    global num_attempts
    satisfied_clauses = num_of_satisfied_clauses(values)
    if (satisfied_clauses == num_clauses):
        return values
    while True:
        failures = 0
        consecutive_failures = 0
        values_copy = values.copy()
        while failures<num_clauses*2 and consecutive_failures<num_clauses:
            num_attempts+=1
            if len(values_copy) == 0:
                values_copy = values.copy()
            least_repeated = find_least_repeated(values_copy)
            values[abs(least_repeated)-1] = -values[abs(least_repeated)-1]
            sat_cl = num_of_satisfied_clauses(values)
            if (sat_cl == num_clauses):
                return values
            if sat_cl < satisfied_clauses:
                failures+=1
                consecutive_failures+=1
            else:
                consecutive_failures = 0
            satisfied_clauses = sat_cl
            values_copy.remove(least_repeated)
        values = random_values()


if __name__ == '__main__':
    read_file(sys.argv)
    check_clauses()
    random_value = random_values()
    result = modify(random_value)
    print("s SATISFIABLE")
    #result_str = "v"
    """for i in result:
                    result_str = result_str + " " + str(i)"""
    result=str(result).replace(",", "")[:-1]
    result = result[1:]
    print("v " +result)
    #print(result_str)
    #print("Amb número d'intents:")
    print("c "+ str(num_attempts))
