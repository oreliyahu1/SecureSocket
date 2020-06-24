import sys
import os
import argparse
import ipaddress
import _thread
import math
import socket
import json

from SecureSocket.ISecureSocket import ISecureSocket
from SecureSocket.SecureServer import SecureServer
from SecureSocket.SecureClient import SecureClient

from Crypto.CryptoMaker import CryptoMaker

cmd_options: argparse.ArgumentParser

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# utility functions
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


def get_crypto_settings() -> (str, str, str, str):
    crypto, block_mode, digital_signature, key_exchange = None, None, None, None
    if cmd_options.settings.get('crypto'):
        crypto = cmd_options.settings['crypto']['type']
    if cmd_options.settings.get('block_mode'):
        block_mode = cmd_options.settings['block_mode']['type']
    if cmd_options.settings.get('digital_signature'):
        digital_signature = cmd_options.settings['digital_signature']['type']
    if cmd_options.settings.get('key_exchange'):
        key_exchange = cmd_options.settings['key_exchange']['type']
    return crypto, block_mode, digital_signature, key_exchange


def get_app_crypto_settings() -> (str, str, str, str):
    crypto_settings, block_mode_settings, digital_signature_settings, key_exchange_settings = None, None, None, None
    crypto, block_mode, digital_signature, key_exchange = get_crypto_settings()
    if crypto:
        crypto_settings = cmd_options.settings[crypto]
    if block_mode:
        block_mode_settings = cmd_options.settings[block_mode]
    if digital_signature:
        digital_signature_settings = cmd_options.settings[digital_signature]
    if key_exchange:
        key_exchange_settings = cmd_options.settings[key_exchange]
    return crypto_settings, block_mode_settings, digital_signature_settings, key_exchange_settings


def print_settings():
    crypto, block_mode, digital_signature, key_exchange = get_crypto_settings()
    crypto_settings, block_mode_settings, digital_signature_settings, key_exchange_settings = get_app_crypto_settings()
    print('_________________________________________________________')
    print('settings')
    if crypto:
        print('crypto:', crypto)
        for key, value in crypto_settings.items():
            print(key, ': ', value)
        print('')

    if block_mode:
        print('block cipher mode:', block_mode)
        for key, value in block_mode_settings.items():
            print(key, ': ', value)
        print('')

    if digital_signature:
        print('digital signature:', digital_signature)
        for key, value in digital_signature_settings.items():
            print(key, ': ', value)
        print('')

    if key_exchange:
        print('key exchange:', key_exchange)
        for key, value in key_exchange_settings.items():
            print(key, ': ', value)
        print('')
    print('_________________________________________________________')
    print('')


def cmd_parser():
    global cmd_options

    parser = argparse.ArgumentParser()
    parser.add_argument('-server', help='run as server mode',
                        action='store_true', default=False)
    parser.add_argument('-client', help='run as server mode',
                        action='store_true', default=False)
    parser.add_argument('-ip', help='ip address',
                        default='127.0.0.1')
    parser.add_argument('-port', help='connection port (range 0-65535)', type=int,
                        default=8080)
    parser.add_argument('-max_buffer', help='max buffer receive (power of 2)', type=int,
                        default=4096)
    parser.add_argument('-settings', help='settings file', type=str,
                        default="{}\\{}".format(os.path.abspath(os.path.dirname(sys.argv[0])), "crypto_settings.json"))
    cmd_options = parser.parse_args()

    if (cmd_options.server and cmd_options.client) or (not cmd_options.server and not cmd_options.client):
        raise Exception('You need to select one mode - server / client')

    try:
        ipaddress.ip_address(cmd_options.ip)
    except ValueError:
        raise Exception('Please enter a valid ip address')

    if not 0 <= cmd_options.port <= 65535:
        raise Exception('Please enter a valid port')

    if not 1 <= cmd_options.max_buffer <= math.pow(2, 20) or not math.log(int(cmd_options.max_buffer), 2).is_integer():
        raise Exception('Please enter a max buffer size (power of 2)')

    if cmd_options.server:
        if os.path.exists(cmd_options.settings):
            with open(cmd_options.settings) as crypto_settings:
                cmd_options.settings = json.load(crypto_settings)
        else:
            raise Exception('Cannot find settings file')
    else:
        cmd_options.server = None


def main():
    cmd_parser()
    cs_socket: ISecureSocket

    if cmd_options.server:
        cs_socket = SecureServer(cmd_options.settings, CryptoMaker(), cmd_options.ip, cmd_options.port, cmd_options.max_buffer)
        print_settings()
    else:
        cs_socket = SecureClient(CryptoMaker(), cmd_options.ip, cmd_options.port, cmd_options.max_buffer)

    print('Starting connection')
    cs_socket.secure_start()

    if cmd_options.server:
        handle_server(cs_socket)
    elif cmd_options.client:
        handle_client(cs_socket)


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# client functions
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


def recv_msg_client(client: SecureClient):
    try:
        while True:
            recv_message = client.secure_recv()
            for msg in recv_message:
                try:
                    print('new message from {}: {}'.format(client.socket.getpeername(), msg))
                except ValueError as ve:
                    print('recv_msg error: ', ve)
    except ConnectionResetError as ce:
        client.close()
        print('recv_msg error: ', ce)


def handle_client(client: SecureClient):
    print('Connection successful')
    try:
        _thread.start_new_thread(recv_msg_client, (client,))
        while True:
            try:
                u_msg = input("Message: ")
                if len(u_msg):
                    client.secure_send(u_msg)
            except ValueError as ve:
                print('handle_client error: ', ve)
    except ConnectionResetError as ce:
        client.close()
        print('handle_client error: ', ce)


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# server functions
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


def handle_server(server: SecureServer):
    print('Waiting for new clients')
    while True:
        (client_socket, ip_address) = server.secure_get_new_connection()
        print('New connection {0}'.format(ip_address))
        _thread.start_new_thread(client_thread, (server, client_socket,))


def recv_msg_server(server: SecureServer, client_socket):
    try:
        while True:
            recv_message = server.secure_recv_from_socket(client_socket)
            for msg in recv_message:
                try:
                    print('new message from {}: {}'.format(client_socket.getpeername(), msg))
                except ValueError as ve:
                    print('recv_msg_server error: ', ve)
    except ConnectionResetError as ce:
        client_socket.close()
        print('recv_msg_server error: ', ce)


def client_thread(server: ISecureSocket, client_socket: socket.socket):
    try:
        _thread.start_new_thread(recv_msg_server, (server, client_socket,))
        while True:
            try:
                u_msg = input("Message: ")
                if len(u_msg):
                    server.secure_send_to_socket(client_socket, u_msg)
            except ValueError as ve:
                print('handle_client error: ', ve)
    except ConnectionResetError as ce:
        client_socket.close()
        print('client_thread error: ', ce)


if __name__ == "__main__":
    #try:
    main()
    #except Exception as e:
    #    print('CryptoApp Error:', e)
