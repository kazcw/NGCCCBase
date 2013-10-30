import Queue

import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from bitcoin.core import x, b2x, lx, b2lx, CTransaction
import bitcoin.base58

class UTXO(object):
    """represents an unspent transaction output"""
    def __init__(self, txhash, outindex, value, script):
        self.txhash = txhash
        self.outindex = outindex
        self.value = value
        self.script = script
        self.address_rec = None
        self.colorvalues = None
        self.utxo_rec = None

class Fetcher(object):
    def __init__(self, interface):
        self.interface = interface

    def get_for_address(self, address):
        req = ('blockchain.address.get_history', [address])
        history = self.interface.synchronous_get([ req ])[0]
        script_pubkey =  bitcoin.core.CBitcoinAddress(address).to_scriptPubKey()

        spent = {}
        utxos = []
        for entry in history:
            tx_hash = entry['tx_hash']
            tx_height = entry['height']
            req = ('blockchain.transaction.get', [tx_hash, tx_height])
            tx_hex = self.interface.synchronous_get([ req ])[0]
            tx_bin = bitcoin.core.x(tx_hex)
            tx = bitcoin.core.CTransaction.deserialize(tx_bin)
            for vin in tx.vin:
                spent[(bitcoin.core.b2lx(vin.prevout.hash), vin.prevout.n)] = 1
            for outindex, vout in enumerate(tx.vout):
                # FIXME: handle other transaction types
                if vout.scriptPubKey != script_pubkey:
                    continue
                utxos += [UTXO(tx_hash, outindex, vout.nValue, b2x(vout.scriptPubKey))]

        return [u for u in utxos if not (u.txhash, u.outindex) in spent]
