from PIL import Image
import hashlib
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
import base64
import numpy as np

# Função para embutir texto na imagem (Esteganografia)
def embed_text_in_image(image_path, output_path, message):
    image = Image.open(image_path)
    encoded = image.copy()
    width, height = image.size
    message += chr(0)  # Delimitador de fim de mensagem

    binary_message = ''.join([format(ord(char), '08b') for char in message])
    data_index = 0

    for y in range(height):
        for x in range(width):
            pixel = list(image.getpixel((x, y)))
            for n in range(3):  # RGB
                if data_index < len(binary_message):
                    pixel[n] = pixel[n] & ~1 | int(binary_message[data_index])
                    data_index += 1
            encoded.putpixel((x, y), tuple(pixel))
            if data_index >= len(binary_message):
                break
        if data_index >= len(binary_message):
            break

    encoded.save(output_path)
    print("Texto embutido com sucesso!")

# Função para recuperar texto da imagem (Esteganografia)
def retrieve_text_from_image(image_path):
    image = Image.open(image_path)
    binary_message = ""
    
    for y in range(image.height):
        for x in range(image.width):
            pixel = image.getpixel((x, y))
            for n in range(3):  # RGB
                binary_message += str(pixel[n] & 1)

    bytes_message = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]
    message = "".join([chr(int(byte, 2)) for byte in bytes_message])
    return message.split(chr(0))[0]

# Função para gerar hash da imagem
def generate_image_hash(image_path):
    with open(image_path, "rb") as f:
        bytes = f.read()
        hash_value = hashlib.sha256(bytes).hexdigest()
    return hash_value

# Função para encriptar uma mensagem usando chave pública e privada
def encrypt_message(public_key, message):
    encrypted = public_key.encrypt(
        message.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return base64.b64encode(encrypted).decode()

# Função para decriptar uma mensagem usando chave privada
def decrypt_message(private_key, encrypted_message):
    encrypted_bytes = base64.b64decode(encrypted_message)
    decrypted = private_key.decrypt(
        encrypted_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted.decode()

# Função para gerar chave pública e privada
def generate_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

# Menu de opções
def main():
    private_key, public_key = generate_keys()
    while True:
        print("\nMenu de Opções:")
        print("(1) Embutir texto em uma imagem (Esteganografia)")
        print("(2) Recuperar texto de uma imagem (Esteganografia)")
        print("(3) Gerar hash das imagens original e alterada")
        print("(4) Encriptar mensagem usando chave pública e privada")
        print("(5) Decriptar mensagem usando chave pública e privada")
        print("(S ou s) Sair")

        option = input("Escolha uma opção: ")
        if option in ["S", "s"]:
            break
        elif option == "1":
            image_path = input("Caminho da imagem original: ")
            output_path = input("Caminho para salvar imagem alterada: ")
            message = input("Digite a mensagem a ser embutida: ")
            embed_text_in_image(image_path, output_path, message)
        elif option == "2":
            image_path = input("Caminho da imagem alterada: ")
            message = retrieve_text_from_image(image_path)
            print("Mensagem recuperada:", message)
        elif option == "3":
            original_image = input("Caminho da imagem original: ")
            modified_image = input("Caminho da imagem alterada: ")
            original_hash = generate_image_hash(original_image)
            modified_hash = generate_image_hash(modified_image)
            print("Hash da imagem original:", original_hash)
            print("Hash da imagem alterada:", modified_hash)
            if original_hash != modified_hash:
                print("A imagem foi modificada.")
            else:
                print("As imagens são idênticas.")
        elif option == "4":
            message = input("Digite a mensagem a ser encriptada: ")
            encrypted_message = encrypt_message(public_key, message)
            print("Mensagem encriptada:", encrypted_message)
        elif option == "5":
            encrypted_message = input("Digite a mensagem encriptada: ")
            decrypted_message = decrypt_message(private_key, encrypted_message)
            print("Mensagem decriptada:", decrypted_message)
        else:
            print("Opção inválida. Tente novamente.")

main()