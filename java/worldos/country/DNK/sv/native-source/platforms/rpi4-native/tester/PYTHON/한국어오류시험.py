from Svenska import systemfel, 다시시도오류, skapa_datagram, få_datagram, Stäng_nätverk, läsa_fil, utmatningsposition

deltagare = skapa_datagram(0)
try:
    try:
        få_datagram(deltagare)
        raise AssertionError("비어 있는 datagram 대기에서 예외가 필요합니다.")
    except systemfel as fel:
        assert fel.INDEX == 다시시도오류
        assert fel.설명 == "operativsystem 작업에 실패했습니다."
        utmatningsposition("Svenska datagram fel_31f743d2 verifiera")
finally:
    Stäng_nätverk(deltagare)
try:
    läsa_fil("/없는파일")
except systemfel as fel:
    assert fel.INDEX == 2
    utmatningsposition("Svenska filnamn fel_31f743d2 verifiera")
else:
    raise AssertionError("filnamn 없음 예외가 필요합니다.")
