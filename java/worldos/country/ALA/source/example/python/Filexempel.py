from Svenska import utmatningsposition, skriva_fil, läsa_fil, koda_SMS, 글해독
data = "PYTHON filnamn: Svenska 😀\n"
skriva_fil("python.txt", koda_SMS(data))
läsa_SMS_värde = 글해독(läsa_fil("python.txt"))
assert läsa_SMS_värde == data
utmatningsposition(läsa_SMS_värde, 끝="")
