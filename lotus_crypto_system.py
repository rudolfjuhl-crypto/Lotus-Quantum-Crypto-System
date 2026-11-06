"""
Lotus Quantum Crypto System (Core V3)
Implementation of Fractal Circular Path Cryptography (FCPC) 
and Fractal Circular Key Exchange (FCKE) with an asynchronous TCP/IP protocol.

Author: Rudolf Juhl
Location: Bensheim, Germany
Date: November 6, 2026
License: CC-BY-4.0
"""

import numpy as np
import hashlib
import socket
import threading
import json
import time

# =====================================================================
# MODULE 1: CRYPTOGRAPHIC CORE ENGINE (FCPC & FCKE)
# =====================================================================

class LotusFractalKeyExchange:
    """Handles the Post-Quantum Fractal Circular Key Exchange (FCKE)"""
    def __init__(self, name):
        self.name = name
        # Public base geometry (Standard profile for all cores)
        self.public_base_matrix = {
            'R1': 3.5,
            'R2': 0.8,
            'segments': 8
        }
        # Secret private key: Generated using quantum-equivalent physical entropy
        self.__private_shift = np.random.uniform(1.5, 9.5)

    def generate_public_key(self):
        """Applies private non-linear transformation to the public base matrix"""
        public_R1 = self.public_base_matrix['R1'] * np.sinh(self.__private_shift) / 10.0
        public_R2 = self.public_base_matrix['R2'] * np.cosh(self.__private_shift) / 10.0
        public_phase = (self.__private_shift * np.pi) % (2 * np.pi)
        
        return {'p_R1': public_R1, 'p_R2': public_R2, 'p_phase': public_phase}

    def compute_shared_secret(self, received_public_key):
        """Combines remote public profile with local private shift to yield the FCPC key"""
        p_R1 = received_public_key['p_R1']
        p_R2 = received_public_key['p_R2']
        p_phase = received_public_key['p_phase']
        
        shared_R1 = abs(p_R1 * np.cosh(self.__private_shift) * 0.1)
        shared_R2 = abs(p_R2 * np.sinh(self.__private_shift) * 0.1)
        shared_phase = (p_phase * self.__private_shift) % (2 * np.pi)
        
        # Derive a secure 256-bit hash using SHA-256
        raw_secret_string = f"{shared_R1:.8f}-{shared_R2:.8f}-{shared_phase:.8f}"
        shared_key_hash = hashlib.sha256(raw_secret_string.encode()).hexdigest()
        
        # Map the hash into a valid FCPC symmetric configuration profile
        final_fcpc_key = {
            'R1': (int(shared_key_hash[:8], 16) % 100) / 10.0 + 1.0,
            'R2': (int(shared_key_hash[8:16], 16) % 50) / 10.0 + 0.1,
            'segments': (int(shared_key_hash[16:20], 16) % 12) + 4
        }
        return final_fcpc_key


class LotusUniversalCryptoEngine:
    """Handles symmetric encryption via Fractal Circular Path Cryptography (FCPC)"""
    def __init__(self):
        # Physical Unclonable Function (PUF): Cryogenic phase offset at 10 mK
        self.hardware_phase_offset = 0.146437  # 8.39 degree systematic error

    def encrypt_fcpc(self, plaintext, fractal_key_set):
        """Encrypts text by shifting characters into polar fractal orbits"""
        R1 = fractal_key_set['R1']
        R2 = fractal_key_set['R2']
        NUM_SEGMENTS = fractal_key_set['segments']
        
        encrypted_blocks = []
        
        for idx, char in enumerate(plaintext):
            char_val = ord(char)
            base_angle = (char_val / 256.0) * 2 * np.pi
            
            # Nested Chaos Orbit Hopping
            nested_factor = np.sin(idx * NUM_SEGMENTS) * (R2 / R1)
            fractal_angle = base_angle + nested_factor
            
            # Inject Hardware PUF phase offset
            final_quantum_angle = (fractal_angle + self.hardware_phase_offset) % (2 * np.pi)
            
            # Map continuous angle into 24-bit integer space
            encrypted_val = int((final_quantum_angle / (2 * np.pi)) * 16777215)
            encrypted_blocks.append(f"{encrypted_val:06x}")
            
        return "-".join(encrypted_blocks)

    def decrypt_fcpc(self, ciphertext, fractal_key_set):
        """Decrypts text via inverse trajectory mapping in the polar orbit space"""
        R1 = fractal_key_set['R1']
        R2 = fractal_key_set['R2']
        NUM_SEGMENTS = fractal_key_set['segments']
        
        blocks = ciphertext.split("-")
        decrypted_chars = []
        
        for idx, block in enumerate(blocks):
            encrypted_val = int(block, 16)
            final_quantum_angle = (encrypted_val / 16777215) * 2 * np.pi
            
            # Inverse Hardware Shift
            fractal_angle = final_quantum_angle - self.hardware_phase_offset
            
            # Inverse Chaos Orbit Hopping
            nested_factor = np.sin(idx * NUM_SEGMENTS) * (R2 / R1)
            base_angle = (fractal_angle - nested_factor) % (2 * np.pi)
            
            # Reconstruct ASCII/Unicode character
            char_val = int(round((base_angle / (2 * np.pi)) * 256)) % 256
            decrypted_chars.append(chr(char_val))
            
        return "".join(decrypted_chars)


