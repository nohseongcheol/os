from Nederlands import systeemfout, 다시시도오류, open_datagram, ontvangen_datagram, Sluiten_net, 파일읽기, tekstuitvoer

eindpunt = open_datagram(0)
try:
    try:
        ontvangen_datagram(eindpunt)
        raise AssertionError("비어 있는 datagram 대기에서 예외가 필요합니다.")
    except systeemfout as fout:
        assert fout.INDEX == 다시시도오류
        assert fout.설명 == "besturingssysteem 작업에 실패했습니다."
        tekstuitvoer("Nederlands datagram uitzondering bevestigen")
finally:
    Sluiten_net(eindpunt)
try:
    파일읽기("/없는파일")
except systeemfout as fout:
    assert fout.INDEX == 2
    tekstuitvoer("Nederlands bestand uitzondering bevestigen")
else:
    raise AssertionError("bestand 없음 예외가 필요합니다.")
