import abc
from ICrypto import ICryptoMessage, ICrypto, ISignature


class ICryptoMessageGenerator(object, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __init__(self, crp: ICrypto, private_sig: ISignature = None, public_sig: ISignature = None):
        raise NotImplementedError('ICryptoMessageGenerator: __init__ function is not defined')

    @abc.abstractmethod
    def generate_message(self, pain_text: str) -> ICryptoMessage:
        raise NotImplementedError('ICryptoMessageGenerator: generate_message function is not defined')

    @abc.abstractmethod
    def degenerate_message(self, c_msg: ICryptoMessage) -> str:
        raise NotImplementedError('ICryptoMessageGenerator: degenerate_message function is not defined')

    @abc.abstractmethod
    def get_crypto(self) -> ICrypto:
        raise NotImplementedError('ICryptoMessageGenerator: get_crypto function is not defined')

    @abc.abstractmethod
    def set_crypto(self, crp: ICrypto):
        raise NotImplementedError('ICryptoMessageGenerator: set_crypto function is not defined')

    def set_private_signature(self, private_sig: ISignature):
        raise NotImplementedError('ICryptoMessageGenerator: set_private_signature function is not defined')

    def set_public_signature(self, public_sig: ISignature):
        raise NotImplementedError('ICryptoMessageGenerator: set_public_signature function is not defined')

    def get_private_signature(self) -> ISignature:
        raise NotImplementedError('ICryptoMessageGenerator: get_private_signature function is not defined')

    def get_public_signature(self) -> ISignature:
        raise NotImplementedError('ICryptoMessageGenerator: get_public_signature function is not defined')