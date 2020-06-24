from Crypto.CryptoMessage import CryptoMessage
from ICrypto.ICryptoMessageGenerator import ICryptoMessageGenerator
from ICrypto.ICryptoMessage import ICryptoMessage
from ICrypto.ICrypto import ICrypto
from ICrypto.ISignature import ISignature


class AppMessageGenerator(ICryptoMessageGenerator):

    def __init__(self, crp: ICrypto, private_sig: ISignature, public_sig: ISignature = None):
        self.crp = crp
        self.private_sig = private_sig
        self.public_sig = public_sig
        if self.public_sig is None:
            self.public_sig = self.private_sig

    def generate_message(self, pain_text: str) -> ICryptoMessage:
        cipher_text = self.crp.encryption(pain_text)
        signature = self.private_sig.get_signature(' '.join(cipher_text))
        return CryptoMessage(cipher_text, signature)

    def degenerate_message(self, c_msg: ICryptoMessage) -> str:
        if c_msg.get_signature() is None:
            raise ValueError('AppMessageGenerator_degenerate_message: c_msg.signature None value')

        if self.public_sig.verification(self.public_sig.get_verification(c_msg.get_signature(), ' '.join(c_msg.get_message()))):
            return self.crp.decryption(c_msg.get_message())

        raise ValueError('AppMessageGenerator_degenerate_message: sender verification failed')

    def get_crypto(self) -> ICrypto:
        return self.crp

    def set_crypto(self, crp: ICrypto):
        self.crp = crp

    def set_private_signature(self, private_sig: ISignature):
        self.private_sig = private_sig

    def set_public_signature(self, public_sig: ISignature):
        self.public_sig = public_sig
        if self.public_sig is None:
            self.public_sig = self.private_sig

    def get_private_signature(self) -> ISignature:
        return self.private_sig

    def get_public_signature(self) -> ISignature:
        return self.public_sig
