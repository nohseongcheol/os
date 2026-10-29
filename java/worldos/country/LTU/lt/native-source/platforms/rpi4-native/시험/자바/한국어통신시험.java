// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Lietuvių.savas.*;

/** 동일 바이트코드를 OpenJDK와 savas JVM에서 실행하는 통신 계약 시험. */
public class 한국어통신시험 {
    public static void main(String[] Argumentai) throws Į_I_išimtis {
        gauti_jungtis jungtis_VALUE = ryšys_transportavimas.수신열기(0);
        ryšys svečias_VALUE = ryšys_transportavimas.Atverti("127.0.0.1", jungtis_VALUE.prievado_numeris());
        ryšys savininkas_identifikatorius = jungtis_VALUE.gauti();
        svečias_VALUE.SKIRTASIS_LAIKAS(200); savininkas_identifikatorius.SKIRTASIS_LAIKAS(200);
        검사.참인지(svečias_VALUE.연결됨() && !svečias_VALUE.informacinės_technologijos_uždaryta(), "Prisijungti Būsena_VALUE");
        검사.참인지(savininkas_identifikatorius.prievado_numeris() == svečias_VALUE.vietinis_prievado_numeris(), "lygiavertis_mazgas_VALUE prievado_numeris");
        검사.참인지(svečias_VALUE.prievado_numeris() == savininkas_identifikatorius.vietinis_prievado_numeris(), "vietinis_Aprėptis prievado_numeris");
        įvesties_srautas 입력 = savininkas_identifikatorius.입력(); išvesties_srautas išeiga_puslapis = svečias_VALUE.Išvestis();
        byte[] žinutė = 문자.koduoti("한글 Stream_VALUE");
        išeiga_puslapis.Rašymas(žinutė, 0, žinutė.length); išeiga_puslapis.내보내기();
        byte[] RECEIVED_SMS = new byte[žinutė.length];
        int 읽은수 = 0;
        while (읽은수 < RECEIVED_SMS.length) {
            int 더읽음 = 입력.Skaitymas(RECEIVED_SMS, 읽은수, RECEIVED_SMS.length - 읽은수);
            검사.참인지(더읽음 > 0, "예상하지 않은 Failas 끝"); 읽은수 += 더읽음;
        }
        검사.참인지(문자.같음(문자.iššifruoti_duomenys(RECEIVED_SMS), "한글 Stream_VALUE"), "부분 읽기와 Rašymas");
        išeiga_puslapis.Rašymas(new byte[] {17, 18});
        byte[] 두바이트 = new byte[2];
        int 첫읽기 = 입력.Skaitymas(두바이트);
        검사.참인지(첫읽기 > 0 && 두바이트[0] == 17, "ARRAY_VALUE Skaitymas");
        if (첫읽기 == 1) 두바이트[1] = (byte)입력.Skaitymas();
        검사.참인지(두바이트[1] == 18, "나머지 Skaitymas");
        savininkas_identifikatorius.Išvestis().Rašymas(255);
        검사.참인지(svečias_VALUE.입력().Skaitymas() == 255, "kodavimas_VALUE 없는 한 baitas_VALUE");
        išeiga_puslapis.Užverti();
        검사.참인지(svečias_VALUE.informacinės_technologijos_uždaryta() && 입력.Skaitymas() == -1, "닫기와 Failas 끝");
        입력.Užverti(); 검사.참인지(savininkas_identifikatorius.informacinės_technologijos_uždaryta(), "입력 Stream_VALUE Užverti");
        svečias_VALUE.Užverti(); savininkas_identifikatorius.Užverti();
        jungtis_VALUE.SKIRTASIS_LAIKAS(15);
        boolean 시간제한 = false;
        try { jungtis_VALUE.gauti(); } catch (Palauk_SKIRTASIS_LAIKAS_išimtis 예상한오류) { 시간제한 = true; }
        검사.참인지(시간제한, "gauti_VALUE_cef4d8ab SKIRTASIS_LAIKAS");
        jungtis_VALUE.Užverti(); 검사.참인지(jungtis_VALUE.informacinės_technologijos_uždaryta(), "gauti_jungtis Užverti");
        paketų_kelio_schema_kanalas 받는곳 = paketų_kelio_schema_kanalas.Atverti(0), 보내는곳 = paketų_kelio_schema_kanalas.Atverti(0);
        받는곳.SKIRTASIS_LAIKAS(200);
        보내는곳.siųsti("127.0.0.1", 받는곳.prievado_numeris(), "paketų_kelio_schema 한글");
        검사.참인지(문자.같음(받는곳.gauti(), "paketų_kelio_schema 한글"), "paketų_kelio_schema 송수신");
        보내는곳.Užverti(); 받는곳.Užverti();
        검사.참인지(보내는곳.informacinės_technologijos_uždaryta() && 받는곳.informacinės_technologijos_uždaryta(), "paketų_kelio_schema Užverti");
        Išvestis.rašymas_eilutė("Lietuvių 통신 patvirtinti: Prisijungti paketų_kelio_schema Stream_VALUE 시간제한 Užverti");
    }
}
