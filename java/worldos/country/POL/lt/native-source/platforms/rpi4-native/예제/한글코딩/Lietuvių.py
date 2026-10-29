"""savas branduolys_VALUE MicroPython에서 사용하는 한글 FUNCTION_VALUE Pavadinimas_2."""
import jkoros as operacinė_sistema
Išvestis = print
파일읽기 = operacinė_sistema.read
rašymas_Failas = operacinė_sistema.write
pašalinti_Failas = operacinė_sistema.remove
입력읽기 = operacinė_sistema.stdin
piešti_stačiakampis = operacinė_sistema.rect
그림기다리기 = operacinė_sistema.wait_key
밀리초 = operacinė_sistema.ticks_ms
kurti_paketų_kelio_schema = operacinė_sistema.udp_open
siųsti_paketų_kelio_schema = operacinė_sistema.udp_send
siųsti_išorinis_paketų_kelio_schema = operacinė_sistema.udp_sendto
gauti_paketų_kelio_schema = operacinė_sistema.udp_recv
Uždaryti_tinklas = operacinė_sistema.udp_close

def 글해독(duomenys):
    return duomenys.decode("utf-8")
