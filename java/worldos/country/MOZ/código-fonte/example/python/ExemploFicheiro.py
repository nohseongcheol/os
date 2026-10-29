from Português import saídaTexto, gravar_Arquivo, leitura_Arquivo, codificar_SMS, 글해독
dados = "PYTHON ficheiro: Português 😀\n"
gravar_Arquivo("python.txt", codificar_SMS(dados))
leitura_SMS_VALOR = 글해독(leitura_Arquivo("python.txt"))
assert leitura_SMS_VALOR == dados
saídaTexto(leitura_SMS_VALOR, 끝="")
