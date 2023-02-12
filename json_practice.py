# -*- coding: utf-8 -*-
import socket
import sys
import ipaddress



from flask import *
from flask_cors import CORS

# 正引き
def foward_lookup(domain):
	try:
		return socket.gethostbyname(domain)
	except:
		return False

# 逆引き
def reverse_lookup(ip):
	try:
		#pythonは型が明記されていないからデバックモードで型を確認する。printじゃ型違っても表記同じ。
		ip = str(ip)
		print(ip)
		return socket.gethostbyaddr(ip)[0]
	except:
		return False


app = Flask(__name__)

CORS(
    app,
    supports_credentials=True
)


@app.route("/")
def index():

    req = request.args
    #user_id = req.get("ipaddress")
    #//
    network_string =req.get("ipaddress")+"/"+req.get("netmask")
    network = ipaddress.ip_network(network_string)


    ResultIpaddress = list(network.hosts())
    ResultIpAddressAfterConvert = []

    #各リストの要素をstrにする。
    for list_line in ResultIpaddress:
        ResultIpAddressAfterConvert.append(str(list_line))
    #print(list(ResultIpAddressAfterConvert))
    #ResultIpaddress = ["a","b","c"]
    #ipv4っていう型だから、変な文字列がついていた
    #**********ホストアドレス**************
    MyHostAddress = str(network.broadcast_address)

    #*********ネットワークアドレス***********
    MyNetworkAddress = str(network.network_address)
    return_api = {"ipaddress":ResultIpAddressAfterConvert,"hostaddress":MyHostAddress,"networkaddress":MyNetworkAddress}
    
    return jsonify(return_api)

if __name__ == "__main__":
    app.run(port=8888)