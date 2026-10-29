// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 프레임버퍼 위의 작은 실행 화면. 입력은 UART의 TAB/ENTER/Q를 사용한다.
 * 자체 5x7 영문 글꼴의 제한된 UI이며 Swing, USB HID, 한글 입력기는 아니다.
 */
public final class igalaujaq {
    static String 문자들 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+-.:";
    // 문자마다 7행 × 두 자리 16진수. 프로젝트가 직접 정의한 5x7 titirausiq_atuutilik.
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
    static int 숫자(int immikkuuqtuq_atuutilik) { return immikkuuqtuq_atuutilik <= '9' ? immikkuuqtuq_atuutilik - '0' : immikkuuqtuq_atuutilik - 'A' + 10; }
    static void titiqqaq(int 가로, int 세로, String Ilulingit_atuutilik, int 색) {
        for (int immikkuuqtuq_atuutilik = 0; immikkuuqtuq_atuutilik < Ilulingit_atuutilik.length(); immikkuuqtuq_atuutilik++) {
            int 찾음 = -1;
            for (int 후보 = 0; 후보 < 문자들.length(); 후보++) if (문자들.charAt(후보) == Ilulingit_atuutilik.charAt(immikkuuqtuq_atuutilik)) 찾음 = 후보;
            if (찾음 < 0) continue;
            for (int sanimukutaak_atuutilik = 0; sanimukutaak_atuutilik < 7; sanimukutaak_atuutilik++) {
                int 위치 = 찾음 * 14 + sanimukutaak_atuutilik * 2;
                int bit_atuutilik = 숫자(모양들.charAt(위치)) * 16 + 숫자(모양들.charAt(위치 + 1));
                for (int ammukutaak_atuutilik = 0; ammukutaak_atuutilik < 5; ammukutaak_atuutilik++) if ((bit_atuutilik & (16 >> ammukutaak_atuutilik)) != 0)
                    kernel.사각형(가로 + immikkuuqtuq_atuutilik * 12 + ammukutaak_atuutilik * 2, 세로 + sanimukutaak_atuutilik * 2, 2, 2, 색);
            }
        }
    }
    static void 그리기(int nirulussimaniq_atuutilik, String qanuilinganiq_atuutilik) {
        kernel.사각형(0, 0, 보드.화면너비(), 보드.화면높이(), 0x302018);
        kernel.사각형(32, 24, 576, 432, 0xefe8e2);
        kernel.사각형(32, 24, 576, 48, 0x905020);
        titiqqaq(52, 40, "JKOROS PROGRAMS", 0xffffff);
        for (int nalunaiqsimavik = 0; nalunaiqsimavik < 5; nalunaiqsimavik++) {
            kernel.사각형(64, 112 + nalunaiqsimavik * 52, 512, 40, nalunaiqsimavik == nirulussimaniq_atuutilik ? 0xd0a040 : 0xd8d0c8);
            titiqqaq(84, 128 + nalunaiqsimavik * 52, nalunaiqsimavik == 0 ? "RUN C++ FILE PROGRAM" : nalunaiqsimavik == 1 ? "RUN UDP LOOPBACK" : nalunaiqsimavik == 2 ? "COMPILE AND RUN JAVA" : nalunaiqsimavik == 3 ? "RUN MICROPYTHON" : "OPEN TERMINAL", 0x201810);
        }
        titiqqaq(68, 384, qanuilinganiq_atuutilik, 0x205020);
        titiqqaq(52, 420, "TAB SELECT  ENTER RUN  Q EXIT", 0x302018);
    }
    public static void 실행() {
        if (보드.화면준비() == 0) { 단말.titiraq("GUI unavailable\n"); return; }
        int nirulussimaniq_atuutilik = 0;
        String qanuilinganiq_atuutilik = "READY";
        boolean 앞줄 = 명령해석기.앞줄;
        그리기(nirulussimaniq_atuutilik, qanuilinganiq_atuutilik);
        단말.titiraq("GUI READY: UART TAB selects, ENTER runs, Q exits\n");
        while (true) {
            int 입력 = 보드.직렬읽기();
            if (입력 < 0) { 보드.양보(); continue; }
            if (입력 == 10 && 앞줄) { 앞줄 = false; continue; }
            앞줄 = 입력 == 13;
            if (입력 >= '1' && 입력 <= '5') { nirulussimaniq_atuutilik = 입력 - '1'; 입력 = 13; }
            if (입력 == 't' || 입력 == 'T') { 명령해석기.터미널(false); return; }
            if (입력 == 'q' || 입력 == 'Q' || 입력 == 27) break;
            if (입력 == 9 || 입력 == 'j') {
                nirulussimaniq_atuutilik = (nirulussimaniq_atuutilik + 1) % 5; 그리기(nirulussimaniq_atuutilik, qanuilinganiq_atuutilik); 단말.titiraq("GUI FOCUS "); 단말.수(nirulussimaniq_atuutilik); 단말.문자(10);
            } else if (입력 == 13 || 입력 == 10) {
                if (nirulussimaniq_atuutilik == 4) { 명령해석기.터미널(false); return; }
                int 결과;
                if (nirulussimaniq_atuutilik < 2) 결과 = 보드.사용자실행(nirulussimaniq_atuutilik == 0 ? 0 : 9);
                else if (nirulussimaniq_atuutilik == 2) {
                    결과 = 명령해석기.예제실행(10, "Hello.java");
                    if (결과 == 0) 결과 = 명령해석기.예제실행(11, "Hello");
                } else 결과 = 명령해석기.예제실행(12, "hello.py");
                qanuilinganiq_atuutilik = 결과 != 0 ? "PROGRAM FAILED" : nirulussimaniq_atuutilik == 0 ? "C++ FILE OK" : nirulussimaniq_atuutilik == 1 ? "UDP LOOPBACK OK" : nirulussimaniq_atuutilik == 2 ? "JAVA OK" : "MICROPYTHON OK";
                그리기(nirulussimaniq_atuutilik, qanuilinganiq_atuutilik);
                단말.titiraq("GUI ACTION "); 단말.수(nirulussimaniq_atuutilik); 단말.titiraq(" RESULT "); 단말.수(결과); 단말.문자(10);
            }
        }
        kernel.화면();
        단말.titiraq("GUI EXIT\n");
    }
}
