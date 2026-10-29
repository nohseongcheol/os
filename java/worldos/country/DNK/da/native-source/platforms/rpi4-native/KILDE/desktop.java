// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 프레임버퍼 위의 작은 Udfør_kommando skærmbillede. 입력은 UART의 TAB/ENTER/Q를 사용한다.
 * eget 5x7 영문 글꼴의 제한된 UI이며 Swing, USB HID, 한글 입력기는 아니다.
 */
public final class desktop {
    static String 문자들 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+-.:";
    // 문자마다 7행 × 두 positionsindeks 16진수. 프로젝트가 직접 정의한 5x7 skrifttype_VÆRDI.
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
    static int ciffer_VÆRDI(int tegn_VÆRDI) { return tegn_VÆRDI <= '9' ? tegn_VÆRDI - '0' : tegn_VÆRDI - 'A' + 10; }
    static void Tekst(int 가로, int Lodret_placere, String Indhold_VÆRDI, int 색) {
        for (int tegn_VÆRDI = 0; tegn_VÆRDI < Indhold_VÆRDI.length(); tegn_VÆRDI++) {
            int 찾음 = -1;
            for (int 후보 = 0; 후보 < 문자들.length(); 후보++) if (문자들.charAt(후보) == Indhold_VÆRDI.charAt(tegn_VÆRDI)) 찾음 = 후보;
            if (찾음 < 0) continue;
            for (int post_VÆRDI = 0; post_VÆRDI < 7; post_VÆRDI++) {
                int Placering = 찾음 * 14 + post_VÆRDI * 2;
                int bit_VÆRDI = ciffer_VÆRDI(모양들.charAt(Placering)) * 16 + ciffer_VÆRDI(모양들.charAt(Placering + 1));
                for (int KOLONNE_VÆRDI = 0; KOLONNE_VÆRDI < 5; KOLONNE_VÆRDI++) if ((bit_VÆRDI & (16 >> KOLONNE_VÆRDI)) != 0)
                    kerne.rektangel(가로 + tegn_VÆRDI * 12 + KOLONNE_VÆRDI * 2, Lodret_placere + post_VÆRDI * 2, 2, 2, 색);
            }
        }
    }
    static void Paint_skærmbillede(int markering_VÆRDI, String status_VÆRDI) {
        kerne.rektangel(0, 0, Tavle.화면너비(), Tavle.화면높이(), 0x302018);
        kerne.rektangel(32, 24, 576, 432, 0xefe8e2);
        kerne.rektangel(32, 24, 576, 48, 0x905020);
        Tekst(52, 40, "JKOROS PROGRAMS", 0xffffff);
        for (int INDEKS = 0; INDEKS < 5; INDEKS++) {
            kerne.rektangel(64, 112 + INDEKS * 52, 512, 40, INDEKS == markering_VÆRDI ? 0xd0a040 : 0xd8d0c8);
            Tekst(84, 128 + INDEKS * 52, INDEKS == 0 ? "RUN C++ FILE PROGRAM" : INDEKS == 1 ? "RUN UDP LOOPBACK" : INDEKS == 2 ? "COMPILE AND RUN JAVA" : INDEKS == 3 ? "RUN MICROPYTHON" : "OPEN TERMINAL", 0x201810);
        }
        Tekst(68, 384, status_VÆRDI, 0x205020);
        Tekst(52, 420, "TAB SELECT  ENTER RUN  Q EXIT", 0x302018);
    }
    public static void Udfør_kommando() {
        if (Tavle.Tilrettelæg_skærmbillede() == 0) { 단말.Skrive("GUI unavailable\n"); return; }
        int markering_VÆRDI = 0;
        String status_VÆRDI = "READY";
        boolean Forrige_linje = 명령해석기.Forrige_linje;
        Paint_skærmbillede(markering_VÆRDI, status_VÆRDI);
        단말.Skrive("GUI READY: UART TAB selects, ENTER runs, Q exits\n");
        while (true) {
            int input_VÆRDI = Tavle.직렬읽기();
            if (input_VÆRDI < 0) { Tavle.AFKAST_CPU(); continue; }
            if (input_VÆRDI == 10 && Forrige_linje) { Forrige_linje = false; continue; }
            Forrige_linje = input_VÆRDI == 13;
            if (input_VÆRDI >= '1' && input_VÆRDI <= '5') { markering_VÆRDI = input_VÆRDI - '1'; input_VÆRDI = 13; }
            if (input_VÆRDI == 't' || input_VÆRDI == 'T') { 명령해석기.Terminal(false); return; }
            if (input_VÆRDI == 'q' || input_VÆRDI == 'Q' || input_VÆRDI == 27) break;
            if (input_VÆRDI == 9 || input_VÆRDI == 'j') {
                markering_VÆRDI = (markering_VÆRDI + 1) % 5; Paint_skærmbillede(markering_VÆRDI, status_VÆRDI); 단말.Skrive("GUI FOCUS "); 단말.tal(markering_VÆRDI); 단말.문자(10);
            } else if (input_VÆRDI == 13 || input_VÆRDI == 10) {
                if (markering_VÆRDI == 4) { 명령해석기.Terminal(false); return; }
                int KR;
                if (markering_VÆRDI < 2) KR = Tavle.køre_bruger_app(markering_VÆRDI == 0 ? 0 : 9);
                else if (markering_VÆRDI == 2) {
                    KR = 명령해석기.예제실행(10, "Hello.java");
                    if (KR == 0) KR = 명령해석기.예제실행(11, "Hello");
                } else KR = 명령해석기.예제실행(12, "hello.py");
                status_VÆRDI = KR != 0 ? "PROGRAM FAILED" : markering_VÆRDI == 0 ? "C++ FILE OK" : markering_VÆRDI == 1 ? "UDP LOOPBACK OK" : markering_VÆRDI == 2 ? "JAVA OK" : "MICROPYTHON OK";
                Paint_skærmbillede(markering_VÆRDI, status_VÆRDI);
                단말.Skrive("GUI ACTION "); 단말.tal(markering_VÆRDI); 단말.Skrive(" RESULT "); 단말.tal(KR); 단말.문자(10);
            }
        }
        kerne.skærmbillede();
        단말.Skrive("GUI EXIT\n");
    }
}
