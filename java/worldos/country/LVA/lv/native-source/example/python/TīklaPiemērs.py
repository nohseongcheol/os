from Latviešu import Izvade, atvērt_datogramma, sūtīt_ārējs_datogramma, saņemt_datogramma, Aizvērt_tīkls, 밀리초
from Latviešu import sistēma_kļūda, 다시시도오류, kodēt_SMS, 명령인수, vesels_skaitlis
dalībnieks = atvērt_datogramma(0)
try:
    datogramma = kodēt_SMS("PYTHON UDP lv")
    sūtīt_ārējs_datogramma(dalībnieks, "10.0.2.2", vesels_skaitlis(명령인수[1]), datogramma)
    Palaist = 밀리초()
    while True:
        try:
            atbilde, ports_VALUE = saņemt_datogramma(dalībnieks)
            break
        except sistēma_kļūda as Kļūda:
            if Kļūda.INDEX != 다시시도오류 or 밀리초() - Palaist >= 700:
                raise
    assert atbilde == datogramma
    Izvade("PYTHON 네트워크 verificēt: UDP lv")
finally:
    Aizvērt_tīkls(dalībnieks)
