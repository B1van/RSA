import math
import random
import string
def text_to_decimal(text):
    chars = string.ascii_letters + string.digits + string.punctuation + ' '
    decimal_value = 0
    for i in range(len(text)):
        char_index = chars.index(text[i])
        decimal_value = decimal_value * len(chars) + char_index
    return decimal_value

def decimal_to_text(decimal_value):
    chars = string.ascii_letters + string.digits + string.punctuation + ' '
    text = ''
    while decimal_value > 0:
        char_index = decimal_value % len(chars)
        text = chars[char_index] + text
        decimal_value = decimal_value // len(chars)
    return text

def is_prime(n):
    if n % 2 == 0 and n > 2:
        return False
    for i in range(20):
        a = random.randint(2,n-1)
        if pow(a,n-1,n) != 1:
            return False
    return True

def generate_prime(n):
    while True:
        if n % 2 == 0:
            n+=1
        if is_prime(n):
            return n
        n += 2
import random

def pollard_rho(n):
    if n % 2 == 0:
        return 2

    def f(x):
        return (x**2 - 1) % n

    x, y, d = 2, 2, 1
    while d == 1:
        x = f(x)
        y = f(f(y))
        d = gcd(abs(x-y), n)

    if d == n:
        while True:
            y = f(y)
            d = gcd(abs(x-y), n)
            if d > 1:
                break

    return d

def factorize(n):
    factors = []
    while n % 2 == 0:
        factors.append(2)
        n //= 2

    while n > 1:
        f = pollard_rho(n)
        factors.append(f)
        n //= f

    return factors


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def is_coprime(a, b):
    return gcd(a, b) == 1

def find_coprime(n):
    while True:
        random_number = random.randint(2, int(math.sqrt(n-1)))
        if is_coprime(random_number, n):
            return random_number

def generate_exponent(p,q):
    a = (p-1)*(q-1)
    exponent = find_coprime(a)
    return exponent

def extended_gcd(a, b):
    x, y, u, v = 0, 1, 1, 0
    while a != 0:
        q, r = b // a, b % a
        m, n = x - u * q, y - v * q
        b, a, x, y, u, v = a, r, u, v, m, n 
    return b, x, y

def mod_inverse(e, phi):
    gcd, x, y = extended_gcd(e, phi)
    if gcd == 1:
        return x % phi
def power_mod(base, exponent, modulus):
    result = 1
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        base = (base * base) % modulus
        exponent //= 2
    return result

def generate_key():
    p = generate_prime(random.randint(2**64,2**65))
    q = generate_prime(random.randint(2**64, p))
    print("Большое простое число:", p, q)
    exponent = generate_exponent(p, q)
    d = mod_inverse(exponent, (p-1)*(q-1))
    n = p*q
    print("Закрытый ключ:", d)
    print('Открытый ключ:', exponent, n)
    return p,q,exponent,n,d

def encrypt(text, exponent, n):
    message = text_to_decimal(text)
    message = str(message)
    print(message)
    encrypted_numbers = []
    for i in range(0,len(message),len(str(n)) -1):
            encrypted_numbers.append((message[i:i+len(str(n))-1]))
    print(encrypted_numbers)
    encrypted_message = ''
    for i in range(len(encrypted_numbers)):
        encrypted_numbers[i] = str(power_mod(int(encrypted_numbers[i]), exponent, n))
        encrypted_message += str(decimal_to_text(int(encrypted_numbers[i]))) + '$5@'
    print(encrypted_numbers)
    return encrypted_message

def decrypt(text, d, n):
    encrypted_message = text.split('$5@')
    decrypt_numbers = []
    for i in range(len(encrypted_message)-1):
        decrypt_numbers.append(text_to_decimal(encrypted_message[i]))
    for i in range(len(decrypt_numbers)):
        decrypt_numbers[i] = str(power_mod(int(decrypt_numbers[i]), d, n))
    decrypt_numbers_str = ''
    print(decrypt_numbers)
    for i in range(len(decrypt_numbers)-1):
        if len(decrypt_numbers[i]) < len(str(n)) - 1:
            decrypt_numbers[i] = '0'+ decrypt_numbers[i]
    for elem in decrypt_numbers:
        decrypt_numbers_str += str(elem)
    print(decrypt_numbers_str)
    decrypted_message = decimal_to_text(int(decrypt_numbers_str))
    return decrypted_message
choose_1 = int(input("[1] Зашифрование \n[2] Расшифрование\n[3] Факторизация\n"))
if choose_1 == 1:
    choose = int(input("[1] Сгенерировать ключи\n[2] Ввести ключи\n"))
    if choose == 1:
        p, q,exponent,n,d = generate_key()
        file = str(input("Введите название файла для чтения: "))
        with open(file, 'r') as f:
            lines = f.readline()
        text = lines.upper()
        print(text)
        encrypted_text = encrypt(text,exponent,n)
        print("Зашифрованный текст:", encrypted_text)
        with open('output.txt', 'w', encoding = 'utf-8') as f:
            f.write(encrypted_text)

    if choose == 2:
        p = int(input())
        q = int(input())
        exponent = generate_exponent(p,q)
        n = p*q
        d = mod_inverse(exponent, (p-1)*(q-1))
        file = str(input("Введите название файла для чтения"))
        with open(file, 'r') as f:
            text = f.readline().upper()
        encrypted_text = encrypt(text,exponent,n)
        print("n:", n, "\nd:", d)
        print("Зашифрованный текст:", encrypted_text)
        with open('output.txt', 'w') as f:
            f.write(encrypted_text)
elif choose_1 == 2:
        n = int(input("Введите n: "))
        d = int(input("Введите d: "))
        file = str(input("Введите название файла для чтения: "))
        with open(file, 'r') as f:
            text = f.readline()
        decrypted_text = decrypt(text,d,n)
        print("Расшифрованный текст:", decrypted_text)
elif choose_1 == 3:
    n = int(input("Введите число для факторизации: "))
    factors = factorize(n)
    print("делители числа:", factors)