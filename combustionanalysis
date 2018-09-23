from bs4 import BeautifulSoup as bs
import requests

''' 
requisites: install "bs4", "requests" packages
a script that finds the EF (option for MF as well) of a compound, given information from combustion reaction

-IMPORTANT NOTE: due to the impreciseness of input values (and floating-point precision), the code has to interpret
 which float values are supposed to be integers. parameters (that can be tweaked) that govern this interpretation are
 ERRORMARGIN and MAX_FRAC_CHECK, see below. that said, this is effectively always a GUESS at what the correct value is, 
 so remember to inspect log data to check for sensibility and know that due to the impreciseness of the process, 
 there may still be issues like the EF having decimals, or not being fully reduced. be cautious.

-note: while most values are floats (quite precise), 
 some values are rounded via the acceptable C:12,O:16,H:1 metrics

-ANNOTATIONS (on interesting bug fixes):
 
 -- checking for error margin in rounding: can't set "base value" to (float + 0.5):
    the 0.5 isn't supposed to be there for error margin checking value, just for rounding

'''


CMOLARMASS = 12
OMOLARMASS = 16
HMOLARMASS = 1


def take_input():

    print("format: input masses as raw floats (no units taken - must already be same)")

    moleculeMass0 = input("has oxygen? if so, enter mass of molecule. otherwise, enter NO")
    co2_mass0 = float(input("enter mass of CO2: "))
    h2o_mass0 = float(input("enter mass of H2O: "))
    molarMassVal0 = input("calculate molecular formula? if so, enter molar mass of substance. otherwise, enter NO")
    params0 = input("change integer checking parameter values? if so, enter csv (margin,frac). otherwise, enter NO")
    return moleculeMass0, co2_mass0, h2o_mass0, molarMassVal0, params0.split(",")



def find_empirical_value(c_float, h_float, o_float):

    print("note: initial division did not result in integer values. now attempting to find scale by which to multiply.")
    for i in range(2, MAX_FRAC_CHECK):
        ctest, htest, otest = c_float*i, h_float*i, o_float*i
        if (abs(int(ctest + 0.5) - ctest) < ERRORMARGIN
            and abs(int(htest + 0.5) - htest) < ERRORMARGIN
            and abs(int(otest + 0.5) - otest) < ERRORMARGIN):
            return int(ctest+0.5), int(htest+0.5), int(otest+0.5)

    #problem is either unsolvable, or error margins / fraction thresholds need to be relaxed slightly
    raise Exception("InputError: no good integer match found for these decimal values," +
            "with fraction threshold at " + str(MAX_FRAC_CHECK) + " and error margin at " + str(ERRORMARGIN))
    return None, None, None


cycle = 'CONT'
while not cycle == 'DONE':

    moleculeMass, co2_mass, h2o_mass, molarMassVal, params = take_input()
    ERRORMARGIN = 0.2  # this represents the error margin with which to consider a float what should be an integer
    MAX_FRAC_CHECK = 10  # if this value is c, that means the smallest fraction that floats will be checked for is "1/c"
    if params[0] != "NO":
        ERRORMARGIN, MAX_FRAC_CHECK = float(params[0]), float(params[1])
    print("current error margin: " + str(ERRORMARGIN) +
          ", current maximum fraction check denominator value: " + str(MAX_FRAC_CHECK))
    oValue = moleculeMass

    # do percent mass computations: find masses of carbon and hydrogen
    cmass = (3 * co2_mass) / 11  # 3/11 is constant mass percent of carbon in CO2
    print("c % mass: " + str(cmass))
    hmass = (h2o_mass) / 9  # 1/9 is constant mass percent of hydrogen in H20
    print("h % mass: " + str(hmass))

    # find oxygen mass if present (from molecule – overall does not work due to O2 reactant in combustion)
    if oValue != "NO":
        omass = float(moleculeMass) - cmass - hmass
        print("o mass: " + str(omass))

    cmoles = cmass / CMOLARMASS
    print("moles of C: " + str(cmoles))

    hmoles = hmass / HMOLARMASS
    print("moles of H: " + str(hmoles))

    if oValue != "NO":
        omoles = omass / OMOLARMASS
        print("moles of O: " + str(omoles))

    minMoleVal = min(cmoles, hmoles)
    if oValue != "NO":
        minMoleVal = min(minMoleVal, omoles)
    cval = (cmoles / minMoleVal)  #calculates the count for C in empirical formula, via div + round
    hval = (hmoles / minMoleVal)  #calculates the count for H in empirical formula, via div + round
    if oValue != "NO":
        oval = (omoles / minMoleVal)  #calculates the count for O in empirical formula, via div + round
        #print("TEST (goal: error margin parameter tweaking necessary?) :" + str(cval), str(hval), str(oval))
        if (abs(int(cval+0.5) - cval) < ERRORMARGIN
            and abs(int(hval+0.5) - hval) < ERRORMARGIN
            and abs(int(oval+0.5) - oval) < ERRORMARGIN):
            cval, hval, oval = int(cval+0.5), int(hval+0.5), int(oval+0.5)
        else:
            cval, hval, oval = find_empirical_value(cval, hval, oval)
    else:
        if abs(int(cval+0.5) - cval) < ERRORMARGIN and abs(int(hval+0.5) - hval) < ERRORMARGIN:
            cval, hval = int(cval+0.5), int(hval+0.5)
        else:
            cval, hval = find_empirical_value(cval, hval, 0)[:2]

    if oValue != "NO":
        print("empirical formula: " + 'C' + str(cval) + 'H' + str(hval) + 'O' + str(oval))
    else:
        print("empirical formula: " + 'C' + str(cval) + 'H' + str(hval))

    if molarMassVal != "NO":
        # note that with fully precise floats, could do moleculeMass / minMoleVal to get EF molar mass
        empiricalMolarMass = CMOLARMASS*cval + HMOLARMASS*hval
        if oValue != "NO":
            empiricalMolarMass += OMOLARMASS*oval
        print("molar mass of empirical formula:" + str(empiricalMolarMass))
        scale = int(float(molarMassVal)/empiricalMolarMass)
        if oValue != "NO":
            print("molecular formula: " + 'C' + str(cval*scale) + 'H' + str(hval*scale) + 'O' + str(oval*scale))
        else:
            print("empirical formula: " + 'C' + str(cval*scale) + 'H' + str(hval*scale))

    cycle = input("type CONT to do another combustion reaction, type DONE to stop")