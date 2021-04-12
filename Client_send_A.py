import sys
from socket import *

# Global Variables
transactionFee = 2
accountA1Balance = 1000
accountA2Balance = 1000
clientMenuDispatcher = {}  # used to invoke functions
serverName = "localhost"
serverPort = 10000
clientSocket = socket(AF_INET, SOCK_DGRAM)



def doesAmountExceedBalance(account, amount):
    # Still need to implement reading from unconfirmed_balance_tx.txt instead of
    # having balance amount be hardcoded
    if account == "A0000001":
        if amount + transactionFee > accountA1Balance:
            return True
        else:
            return False
    else:
        if amount + transactionFee > accountA2Balance:
            return True
        else:
            return False


def clientMenu():
    print("Client Menu")
    print("1. Enter a new transcation.")
    print("2. Current Account(s) balance.")
    print("3. View unconfirmed transactions.")
    print("4. View last X amount of confirmed transactions.")
    print("5. Print the blockchain.")
    print("6. Exit")
    validSelection = range(1, 7)
    userSelection = int(input())
    if userSelection not in validSelection:
        print("Invalid selection please try again\n\n")
        clientMenu()

    functionIndex = str(userSelection)
    clientMenuDispatcher[functionIndex]()

    # End of program #
    clientSocket.close()


def creditAccount(account, amount):
    global accountA1Balance
    global accountA2Balance
    if account == "A0000001":
        accountA1Balance -= amount
    if account == "A0000002":
        accountA2Balance -= amount


def newTransaction():
    accountTo = ""
    accountFrom = ""
    print("Select account to pay from")
    print("1. Account A0000001")
    print("2. Account A0000002")
    userInput = int(input())
    if userInput == 1:
        accountFrom = "A0000001"
    if userInput == 2:
        accountFrom = "A0000002"

    print("Select account to pay to")
    print("1. Account B0000001")
    print("2. Account B0000002")
    userInput = int(input())

    if userInput == 1:
        accountTo = "B0000001"
    if userInput == 2:
        accountTo = "B0000002"

    amountInDecimal = int(input("Please enter amount to pay: "))

    # make sure amount they are attempting to pay with, does not exceed their account balance
    amountExceeded = doesAmountExceedBalance(accountFrom, amountInDecimal)
    if amountExceeded:
        print("\n\n\nAmount exceeds account balance, please try again.")
        newTransaction()

    # convert amount from decimal to hex and also convert hex number to 4 byte representation
    amountInHex = hex(amountInDecimal).split("x")[-1]
    numberOfZerosToPrepend = 8 - len(amountInHex)
    adjustedHex = ""

    for x in range(numberOfZerosToPrepend):
        adjustedHex += "0"

    adjustedHex += amountInHex
    messageToServer = accountFrom + ":" + accountTo + ":" + adjustedHex

    # reduce account by transaction amount
    creditAccount(accountFrom, amountInDecimal)
    print("Balance after credit: ", accountA1Balance)  # for account a1
    # writing to Unconfirmed_T.txt
    ledger = open("Unconfirmed_T.txt", "w")
    ledger.write(messageToServer)
    ledger.close()

    # sending message to server
    clientSocket.sendto(messageToServer.encode(), (serverName, serverPort))
    modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
    print(modifiedMessage.decode())

def viewBalance():
    print("\n\nviewBalance function")
    clientMenu()


def viewUnconfrimedTx():
    print("\n\nviewUnconfirmedTx function")
    clientMenu()


def viewLastXTxs():
    print("\n\nviewlastXTxs function")
    clientMenu()


def printBlockChain():
    print("\n\nprintBlockChain function")
    clientMenu()

def exitProgram():
    print("Exiting program...")
    sys.exit(0)

# initialize our dispatcher
clientMenuDispatcher = {
    "1": newTransaction,
    "2": viewBalance,
    "3": viewUnconfrimedTx,
    "4": viewLastXTxs,
    "5": printBlockChain,
    "6": exitProgram
}


while 1:
    clientMenu()
