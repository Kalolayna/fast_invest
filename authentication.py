credentials = {
    'usuario1': 'senha1',
    'usuario2': 'senha2'
}

def authenticate(username, password):
    if username in credentials and credentials[username] == password:
        return True
    else:
        return False