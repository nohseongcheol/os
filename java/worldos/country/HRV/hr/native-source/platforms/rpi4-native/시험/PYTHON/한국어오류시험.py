from hrvatski import sustav_pogreška, 다시시도오류, otvoreno_datogram, primiti_datogram, Zatvori_mreža, 파일읽기, Izlaz

sudionik = otvoreno_datogram(0)
try:
    try:
        primiti_datogram(sudionik)
        raise AssertionError("비어 있는 datogram 대기에서 예외가 필요합니다.")
    except sustav_pogreška as GREŠKA:
        assert GREŠKA.INDEX == 다시시도오류
        assert GREŠKA.설명 == "operacijski_sustav 작업에 실패했습니다."
        Izlaz("hrvatski datogram iznimka provjeriti")
finally:
    Zatvori_mreža(sudionik)
try:
    파일읽기("/없는파일")
except sustav_pogreška as GREŠKA:
    assert GREŠKA.INDEX == 2
    Izlaz("hrvatski Datoteka iznimka provjeriti")
else:
    raise AssertionError("Datoteka 없음 예외가 필요합니다.")
