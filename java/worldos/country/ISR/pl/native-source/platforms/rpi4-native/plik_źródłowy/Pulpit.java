// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 프레임버퍼 위의 작은 Wykonaj_polecenie 화면. 입력은 UART의 TAB/ENTER/Q를 사용한다.
 * własny 5x7 영문 글꼴의 제한된 UI이며 Swing, USB HID, 한글 입력기는 아니다.
 */
public final class Pulpit {
    static String 문자들 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+-.:";
    // 문자마다 7행 × 두 indeks_pozycji 16진수. 프로젝트가 직접 정의한 5x7 czcionka_WARTOŚĆ.
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
    static int cyfra_WARTOŚĆ(int znak_WARTOŚĆ) { return znak_WARTOŚĆ <= '9' ? znak_WARTOŚĆ - '0' : znak_WARTOŚĆ - 'A' + 10; }
    static void tekst(int 가로, int gałąź_stanowisko, String treść_WARTOŚĆ_cb0f2404, int 색) {
        for (int znak_WARTOŚĆ = 0; znak_WARTOŚĆ < treść_WARTOŚĆ_cb0f2404.length(); znak_WARTOŚĆ++) {
            int 찾음 = -1;
            for (int kandydat = 0; kandydat < 문자들.length(); kandydat++) if (문자들.charAt(kandydat) == treść_WARTOŚĆ_cb0f2404.charAt(znak_WARTOŚĆ)) 찾음 = kandydat;
            if (찾음 < 0) continue;
            for (int WIERSZ_WARTOŚĆ = 0; WIERSZ_WARTOŚĆ < 7; WIERSZ_WARTOŚĆ++) {
                int pozycja = 찾음 * 14 + WIERSZ_WARTOŚĆ * 2;
                int bit_WARTOŚĆ = cyfra_WARTOŚĆ(모양들.charAt(pozycja)) * 16 + cyfra_WARTOŚĆ(모양들.charAt(pozycja + 1));
                for (int kolumna_WARTOŚĆ = 0; kolumna_WARTOŚĆ < 5; kolumna_WARTOŚĆ++) if ((bit_WARTOŚĆ & (16 >> kolumna_WARTOŚĆ)) != 0)
                    jądro.prostokąt(가로 + znak_WARTOŚĆ * 12 + kolumna_WARTOŚĆ * 2, gałąź_stanowisko + WIERSZ_WARTOŚĆ * 2, 2, 2, 색);
            }
        }
    }
    static void 그리기(int zaznaczenie_WARTOŚĆ, String Stan_WARTOŚĆ) {
        jądro.prostokąt(0, 0, Tablica.화면너비(), Tablica.화면높이(), 0x302018);
        jądro.prostokąt(32, 24, 576, 432, 0xefe8e2);
        jądro.prostokąt(32, 24, 576, 48, 0x905020);
        tekst(52, 40, "JKOROS PROGRAMS", 0xffffff);
        for (int INDEKS = 0; INDEKS < 5; INDEKS++) {
            jądro.prostokąt(64, 112 + INDEKS * 52, 512, 40, INDEKS == zaznaczenie_WARTOŚĆ ? 0xd0a040 : 0xd8d0c8);
            tekst(84, 128 + INDEKS * 52, INDEKS == 0 ? "RUN C++ FILE PROGRAM" : INDEKS == 1 ? "RUN UDP LOOPBACK" : INDEKS == 2 ? "COMPILE AND RUN JAVA" : INDEKS == 3 ? "RUN MICROPYTHON" : "OPEN TERMINAL", 0x201810);
        }
        tekst(68, 384, Stan_WARTOŚĆ, 0x205020);
        tekst(52, 420, "TAB SELECT  ENTER RUN  Q EXIT", 0x302018);
    }
    public static void Wykonaj_polecenie() {
        if (Tablica.화면준비() == 0) { 단말.Zapis("GUI unavailable\n"); return; }
        int zaznaczenie_WARTOŚĆ = 0;
        String Stan_WARTOŚĆ = "READY";
        boolean Wstecz_linia = polecenie_interpreter.Wstecz_linia;
        그리기(zaznaczenie_WARTOŚĆ, Stan_WARTOŚĆ);
        단말.Zapis("GUI READY: UART TAB selects, ENTER runs, Q exits\n");
        while (true) {
            int wejście_WARTOŚĆ = Tablica.직렬읽기();
            if (wejście_WARTOŚĆ < 0) { Tablica.Dochód_CPU(); continue; }
            if (wejście_WARTOŚĆ == 10 && Wstecz_linia) { Wstecz_linia = false; continue; }
            Wstecz_linia = wejście_WARTOŚĆ == 13;
            if (wejście_WARTOŚĆ >= '1' && wejście_WARTOŚĆ <= '5') { zaznaczenie_WARTOŚĆ = wejście_WARTOŚĆ - '1'; wejście_WARTOŚĆ = 13; }
            if (wejście_WARTOŚĆ == 't' || wejście_WARTOŚĆ == 'T') { polecenie_interpreter.interpretator_poleceń(false); return; }
            if (wejście_WARTOŚĆ == 'q' || wejście_WARTOŚĆ == 'Q' || wejście_WARTOŚĆ == 27) break;
            if (wejście_WARTOŚĆ == 9 || wejście_WARTOŚĆ == 'j') {
                zaznaczenie_WARTOŚĆ = (zaznaczenie_WARTOŚĆ + 1) % 5; 그리기(zaznaczenie_WARTOŚĆ, Stan_WARTOŚĆ); 단말.Zapis("GUI FOCUS "); 단말.identyfikator(zaznaczenie_WARTOŚĆ); 단말.문자(10);
            } else if (wejście_WARTOŚĆ == 13 || wejście_WARTOŚĆ == 10) {
                if (zaznaczenie_WARTOŚĆ == 4) { polecenie_interpreter.interpretator_poleceń(false); return; }
                int WYNIK;
                if (zaznaczenie_WARTOŚĆ < 2) WYNIK = Tablica.przebieg_użytkownik_program(zaznaczenie_WARTOŚĆ == 0 ? 0 : 9);
                else if (zaznaczenie_WARTOŚĆ == 2) {
                    WYNIK = polecenie_interpreter.예제실행(10, "Hello.java");
                    if (WYNIK == 0) WYNIK = polecenie_interpreter.예제실행(11, "Hello");
                } else WYNIK = polecenie_interpreter.예제실행(12, "hello.py");
                Stan_WARTOŚĆ = WYNIK != 0 ? "PROGRAM FAILED" : zaznaczenie_WARTOŚĆ == 0 ? "C++ FILE OK" : zaznaczenie_WARTOŚĆ == 1 ? "UDP LOOPBACK OK" : zaznaczenie_WARTOŚĆ == 2 ? "JAVA OK" : "MICROPYTHON OK";
                그리기(zaznaczenie_WARTOŚĆ, Stan_WARTOŚĆ);
                단말.Zapis("GUI ACTION "); 단말.identyfikator(zaznaczenie_WARTOŚĆ); 단말.Zapis(" RESULT "); 단말.identyfikator(WYNIK); 단말.문자(10);
            }
        }
        jądro.화면();
        단말.Zapis("GUI EXIT\n");
    }
}
