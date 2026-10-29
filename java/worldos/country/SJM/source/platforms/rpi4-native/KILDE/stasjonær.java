// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 프레임버퍼 위의 작은 Utfør_kommando skjermbilde. 입력은 UART의 TAB/ENTER/Q를 사용한다.
 * eget 5x7 영문 글꼴의 제한된 UI이며 Swing, USB HID, 한글 입력기는 아니다.
 */
public final class stasjonær {
    static String 문자들 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+-.:";
    // 문자마다 7행 × 두 posisjonsindeks 16진수. 프로젝트가 직접 정의한 5x7 skrift_VERDI.
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
    static int siffer_VERDI(int tegn_VERDI) { return tegn_VERDI <= '9' ? tegn_VERDI - '0' : tegn_VERDI - 'A' + 10; }
    static void Tekst(int 가로, int vertikal_plassere, String Innhold_VERDI, int 색) {
        for (int tegn_VERDI = 0; tegn_VERDI < Innhold_VERDI.length(); tegn_VERDI++) {
            int 찾음 = -1;
            for (int 후보 = 0; 후보 < 문자들.length(); 후보++) if (문자들.charAt(후보) == Innhold_VERDI.charAt(tegn_VERDI)) 찾음 = 후보;
            if (찾음 < 0) continue;
            for (int RAD_VERDI = 0; RAD_VERDI < 7; RAD_VERDI++) {
                int Posisjon = 찾음 * 14 + RAD_VERDI * 2;
                int bit_VERDI = siffer_VERDI(모양들.charAt(Posisjon)) * 16 + siffer_VERDI(모양들.charAt(Posisjon + 1));
                for (int spalte_VERDI = 0; spalte_VERDI < 5; spalte_VERDI++) if ((bit_VERDI & (16 >> spalte_VERDI)) != 0)
                    kjerne.rektangel(가로 + tegn_VERDI * 12 + spalte_VERDI * 2, vertikal_plassere + RAD_VERDI * 2, 2, 2, 색);
            }
        }
    }
    static void Paint_skjermbilde(int merket_område_VERDI, String status_VERDI) {
        kjerne.rektangel(0, 0, Tavle.화면너비(), Tavle.화면높이(), 0x302018);
        kjerne.rektangel(32, 24, 576, 432, 0xefe8e2);
        kjerne.rektangel(32, 24, 576, 48, 0x905020);
        Tekst(52, 40, "JKOROS PROGRAMS", 0xffffff);
        for (int INDEKS = 0; INDEKS < 5; INDEKS++) {
            kjerne.rektangel(64, 112 + INDEKS * 52, 512, 40, INDEKS == merket_område_VERDI ? 0xd0a040 : 0xd8d0c8);
            Tekst(84, 128 + INDEKS * 52, INDEKS == 0 ? "RUN C++ FILE PROGRAM" : INDEKS == 1 ? "RUN UDP LOOPBACK" : INDEKS == 2 ? "COMPILE AND RUN JAVA" : INDEKS == 3 ? "RUN MICROPYTHON" : "OPEN TERMINAL", 0x201810);
        }
        Tekst(68, 384, status_VERDI, 0x205020);
        Tekst(52, 420, "TAB SELECT  ENTER RUN  Q EXIT", 0x302018);
    }
    public static void Utfør_kommando() {
        if (Tavle.Forbered_skjermbilde() == 0) { 단말.Skriv("GUI unavailable\n"); return; }
        int merket_område_VERDI = 0;
        String status_VERDI = "READY";
        boolean Forrige_linje = 명령해석기.Forrige_linje;
        Paint_skjermbilde(merket_område_VERDI, status_VERDI);
        단말.Skriv("GUI READY: UART TAB selects, ENTER runs, Q exits\n");
        while (true) {
            int inndata_VERDI = Tavle.직렬읽기();
            if (inndata_VERDI < 0) { Tavle.AVKAST_CPU(); continue; }
            if (inndata_VERDI == 10 && Forrige_linje) { Forrige_linje = false; continue; }
            Forrige_linje = inndata_VERDI == 13;
            if (inndata_VERDI >= '1' && inndata_VERDI <= '5') { merket_område_VERDI = inndata_VERDI - '1'; inndata_VERDI = 13; }
            if (inndata_VERDI == 't' || inndata_VERDI == 'T') { 명령해석기.Terminal(false); return; }
            if (inndata_VERDI == 'q' || inndata_VERDI == 'Q' || inndata_VERDI == 27) break;
            if (inndata_VERDI == 9 || inndata_VERDI == 'j') {
                merket_område_VERDI = (merket_område_VERDI + 1) % 5; Paint_skjermbilde(merket_område_VERDI, status_VERDI); 단말.Skriv("GUI FOCUS "); 단말.nummer(merket_område_VERDI); 단말.문자(10);
            } else if (inndata_VERDI == 13 || inndata_VERDI == 10) {
                if (merket_område_VERDI == 4) { 명령해석기.Terminal(false); return; }
                int KR;
                if (merket_område_VERDI < 2) KR = Tavle.kjøre_bruker_app(merket_område_VERDI == 0 ? 0 : 9);
                else if (merket_område_VERDI == 2) {
                    KR = 명령해석기.예제실행(10, "Hello.java");
                    if (KR == 0) KR = 명령해석기.예제실행(11, "Hello");
                } else KR = 명령해석기.예제실행(12, "hello.py");
                status_VERDI = KR != 0 ? "PROGRAM FAILED" : merket_område_VERDI == 0 ? "C++ FILE OK" : merket_område_VERDI == 1 ? "UDP LOOPBACK OK" : merket_område_VERDI == 2 ? "JAVA OK" : "MICROPYTHON OK";
                Paint_skjermbilde(merket_område_VERDI, status_VERDI);
                단말.Skriv("GUI ACTION "); 단말.nummer(merket_område_VERDI); 단말.Skriv(" RESULT "); 단말.nummer(KR); 단말.문자(10);
            }
        }
        kjerne.skjermbilde();
        단말.Skriv("GUI EXIT\n");
    }
}
