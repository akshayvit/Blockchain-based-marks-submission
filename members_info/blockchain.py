import datetime,hashlib,json

class Blockchain:
    def __init__(self,data):
        self.chain=[]
        self.data=data
        self.create_block(proof=1,previous_hash='0')
    def create_block(self,proof,previous_hash):
        block={'index':len(self.chain)+1,'data':self.data,'timestamp':str(datetime.datetime.now()),'proof':proof,'previous_hash':previous_hash}
        self.chain.append(block)
        return block
    def get_previous_block(self):
        return self.chain[-1]
    def proof_of_work(self,previous_proof):
        check_proof=False
        new_proof=1
        while not check_proof:
            hash_oper=hashlib.sha256(str(new_proof**2-previous_proof**2).encode()).hexdigest()
            if(hash_oper[:4]=='0000'):
                check_proof=True
            else:
                new_proof+=1
        return new_proof
    def hash(self,block):
        encoded_block=json.dumps(block,sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    def is_chain_valid(self,chain):
        previous_block=chain[0]
        curr_block=1
        while curr_block < len(chain) :
            if chain[curr_block]['previous_hash']!=self.hash(previous_block):
                return False
            previous_proof=previous_block['proof']
            proof=chain[curr_block]['proof']
            has_oper=hashlib.sha256(str(proof**2-previous_proof**2).encode()).hexdigest()
            if(has_oper[:4]=='0000'):
                return False
            previous_block=curr_block
            curr_block+=1
        return True
        
