
import time, datetime
import secrets
import os, sys



current_dir = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory by going one level up
parent_dir = os.path.dirname(current_dir)
# Add the parent directory to sys.path
sys.path.append(parent_dir)

import sha256


def calculate_file_hash(file_path):
    with open(file_path, 'rb') as file:
        file_contents = file.read()
        return sha256.generate_hash(file_contents).hex()

class NFT:
    def __init__(self, token_id, metadata, author, owner,file_hash):
        self.token_id = token_id
        self.metadata = metadata
        self.author = author
        self.owner = owner
        self.file_hash = file_hash  # Stockage du hash du fichier
        self.transaction_history = []
    
    def add_transaction(self, sender, receiver, author, prev_block_hash):
        transaction_data = f"{self.token_id}{self.author}{self.owner}{sender}{receiver}{prev_block_hash}{self.file_hash}"
        transaction_hash = sha256.generate_hash(transaction_data).hex()
        self.transaction_history.append({
            "sender": sender,
            "receiver": receiver,
            "author": author,
            "prev_block_hash": prev_block_hash,
            "file_hash": self.file_hash,
            "hash": transaction_hash,
            "title": self.metadata
        })
    
class Block:
    def __init__(self, index, timestamp, transactions, previous_hash,difficulty):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash 
        self.difficulty = difficulty
        self.nonce = 0
        self.salt = secrets.token_hex(16)  # Génération du Random Salt
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_data = f"{self.index}{self.timestamp}{str(self.transactions)}{self.previous_hash}{self.nonce}{self.salt}"

        return sha256.generate_hash(block_data).hex()
    
    def mine_block(self):
        while self.hash[:self.difficulty] != "0" * self.difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.token_registry = {}  # Initialisation du registre des tokens dans la blockchain
        self.difficulty = 2  # Difficulté de la preuve de travail


    def create_genesis_block(self):
        genesis_block = Block(0, time.time(), [], "0", 2)  # Difficulté initiale à 2
        genesis_block.mine_block()  # Miner le bloc pour atteindre la difficulté souhaitée
        return genesis_block

    def create_token(self, token_id, metadata, author, owner, file_hash):
        if token_id not in self.token_registry:
            new_token = NFT(token_id, metadata, author, owner, file_hash)
            #new_token.file_hash = file_hash  # Ajouter le hachage du fichier au NFT
            self.token_registry[token_id] = new_token

            return new_token
        else:
            print("Ce token ID existe déjà.")
            return None

    def transfer_token(self, token_id, new_owner, author):
        if token_id in self.token_registry:
            token = self.token_registry[token_id]

            if token.owner == new_owner:
                print(f"Le propriétaire actuel est déjà {new_owner}.")
            else:
                previous_owner = token.owner
                token.owner = new_owner
                prev_block_hash = self.get_latest_block().hash  # Récupération du hash du bloc précédent
                token.add_transaction(previous_owner, new_owner, author, prev_block_hash)

                print(f"Token {token_id} de {previous_owner} avec autheur {author} transféré à {new_owner} avec hash du doc {token.file_hash}")
                # Convertir le timestamp en objet datetime
                date_time = datetime.datetime.fromtimestamp(time.time())

                # Formater la date et l'heure
                formatted_date_time = date_time.strftime('%d-%m-%Y %H:%M:%S')

                self.add_block(Block(len(self.chain), formatted_date_time, token.transaction_history, self.get_latest_block().hash, self.difficulty))
        else:
            print("Ce token ID n'existe pas.")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.mine_block()
        new_block.hash = new_block.calculate_hash()
        print(f"Le bloc a été miné. Hash du bloc: {new_block.hash}")

        self.chain.append(new_block)

    def validate_blockchain(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return "NON"

            if current_block.previous_hash != previous_block.hash:
                return "NON"

        return "OUI"



# Création d'une instance de la blockchain
def main():

    my_blockchain = Blockchain()

    # acces aux fichier
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file1_path = os.path.join(current_directory, 'file1.pdf')
    file2_path = os.path.join(current_directory, 'file2.pdf')
    file3_path = os.path.join(current_directory, 'file3.pdf')

    ## hashage des files
    file1_hash = calculate_file_hash(file1_path)
    file2_hash = calculate_file_hash(file2_path)
    file3_hash = calculate_file_hash(file3_path)

    # Création de quelques tokens NFT et ajout à la blockchain
    my_blockchain.create_token(1, "Serpent algorithm pdf format",'Lamine', "Lamine",file1_hash)
    my_blockchain.create_token(2, "double ratchet spec.. pdf format","signal", "signal", file2_hash)
    my_blockchain.create_token(3, "double ratchet spec.. pdf format","signal", "signal", file3_hash)

    # Transfert de propriété d'un token et ajout du bloc à la blockchain
    my_blockchain.transfer_token(2, new_owner="Charlie", author='signal')
    my_blockchain.transfer_token(1, new_owner="remi", author='lamine')
    my_blockchain.transfer_token(3, new_owner="utt", author='gs15')


    # Validation de la blockchain
    print("La blockchain est-elle valide ? ", my_blockchain.validate_blockchain())

    # Affichage des blocs de la blockchain
    for block in my_blockchain.chain:
        print(f"Block #{block.index} - Hash: {block.hash} Timestamp: {block.timestamp}")
        print("Transactions:")
        for transaction in block.transactions:
            print(f"   Transaction Hash: {transaction['hash']} - Sender: {transaction['sender']} - Receiver: {transaction['receiver']} - Author: {transaction['author']} - Title: {transaction['title']} - Previous Block Hash: {transaction['prev_block_hash']} - file hash: {transaction['file_hash']}")
        print("\n")

if __name__ == "__main__":
    main()
