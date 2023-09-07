
# Imports
import streamlit as st
from dataclasses import dataclass
from typing import Any, List
import datetime as datetime
import pandas as pd
import hashlib


# Create the data class Record to store transaction data
@dataclass
class Record:
    """
    Class to define the Record information and type
    The Record will be included in the Block information
    """
    sender: str
    receiver: str
    amount: float


# Create the data class Block to store block data
@dataclass
class Block:
    """
    Class to define the Block information and type
    """
    record: Record
    creator_id: int
    prev_hash: str = "0"
    timestamp: str = datetime.datetime.utcnow().strftime("%H:%M:%S")
    nonce: int = 0

    # Create the hashing method hash_block() to encrypt the Block data
    def hash_block(self):
        """
        Method to hash the Block information
        """
        sha = hashlib.sha256()

        record = str(self.record).encode()
        sha.update(record)

        creator_id = str(self.creator_id).encode()
        sha.update(creator_id)

        timestamp = str(self.timestamp).encode()
        sha.update(timestamp)

        prev_hash = str(self.prev_hash).encode()
        sha.update(prev_hash)

        nonce = str(self.nonce).encode()
        sha.update(nonce)

        return sha.hexdigest()


# Create the data class PyChain to create the blockchain links
@dataclass
class PyChain:
    """
    Class to define the proof of work, validate the transaction,
    and link the block to the chain
    """
    chain: List[Block]
    difficulty: int = 4

    # Create the method proof_of_work() to prove the mining of the hash
    def proof_of_work(self, block):

        calculated_hash = block.hash_block()

        num_of_zeros = "0" * self.difficulty

        while not calculated_hash.startswith(num_of_zeros):

            block.nonce += 1

            calculated_hash = block.hash_block()

        print("Wining Hash", calculated_hash)
        return block

    # Create the method add_block() to link a block to the chain after validation
    def add_block(self, candidate_block):
        block = self.proof_of_work(candidate_block)
        self.chain += [block]

    # Create the method is_valid() to validate a mined hash and link the block
    def is_valid(self):
        block_hash = self.chain[0].hash_block()

        for block in self.chain[1:]:
            if block_hash != block.prev_hash:
                print("Blockchain is invalid!")
                return False

            block_hash = block.hash_block()

        print("Blockchain is Valid")
        return True

# Streamlit Code

# Adds the cache decorator for Streamlit
@st.cache(allow_output_mutation=True)
def setup():
    print("Initializing Chain")
    return PyChain([Block("Genesis", 0)])


st.markdown("# PyChain")
st.markdown("## Store a Transaction Record in the PyChain")

pychain = setup()

# Get a value for `sender` from the user.
Record.sender = st.text_input("Add Sender", placeholder="Enter A Valid PyChain Wallet Address")

# Get a value for `receiver` from the user.
Record.receiver = st.text_input("Add Receiver", placeholder="Enter A Valid PyChain Wallet Address")

# Get a value for `amount` from the user.
Record.amount = st.text_input("Add Amount", placeholder="Enter The Amount That Was Transfered")

# Write new block to the blockchain
if st.button("Add Block"):
    prev_block = pychain.chain[-1]
    prev_block_hash = prev_block.hash_block()

    new_block = Block(
        record=Record,
        creator_id=42,
        prev_hash=prev_block_hash
    )

    pychain.add_block(new_block)
    st.balloons()

# Display the Blockchain Ledger
st.markdown("## The PyChain Ledger")
pychain_df = pd.DataFrame(pychain.chain).astype(str)
st.write(pychain_df)

# Changes level for `difficulty` data attribute of the `PyChain` data class (`pychain.difficulty`) with this new `difficulty` value
pychain.difficulty = st.sidebar.slider("Block Difficulty", 1, 5, 2)

st.sidebar.write("# Block Inspector")
selected_block = st.sidebar.selectbox(
    "Which block would you like to see?", pychain.chain
)

st.sidebar.write(selected_block)

if st.button("Validate Chain"):
    st.write(pychain.is_valid())