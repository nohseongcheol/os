// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 프레임버퍼 위의 작은 tekeleza_amri 화면. 입력은 UART의 TAB/ENTER/Q를 사용한다.
 * 자체 5x7 영문 글꼴의 제한된 UI이며 Swing, USB HID, 한글 입력기는 아니다.
 */
public final class Eneo_kazi {
    static String 문자들 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+-.:";
    // 문자마다 7행 × 두 자리 16진수. 프로젝트가 직접 정의한 5x7 fonti_thamani.
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
    static int dijiti_thamani(int kibambo_thamani) { return kibambo_thamani <= '9' ? kibambo_thamani - '0' : kibambo_thamani - 'A' + 10; }
    static void SMS(int 가로, int 세로, String maudhui_thamani, int 색) {
        for (int kibambo_thamani = 0; kibambo_thamani < maudhui_thamani.length(); kibambo_thamani++) {
            int 찾음 = -1;
            for (int 후보 = 0; 후보 < 문자들.length(); 후보++) if (문자들.charAt(후보) == maudhui_thamani.charAt(kibambo_thamani)) 찾음 = 후보;
            if (찾음 < 0) continue;
            for (int kumbukumbu_thamani = 0; kumbukumbu_thamani < 7; kumbukumbu_thamani++) {
                int 위치 = 찾음 * 14 + kumbukumbu_thamani * 2;
                int biti_thamani = dijiti_thamani(모양들.charAt(위치)) * 16 + dijiti_thamani(모양들.charAt(위치 + 1));
                for (int safuwima_thamani = 0; safuwima_thamani < 5; safuwima_thamani++) if ((biti_thamani & (16 >> safuwima_thamani)) != 0)
                    kiini.사각형(가로 + kibambo_thamani * 12 + safuwima_thamani * 2, 세로 + kumbukumbu_thamani * 2, 2, 2, 색);
            }
        }
    }
    static void 그리기(int uteuzi_thamani, String hali_thamani) {
        kiini.사각형(0, 0, 보드.화면너비(), 보드.화면높이(), 0x302018);
        kiini.사각형(32, 24, 576, 432, 0xefe8e2);
        kiini.사각형(32, 24, 576, 48, 0x905020);
        SMS(52, 40, "JKOROS PROGRAMS", 0xffffff);
        for (int kielezo = 0; kielezo < 5; kielezo++) {
            kiini.사각형(64, 112 + kielezo * 52, 512, 40, kielezo == uteuzi_thamani ? 0xd0a040 : 0xd8d0c8);
            SMS(84, 128 + kielezo * 52, kielezo == 0 ? "RUN C++ FILE PROGRAM" : kielezo == 1 ? "RUN UDP LOOPBACK" : kielezo == 2 ? "COMPILE AND RUN JAVA" : kielezo == 3 ? "RUN MICROPYTHON" : "OPEN TERMINAL", 0x201810);
        }
        SMS(68, 384, hali_thamani, 0x205020);
        SMS(52, 420, "TAB SELECT  ENTER RUN  Q EXIT", 0x302018);
    }
    public static void tekeleza_amri() {
        if (보드.화면준비() == 0) { 단말.andika("GUI unavailable\n"); return; }
        int uteuzi_thamani = 0;
        String hali_thamani = "READY";
        boolean 앞줄 = 명령해석기.앞줄;
        그리기(uteuzi_thamani, hali_thamani);
        단말.andika("GUI READY: UART TAB selects, ENTER runs, Q exits\n");
        while (true) {
            int 입력 = 보드.직렬읽기();
            if (입력 < 0) { 보드.ahirisha_CPU(); continue; }
            if (입력 == 10 && 앞줄) { 앞줄 = false; continue; }
            앞줄 = 입력 == 13;
            if (입력 >= '1' && 입력 <= '5') { uteuzi_thamani = 입력 - '1'; 입력 = 13; }
            if (입력 == 't' || 입력 == 'T') { 명령해석기.터미널(false); return; }
            if (입력 == 'q' || 입력 == 'Q' || 입력 == 27) break;
            if (입력 == 9 || 입력 == 'j') {
                uteuzi_thamani = (uteuzi_thamani + 1) % 5; 그리기(uteuzi_thamani, hali_thamani); 단말.andika("GUI FOCUS "); 단말.수(uteuzi_thamani); 단말.문자(10);
            } else if (입력 == 13 || 입력 == 10) {
                if (uteuzi_thamani == 4) { 명령해석기.터미널(false); return; }
                int 결과;
                if (uteuzi_thamani < 2) 결과 = 보드.endesha_mtumiaji_programu(uteuzi_thamani == 0 ? 0 : 9);
                else if (uteuzi_thamani == 2) {
                    결과 = 명령해석기.예제실행(10, "Hello.java");
                    if (결과 == 0) 결과 = 명령해석기.예제실행(11, "Hello");
                } else 결과 = 명령해석기.예제실행(12, "hello.py");
                hali_thamani = 결과 != 0 ? "PROGRAM FAILED" : uteuzi_thamani == 0 ? "C++ FILE OK" : uteuzi_thamani == 1 ? "UDP LOOPBACK OK" : uteuzi_thamani == 2 ? "JAVA OK" : "MICROPYTHON OK";
                그리기(uteuzi_thamani, hali_thamani);
                단말.andika("GUI ACTION "); 단말.수(uteuzi_thamani); 단말.andika(" RESULT "); 단말.수(결과); 단말.문자(10);
            }
        }
        kiini.화면();
        단말.andika("GUI EXIT\n");
    }
}
