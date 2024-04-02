#!/usr/bin/python

"""A finance library for Python.

All interest rates are to be expressed in decimal notation
(i.e. 0.0825 instead of 8.25)

This library has been placed in the public domain.

Version history:

1.0 - 2001-01 - Initial program
                Rupert Scammell <rupe@sbcglobal.net>

2.0 - 2001-03 - Additions and revisions (compound interest present value,
                equivalent value of an annuity)
                Louis Luangkesorn <lluang@northwestern.edu>
                
2.1 - 2004-01 - Readability changes
                Matthew Scott <spud@goldenspud.com>

2.2 - 2004-01 - Minor name changes, addition of amortizationTable function
                Matthew Scott <spud@goldenspud.com>

2.3 - 2004-02 - Delay to first payment can be variable in amortization.
                Matthew Scott <spud@goldenspud.com>

2.4 - 2004-03 - Corrected algorithm in amortization where delay != 30.
                Use fixedpoint if available (highly recommended since it
                uses bankers' rounding, which is pretty much required if
                you are writing a financial app - See
                http://fixedpoint.sf.net/ for the fixedpoint module)
                Matthew Scott <spud@goldenspud.com>
"""


import sys
import math

try:
    import fixedpoint
    FIXEDPOINT = True
except:
    FIXEDPOINT = False
    

def amortization(loan, r, c, n, delay=30):
    """Amortization

    If delay is not equal to 30, assumes that a payment period of one
    month means exactly 30 days.

    Returns: The amount of money that needs to be paid at the end of
    each period to get rid of the total loan.

    Input values:
    loan : Total loan amount
    r : annual interest rate
    c : number of compounding periods a year
    n : total number of compounding periods
    delay : number of days until first payment is due
    """
    if loan == 0.0:
        return 0.0
    ipp = r / c
    amt = (loan * ipp) / (1 - ((1 + ipp) ** (-n)))
    if FIXEDPOINT:
        amt = float(fixedpoint.FixedPoint(fixedpoint.FixedPoint(amt, 3), 2))
    if delay != 30:
        # Brute-force calculate the correct payment amount.
        # First, determine the direction of adjustment.
        if delay > 30:
            adjustment = 0.01
        elif delay < 30:
            adjustment = -0.01
        # While the absolute value of the discrepancy on the last
        # payment continues to dwindle, keep calculating.
        amt = float('%.2f' % amt)
        smallestDiscrepancy = 10000.00
        closestAmt = amt
        continueCalculating = True
        while continueCalculating:
            amt = float('%.2f' % (amt + adjustment))
            # Amortize based on amount, then calculate discrepancy
            # of principal reduction on last payment.
            principal = loan
            interestPerPeriod = r / c
            firstPeriodFactor = (delay / 30.0)
            interestPerFirstPeriod = interestPerPeriod * firstPeriodFactor
            period = 1
            interestAmount = principal * interestPerFirstPeriod
            if FIXEDPOINT:
                interestAmount = float(fixedpoint.FixedPoint(
                    fixedpoint.FixedPoint(interestAmount, 3), 2))
            else:
                interestAmount = float('%.2f' % interestAmount)
            principalReduction = amt - interestAmount
            principal -= principalReduction
            while principal > 0.0:
                period += 1
                interestAmount = principal * interestPerPeriod
                if FIXEDPOINT:
                    interestAmount = float(fixedpoint.FixedPoint(
                        fixedpoint.FixedPoint(interestAmount, 3), 2))
                else:
                    interestAmount = float('%.2f' % interestAmount)
                principalReduction = amt - interestAmount
                newBalance = principal - principalReduction
                if period == n:
                    discrepancy = abs(newBalance)
                    if (delay > 30 and newBalance > 0.0) or \
                             (delay < 30 and newBalance < 0.0):
                        smallestDiscrepancy = discrepancy
                        closestAmt = amt
                    else:
                        # use amount with negative discrepancy closest to zero
                        if delay > 30:
                            smallestDiscrepancy = discrepancy
                            closestAmt = amt
                        continueCalculating = False
                principal = newBalance
        amt = closestAmt
    return amt


