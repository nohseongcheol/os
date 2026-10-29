// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 프레임버퍼 위의 작은 keyra_skipun 화면. 입력은 UART의 TAB/ENTER/Q를 사용한다.
 * eigin 5x7 영문 글꼴의 제한된 UI이며 Swing, USB HID, 한글 입력기는 아니다.
 */
public final class skjáborð {
    static String 문자들 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+-.:";
    // 문자마다 7행 × 두 staða_INDEX 16진수. 프로젝트가 직접 정의한 5x7 leturgerð_VALUE.
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
    static int tölustafur_VALUE(int stafur_VALUE) { return stafur_VALUE <= '9' ? stafur_VALUE - '0' : stafur_VALUE - 'A' + 10; }
    static void Texti(int 가로, int Lóðrétt_staða, String Efni_VALUE, int 색) {
        for (int stafur_VALUE = 0; stafur_VALUE < Efni_VALUE.length(); stafur_VALUE++) {
            int 찾음 = -1;
            for (int 후보 = 0; 후보 < 문자들.length(); 후보++) if (문자들.charAt(후보) == Efni_VALUE.charAt(stafur_VALUE)) 찾음 = 후보;
            if (찾음 < 0) continue;
            for (int ROW_VALUE = 0; ROW_VALUE < 7; ROW_VALUE++) {
                int Staðsetning = 찾음 * 14 + ROW_VALUE * 2;
                int biti_VALUE = tölustafur_VALUE(모양들.charAt(Staðsetning)) * 16 + tölustafur_VALUE(모양들.charAt(Staðsetning + 1));
                for (int COLUMN_VALUE = 0; COLUMN_VALUE < 5; COLUMN_VALUE++) if ((biti_VALUE & (16 >> COLUMN_VALUE)) != 0)
                    kjarni.사각형(가로 + stafur_VALUE * 12 + COLUMN_VALUE * 2, Lóðrétt_staða + ROW_VALUE * 2, 2, 2, 색);
            }
        }
    }
    static void 그리기(int val_VALUE, String staða_VALUE_e10195a1) {
        kjarni.사각형(0, 0, bretti.화면너비(), bretti.화면높이(), 0x302018);
        kjarni.사각형(32, 24, 576, 432, 0xefe8e2);
        kjarni.사각형(32, 24, 576, 48, 0x905020);
        Texti(52, 40, "JKOROS PROGRAMS", 0xffffff);
        for (int INDEX = 0; INDEX < 5; INDEX++) {
            kjarni.사각형(64, 112 + INDEX * 52, 512, 40, INDEX == val_VALUE ? 0xd0a040 : 0xd8d0c8);
            Texti(84, 128 + INDEX * 52, INDEX == 0 ? "RUN C++ FILE PROGRAM" : INDEX == 1 ? "RUN UDP LOOPBACK" : INDEX == 2 ? "COMPILE AND RUN JAVA" : INDEX == 3 ? "RUN MICROPYTHON" : "OPEN TERMINAL", 0x201810);
        }
        Texti(68, 384, staða_VALUE_e10195a1, 0x205020);
        Texti(52, 420, "TAB SELECT  ENTER RUN  Q EXIT", 0x302018);
    }
    public static void keyra_skipun() {
        if (bretti.화면준비() == 0) { 단말.Skrift("GUI unavailable\n"); return; }
        int val_VALUE = 0;
        String staða_VALUE_e10195a1 = "READY";
        boolean 앞줄 = 명령해석기.앞줄;
        그리기(val_VALUE, staða_VALUE_e10195a1);
        단말.Skrift("GUI READY: UART TAB selects, ENTER runs, Q exits\n");
        while (true) {
            int 입력 = bretti.직렬읽기();
            if (입력 < 0) { bretti.YIELD_örgjörvi(); continue; }
            if (입력 == 10 && 앞줄) { 앞줄 = false; continue; }
            앞줄 = 입력 == 13;
            if (입력 >= '1' && 입력 <= '5') { val_VALUE = 입력 - '1'; 입력 = 13; }
            if (입력 == 't' || 입력 == 'T') { 명령해석기.Skjáhermir(false); return; }
            if (입력 == 'q' || 입력 == 'Q' || 입력 == 27) break;
            if (입력 == 9 || 입력 == 'j') {
                val_VALUE = (val_VALUE + 1) % 5; 그리기(val_VALUE, staða_VALUE_e10195a1); 단말.Skrift("GUI FOCUS "); 단말.númer(val_VALUE); 단말.문자(10);
            } else if (입력 == 13 || 입력 == 10) {
                if (val_VALUE == 4) { 명령해석기.Skjáhermir(false); return; }
                int NIÐURSTAÐA;
                if (val_VALUE < 2) NIÐURSTAÐA = bretti.runa_notandi_forrit(val_VALUE == 0 ? 0 : 9);
                else if (val_VALUE == 2) {
                    NIÐURSTAÐA = 명령해석기.예제실행(10, "Hello.java");
                    if (NIÐURSTAÐA == 0) NIÐURSTAÐA = 명령해석기.예제실행(11, "Hello");
                } else NIÐURSTAÐA = 명령해석기.예제실행(12, "hello.py");
                staða_VALUE_e10195a1 = NIÐURSTAÐA != 0 ? "PROGRAM FAILED" : val_VALUE == 0 ? "C++ FILE OK" : val_VALUE == 1 ? "UDP LOOPBACK OK" : val_VALUE == 2 ? "JAVA OK" : "MICROPYTHON OK";
                그리기(val_VALUE, staða_VALUE_e10195a1);
                단말.Skrift("GUI ACTION "); 단말.númer(val_VALUE); 단말.Skrift(" RESULT "); 단말.númer(NIÐURSTAÐA); 단말.문자(10);
            }
        }
        kjarni.화면();
        단말.Skrift("GUI EXIT\n");
    }
}
