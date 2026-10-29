from Isi_Zulu import isistimu_iphutha, 다시시도오류, 전문통신열기, 전문받기, vala_iNethiwekhi, 파일읽기, 출력

종단 = 전문통신열기(0)
try:
    try:
        전문받기(종단)
        raise AssertionError("비어 있는 전문 대기에서 예외가 필요합니다.")
    except isistimu_iphutha as Iphutha:
        assert Iphutha.thola_inkomba == 다시시도오류
        assert Iphutha.설명 == "isistimu_yokusebenza 작업에 실패했습니다."
        출력("Isi_Zulu 전문 예외 qiniseka")
finally:
    vala_iNethiwekhi(종단)
try:
    파일읽기("/없는파일")
except isistimu_iphutha as Iphutha:
    assert Iphutha.thola_inkomba == 2
    출력("Isi_Zulu Ihele 예외 qiniseka")
else:
    raise AssertionError("Ihele 없음 예외가 필요합니다.")
