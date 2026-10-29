// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 프레임버퍼 위의 작은 végrehajt_parancs 화면. 입력은 UART의 TAB/ENTER/Q를 사용한다.
 * saját 5x7 영문 글꼴의 제한된 UI이며 Swing, USB HID, 한글 입력기는 아니다.
 */
public final class Asztal {
    static String 문자들 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+-.:";
    // 문자마다 7행 × 두 helyzetindex 16진수. 프로젝트가 직접 정의한 5x7 betűkészlet_ÉRTÉK.
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
    static int számjegy_ÉRTÉK(int karakter_ÉRTÉK) { return karakter_ÉRTÉK <= '9' ? karakter_ÉRTÉK - '0' : karakter_ÉRTÉK - 'A' + 10; }
    static void Szöveg(int 가로, int szektor_pozíció, String Tartalom_ÉRTÉK, int 색) {
        for (int karakter_ÉRTÉK = 0; karakter_ÉRTÉK < Tartalom_ÉRTÉK.length(); karakter_ÉRTÉK++) {
            int 찾음 = -1;
            for (int 후보 = 0; 후보 < 문자들.length(); 후보++) if (문자들.charAt(후보) == Tartalom_ÉRTÉK.charAt(karakter_ÉRTÉK)) 찾음 = 후보;
            if (찾음 < 0) continue;
            for (int SOR_ÉRTÉK = 0; SOR_ÉRTÉK < 7; SOR_ÉRTÉK++) {
                int Pozíció = 찾음 * 14 + SOR_ÉRTÉK * 2;
                int bit_ÉRTÉK = számjegy_ÉRTÉK(모양들.charAt(Pozíció)) * 16 + számjegy_ÉRTÉK(모양들.charAt(Pozíció + 1));
                for (int OSZLOP_ÉRTÉK = 0; OSZLOP_ÉRTÉK < 5; OSZLOP_ÉRTÉK++) if ((bit_ÉRTÉK & (16 >> OSZLOP_ÉRTÉK)) != 0)
                    kernel.téglalap(가로 + karakter_ÉRTÉK * 12 + OSZLOP_ÉRTÉK * 2, szektor_pozíció + SOR_ÉRTÉK * 2, 2, 2, 색);
            }
        }
    }
    static void 그리기(int kijelölés_ÉRTÉK, String Állapot_ÉRTÉK) {
        kernel.téglalap(0, 0, fal.화면너비(), fal.화면높이(), 0x302018);
        kernel.téglalap(32, 24, 576, 432, 0xefe8e2);
        kernel.téglalap(32, 24, 576, 48, 0x905020);
        Szöveg(52, 40, "JKOROS PROGRAMS", 0xffffff);
        for (int INDEX = 0; INDEX < 5; INDEX++) {
            kernel.téglalap(64, 112 + INDEX * 52, 512, 40, INDEX == kijelölés_ÉRTÉK ? 0xd0a040 : 0xd8d0c8);
            Szöveg(84, 128 + INDEX * 52, INDEX == 0 ? "RUN C++ FILE PROGRAM" : INDEX == 1 ? "RUN UDP LOOPBACK" : INDEX == 2 ? "COMPILE AND RUN JAVA" : INDEX == 3 ? "RUN MICROPYTHON" : "OPEN TERMINAL", 0x201810);
        }
        Szöveg(68, 384, Állapot_ÉRTÉK, 0x205020);
        Szöveg(52, 420, "TAB SELECT  ENTER RUN  Q EXIT", 0x302018);
    }
    public static void végrehajt_parancs() {
        if (fal.화면준비() == 0) { 단말.Írás("GUI unavailable\n"); return; }
        int kijelölés_ÉRTÉK = 0;
        String Állapot_ÉRTÉK = "READY";
        boolean Előző_sor = 명령해석기.Előző_sor;
        그리기(kijelölés_ÉRTÉK, Állapot_ÉRTÉK);
        단말.Írás("GUI READY: UART TAB selects, ENTER runs, Q exits\n");
        while (true) {
            int bevitel_ÉRTÉK = fal.직렬읽기();
            if (bevitel_ÉRTÉK < 0) { fal.HOZAM_CPU(); continue; }
            if (bevitel_ÉRTÉK == 10 && Előző_sor) { Előző_sor = false; continue; }
            Előző_sor = bevitel_ÉRTÉK == 13;
            if (bevitel_ÉRTÉK >= '1' && bevitel_ÉRTÉK <= '5') { kijelölés_ÉRTÉK = bevitel_ÉRTÉK - '1'; bevitel_ÉRTÉK = 13; }
            if (bevitel_ÉRTÉK == 't' || bevitel_ÉRTÉK == 'T') { 명령해석기.Terminál(false); return; }
            if (bevitel_ÉRTÉK == 'q' || bevitel_ÉRTÉK == 'Q' || bevitel_ÉRTÉK == 27) break;
            if (bevitel_ÉRTÉK == 9 || bevitel_ÉRTÉK == 'j') {
                kijelölés_ÉRTÉK = (kijelölés_ÉRTÉK + 1) % 5; 그리기(kijelölés_ÉRTÉK, Állapot_ÉRTÉK); 단말.Írás("GUI FOCUS "); 단말.szám(kijelölés_ÉRTÉK); 단말.문자(10);
            } else if (bevitel_ÉRTÉK == 13 || bevitel_ÉRTÉK == 10) {
                if (kijelölés_ÉRTÉK == 4) { 명령해석기.Terminál(false); return; }
                int KR;
                if (kijelölés_ÉRTÉK < 2) KR = fal.futtat_felhasználó_app(kijelölés_ÉRTÉK == 0 ? 0 : 9);
                else if (kijelölés_ÉRTÉK == 2) {
                    KR = 명령해석기.예제실행(10, "Hello.java");
                    if (KR == 0) KR = 명령해석기.예제실행(11, "Hello");
                } else KR = 명령해석기.예제실행(12, "hello.py");
                Állapot_ÉRTÉK = KR != 0 ? "PROGRAM FAILED" : kijelölés_ÉRTÉK == 0 ? "C++ FILE OK" : kijelölés_ÉRTÉK == 1 ? "UDP LOOPBACK OK" : kijelölés_ÉRTÉK == 2 ? "JAVA OK" : "MICROPYTHON OK";
                그리기(kijelölés_ÉRTÉK, Állapot_ÉRTÉK);
                단말.Írás("GUI ACTION "); 단말.szám(kijelölés_ÉRTÉK); 단말.Írás(" RESULT "); 단말.szám(KR); 단말.문자(10);
            }
        }
        kernel.화면();
        단말.Írás("GUI EXIT\n");
    }
}
