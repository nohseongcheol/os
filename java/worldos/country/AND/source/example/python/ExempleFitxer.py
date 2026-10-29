from Català import Sortida, escriure_arxiu, tancar_arxiu, 글부호화, 글해독
dades = "PYTHON Fitxer: Català 😀\n"
escriure_arxiu("python.txt", 글부호화(dades))
tancar_SMS_VALOR = 글해독(tancar_arxiu("python.txt"))
assert tancar_SMS_VALOR == dades
Sortida(tancar_SMS_VALOR, 끝="")
