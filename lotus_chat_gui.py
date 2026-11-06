"""
Lotus Secure Messenger - Graphical User Interface (GUI)
Asynchronous Tkinter Chat client integrating FCPC and FCKE.

Author: Rudolf Juhl
Location: Bensheim, Germany
Date: November 6, 2026
License: CC-BY-4.0
"""

import tkinter as tk
from tkinter import ttk, messagebox
import socket
import threading
import json
import time

# Import the core cryptographic and network constants from your primary module
from lotus_crypto_system import (
    LotusFractalKeyExchange, 
    LotusUniversalCryptoEngine,
    MAGIC_BYTE,
    HOST,
    PORT,
    build_protocol_frame,
    read_protocol_frame
)

class LotusChatGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Lotus Secure Messenger - Core V3 (FCPC)")
        self.root.geometry("650x550")
        self.root.configure(bg="#1e1e24")

        # Network & Crypto State Variables
        self.client_socket = None
        self.is_connected = False
        self.shared_fcpc_key = None
        
        # Initialize Cryptographic Infrastructure under Rudolf Juhl specification
        self.crypto_engine = LotusUniversalCryptoEngine()
        self.fcke = LotusFractalKeyExchange("GUI_Client_Core")

        # Style Configuration (Modern Dark-Mode Industrial Layout)
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('.', background='#1e1e24', foreground='#ffffff')
        self.style.configure('TLabel', background='#1e1e24', foreground='#00ffcc', font=('Courier', 10, 'bold'))
        self.style.configure('TButton', background='#00ffcc', foreground='#1e1e24', font=('Helvetica', 10, 'bold'))
        
        self.create_widgets()

    def create_widgets(self):
        """Builds the layout structure of the cryptographic chat application"""
        # --- TOP LAYER: NETWORK CONTROL ---
        status_frame = ttk.Frame(self.root, padding=10)
        status_frame.pack(fill=tk.X)
        
        self.status_label = ttk.Label(status_frame, text="STATUS: DISCONNECTED (OFFLINE)", foreground="#ff3333")
        self.status_label.pack(side=tk.LEFT)
        
        self.connect_btn = ttk.Button(status_frame, text="Quantum Handshake (FCKE)", command=self.start_connection)
        self.connect_btn.pack(side=tk.RIGHT)

        # --- CENTER LAYER: CHAT HISTORY STREAM ---
        chat_frame = ttk.Frame(self.root, padding=10)
        chat_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(chat_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.chat_display = tk.Text(
            chat_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set,
            bg="#2a2a35", fg="#ffffff", insertbackground="#00ffcc",
            font=("Helvetica", 11), padding=10, state=tk.DISABLED
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.chat_display.yview)
        
        # Define formatting tags for plaintext and encrypted orbits
        self.chat_display.tag_config('system', foreground='#00ffcc', font=('Courier', 10, 'italic'))
        self.chat_display.tag_config('me', foreground='#ffff00')
        self.chat_display.tag_config('remote', foreground='#00ffcc')
        self.chat_display.tag_config('chiffre', foreground='#8888aa', font=('Courier', 9))

        # --- BOTTOM LAYER: CRYPTO PAYLOAD INPUT ---
        input_frame = ttk.Frame(self.root, padding=10)
        input_frame.pack(fill=tk.X)
        
        self.msg_entry = tk.Entry(
            input_frame, bg="#2a2a35", fg="#ffffff", insertbackground="#00ffcc",
            font=("Helvetica", 11), borderwidth=1, relief=tk.SOLID
        )
        self.msg_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8, padx=(0, 10))
        self.msg_entry.bind("<Return>", lambda event: self.send_message())
        
        self.send_btn = ttk.Button(input_frame, text="Send Payload", command=self.send_message, state=tk.DISABLED)
        self.send_btn.pack(side=tk.RIGHT, ipady=5)

    def log_message(self, tag, prefix, text, chiffre=None):
        """Handles internal display formatting inside the secure layout"""
        self.chat_display.config(state=tk.NORMAL)
        if tag == 'system':
            self.chat_display.insert(tk.END, f"[SYSTEM] {text}\n", 'system')
        else:
            self.chat_display.insert(tk.END, f"{prefix}: {text}\n", tag)
            if chiffre:
                self.chat_display.insert(tk.END, f"  └─ FCPC-Orbits: {chiffre}\n", 'chiffre')
        self.chat_display.insert(tk.END, "\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)

    def start_connection(self):
        """Dispatches connection routine asynchronously to prevent UI freeze"""
        self.connect_btn.config(state=tk.DISABLED)
        threading.Thread(target=self.network_handshake_and_listen, daemon=True).start()

    def network_handshake_and_listen(self):
        """Executes binary protocol handshake and opens the decryption stream loop"""
        try:
            self.log_message('system', '', f"Connecting to secure routing node at {HOST}:{PORT}...")
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((HOST, PORT))
            
            # --- PHASE 1: ASYMMETRIC HANDSHAKE (FCKE) ---
            self.log_message('system', '', "Initiating Fractal Circular Key Exchange (FCKE)...")
            client_public = self.fcke.generate_public_key()
            
            # Send Packet Type 0x01 (FCKE_INIT)
            init_frame = build_protocol_frame(0x01, json.dumps(client_public))
            self.client_socket.sendall(init_frame)
            
            # Read Response Frame from Stream
            packet_type, payload = read_protocol_frame(self.client_socket)
            
            if packet_type == 0x02:  # FCKE_REPLY
                server_public_profile = json.loads(payload)
                # Compute symmetric keys out of non-commutative group dimensions
                self.shared_fcpc_key = self.fcke.compute_shared_secret(server_public_profile)
                
                # Update UI elements for secure data state
                self.is_connected = True
                self.status_label.config(text="STATUS: SECURED (ONLINE / FCPC ACTIVE)", foreground="#00ffcc")
                self.send_btn.config(state=tk.NORMAL)
                self.log_message('system', '', "🔐 Channels fully encrypted via Post-Quantum FCPC Orbits.")
                
                # --- PHASE 2: CONTINUOUS STREAM DECRYPTION ---
                self.listen_to_server()
                    
        except Exception as e:
            messagebox.showerror("Network Exception", f"Connection routine failed:\n{e}")
            self.status_label.config(text="STATUS: CONNECTION ERROR", foreground="#ff3333")
            self.connect_btn.config(state=tk.NORMAL)

    def listen_to_server(self):
        """Listens continuously for incoming FCPC encrypted data frames (Type 0x03)"""
        try:
            while self.is_connected:
                packet_type, payload = read_protocol_frame(self.client_socket)
                if packet_type is None: 
                    break
                
                if packet_type == 0x03:  # FCPC_DATA Frame
                    # Direct on-the-fly decryption with hardware phase calibration
                    plaintext = self.crypto_engine.decrypt_fcpc(payload, self.shared_fcpc_key)
                    self.log_message('remote', "Remote Node", plaintext, chiffre=payload)
        except:
            pass
        finally:
            self.is_connected = False
            self.status_label.config(text="STATUS: CONNECTION TERMINATED", foreground="#ff3333")
            self.send_btn.config(state=tk.DISABLED)
            self.connect_btn.config(state=tk.NORMAL)

    def send_message(self):
        """Encrypts plaintext inputs on-chip and broadcasts the frame over the wire"""
        msg = self.msg_entry.get().strip()
        if msg and self.is_connected and self.shared_fcpc_key:
            try:
                # Encrypt data locally before passing it to the network socket
                ciphertext = self.crypto_engine.encrypt_fcpc(msg, self.shared_fcpc_key)
                
                # Build Data Frame (Type 0x03) and dispatch
                data_frame = build_protocol_frame(0x03, ciphertext)
                self.client_socket.sendall(data_frame)
                
                # Commit local display log
                self.log_message('me', "You", msg, chiffre=ciphertext)
                self.msg_entry.delete(0, tk.END)
            except Exception as e:
                self.log_message('system', '', f"Payload execution failure: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = LotusChatGUI(root)
    root.mainloop()
