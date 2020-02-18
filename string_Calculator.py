# Author: Weihang Yuan
# this code solves a string that contains numbers, operators (+, -, *, /), and possibly spaces.
# I chose to write the code recursively because each meaningful operator divide the string into two smaller thunks that can be solved individually.

import math


def solve_eq(aString):
    # because * and / operators have higher priority compared to + and -, dividing the string based on + or - first
    bString = aString.replace(" ", "")  # space should be removed
    bString = bString.replace("--", "")     # remove double negative
    if "/0" in bString:
        print("divided by 0 undefined.")
        return
    if "+" in bString:
        aList = bString.split("+")
        result = solve_eq(aList[0])
        for i in aList[1:]:
            result = result + solve_eq(i)
        if "." in bString:  # check whether to return an int
            return result
        else:
            if int(result) == result:
                return int(result)
            else:
                return result
    if "-" in bString:  # negative sign is much more complicated to handle because combined with * or / it can cause sign flip
        aCount = 0
        bCount = 0
        aList = []
        aItem = None
        for i in range(len(bString)):
            if ((bString[i] == "-") and (bString[i - 1] != "*" and bString[i - 1] != "/") and (i != 0)):
                aList.append(aItem)
                aItem = "-"
            else:
                if aItem == None:
                    aItem = bString[i]
                else:
                    aItem += bString[i]
                    if i == (len(bString) - 1):
                        aList.append(aItem)
        for i in aList[0]:
            if i == "-":
                aCount += 1
        if (aCount % 2) == 1:  # in each chunk, because all the + and - are removed, the sign can be determined by the number of -
            result = - solve_eq(aList[0].replace("-", ""))
        else:
            result = solve_eq(aList[0].replace("-", ""))
            for i in aList[1:]:
                for q in i:
                    if q == "-":
                        bCount += 1
                if (bCount % 2) == 1:
                    result = result - solve_eq(i.replace("-", ""))
                else:
                    result = result + solve_eq(i.replace("-", ""))
            bCount = 0
        return result
    else:
        bString = bString + "*"
        aCount = 0
        bCount = 0
        for i in bString:
            # bCount is counting the index of current char
            # extract first number
            if i == "*" and aCount == 0:
                result = float(bString[aCount: bCount])
                aCount = bCount + 1
                trigger = 1
            if i == "/" and aCount == 0:
                result = float(bString[aCount: bCount])
                aCount = bCount + 1
                trigger = -1
            # trigger keeps track of whether a * or a / should be performed
            # after the first number continue the process every time an operator is found, at this point only * or /
            if i == "*":
                if trigger == 1:
                    try:
                        result = result * float(bString[aCount: bCount])
                        aCount = bCount + 1
                    except:
                        aCount = bCount + 1
                else:
                    try:
                        result = result / float(bString[aCount: bCount])
                        aCount = bCount + 1
                        trigger = 1
                    except:
                        aCount = bCount + 1
                        trigger = 1
            if i == "/":
                if trigger == 1:
                    try:
                        result = result * float(bString[aCount: bCount])
                        aCount = bCount + 1
                        trigger = -1
                    except:
                        aCount = bCount + 1
                        trigger = -1
                else:
                    try:
                        result = result / float(bString[aCount: bCount])
                        aCount = bCount + 1
                    except:
                        aCount = bCount + 1
            bCount += 1
        return result


# examples
# print(solve_eq("- 8 * --- 5 + 3 / 0"))
# print(solve_eq(""))
# print(solve_eq("2*3-1+5/8"))
