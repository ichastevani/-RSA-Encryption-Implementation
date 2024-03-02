import tkinter as tk
from tkinter import ttk

class RSA_GUI:
    def __init__(self, master):
        self.master = master
        self.master.title("RSA Algorithm with GUI")

        # Variables
        self.p_var = tk.StringVar()
        self.q_var = tk.StringVar()
        self.e_var = tk.StringVar()
        self.d_var = tk.StringVar()
        self.n_var = tk.StringVar()
        self.phi_n_var = tk.StringVar()
        self.public_key_var = tk.StringVar()
        self.private_key_var = tk.StringVar()
        self.message_var = tk.StringVar()
        self.encrypted_message_var = tk.StringVar()
        self.decrypted_message_var = tk.StringVar()

        # UI Elements
        self.create_widgets()

    def create_widgets(self):
        # Input Section
        input_frame = ttk.Frame(self.master, padding="10")
        input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        ttk.Label(input_frame, text="Enter prime number p:").grid(row=0, column=0, sticky="w")
        ttk.Entry(input_frame, textvariable=self.p_var).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Enter prime number q:").grid(row=1, column=0, sticky="w")
        ttk.Entry(input_frame, textvariable=self.q_var).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Enter public exponent e:").grid(row=2, column=0, sticky="w")
        ttk.Entry(input_frame, textvariable=self.e_var).grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(input_frame, text="Generate Keys", command=self.generate_keys).grid(row=3, column=0, columnspan=2, pady=10)

        # RSA Steps Section
        rsa_steps_frame = ttk.Frame(self.master, padding="10")
        rsa_steps_frame.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        ttk.Label(rsa_steps_frame, text="RSA Steps:").grid(row=0, column=0, sticky="w")

        rsa_steps_text = tk.Text(rsa_steps_frame, height=15, width=70)
        rsa_steps_text.grid(row=1, column=0, sticky="w")

        # Output Section
        output_frame = ttk.Frame(self.master, padding="10")
        output_frame.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        ttk.Label(output_frame, text="Public Key:").grid(row=0, column=0, sticky="w")
        ttk.Entry(output_frame, textvariable=self.public_key_var, state="readonly").grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(output_frame, text="Private Key:").grid(row=1, column=0, sticky="w")
        ttk.Entry(output_frame, textvariable=self.private_key_var, state="readonly").grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(output_frame, text="Enter message:").grid(row=2, column=0, sticky="w")
        ttk.Entry(output_frame, textvariable=self.message_var).grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(output_frame, text="Encrypt/Decrypt", command=self.encrypt_decrypt).grid(row=3, column=0, columnspan=2, pady=10)

        ttk.Label(output_frame, text="Encrypted Message:").grid(row=4, column=0, sticky="w")
        ttk.Entry(output_frame, textvariable=self.encrypted_message_var, state="readonly").grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(output_frame, text="Decrypted Message:").grid(row=5, column=0, sticky="w")
        ttk.Entry(output_frame, textvariable=self.decrypted_message_var, state="readonly").grid(row=5, column=1, padx=5, pady=5)

    def generate_keys(self):
        try:
            p = int(self.p_var.get())
            q = int(self.q_var.get())
            e = int(self.e_var.get())

            # Step 1
            n = p * q
            self.n_var.set(n)

            # Step 2
            phi_n = (p - 1) * (q - 1)
            self.phi_n_var.set(phi_n)

            # Step 3
            d = self.modular_inverse(e, phi_n)
            self.d_var.set(d)

            # Step 4
            public_key = (e, n)
            private_key = (d, n)
            self.public_key_var.set(str(public_key))
            self.private_key_var.set(str(private_key))

            # Display RSA steps
            rsa_steps = f"Pemilihan Dua Bilangan Prima Besar:\n\n"
            rsa_steps += f"1. p = {p}, q = {q}\n"
            rsa_steps += f"2. n = p * q = {n}\n\n"
            rsa_steps += f"Perhitungan Fungsi Euler Totient (φ(n)):\n\n"
            rsa_steps += f"3. φ(n) = (p-1) * (q-1) = {phi_n}\n\n"
            rsa_steps += f"Pemilihan Eksponen Publik (e):\n\n"
            rsa_steps += f"4. e = {e}\n\n"
            rsa_steps += f"Perhitungan Eksponen Privat (d):\n\n"
            rsa_steps += f"5. d * e ≡ 1 (mod φ(n)) => {d} * {e} ≡ 1 (mod {phi_n})\n\n"
            rsa_steps += f"Penyusunan Kunci Publik dan Kunci Privat:\n\n"
            rsa_steps += f"6. Kunci Publik: {public_key}\n"
            rsa_steps += f"7. Kunci Privat: {private_key}\n"

            self.update_text(rsa_steps)
        except ValueError:
            self.update_text("Invalid input. Please enter valid numbers for p, q, and e.")

    def encrypt_decrypt(self):
        try:
            n = int(self.n_var.get())
            e = int(self.e_var.get())
            d = int(self.d_var.get())
            message = self.message_var.get().lower()

            # Convert each letter to a two-digit numeric value (a=00, b=01, ..., z=25)
            numeric_values = [str(ord(char) - ord('a')).zfill(2) for char in message if char.isalpha()]

            # Display blocks before encryption
            block_size = len(str(n-1))
            blocks_before_encryption = [numeric_values[i:i+block_size] for i in range(0, len(numeric_values), block_size)]

            # Join numeric values into a single string
            numeric_string = ''.join(numeric_values)

            # Break the numeric string into blocks with a range of 0 <= block < (n-1)
            blocks = [numeric_string[i:i+block_size] for i in range(0, len(numeric_string), block_size)]

            # Encrypt each block using the public key
            encrypted_blocks = [str(pow(int(block), e, n)).zfill(block_size) for block in blocks]
            self.encrypted_message_var.set(' '.join(encrypted_blocks))

            # Decrypt each block using the private key
            decrypted_blocks = [str(pow(int(block), d, n)).zfill(len(block)) for block in encrypted_blocks]

            # Combine decrypted blocks into a single string
            decrypted_text = ''.join(decrypted_blocks)

            # Convert each two-digit numeric value back to a letter
            decrypted_text = ''.join([chr(int(decrypted_text[i:i+2]) + ord('a')) for i in range(0, len(decrypted_text), 2)])
            self.decrypted_message_var.set(decrypted_text)

            # Tampilkan langkah-langkah enkripsi/dekripsi
            encryption_steps = "Enkripsi:\n\n"
            encryption_steps += f"8. Pesan M yang akan dienkripsi: {message}\n"
            encryption_steps += f"9. Pesan dalam bentuk blok sebelum enkripsi: {blocks_before_encryption}\n"
            encryption_steps += f"10. Pesan terenkripsi C ≡ M^e (mod n) => {encrypted_blocks}\n\n"
            encryption_steps += "Dekripsi:\n\n"
            encryption_steps += f"11. Pesan terenkripsi C: {encrypted_blocks}\n"
            encryption_steps += f"12. Pesan yang didekripsi M ≡ C^d (mod n) => {decrypted_text}\n"

            self.update_text(encryption_steps)

        except ValueError:
            self.update_text("Invalid input. Please enter valid numbers for p, q, and e.")


    def update_text(self, text):
        rsa_steps_text = self.master.children["!frame2"].children["!text"]
        rsa_steps_text.config(state="normal")
        rsa_steps_text.delete(1.0, tk.END)
        rsa_steps_text.insert(tk.END, text)
        rsa_steps_text.config(state="disabled")

    def modular_inverse(self, a, m):
        # Extended Euclidean Algorithm to find modular inverse
        m0, x0, x1 = m, 0, 1
        while a > 1:
            q = a // m
            m, a = a % m, m
            x0, x1 = x1 - q * x0, x0
        return x1 + m0 if x1 < 0 else x1

def main():
    root = tk.Tk()
    rsa_gui = RSA_GUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
