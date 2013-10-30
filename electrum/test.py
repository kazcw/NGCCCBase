#!/usr/bin/python

import utxo
import interface

interface = interface.Interface(interface.pick_random_server())
interface.start(None, True)

fetcher = utxo.Fetcher(interface)
address = '3BTChqkFai51wFwrHSVdvSW9cPXifrJ7jC'
for utxo in fetcher.get_for_address(address):
    print(repr((address, utxo.txhash, utxo.outindex, utxo.value, utxo.script)))
