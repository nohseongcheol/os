from polski import błąd_systemu, 다시시도오류, otwarty_datagram, odbierać_datagram, Zamknij_sieć, 파일읽기, pozycja_wyjścia

uczestnik = otwarty_datagram(0)
try:
    try:
        odbierać_datagram(uczestnik)
        raise AssertionError("비어 있는 datagram 대기에서 예외가 필요합니다.")
    except błąd_systemu as błąd:
        assert błąd.INDEKS == 다시시도오류
        assert błąd.설명 == "system_operacyjny 작업에 실패했습니다."
        pozycja_wyjścia("polski datagram wyjątek 확인")
finally:
    Zamknij_sieć(uczestnik)
try:
    파일읽기("/없는파일")
except błąd_systemu as błąd:
    assert błąd.INDEKS == 2
    pozycja_wyjścia("polski nazwa_pliku wyjątek 확인")
else:
    raise AssertionError("nazwa_pliku 없음 예외가 필요합니다.")
