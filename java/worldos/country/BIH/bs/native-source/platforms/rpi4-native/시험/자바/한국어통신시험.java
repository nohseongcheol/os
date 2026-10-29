// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.*;

/** 동일 바이트코드를 OpenJDK와 자체 JVM에서 실행하는 통신 계약 시험. */
public class 한국어통신시험 {
    public static void main(String[] Argumenti) throws U_I_izuzetak {
        수신창구 port_VALUE = 연결통신.수신열기(0);
        veza gost_VALUE = 연결통신.Otvori("127.0.0.1", port_VALUE.broj_priključka());
        veza vlasnik_identifikator = port_VALUE.받기();
        gost_VALUE.TIMEOUT(200); vlasnik_identifikator.TIMEOUT(200);
        검사.참인지(gost_VALUE.연결됨() && !gost_VALUE.닫힘(), "Spoji_se stanje_VALUE");
        검사.참인지(vlasnik_identifikator.broj_priključka() == gost_VALUE.lokalni_broj_priključka(), "peer_VALUE broj_priključka");
        검사.참인지(gost_VALUE.broj_priključka() == vlasnik_identifikator.lokalni_broj_priključka(), "lokalni_opseg broj_priključka");
        입력흐름 입력 = vlasnik_identifikator.입력(); 출력흐름 출력쪽 = gost_VALUE.Ispis();
        byte[] poruka = 문자.부호화("한글 tok_VALUE");
        출력쪽.Piši(poruka, 0, poruka.length); 출력쪽.내보내기();
        byte[] RECEIVED_SMS = new byte[poruka.length];
        int 읽은수 = 0;
        while (읽은수 < RECEIVED_SMS.length) {
            int 더읽음 = 입력.Čitaj(RECEIVED_SMS, 읽은수, RECEIVED_SMS.length - 읽은수);
            검사.참인지(더읽음 > 0, "예상하지 않은 Fajl 끝"); 읽은수 += 더읽음;
        }
        검사.참인지(문자.같음(문자.dešifrirati_podaci(RECEIVED_SMS), "한글 tok_VALUE"), "부분 읽기와 Piši");
        출력쪽.Piši(new byte[] {17, 18});
        byte[] 두바이트 = new byte[2];
        int 첫읽기 = 입력.Čitaj(두바이트);
        검사.참인지(첫읽기 > 0 && 두바이트[0] == 17, "niz_VALUE Čitaj");
        if (첫읽기 == 1) 두바이트[1] = (byte)입력.Čitaj();
        검사.참인지(두바이트[1] == 18, "나머지 Čitaj");
        vlasnik_identifikator.Ispis().Piši(255);
        검사.참인지(gost_VALUE.입력().Čitaj() == 255, "kodiranje_VALUE 없는 한 bajt_VALUE");
        출력쪽.Zatvori();
        검사.참인지(gost_VALUE.닫힘() && 입력.Čitaj() == -1, "닫기와 Fajl 끝");
        입력.Zatvori(); 검사.참인지(vlasnik_identifikator.닫힘(), "입력 tok_VALUE Zatvori");
        gost_VALUE.Zatvori(); vlasnik_identifikator.Zatvori();
        port_VALUE.TIMEOUT(15);
        boolean 시간제한 = false;
        try { port_VALUE.받기(); } catch (čekaj_TIMEOUT_izuzetak 예상한오류) { 시간제한 = true; }
        검사.참인지(시간제한, "수신 TIMEOUT");
        port_VALUE.Zatvori(); 검사.참인지(port_VALUE.닫힘(), "수신창구 Zatvori");
        전문통로 받는곳 = 전문통로.Otvori(0), 보내는곳 = 전문통로.Otvori(0);
        받는곳.TIMEOUT(200);
        보내는곳.poslati("127.0.0.1", 받는곳.broj_priključka(), "전문 한글");
        검사.참인지(문자.같음(받는곳.받기(), "전문 한글"), "전문 송수신");
        보내는곳.Zatvori(); 받는곳.Zatvori();
        검사.참인지(보내는곳.닫힘() && 받는곳.닫힘(), "전문 Zatvori");
        Ispis.pisati_redak("한국어 통신 potvrditi: Spoji_se 전문 tok_VALUE 시간제한 Zatvori");
    }
}
