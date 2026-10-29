// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 프레임버퍼 위의 작은 실행 화면. 입력은 UART의 TAB/ENTER/Q를 사용한다.
 * 자체 5x7 영문 글꼴의 제한된 UI이며 Swing, USB HID, 한글 입력기는 아니다.
 */
public final class biro {
    static String 문자들 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+-.:";
    // 문자마다 7행 × 두 자리 16진수. 프로젝트가 직접 정의한 5x7 fontere_njaru.
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
    static int 숫자(int alkulal_njaru) { return alkulal_njaru <= '9' ? alkulal_njaru - '0' : alkulal_njaru - 'A' + 10; }
    static void binndi(int 가로, int 세로, String loowdi_njaru, int 색) {
        for (int alkulal_njaru = 0; alkulal_njaru < loowdi_njaru.length(); alkulal_njaru++) {
            int 찾음 = -1;
            for (int 후보 = 0; 후보 < 문자들.length(); 후보++) if (문자들.charAt(후보) == loowdi_njaru.charAt(alkulal_njaru)) 찾음 = 후보;
            if (찾음 < 0) continue;
            for (int winndande_njaru = 0; winndande_njaru < 7; winndande_njaru++) {
                int 위치 = 찾음 * 14 + winndande_njaru * 2;
                int bitere_njaru = 숫자(모양들.charAt(위치)) * 16 + 숫자(모양들.charAt(위치 + 1));
                for (int darol_njaru = 0; darol_njaru < 5; darol_njaru++) if ((bitere_njaru & (16 >> darol_njaru)) != 0)
                    aaluude.사각형(가로 + alkulal_njaru * 12 + darol_njaru * 2, 세로 + winndande_njaru * 2, 2, 2, 색);
            }
        }
    }
    static void 그리기(int cuɓal_njaru, String ngonka_njaru) {
        aaluude.사각형(0, 0, 보드.화면너비(), 보드.화면높이(), 0x302018);
        aaluude.사각형(32, 24, 576, 432, 0xefe8e2);
        aaluude.사각형(32, 24, 576, 48, 0x905020);
        binndi(52, 40, "JKOROS PROGRAMS", 0xffffff);
        for (int joopirdu = 0; joopirdu < 5; joopirdu++) {
            aaluude.사각형(64, 112 + joopirdu * 52, 512, 40, joopirdu == cuɓal_njaru ? 0xd0a040 : 0xd8d0c8);
            binndi(84, 128 + joopirdu * 52, joopirdu == 0 ? "RUN C++ FILE PROGRAM" : joopirdu == 1 ? "RUN UDP LOOPBACK" : joopirdu == 2 ? "COMPILE AND RUN JAVA" : joopirdu == 3 ? "RUN MICROPYTHON" : "OPEN TERMINAL", 0x201810);
        }
        binndi(68, 384, ngonka_njaru, 0x205020);
        binndi(52, 420, "TAB SELECT  ENTER RUN  Q EXIT", 0x302018);
    }
    public static void 실행() {
        if (보드.화면준비() == 0) { 단말.winndude("GUI unavailable\n"); return; }
        int cuɓal_njaru = 0;
        String ngonka_njaru = "READY";
        boolean 앞줄 = 명령해석기.앞줄;
        그리기(cuɓal_njaru, ngonka_njaru);
        단말.winndude("GUI READY: UART TAB selects, ENTER runs, Q exits\n");
        while (true) {
            int 입력 = 보드.직렬읽기();
            if (입력 < 0) { 보드.양보(); continue; }
            if (입력 == 10 && 앞줄) { 앞줄 = false; continue; }
            앞줄 = 입력 == 13;
            if (입력 >= '1' && 입력 <= '5') { cuɓal_njaru = 입력 - '1'; 입력 = 13; }
            if (입력 == 't' || 입력 == 'T') { 명령해석기.터미널(false); return; }
            if (입력 == 'q' || 입력 == 'Q' || 입력 == 27) break;
            if (입력 == 9 || 입력 == 'j') {
                cuɓal_njaru = (cuɓal_njaru + 1) % 5; 그리기(cuɓal_njaru, ngonka_njaru); 단말.winndude("GUI FOCUS "); 단말.수(cuɓal_njaru); 단말.문자(10);
            } else if (입력 == 13 || 입력 == 10) {
                if (cuɓal_njaru == 4) { 명령해석기.터미널(false); return; }
                int 결과;
                if (cuɓal_njaru < 2) 결과 = 보드.huutoraade_kuutoro_tafirde(cuɓal_njaru == 0 ? 0 : 9);
                else if (cuɓal_njaru == 2) {
                    결과 = 명령해석기.예제실행(10, "Hello.java");
                    if (결과 == 0) 결과 = 명령해석기.예제실행(11, "Hello");
                } else 결과 = 명령해석기.예제실행(12, "hello.py");
                ngonka_njaru = 결과 != 0 ? "PROGRAM FAILED" : cuɓal_njaru == 0 ? "C++ FILE OK" : cuɓal_njaru == 1 ? "UDP LOOPBACK OK" : cuɓal_njaru == 2 ? "JAVA OK" : "MICROPYTHON OK";
                그리기(cuɓal_njaru, ngonka_njaru);
                단말.winndude("GUI ACTION "); 단말.수(cuɓal_njaru); 단말.winndude(" RESULT "); 단말.수(결과); 단말.문자(10);
            }
        }
        aaluude.화면();
        단말.winndude("GUI EXIT\n");
    }
}
