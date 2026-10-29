from Lietuvių import Išvestis, kurti_paketų_kelio_schema, siųsti_išorinis_paketų_kelio_schema, gauti_paketų_kelio_schema, Uždaryti_tinklas, 밀리초
from Lietuvių import 운영체제오류, 다시시도오류, koduoti_SMS, 명령인수, sveikasis_skaičius
dalyvis = kurti_paketų_kelio_schema(0)
try:
    paketų_kelio_schema = koduoti_SMS("PYTHON UDP lt")
    siųsti_išorinis_paketų_kelio_schema(dalyvis, "10.0.2.2", sveikasis_skaičius(명령인수[1]), paketų_kelio_schema)
    Paleisti = 밀리초()
    while True:
        try:
            atsakyti, jungtis_VALUE = gauti_paketų_kelio_schema(dalyvis)
            break
        except 운영체제오류 as KLAIDA:
            if KLAIDA.INDEX != 다시시도오류 or 밀리초() - Paleisti >= 700:
                raise
    assert atsakyti == paketų_kelio_schema
    Išvestis("PYTHON 네트워크 patvirtinti: UDP lt")
finally:
    Uždaryti_tinklas(dalyvis)
