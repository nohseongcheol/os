from čeština import chyba_systému, 다시시도오류, otevřít_datagram, dostat_datagram, Zavřít_síť, 파일읽기, výstupní_pozice

účastník = otevřít_datagram(0)
try:
    try:
        dostat_datagram(účastník)
        raise AssertionError("비어 있는 datagram 대기에서 예외가 필요합니다.")
    except chyba_systému as chyba:
        assert chyba.INDEX == 다시시도오류
        assert chyba.설명 == "operační_systém 작업에 실패했습니다."
        výstupní_pozice("čeština datagram výjimka ověřit")
finally:
    Zavřít_síť(účastník)
try:
    파일읽기("/없는파일")
except chyba_systému as chyba:
    assert chyba.INDEX == 2
    výstupní_pozice("čeština název_souboru výjimka ověřit")
else:
    raise AssertionError("název_souboru 없음 예외가 필요합니다.")