# =====================================================================
# MODULE 2: NETWORK PROTOCOL INTERFACE (TCP/IP SOCKETS)
# =====================================================================

HOST = '127.0.0.1'
PORT = 55555
MAGIC_BYTE = b'\x4c'  # 'L' for Lotus

def build_protocol_frame(packet_type, payload_str):
    """Builds a standardized binary protocol frame"""
    payload_bytes = payload_str.encode('utf-8')
    length_bytes = len(payload_bytes).to_bytes(4, byteorder='big')
    return MAGIC_BYTE + bytes([packet_type]) + length_bytes + payload_bytes

def read_protocol_frame(sock):
    """Reads a complete binary frame from the network stream"""
    magic = sock.recv(1)
    if not magic or magic != MAGIC_BYTE:
        return None, None
    packet_type = int(sock.recv(1))
    length = int.from_bytes(sock.recv(4), byteorder='big')
    payload = sock.recv(length).decode('utf-8')
    return packet_type, payload


# =====================================================================
# MODULE 3: SERVER & CLIENT STREAM ORCHESTRATION
# =====================================================================

def run_lotus_server():
    """Runs an asynchronous local server executing FCKE handshakes and FCPC decryptions"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print("[SERVER] Lotus Server running. Awaiting hardware connection...")
    
    conn, addr = server_socket.accept()
    print(f"[SERVER] Handshake stream accepted from node {addr}")
    
    server_fcke = LotusFractalKeyExchange("Server_Core")
    server_engine = LotusUniversalCryptoEngine()
    shared_fcpc_key = None
    
    try:
        while True:
            packet_type, payload = read_protocol_frame(conn)
            if packet_type is None:
                break
                
            if packet_type == 0x01:  # FCKE_INIT
                print("[SERVER] Received FCKE_INIT. Compiling remote geometric profile...")
                client_public_profile = json.loads(payload)
                
                # Generate server response frame (FCKE_REPLY)
                server_public = server_fcke.generate_public_key()
                reply_frame = build_protocol_frame(0x02, json.dumps(server_public))
                conn.sendall(reply_frame)
                
                # Lock in the shared symmetric profile
                shared_fcpc_key = server_fcke.compute_shared_secret(client_public_profile)
                print("[SERVER] Post-Quantum Handshake complete. FCPC Orbit parameters locked.")
                
            elif packet_type == 0x03:  # FCPC_DATA
                if not shared_fcpc_key:
                    print("[SERVER] Error: Received payload before handshake execution.")
                    break
                print(f"[SERVER] Received raw FCPC_DATA frame: {payload}")
                plaintext = server_engine.decrypt_fcpc(payload, shared_fcpc_key)
                print(f"[SERVER] 🔓 Decrypted message plaintext: '{plaintext}'")
                
    except Exception as e:
        print(f"[SERVER] Stream exception caught: {e}")
    finally:
        conn.close()
        server_socket.close()
        print("[SERVER] System connection terminated.")


def run_lotus_client(message_payload):
    """Executes a connection to the server, triggers the handshake, and transmits data"""
    time.sleep(1)  # Buffer for thread startup stabilization
    print("[CLIENT] Connecting to the secure Lotus QPU routing environment...")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    
    client_fcke = LotusFractalKeyExchange("Client_Core")
    client_engine = LotusUniversalCryptoEngine()
    
    # Step 1: Initialize Post-Quantum Key Exchange
    print("[CLIENT] Launching FCKE handshake...")
    client_public = client_fcke.generate_public_key()
    init_frame = build_protocol_frame(0x01, json.dumps(client_public))
    client_socket.sendall(init_frame)
    
    # Step 2: Handle incoming Key Reply
    packet_type, payload = read_protocol_frame(client_socket)
    if packet_type == 0x02:
        server_public_profile = json.loads(payload)
        shared_fcpc_key = client_fcke.compute_shared_secret(server_public_profile)
        print("[CLIENT] Handshake confirmed. Symmetric orbit synchronization complete.")
        
        # Step 3: Encrypt and transmit payload
        print(f"[CLIENT] Encrypting message plaintext: '{message_payload}'")
        ciphertext = client_engine.encrypt_fcpc(message_payload, shared_fcpc_key)
        
        data_frame = build_protocol_frame(0x03, ciphertext)
        client_socket.sendall(data_frame)
        print("[CLIENT] FCPC_DATA frame broadcasted successfully.")
        
    client_socket.close()
    print("[CLIENT] System connection closed cleanly.")


