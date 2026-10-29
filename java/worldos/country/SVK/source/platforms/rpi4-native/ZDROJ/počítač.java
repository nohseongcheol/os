// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 프레임버퍼 위의 작은 Vykonať_príkaz 화면. 입력은 UART의 TAB/ENTER/Q를 사용한다.
 * vlastné 5x7 영문 글꼴의 제한된 UI이며 Swing, USB HID, 한글 입력기는 아니다.
 */
public final class počítač {
    static String 문자들 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+-.:";
    // 문자마다 7행 × 두 pozičný_index 16진수. 프로젝트가 직접 정의한 5x7 písmo_VALUE.
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
    static int číslica_VALUE(int znak_VALUE) { return znak_VALUE <= '9' ? znak_VALUE - '0' : znak_VALUE - 'A' + 10; }
    static void Spracovanie_textu(int 가로, int vertikála_pozícia, String obsah_VALUE, int 색) {
        for (int znak_VALUE = 0; znak_VALUE < obsah_VALUE.length(); znak_VALUE++) {
            int 찾음 = -1;
            for (int 후보 = 0; 후보 < 문자들.length(); 후보++) if (문자들.charAt(후보) == obsah_VALUE.charAt(znak_VALUE)) 찾음 = 후보;
            if (찾음 < 0) continue;
            for (int ROW_VALUE = 0; ROW_VALUE < 7; ROW_VALUE++) {
                int Pozícia = 찾음 * 14 + ROW_VALUE * 2;
                int Bit_VALUE = číslica_VALUE(모양들.charAt(Pozícia)) * 16 + číslica_VALUE(모양들.charAt(Pozícia + 1));
                for (int COLUMN_VALUE = 0; COLUMN_VALUE < 5; COLUMN_VALUE++) if ((Bit_VALUE & (16 >> COLUMN_VALUE)) != 0)
                    jadro.obdĺžnik(가로 + znak_VALUE * 12 + COLUMN_VALUE * 2, vertikála_pozícia + ROW_VALUE * 2, 2, 2, 색);
            }
        }
    }
    static void 그리기(int výber_VALUE, String Stav_VALUE) {
        jadro.obdĺžnik(0, 0, Panel.화면너비(), Panel.화면높이(), 0x302018);
        jadro.obdĺžnik(32, 24, 576, 432, 0xefe8e2);
        jadro.obdĺžnik(32, 24, 576, 48, 0x905020);
        Spracovanie_textu(52, 40, "JKOROS PROGRAMS", 0xffffff);
        for (int INDEX = 0; INDEX < 5; INDEX++) {
            jadro.obdĺžnik(64, 112 + INDEX * 52, 512, 40, INDEX == výber_VALUE ? 0xd0a040 : 0xd8d0c8);
            Spracovanie_textu(84, 128 + INDEX * 52, INDEX == 0 ? "RUN C++ FILE PROGRAM" : INDEX == 1 ? "RUN UDP LOOPBACK" : INDEX == 2 ? "COMPILE AND RUN JAVA" : INDEX == 3 ? "RUN MICROPYTHON" : "OPEN TERMINAL", 0x201810);
        }
        Spracovanie_textu(68, 384, Stav_VALUE, 0x205020);
        Spracovanie_textu(52, 420, "TAB SELECT  ENTER RUN  Q EXIT", 0x302018);
    }
    public static void Vykonať_príkaz() {
        if (Panel.화면준비() == 0) { 단말.Zápis("GUI unavailable\n"); return; }
        int výber_VALUE = 0;
        String Stav_VALUE = "READY";
        boolean 앞줄 = 명령해석기.앞줄;
        그리기(výber_VALUE, Stav_VALUE);
        단말.Zápis("GUI READY: UART TAB selects, ENTER runs, Q exits\n");
        while (true) {
            int vstup_VALUE = Panel.직렬읽기();
            if (vstup_VALUE < 0) { Panel.YIELD_procesor(); continue; }
            if (vstup_VALUE == 10 && 앞줄) { 앞줄 = false; continue; }
            앞줄 = vstup_VALUE == 13;
            if (vstup_VALUE >= '1' && vstup_VALUE <= '5') { výber_VALUE = vstup_VALUE - '1'; vstup_VALUE = 13; }
            if (vstup_VALUE == 't' || vstup_VALUE == 'T') { 명령해석기.Terminál(false); return; }
            if (vstup_VALUE == 'q' || vstup_VALUE == 'Q' || vstup_VALUE == 27) break;
            if (vstup_VALUE == 9 || vstup_VALUE == 'j') {
                výber_VALUE = (výber_VALUE + 1) % 5; 그리기(výber_VALUE, Stav_VALUE); 단말.Zápis("GUI FOCUS "); 단말.수(výber_VALUE); 단말.문자(10);
            } else if (vstup_VALUE == 13 || vstup_VALUE == 10) {
                if (výber_VALUE == 4) { 명령해석기.Terminál(false); return; }
                int KR;
                if (výber_VALUE < 2) KR = Panel.spustiť_používateľ_program(výber_VALUE == 0 ? 0 : 9);
                else if (výber_VALUE == 2) {
                    KR = 명령해석기.예제실행(10, "Hello.java");
                    if (KR == 0) KR = 명령해석기.예제실행(11, "Hello");
                } else KR = 명령해석기.예제실행(12, "hello.py");
                Stav_VALUE = KR != 0 ? "PROGRAM FAILED" : výber_VALUE == 0 ? "C++ FILE OK" : výber_VALUE == 1 ? "UDP LOOPBACK OK" : výber_VALUE == 2 ? "JAVA OK" : "MICROPYTHON OK";
                그리기(výber_VALUE, Stav_VALUE);
                단말.Zápis("GUI ACTION "); 단말.수(výber_VALUE); 단말.Zápis(" RESULT "); 단말.수(KR); 단말.문자(10);
            }
        }
        jadro.화면();
        단말.Zápis("GUI EXIT\n");
    }
}