def amortizationTable(loan, r, c, n, delay=30):
    """Amortization table

    Returns: List of (interestAmount, principalReduction, newBalance)
    tuples detailing the amortization of a loan.  The principal
    reduction on the last payment is rounded off in order to cleanly
    bring the balance down to zero.

    Input values:
    loan : Total loan amount
    r : annual interest rate
    c : number of compounding periods a year
    n : total number of compounding periods
    delay : number of days until first payment is due
    """
    L = []
    payment = float('%.2f' % amortization(loan, r, c, n, delay))
    principal = loan
    interestPerPeriod = r / c
    if delay == 30:
        interestPerFirstPeriod = interestPerPeriod
    else:
        firstPeriodFactor = (delay / 30.0)
        interestPerFirstPeriod = interestPerPeriod * firstPeriodFactor
    period = 0
    while principal > 0.0:
        period += 1
        if period > 1:
            interestAmount = principal * interestPerPeriod
        else:
            interestAmount = principal * interestPerFirstPeriod
        interestAmount = float('%.2f' % interestAmount)
        principalReduction = payment - interestAmount
        newBalance = principal - principalReduction
        # Adjust values if this is the last payment.
        if period == n:
            if newBalance > 0.0:
                principalReduction += newBalance
            elif newBalance < 0.0:
                principalReduction -= newBalance
            newBalance = 0.0
        L.append((interestAmount, principalReduction, newBalance))
        principal = newBalance
    return L


def annualYield(r, c):
    """Annual yield
    
    Returns: Simple interest rate necessary to yield the same amount
    of dollars yielded by the annual rate r compounded c times for one
    year
    
    Input values:
    r : interest rate
    c : number of compounding periods in a year
    """
    y = ((1 + (r / c)) ** c) - 1
    return y


def annuityEquivalentAnnualCost(pval, r, c, n):
    """Equivalent value of an annuity

    Returns: Coupon amount for an annuity given the present value

    Input values:
    pval : present value of annuity
    r : annual interest rate
    c  : number of compounding periods in a year
    n  : total number of payments

    See 'Ordinary annuity formula' above.
    """
    ipp = r / c
    pymt = pval / ((1 - ((1 + ipp) ** (-n))) / ipp)
    return pymt


def annuityOrdinary(pymt, p, r, c, n):
    """Ordinary annuity formula
    
    Returns: future value
    
    Input values:
    pymt : payment made during compounding period
    p : principal
    r : annual interest rate
    c  : number of compounding periods in a year
    n  : total number of payments
    """
    block1 = ((1 + (r / c)) ** n) - 1
    block2 = r / c
    fv = pymt * (block1 / block2)
    return fv


def annuityPresentValue(pymt, r, c, n):
    """Present value of an annuity

    Returns: Lump sum that can be deposited at the beginning of the
    annuity's term, at the same interest rate and with the same
    compounding period, that would yield the same amount as the
    annuity.
   
    Input values:
    pymt : payment made during compounding period
    r : annual interest rate
    c  : number of compounding periods in a year
    n  : total number of payments
    """
    ipp = r / c
    pval = pymt * ((1 - ((1 + ipp) ** (-n))) / ipp)
    return pval


def compoundInterestFutureValue(p, r, c, n):
    """Compound interest future value
    
    Returns: future value
    
    Input values:
    p : principal
    r : interest rate
    c  : number of compounding periods in a year
    n  : (c * t) , total number of compounding periods
    """
    fv = (p * (1 + (r / c))) ** n
    return fv


def compoundInterestPresentValue(p, r, c, n):
    """Compound interest present value

    Returns: present value

    Input values:
    p : principal
    r : interest rate
    c  : number of compounding periods in a year
    n  : (c * t), total number of compounding periods
    """
    pv = (p / ((1 + (r / c)) ** n))
    return pv


def compoundedInterest(fv, p):
    """Compounded interest
    
    Returns: Interest value
    
    Input values:
    fv : Future value
    p  : Principal
    """
    i = fv - p
    return i


def simpleInterest(p, r, t):
    """Simple interest

    Returns: interest value

    Input values:
    p : principal
    r : Interest rate (decimal)
    t : Investment periods
    """
    i = p * r * t
    return i


def simpleInterestFutureValue(p, r, t):
    """Simple interest future value
    
    Returns:  future value
    
    Input values:
    p : principal
    r : Interest rate (decimal)
    t : Investment periods
    """
    fv = p * (1 + r * t)
    return fv