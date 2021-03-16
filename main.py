from datetime import *
from hashlib import sha256

class Transaction:
    def __init__(self, fromAddress, toAddress, amount):
        self.fromAddress = fromAddress
        self.toAddress = toAddress
        self.amount = amount

class Block:
    def __init__(self, transactions, previousHash):
        self.nonce = 0
        self.conception =  datetime.now()
        self.transactions = transactions
        self.previousHash = previousHash
        self.hash = self.calculateHash()

    def calculateHash(self):
        text = ""
        for transaction in self.transactions:
            text += transaction.fromAddress + transaction.toAddress + str(transaction.amount)
        return sha256( ( str(self.nonce) + str(self.conception) + text + self.previousHash ).encode() ).hexdigest()
    
    def mineBlock(self, difficulty):
        print("\nMining block...")
        while (self.hash[:difficulty] != (difficulty * "0") ):
            self.conception = datetime.now()
            self.nonce += 1
            self.hash = self.calculateHash()

        print("\nBlock mined successfully!")
        print("HASH:", self.hash)
        print("")

    def printBlock(self):
        print("conception:", str(self.conception))
        print("hash:", self.hash)
        print("previousHash:", self.previousHash)
        print("nonce:", self.nonce)
        print("----- TRANSACTIONS -----")
        for transaction in self.transactions:
            print("From:", transaction.fromAddress, "   ", "To:", transaction.toAddress, "   ", "Amount:", transaction.amount)
        print()

class Blockchain:
    def __init__(self):
        self.chain = [self.__mineGenesisBlock()]
        self.pendingTransactions = []
        self.difficulty = 5
        self.miningReward = 50

    def __mineGenesisBlock(self):
        print("\nMining genesis block...")
        print("\nGenesis block mined successfully!")
        return Block([], "")

    def checkTransactions(self, block):
        
        toBeRemoved = []

        for transaction in block.transactions:
            fromAddress = transaction.fromAddress
            balance = self.getBalanceOfAddress(fromAddress)
            if balance < transaction.amount:

                toBeRemoved.append(transaction)

        for transaction in toBeRemoved:
            block.transactions.remove(transaction)

        return block

    def minePendingTransactions(self, minerAddress):
        newBlock = Block(self.pendingTransactions, self.chain[-1].hash)
        newBlock = self.checkTransactions(newBlock)
        newBlock.transactions.append(Transaction("Satoshi", minerAddress, self.miningReward))
        newBlock.mineBlock(self.difficulty)
        self.chain.append(newBlock)
        self.pendingTransactions = []

    def createTransaction(self, transaction):
        self.pendingTransactions.append(transaction)

    def getBalanceOfAddress(self, address):
        balance = 0
        for block in self.chain:
            for transaction in block.transactions:
                if transaction.toAddress == address:
                    balance += transaction.amount
                if transaction.fromAddress == address:
                    balance -= transaction.amount
        
        return balance

    def isChainValid(self):
        for i in range(1, len(self.chain)):
            currentBlock = self.chain[i]
            previousBlock = self.chain[i-1]

            if currentBlock.hash != currentBlock.calculateHash():
                return False

            if currentBlock.previousHash != previousBlock.hash:
                return False

        return True

    def printBlockchain(self):
        for block in self.chain:
            block.printBlock()

bitcoin = Blockchain()

bitcoin.createTransaction(Transaction("genesis", "exodus", 50))
bitcoin.createTransaction(Transaction("exodus", "leviticus", 50))
bitcoin.createTransaction(Transaction("leviticus", "genesis", 50))

bitcoin.minePendingTransactions("john")

bitcoin.createTransaction(Transaction("genesis", "exodus", 50))
bitcoin.createTransaction(Transaction("john", "genesis", 50))

bitcoin.minePendingTransactions("paul")

bitcoin.printBlockchain()

print("genesis:", bitcoin.getBalanceOfAddress("genesis"))
print("exodus", bitcoin.getBalanceOfAddress("exodus"))
print("leviticus", bitcoin.getBalanceOfAddress("leviticus"))

print(bitcoin.isChainValid())