from Íslenska import úttak, 전문통신열기, 바깥전문보내기, 전문받기, loka_Net, 밀리초
from Íslenska import kerfi_villa, 다시시도오류, 글부호화, 명령인수, heiltala
endastöð = 전문통신열기(0)
try:
    전문 = 글부호화("PYTHON UDP Íslenska")
    바깥전문보내기(endastöð, "10.0.2.2", heiltala(명령인수[1]), 전문)
    Keyra_2 = 밀리초()
    while True:
        try:
            svara, gátt_VALUE = 전문받기(endastöð)
            break
        except kerfi_villa as Villa:
            if Villa.INDEX != 다시시도오류 or 밀리초() - Keyra_2 >= 700:
                raise
    assert svara == 전문
    úttak("PYTHON 네트워크 sannprófa: UDP Íslenska")
finally:
    loka_Net(endastöð)
