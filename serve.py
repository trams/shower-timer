#!/usr/bin/env python3
"""
HTTPS dev server for shower timer.
Wake Lock and Service Workers require a secure context (HTTPS or localhost).
Run: python3 serve.py
Then open https://<LAN-IP>:8443 on Android and accept the self-signed cert warning.
"""
import http.server
import ssl
import socket
import os
import subprocess
import sys

PORT = 8443
CERT = 'cert.pem'
KEY  = 'key.pem'
ROOT = os.path.dirname(os.path.abspath(__file__))

def local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        return s.getsockname()[0]
    except Exception:
        return '127.0.0.1'
    finally:
        s.close()

def ensure_cert():
    if os.path.exists(CERT) and os.path.exists(KEY):
        return
    print('Generating self-signed certificate...')
    subprocess.check_call([
        'openssl', 'req', '-x509', '-newkey', 'rsa:2048',
        '-keyout', KEY, '-out', CERT,
        '-days', '365', '-nodes',
        '-subj', '/CN=localhost',
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print('Done.')

def main():
    os.chdir(ROOT)
    ensure_cert()

    handler = http.server.SimpleHTTPRequestHandler
    handler.extensions_map = {
        **handler.extensions_map,
        '.json': 'application/json',
        '.js':   'application/javascript',
        '.png':  'image/png',
        '':      'application/octet-stream',
    }

    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain(CERT, KEY)

    with http.server.HTTPServer(('0.0.0.0', PORT), handler) as httpd:
        httpd.socket = ctx.wrap_socket(httpd.socket, server_side=True)
        ip = local_ip()
        print(f'\nShower Timer — HTTPS server running')
        print(f'  Local:   https://localhost:{PORT}')
        print(f'  Network: https://{ip}:{PORT}')
        print('\nOn Android: open the Network URL, tap "Advanced > Proceed" to accept the cert.')
        print('Press Ctrl+C to stop.\n')
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print('\nStopped.')

if __name__ == '__main__':
    main()
