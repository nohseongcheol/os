// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 프레임버퍼 위의 작은 Izvrši_naredba 화면. 입력은 UART의 TAB/ENTER/Q를 사용한다.
 * vlastiti 5x7 영문 글꼴의 제한된 UI이며 Swing, USB HID, 한글 입력기는 아니다.
 */
public final class stolni {
    static String 문자들 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+-.:";
    // 문자마다 7행 × 두 indeks_položaja 16진수. 프로젝트가 직접 정의한 5x7 font_VALUE.
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
    static int znamenka_VALUE(int znak_VALUE) { return znak_VALUE <= '9' ? znak_VALUE - '0' : znak_VALUE - 'A' + 10; }
    static void Tekst(int 가로, int Okomito_položaj, String Sadržaj_VALUE, int 색) {
        for (int znak_VALUE = 0; znak_VALUE < Sadržaj_VALUE.length(); znak_VALUE++) {
            int 찾음 = -1;
            for (int 후보 = 0; 후보 < 문자들.length(); 후보++) if (문자들.charAt(후보) == Sadržaj_VALUE.charAt(znak_VALUE)) 찾음 = 후보;
            if (찾음 < 0) continue;
            for (int ROW_VALUE = 0; ROW_VALUE < 7; ROW_VALUE++) {
                int Položaj = 찾음 * 14 + ROW_VALUE * 2;
                int bit_VALUE = znamenka_VALUE(모양들.charAt(Položaj)) * 16 + znamenka_VALUE(모양들.charAt(Položaj + 1));
                for (int COLUMN_VALUE = 0; COLUMN_VALUE < 5; COLUMN_VALUE++) if ((bit_VALUE & (16 >> COLUMN_VALUE)) != 0)
                    jezgra_sustava.pravokutnik(가로 + znak_VALUE * 12 + COLUMN_VALUE * 2, Okomito_položaj + ROW_VALUE * 2, 2, 2, 색);
            }
        }
    }
    static void 그리기(int odabir_VALUE, String Stanje_VALUE) {
        jezgra_sustava.pravokutnik(0, 0, pano.화면너비(), pano.화면높이(), 0x302018);
        jezgra_sustava.pravokutnik(32, 24, 576, 432, 0xefe8e2);
        jezgra_sustava.pravokutnik(32, 24, 576, 48, 0x905020);
        Tekst(52, 40, "JKOROS PROGRAMS", 0xffffff);
        for (int INDEX = 0; INDEX < 5; INDEX++) {
            jezgra_sustava.pravokutnik(64, 112 + INDEX * 52, 512, 40, INDEX == odabir_VALUE ? 0xd0a040 : 0xd8d0c8);
            Tekst(84, 128 + INDEX * 52, INDEX == 0 ? "RUN C++ FILE PROGRAM" : INDEX == 1 ? "RUN UDP LOOPBACK" : INDEX == 2 ? "COMPILE AND RUN JAVA" : INDEX == 3 ? "RUN MICROPYTHON" : "OPEN TERMINAL", 0x201810);
        }
        Tekst(68, 384, Stanje_VALUE, 0x205020);
        Tekst(52, 420, "TAB SELECT  ENTER RUN  Q EXIT", 0x302018);
    }
    public static void Izvrši_naredba() {
        if (pano.화면준비() == 0) { 단말.Zapisuj("GUI unavailable\n"); return; }
        int odabir_VALUE = 0;
        String Stanje_VALUE = "READY";
        boolean 앞줄 = 명령해석기.앞줄;
        그리기(odabir_VALUE, Stanje_VALUE);
        단말.Zapisuj("GUI READY: UART TAB selects, ENTER runs, Q exits\n");
        while (true) {
            int 입력 = pano.직렬읽기();
            if (입력 < 0) { pano.YIELD_CPU(); continue; }
            if (입력 == 10 && 앞줄) { 앞줄 = false; continue; }
            앞줄 = 입력 == 13;
            if (입력 >= '1' && 입력 <= '5') { odabir_VALUE = 입력 - '1'; 입력 = 13; }
            if (입력 == 't' || 입력 == 'T') { 명령해석기.Terminal(false); return; }
            if (입력 == 'q' || 입력 == 'Q' || 입력 == 27) break;
            if (입력 == 9 || 입력 == 'j') {
                odabir_VALUE = (odabir_VALUE + 1) % 5; 그리기(odabir_VALUE, Stanje_VALUE); 단말.Zapisuj("GUI FOCUS "); 단말.수(odabir_VALUE); 단말.문자(10);
            } else if (입력 == 13 || 입력 == 10) {
                if (odabir_VALUE == 4) { 명령해석기.Terminal(false); return; }
                int REZULTAT;
                if (odabir_VALUE < 2) REZULTAT = pano.izvršiti_korisnik_program(odabir_VALUE == 0 ? 0 : 9);
                else if (odabir_VALUE == 2) {
                    REZULTAT = 명령해석기.예제실행(10, "Hello.java");
                    if (REZULTAT == 0) REZULTAT = 명령해석기.예제실행(11, "Hello");
                } else REZULTAT = 명령해석기.예제실행(12, "hello.py");
                Stanje_VALUE = REZULTAT != 0 ? "PROGRAM FAILED" : odabir_VALUE == 0 ? "C++ FILE OK" : odabir_VALUE == 1 ? "UDP LOOPBACK OK" : odabir_VALUE == 2 ? "JAVA OK" : "MICROPYTHON OK";
                그리기(odabir_VALUE, Stanje_VALUE);
                단말.Zapisuj("GUI ACTION "); 단말.수(odabir_VALUE); 단말.Zapisuj(" RESULT "); 단말.수(REZULTAT); 단말.문자(10);
            }
        }
        jezgra_sustava.화면();
        단말.Zapisuj("GUI EXIT\n");
    }
}
