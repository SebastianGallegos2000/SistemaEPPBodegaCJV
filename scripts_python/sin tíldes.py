def sin_tilde(texto):
    texto_sin_tildes = ''

    for char in texto:
        tildes = ['Á','É','Í','Ó','Ú','á','é','í','ó','ú']
        sin_tildes = ['A','E','I','O','U','a','e','i','o','u']
        char_annadido = char
        for i in range(0,10):
            if(char==tildes[i]):
                char_annadido=sin_tildes[i]
                break
        texto_sin_tildes+=char_annadido
    return texto_sin_tildes




