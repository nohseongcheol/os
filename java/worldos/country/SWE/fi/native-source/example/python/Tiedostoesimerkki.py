from suomi import tulostuspaikka, kirjoitus_Tiedosto, lukea_Tiedosto, koodata_SMS, 글해독
data = "PYTHON tiedoston_nimi: fi 😀\n"
kirjoitus_Tiedosto("python.txt", koodata_SMS(data))
lukea_SMS_ARVO = 글해독(lukea_Tiedosto("python.txt"))
assert lukea_SMS_ARVO == data
tulostuspaikka(lukea_SMS_ARVO, 끝="")
