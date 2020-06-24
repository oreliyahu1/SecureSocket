from ICrypto.ICryptoMessage import ICryptoMessage
from typing import List


class CryptoMessage(ICryptoMessage[List[chr], List[int]]):

    def __init__(self, crp_msg: List[chr], msg_signature: List[int] = None):
        self.c_msg = dict()
        self.c_msg['message'] = crp_msg
        if msg_signature is not None:
            self.c_msg['signature'] = msg_signature

    def get_dict_message(self) -> dict:
        return self.c_msg

    def get_message(self) -> List[chr]:
        return list(self.c_msg.get('message'))
    
    def get_signature(self) -> List[int]:
        return self.c_msg.get('signature')
