from suomi import tulostuspaikka, avata_datagrammi, lähettää_ulkoinen_datagrammi, saada_datagrammi, Sulje_verkko, 밀리초
from suomi import järjestelmävirhe, 다시시도오류, koodata_SMS, 명령인수, kokonaisluku
päätepiste = avata_datagrammi(0)
try:
    datagrammi = koodata_SMS("PYTHON UDP fi")
    lähettää_ulkoinen_datagrammi(päätepiste, "10.0.2.2", kokonaisluku(명령인수[1]), datagrammi)
    Suorita_2 = 밀리초()
    while True:
        try:
            palaute, portti_ARVO = saada_datagrammi(päätepiste)
            break
        except järjestelmävirhe as VIRHE:
            if VIRHE.INDEKSI != 다시시도오류 or 밀리초() - Suorita_2 >= 700:
                raise
    assert palaute == datagrammi
    tulostuspaikka("PYTHON 네트워크 tarkistaa: UDP fi")
finally:
    Sulje_verkko(päätepiste)
