// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 프레임버퍼 위의 작은 Suorita_komento 화면. 입력은 UART의 TAB/ENTER/Q를 사용한다.
 * oma 5x7 영문 글꼴의 제한된 UI이며 Swing, USB HID, 한글 입력기는 아니다.
 */
public final class työpöytä {
    static String 문자들 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+-.:";
    // 문자마다 7행 × 두 sijainti 16진수. 프로젝트가 직접 정의한 5x7 fontti_ARVO.
    static String 모양들 =
        "0E11111F111111" + "1E11111E11111E" + "0F10101010100F" + "1E11111111111E" +
        "1F10101E10101F" + "1F10101E101010" + "0F10101711110F" + "1111111F111111" +
        "0E04040404040E" + "0702020212120C" + "11121418141211" + "1010101010101F" +
        "111B1515111111" + "11191915131311" + "0E11111111110E" + "1E11111E101010" +
        "0E11111115120D" + "1E11111E141211" + "0F10100E01011E" + "1F040404040404" +
        "1111111111110E" + "11111111110A04" + "11111115151B11" + "11110A040A1111" +
        "11110A04040404" + "1F01020408101F" + "0E11131519110E" + "040C040404040E" +
        "0E11010204081F" + "1E01010601011E" + "02060A121F0202" + "1F10101E01011E" +
        "0E10101E11110E" + "1F010204080808" + "0E11110E11110E" + "0E11110F01010E" +
        "0004041F040400" + "0000001F000000" + "00000000000C0C" + "000C0C000C0C00";
    static int numero_ARVO(int merkki_ARVO) { return merkki_ARVO <= '9' ? merkki_ARVO - '0' : merkki_ARVO - 'A' + 10; }
    static void teksti(int 가로, int toimiala_toimi, String Sisältö_ARVO, int 색) {
        for (int merkki_ARVO = 0; merkki_ARVO < Sisältö_ARVO.length(); merkki_ARVO++) {
            int 찾음 = -1;
            for (int 후보 = 0; 후보 < 문자들.length(); 후보++) if (문자들.charAt(후보) == Sisältö_ARVO.charAt(merkki_ARVO)) 찾음 = 후보;
            if (찾음 < 0) continue;
            for (int RIVI_ARVO = 0; RIVI_ARVO < 7; RIVI_ARVO++) {
                int paikka = 찾음 * 14 + RIVI_ARVO * 2;
                int bitti_ARVO = numero_ARVO(모양들.charAt(paikka)) * 16 + numero_ARVO(모양들.charAt(paikka + 1));
                for (int SARAKE_ARVO = 0; SARAKE_ARVO < 5; SARAKE_ARVO++) if ((bitti_ARVO & (16 >> SARAKE_ARVO)) != 0)
                    ydin.suorakulmio(가로 + merkki_ARVO * 12 + SARAKE_ARVO * 2, toimiala_toimi + RIVI_ARVO * 2, 2, 2, 색);
            }
        }
    }
    static void 그리기(int valinta_ARVO, String Tila_ARVO) {
        ydin.suorakulmio(0, 0, Taulu.화면너비(), Taulu.화면높이(), 0x302018);
        ydin.suorakulmio(32, 24, 576, 432, 0xefe8e2);
        ydin.suorakulmio(32, 24, 576, 48, 0x905020);
        teksti(52, 40, "JKOROS PROGRAMS", 0xffffff);
        for (int INDEKSI = 0; INDEKSI < 5; INDEKSI++) {
            ydin.suorakulmio(64, 112 + INDEKSI * 52, 512, 40, INDEKSI == valinta_ARVO ? 0xd0a040 : 0xd8d0c8);
            teksti(84, 128 + INDEKSI * 52, INDEKSI == 0 ? "RUN C++ FILE PROGRAM" : INDEKSI == 1 ? "RUN UDP LOOPBACK" : INDEKSI == 2 ? "COMPILE AND RUN JAVA" : INDEKSI == 3 ? "RUN MICROPYTHON" : "OPEN TERMINAL", 0x201810);
        }
        teksti(68, 384, Tila_ARVO, 0x205020);
        teksti(52, 420, "TAB SELECT  ENTER RUN  Q EXIT", 0x302018);
    }
    public static void Suorita_komento() {
        if (Taulu.화면준비() == 0) { 단말.Kirjoitus("GUI unavailable\n"); return; }
        int valinta_ARVO = 0;
        String Tila_ARVO = "READY";
        boolean Edellinen_rivi = 명령해석기.Edellinen_rivi;
        그리기(valinta_ARVO, Tila_ARVO);
        단말.Kirjoitus("GUI READY: UART TAB selects, ENTER runs, Q exits\n");
        while (true) {
            int syöte_ARVO = Taulu.직렬읽기();
            if (syöte_ARVO < 0) { Taulu.TUOTTO_suoritin(); continue; }
            if (syöte_ARVO == 10 && Edellinen_rivi) { Edellinen_rivi = false; continue; }
            Edellinen_rivi = syöte_ARVO == 13;
            if (syöte_ARVO >= '1' && syöte_ARVO <= '5') { valinta_ARVO = syöte_ARVO - '1'; syöte_ARVO = 13; }
            if (syöte_ARVO == 't' || syöte_ARVO == 'T') { 명령해석기.komentotulkki(false); return; }
            if (syöte_ARVO == 'q' || syöte_ARVO == 'Q' || syöte_ARVO == 27) break;
            if (syöte_ARVO == 9 || syöte_ARVO == 'j') {
                valinta_ARVO = (valinta_ARVO + 1) % 5; 그리기(valinta_ARVO, Tila_ARVO); 단말.Kirjoitus("GUI FOCUS "); 단말.numero(valinta_ARVO); 단말.문자(10);
            } else if (syöte_ARVO == 13 || syöte_ARVO == 10) {
                if (valinta_ARVO == 4) { 명령해석기.komentotulkki(false); return; }
                int TULOS;
                if (valinta_ARVO < 2) TULOS = Taulu.suorittaa_käyttäjä_ohjelma(valinta_ARVO == 0 ? 0 : 9);
                else if (valinta_ARVO == 2) {
                    TULOS = 명령해석기.예제실행(10, "Hello.java");
                    if (TULOS == 0) TULOS = 명령해석기.예제실행(11, "Hello");
                } else TULOS = 명령해석기.예제실행(12, "hello.py");
                Tila_ARVO = TULOS != 0 ? "PROGRAM FAILED" : valinta_ARVO == 0 ? "C++ FILE OK" : valinta_ARVO == 1 ? "UDP LOOPBACK OK" : valinta_ARVO == 2 ? "JAVA OK" : "MICROPYTHON OK";
                그리기(valinta_ARVO, Tila_ARVO);
                단말.Kirjoitus("GUI ACTION "); 단말.numero(valinta_ARVO); 단말.Kirjoitus(" RESULT "); 단말.numero(TULOS); 단말.문자(10);
            }
        }
        ydin.화면();
        단말.Kirjoitus("GUI EXIT\n");
    }
}
