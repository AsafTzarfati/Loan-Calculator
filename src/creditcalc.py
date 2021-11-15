import sys
from math import ceil, log, pow
import argparse
YEAR = 12  # months
NUM_OF_ARGS = 5


def calc(loan_interest, periods):
    return loan_interest * pow(1 + loan_interest, periods) / (pow(1 + loan_interest, periods) - 1)


def months_to_years(months):
    years = res_periods // YEAR
    months = res_periods % YEAR
    return years, months


def diff_payment(principal_loan, periods, loan_interest):
    def diff_payment_calc(principal_loan, periods, loan_interest, m):
        return ceil((principal_loan/periods) + loan_interest * (principal_loan - (principal_loan * (m-1)) / periods))

    return [diff_payment_calc(principal_loan, periods, loan_interest, month) for month in range(1, periods + 1)]


parser = argparse.ArgumentParser(description='Loan Calculator')
parser.add_argument('--type', type=str, choices=["diff", "annuity"],
                    help='--type indicates the type of payment: "annuity" or "diff" (differentiated).')
parser.add_argument('--payment', type=int,
                    help="--payment is the monthly payment amount.")
parser.add_argument('--principal', type=int,
                    help="--principal is means to principal loan and used for calculations of both types of payment.")
parser.add_argument('--periods', type=int,
                    help="--periods denotes the number of months needed to repay the loan.")
parser.add_argument('--interest', type=float,
                    help="--interest is specified without a percent sign."
                         " Note that it can accept a floating-point value.")
args = parser.parse_args()
if len(sys.argv) == NUM_OF_ARGS and args.type is not None and args.interest is not None:
    loan_interest = (args.interest / YEAR) / 100
    if args.type == "annuity":
        """Calculation of the loan periods"""
        if args.periods is None:
            res_periods = ceil(log(args.payment / (args.payment - (loan_interest * args.principal)), loan_interest + 1))
            if res_periods <= YEAR:
                print("\nIt will take {periods} months to repay this loan!")
            else:
                years, months = months_to_years(res_periods)
                if months == 0:
                    print(f"\nIt will take {years} years to repay this loan!")
                else:
                    print(f"\nIt will take {years} years and {months} months to repay this loan!")
                print(f"\nOverpayment = {(args.payment * res_periods) - args.principal}")

            """Calculation of the loan principal"""
        elif args.principal is None and args.periods > 0:
            denominator = calc(loan_interest, args.periods)
            loan_principal = int(args.payment / denominator)
            print(f"Your loan principal = {loan_principal}!")
            print(f"\nOverpayment = {(args.payment * args.periods) - loan_principal}")

            """Calculation of the monthly payment"""
        elif args.payment is None and args.periods > 0:
            monthly_payment = ceil(args.principal * calc(loan_interest, args.periods))
            print(f"\nYour monthly payment = {monthly_payment}!")
            print(f"\nOverpayment = {(monthly_payment * args.periods) - args.principal}")
        else:
            print("Incorrect parameters")

    elif args.type == "diff":
        if args.payment is not None:
            print("Incorrect parameters")
        else:
            """Calculation of differentiated monthly payment"""
            payment_list = diff_payment(args.principal, args.periods, loan_interest)
            for month, payment in enumerate(payment_list, 1):
                print(f"Month {month}: payment is {payment}")
            print(f"\nOverpayment = {sum(payment_list) - args.principal}")
else:
    print("Incorrect parameters")
