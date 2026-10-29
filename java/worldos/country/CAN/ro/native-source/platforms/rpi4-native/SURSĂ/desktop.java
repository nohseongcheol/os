// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 프레임버퍼 위의 작은 executa_comandă 화면. 입력은 UART의 TAB/ENTER/Q를 사용한다.
 * propriu 5x7 영문 글꼴의 제한된 UI이며 Swing, USB HID, 한글 입력기는 아니다.
 */
public final class desktop {
    static String 문자들 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+-.:";
    // 문자마다 7행 × 두 index_de_poziție 16진수. 프로젝트가 직접 정의한 5x7 font_VALUE.
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
    static int cifră_VALUE(int caracter_VALUE) { return caracter_VALUE <= '9' ? caracter_VALUE - '0' : caracter_VALUE - 'A' + 10; }
    static void SMS(int 가로, int Verticală_poziție, String Conținut_VALUE, int 색) {
        for (int caracter_VALUE = 0; caracter_VALUE < Conținut_VALUE.length(); caracter_VALUE++) {
            int 찾음 = -1;
            for (int 후보 = 0; 후보 < 문자들.length(); 후보++) if (문자들.charAt(후보) == Conținut_VALUE.charAt(caracter_VALUE)) 찾음 = 후보;
            if (찾음 < 0) continue;
            for (int ROW_VALUE = 0; ROW_VALUE < 7; ROW_VALUE++) {
                int Poziție = 찾음 * 14 + ROW_VALUE * 2;
                int bit_VALUE = cifră_VALUE(모양들.charAt(Poziție)) * 16 + cifră_VALUE(모양들.charAt(Poziție + 1));
                for (int COLUMN_VALUE = 0; COLUMN_VALUE < 5; COLUMN_VALUE++) if ((bit_VALUE & (16 >> COLUMN_VALUE)) != 0)
                    nucleu.dreptunghi(가로 + caracter_VALUE * 12 + COLUMN_VALUE * 2, Verticală_poziție + ROW_VALUE * 2, 2, 2, 색);
            }
        }
    }
    static void 그리기(int selecție_VALUE, String Stare_VALUE) {
        nucleu.dreptunghi(0, 0, Avizier.화면너비(), Avizier.화면높이(), 0x302018);
        nucleu.dreptunghi(32, 24, 576, 432, 0xefe8e2);
        nucleu.dreptunghi(32, 24, 576, 48, 0x905020);
        SMS(52, 40, "JKOROS PROGRAMS", 0xffffff);
        for (int INDEX = 0; INDEX < 5; INDEX++) {
            nucleu.dreptunghi(64, 112 + INDEX * 52, 512, 40, INDEX == selecție_VALUE ? 0xd0a040 : 0xd8d0c8);
            SMS(84, 128 + INDEX * 52, INDEX == 0 ? "RUN C++ FILE PROGRAM" : INDEX == 1 ? "RUN UDP LOOPBACK" : INDEX == 2 ? "COMPILE AND RUN JAVA" : INDEX == 3 ? "RUN MICROPYTHON" : "OPEN TERMINAL", 0x201810);
        }
        SMS(68, 384, Stare_VALUE, 0x205020);
        SMS(52, 420, "TAB SELECT  ENTER RUN  Q EXIT", 0x302018);
    }
    public static void executa_comandă() {
        if (Avizier.화면준비() == 0) { 단말.Scriere("GUI unavailable\n"); return; }
        int selecție_VALUE = 0;
        String Stare_VALUE = "READY";
        boolean Anteriorul_linie = 명령해석기.Anteriorul_linie;
        그리기(selecție_VALUE, Stare_VALUE);
        단말.Scriere("GUI READY: UART TAB selects, ENTER runs, Q exits\n");
        while (true) {
            int 입력 = Avizier.직렬읽기();
            if (입력 < 0) { Avizier.YIELD_CPU(); continue; }
            if (입력 == 10 && Anteriorul_linie) { Anteriorul_linie = false; continue; }
            Anteriorul_linie = 입력 == 13;
            if (입력 >= '1' && 입력 <= '5') { selecție_VALUE = 입력 - '1'; 입력 = 13; }
            if (입력 == 't' || 입력 == 'T') { 명령해석기.Terminal(false); return; }
            if (입력 == 'q' || 입력 == 'Q' || 입력 == 27) break;
            if (입력 == 9 || 입력 == 'j') {
                selecție_VALUE = (selecție_VALUE + 1) % 5; 그리기(selecție_VALUE, Stare_VALUE); 단말.Scriere("GUI FOCUS "); 단말.수(selecție_VALUE); 단말.문자(10);
            } else if (입력 == 13 || 입력 == 10) {
                if (selecție_VALUE == 4) { 명령해석기.Terminal(false); return; }
                int KR;
                if (selecție_VALUE < 2) KR = Avizier.rula_utilizator_program(selecție_VALUE == 0 ? 0 : 9);
                else if (selecție_VALUE == 2) {
                    KR = 명령해석기.예제실행(10, "Hello.java");
                    if (KR == 0) KR = 명령해석기.예제실행(11, "Hello");
                } else KR = 명령해석기.예제실행(12, "hello.py");
                Stare_VALUE = KR != 0 ? "PROGRAM FAILED" : selecție_VALUE == 0 ? "C++ FILE OK" : selecție_VALUE == 1 ? "UDP LOOPBACK OK" : selecție_VALUE == 2 ? "JAVA OK" : "MICROPYTHON OK";
                그리기(selecție_VALUE, Stare_VALUE);
                단말.Scriere("GUI ACTION "); 단말.수(selecție_VALUE); 단말.Scriere(" RESULT "); 단말.수(KR); 단말.문자(10);
            }
        }
        nucleu.화면();
        단말.Scriere("GUI EXIT\n");
    }
}
