# EquityLoanLVRSim

Uses historical Index Prices (assuming ETF is a 1-1 relationship with index)
Runs a simulation based on the next 180 months of data, against various LVR ratios for the loan.
Breach occurs when loan is in negative equity (Loan Value > Equity Value).

Data sourced from MSCI World index from 1969, 
and Robert Shiller from 1946 http://www.econ.yale.edu/~shiller/data.htm

Loan Principal calculation function taken from https://pbpython.com/amortization-model-revised.html