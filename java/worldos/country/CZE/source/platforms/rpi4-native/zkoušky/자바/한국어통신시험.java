// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import čeština.vlastní.*;

/** 동일 바이트코드를 OpenJDK와 vlastní JVM에서 실행하는 komunikace 계약 zkoušky. */
public class 한국어통신시험 {
    public static void main(String[] argumenty) throws vstup_a_výstup_výjimka {
        dostat_port port_HODNOTA = kontakt_přenos.수신열기(0);
        kontakt host_HODNOTA = kontakt_přenos.Otevřít("127.0.0.1", port_HODNOTA.číslo_portu());
        kontakt vlastník_identifikátor = port_HODNOTA.dostat();
        host_HODNOTA.TIMEOUT(200); vlastník_identifikátor.TIMEOUT(200);
        검사.참인지(host_HODNOTA.연결됨() && !host_HODNOTA.informační_systémy_uzavřeno(), "Připojit Stav_HODNOTA");
        검사.참인지(vlastník_identifikátor.číslo_portu() == host_HODNOTA.místní_číslo_portu(), "partner_HODNOTA číslo_portu");
        검사.참인지(host_HODNOTA.číslo_portu() == vlastník_identifikátor.místní_číslo_portu(), "místní_obor číslo_portu");
        vstupní_datový_proud vstup_HODNOTA = vlastník_identifikátor.vstup_HODNOTA(); výstupní_datový_proud výstup_stránka = host_HODNOTA.výstupní_pozice();
        byte[] e_mail = 문자.kódovat("한글 tok_HODNOTA");
        výstup_stránka.Zápis(e_mail, 0, e_mail.length); výstup_stránka.내보내기();
        byte[] RECEIVED_SMS = new byte[e_mail.length];
        int 읽은수 = 0;
        while (읽은수 < RECEIVED_SMS.length) {
            int 더읽음 = vstup_HODNOTA.Čtení(RECEIVED_SMS, 읽은수, RECEIVED_SMS.length - 읽은수);
            검사.참인지(더읽음 > 0, "예상하지 않은 název_souboru 끝"); 읽은수 += 더읽음;
        }
        검사.참인지(문자.같음(문자.dešifrovat_data(RECEIVED_SMS), "한글 tok_HODNOTA"), "부분 읽기와 Zápis");
        výstup_stránka.Zápis(new byte[] {17, 18});
        byte[] 두바이트 = new byte[2];
        int 첫읽기 = vstup_HODNOTA.Čtení(두바이트);
        검사.참인지(첫읽기 > 0 && 두바이트[0] == 17, "pole_HODNOTA Čtení");
        if (첫읽기 == 1) 두바이트[1] = (byte)vstup_HODNOTA.Čtení();
        검사.참인지(두바이트[1] == 18, "나머지 Čtení");
        vlastník_identifikátor.výstupní_pozice().Zápis(255);
        검사.참인지(host_HODNOTA.vstup_HODNOTA().Čtení() == 255, "Encoding_HODNOTA 없는 한 bajt_HODNOTA");
        výstup_stránka.Zavřené();
        검사.참인지(host_HODNOTA.informační_systémy_uzavřeno() && vstup_HODNOTA.Čtení() == -1, "닫기와 název_souboru 끝");
        vstup_HODNOTA.Zavřené(); 검사.참인지(vlastník_identifikátor.informační_systémy_uzavřeno(), "vstup_HODNOTA tok_HODNOTA Zavřené");
        host_HODNOTA.Zavřené(); vlastník_identifikátor.Zavřené();
        port_HODNOTA.TIMEOUT(15);
        boolean spuštění_TIMEOUT = false;
        try { port_HODNOTA.dostat(); } catch (počkej_TIMEOUT_výjimka 예상한오류) { spuštění_TIMEOUT = true; }
        검사.참인지(spuštění_TIMEOUT, "dostat_HODNOTA TIMEOUT");
        port_HODNOTA.Zavřené(); 검사.참인지(port_HODNOTA.informační_systémy_uzavřeno(), "dostat_port Zavřené");
        datagram_Kanál 받는곳 = datagram_Kanál.Otevřít(0), 보내는곳 = datagram_Kanál.Otevřít(0);
        받는곳.TIMEOUT(200);
        보내는곳.poslat("127.0.0.1", 받는곳.číslo_portu(), "datagram 한글");
        검사.참인지(문자.같음(받는곳.dostat(), "datagram 한글"), "datagram 송수신");
        보내는곳.Zavřené(); 받는곳.Zavřené();
        검사.참인지(보내는곳.informační_systémy_uzavřeno() && 받는곳.informační_systémy_uzavřeno(), "datagram Zavřené");
        výstupní_pozice.zápis_čára("čeština komunikace ověřit: Připojit datagram tok_HODNOTA spuštění_TIMEOUT Zavřené");
    }
}
