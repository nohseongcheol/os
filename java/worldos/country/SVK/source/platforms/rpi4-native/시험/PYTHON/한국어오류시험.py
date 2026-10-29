from Slovenský import systém_Chyba, 다시시도오류, otvoriť_datagram, dostať_datagram, Zavrieť_sieť, 파일읽기, Výstup

účastník = otvoriť_datagram(0)
try:
    try:
        dostať_datagram(účastník)
        raise AssertionError("비어 있는 datagram 대기에서 예외가 필요합니다.")
    except systém_Chyba as chyba:
        assert chyba.INDEX == 다시시도오류
        assert chyba.설명 == "operačný_systém 작업에 실패했습니다."
        Výstup("Slovenský datagram výnimka overiť")
finally:
    Zavrieť_sieť(účastník)
try:
    파일읽기("/없는파일")
except systém_Chyba as chyba:
    assert chyba.INDEX == 2
    Výstup("Slovenský Súbor výnimka overiť")
else:
    raise AssertionError("Súbor 없음 예외가 필요합니다.")
