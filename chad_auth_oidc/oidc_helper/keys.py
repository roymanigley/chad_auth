import os
from pathlib import Path

from Crypto.PublicKey import RSA


class __Util(object):

    _private_key = None
    _public_key = None

    def init_keys(self, base_dir) -> None:
        self.path_keys = os.path.join(base_dir, 'keys')
        self.path_public_key = os.path.join(self.path_keys, 'rsa.pub')
        self.path_private_key = os.path.join(self.path_keys, 'rsa.priv')

        if Path(self.path_public_key).exists() and Path(self.path_private_key).exists():
            return

        if not Path(self.path_keys).exists():
            os.mkdir(self.path_keys)

        generated = RSA.generate(2046)
        with open(self.path_public_key, 'wb') as f:
            self._public_key = generated.public_key().export_key('DER')
            f.write(self._public_key)
        with open(self.path_private_key, 'wb') as f:
            self._private_key = generated.exportKey('DER')
            f.write(self._private_key)

    def load_public_key(self) -> bytes:
        if self._public_key is None:
            with open(self.path_public_key, 'rb') as f:
                self._public_key = f.read()
        return self._public_key

    def load_private_key(self) -> bytes:
        if self._private_key is None:
            with open(self.path_private_key, 'rb') as f:
                self._private_key = f.read()
        return self._private_key


Util = __Util()
