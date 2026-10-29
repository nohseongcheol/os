"""oma ydin_ARVO MicroPython에서 사용하는 한글 funktio_ARVO Nimi."""
import jkoros as käyttöjärjestelmä
tulostuspaikka = print
lukea_Tiedosto = käyttöjärjestelmä.read
kirjoitus_Tiedosto = käyttöjärjestelmä.write
poistaa_Tiedosto = käyttöjärjestelmä.remove
lukea_syöte = käyttöjärjestelmä.stdin
Piirrä_suorakulmio = käyttöjärjestelmä.rect
그림기다리기 = käyttöjärjestelmä.wait_key
밀리초 = käyttöjärjestelmä.ticks_ms
avata_datagrammi = käyttöjärjestelmä.udp_open
lähettää_datagrammi = käyttöjärjestelmä.udp_send
lähettää_ulkoinen_datagrammi = käyttöjärjestelmä.udp_sendto
saada_datagrammi = käyttöjärjestelmä.udp_recv
Sulje_verkko = käyttöjärjestelmä.udp_close

def 글해독(data):
    return data.decode("utf-8")
