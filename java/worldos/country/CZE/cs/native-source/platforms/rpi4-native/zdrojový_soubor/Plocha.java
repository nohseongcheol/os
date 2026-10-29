// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 프레임버퍼 위의 작은 Provést_příkaz 화면. 입력은 UART의 TAB/ENTER/Q를 사용한다.
 * vlastní 5x7 영문 글꼴의 제한된 UI이며 Swing, USB HID, 한글 입력기는 아니다.
 */
public final class Plocha {
    static String 문자들 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+-.:";
    // 문자마다 7행 × 두 poziční_index 16진수. 프로젝트가 직접 정의한 5x7 písmo_HODNOTA.
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
    static int číslice_HODNOTA(int znak_HODNOTA) { return znak_HODNOTA <= '9' ? znak_HODNOTA - '0' : znak_HODNOTA - 'A' + 10; }
    static void text(int 가로, int Svislá_pozice, String Obsah_HODNOTA, int 색) {
        for (int znak_HODNOTA = 0; znak_HODNOTA < Obsah_HODNOTA.length(); znak_HODNOTA++) {
            int 찾음 = -1;
            for (int 후보 = 0; 후보 < 문자들.length(); 후보++) if (문자들.charAt(후보) == Obsah_HODNOTA.charAt(znak_HODNOTA)) 찾음 = 후보;
            if (찾음 < 0) continue;
            for (int ŘÁDEK_HODNOTA = 0; ŘÁDEK_HODNOTA < 7; ŘÁDEK_HODNOTA++) {
                int pozice = 찾음 * 14 + ŘÁDEK_HODNOTA * 2;
                int bit_HODNOTA = číslice_HODNOTA(모양들.charAt(pozice)) * 16 + číslice_HODNOTA(모양들.charAt(pozice + 1));
                for (int SLOUPEC_HODNOTA = 0; SLOUPEC_HODNOTA < 5; SLOUPEC_HODNOTA++) if ((bit_HODNOTA & (16 >> SLOUPEC_HODNOTA)) != 0)
                    jádro.obdélník(가로 + znak_HODNOTA * 12 + SLOUPEC_HODNOTA * 2, Svislá_pozice + ŘÁDEK_HODNOTA * 2, 2, 2, 색);
            }
        }
    }
    static void 그리기(int výběr_HODNOTA, String Stav_HODNOTA) {
        jádro.obdélník(0, 0, Panel.화면너비(), Panel.화면높이(), 0x302018);
        jádro.obdélník(32, 24, 576, 432, 0xefe8e2);
        jádro.obdélník(32, 24, 576, 48, 0x905020);
        text(52, 40, "JKOROS PROGRAMS", 0xffffff);
        for (int INDEX = 0; INDEX < 5; INDEX++) {
            jádro.obdélník(64, 112 + INDEX * 52, 512, 40, INDEX == výběr_HODNOTA ? 0xd0a040 : 0xd8d0c8);
            text(84, 128 + INDEX * 52, INDEX == 0 ? "RUN C++ FILE PROGRAM" : INDEX == 1 ? "RUN UDP LOOPBACK" : INDEX == 2 ? "COMPILE AND RUN JAVA" : INDEX == 3 ? "RUN MICROPYTHON" : "OPEN TERMINAL", 0x201810);
        }
        text(68, 384, Stav_HODNOTA, 0x205020);
        text(52, 420, "TAB SELECT  ENTER RUN  Q EXIT", 0x302018);
    }
    public static void Provést_příkaz() {
        if (Panel.화면준비() == 0) { 단말.Zápis("GUI unavailable\n"); return; }
        int výběr_HODNOTA = 0;
        String Stav_HODNOTA = "READY";
        boolean Předchozí_čára = příkaz_interpret.Předchozí_čára;
        그리기(výběr_HODNOTA, Stav_HODNOTA);
        단말.Zápis("GUI READY: UART TAB selects, ENTER runs, Q exits\n");
        while (true) {
            int vstup_HODNOTA = Panel.직렬읽기();
            if (vstup_HODNOTA < 0) { Panel.YIELD_CPU(); continue; }
            if (vstup_HODNOTA == 10 && Předchozí_čára) { Předchozí_čára = false; continue; }
            Předchozí_čára = vstup_HODNOTA == 13;
            if (vstup_HODNOTA >= '1' && vstup_HODNOTA <= '5') { výběr_HODNOTA = vstup_HODNOTA - '1'; vstup_HODNOTA = 13; }
            if (vstup_HODNOTA == 't' || vstup_HODNOTA == 'T') { příkaz_interpret.interpret_příkazů(false); return; }
            if (vstup_HODNOTA == 'q' || vstup_HODNOTA == 'Q' || vstup_HODNOTA == 27) break;
            if (vstup_HODNOTA == 9 || vstup_HODNOTA == 'j') {
                výběr_HODNOTA = (výběr_HODNOTA + 1) % 5; 그리기(výběr_HODNOTA, Stav_HODNOTA); 단말.Zápis("GUI FOCUS "); 단말.číslo(výběr_HODNOTA); 단말.문자(10);
            } else if (vstup_HODNOTA == 13 || vstup_HODNOTA == 10) {
                if (výběr_HODNOTA == 4) { příkaz_interpret.interpret_příkazů(false); return; }
                int VÝSLEDEK;
                if (výběr_HODNOTA < 2) VÝSLEDEK = Panel.spustit_uživatel_program(výběr_HODNOTA == 0 ? 0 : 9);
                else if (výběr_HODNOTA == 2) {
                    VÝSLEDEK = příkaz_interpret.예제실행(10, "Hello.java");
                    if (VÝSLEDEK == 0) VÝSLEDEK = příkaz_interpret.예제실행(11, "Hello");
                } else VÝSLEDEK = příkaz_interpret.예제실행(12, "hello.py");
                Stav_HODNOTA = VÝSLEDEK != 0 ? "PROGRAM FAILED" : výběr_HODNOTA == 0 ? "C++ FILE OK" : výběr_HODNOTA == 1 ? "UDP LOOPBACK OK" : výběr_HODNOTA == 2 ? "JAVA OK" : "MICROPYTHON OK";
                그리기(výběr_HODNOTA, Stav_HODNOTA);
                단말.Zápis("GUI ACTION "); 단말.číslo(výběr_HODNOTA); 단말.Zápis(" RESULT "); 단말.číslo(VÝSLEDEK); 단말.문자(10);
            }
        }
        jádro.화면();
        단말.Zápis("GUI EXIT\n");
    }
}
