from isiXhosa import inkqubo_impazamo, 다시시도오류, 전문통신열기, 전문받기, vala_Inethiwekhi, 파일읽기, 출력

종단 = 전문통신열기(0)
try:
    try:
        전문받기(종단)
        raise AssertionError("비어 있는 전문 대기에서 예외가 필요합니다.")
    except inkqubo_impazamo as Impazamo:
        assert Impazamo.indeksa == 다시시도오류
        assert Impazamo.설명 == "Indlela_yokusebenza 작업에 실패했습니다."
        출력("isiXhosa 전문 예외 ngqinisisa")
finally:
    vala_Inethiwekhi(종단)
try:
    파일읽기("/없는파일")
except inkqubo_impazamo as Impazamo:
    assert Impazamo.indeksa == 2
    출력("isiXhosa iFayili 예외 ngqinisisa")
else:
    raise AssertionError("iFayili 없음 예외가 필요합니다.")
