// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import slovenščina.lastno.*;

/** 동일 바이트코드를 OpenJDK와 lastno JVM에서 실행하는 통신 계약 시험. */
public class 한국어통신시험 {
    public static void main(String[] Argumenti) throws V_I_izjema {
        sprejeti_sprejemati_prejeti_prejemati_vrata vrata_VALUE = 연결통신.수신열기(0);
        povezava gost_VALUE = 연결통신.Odpri("127.0.0.1", vrata_VALUE.številka_vrat());
        povezava lastnik_identifikator = vrata_VALUE.sprejeti_sprejemati_prejeti_prejemati();
        gost_VALUE.TIMEOUT(200); lastnik_identifikator.TIMEOUT(200);
        검사.참인지(gost_VALUE.연결됨() && !gost_VALUE.닫힘(), "Poveži stanje_VALUE");
        검사.참인지(lastnik_identifikator.številka_vrat() == gost_VALUE.lokalen_krajeven_številka_vrat(), "enakovreden_VALUE številka_vrat");
        검사.참인지(gost_VALUE.številka_vrat() == lastnik_identifikator.lokalen_krajeven_številka_vrat(), "lokalen_krajeven_obseg številka_vrat");
        vhodni_tok 입력 = lastnik_identifikator.입력(); izhodni_tok 출력쪽 = gost_VALUE.Izpis();
        byte[] e_pošta = 문자.kodirati("한글 tok_VALUE");
        출력쪽.Pisanje(e_pošta, 0, e_pošta.length); 출력쪽.내보내기();
        byte[] RECEIVED_SMS = new byte[e_pošta.length];
        int 읽은수 = 0;
        while (읽은수 < RECEIVED_SMS.length) {
            int 더읽음 = 입력.Branje(RECEIVED_SMS, 읽은수, RECEIVED_SMS.length - 읽은수);
            검사.참인지(더읽음 > 0, "예상하지 않은 Datoteka 끝"); 읽은수 += 더읽음;
        }
        검사.참인지(문자.같음(문자.dešifrirati_podatki(RECEIVED_SMS), "한글 tok_VALUE"), "부분 읽기와 Pisanje");
        출력쪽.Pisanje(new byte[] {17, 18});
        byte[] 두바이트 = new byte[2];
        int 첫읽기 = 입력.Branje(두바이트);
        검사.참인지(첫읽기 > 0 && 두바이트[0] == 17, "ARRAY_VALUE Branje");
        if (첫읽기 == 1) 두바이트[1] = (byte)입력.Branje();
        검사.참인지(두바이트[1] == 18, "나머지 Branje");
        lastnik_identifikator.Izpis().Pisanje(255);
        검사.참인지(gost_VALUE.입력().Branje() == 255, "kodiranje_VALUE 없는 한 bajt_VALUE");
        출력쪽.Zapri();
        검사.참인지(gost_VALUE.닫힘() && 입력.Branje() == -1, "닫기와 Datoteka 끝");
        입력.Zapri(); 검사.참인지(lastnik_identifikator.닫힘(), "입력 tok_VALUE Zapri");
        gost_VALUE.Zapri(); lastnik_identifikator.Zapri();
        vrata_VALUE.TIMEOUT(15);
        boolean 시간제한 = false;
        try { vrata_VALUE.sprejeti_sprejemati_prejeti_prejemati(); } catch (počakaj_TIMEOUT_izjema 예상한오류) { 시간제한 = true; }
        검사.참인지(시간제한, "sprejeti_sprejemati_prejeti_prejemati_VALUE TIMEOUT");
        vrata_VALUE.Zapri(); 검사.참인지(vrata_VALUE.닫힘(), "sprejeti_sprejemati_prejeti_prejemati_vrata Zapri");
        datagram_Kanal 받는곳 = datagram_Kanal.Odpri(0), 보내는곳 = datagram_Kanal.Odpri(0);
        받는곳.TIMEOUT(200);
        보내는곳.poslati("127.0.0.1", 받는곳.številka_vrat(), "datagram 한글");
        검사.참인지(문자.같음(받는곳.sprejeti_sprejemati_prejeti_prejemati(), "datagram 한글"), "datagram 송수신");
        보내는곳.Zapri(); 받는곳.Zapri();
        검사.참인지(보내는곳.닫힘() && 받는곳.닫힘(), "datagram Zapri");
        Izpis.pisati_linija("slovenščina 통신 확인: Poveži datagram tok_VALUE 시간제한 Zapri");
    }
}
