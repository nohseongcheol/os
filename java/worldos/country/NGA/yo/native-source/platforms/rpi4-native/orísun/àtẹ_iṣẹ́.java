// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 프레임버퍼 위의 작은 ṣiṣẹ́_àṣẹ 화면. 입력은 UART의 TAB/ENTER/Q를 사용한다.
 * 자체 5x7 영문 글꼴의 제한된 UI이며 Swing, USB HID, 한글 입력기는 아니다.
 */
public final class àtẹ_iṣẹ́ {
    static String 문자들 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+-.:";
    // 문자마다 7행 × 두 자리 16진수. 프로젝트가 직접 정의한 5x7 ìrísí_lẹ́tà_iye.
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
    static int díjììtì_iye(int ẹyọ_ọ̀rọ̀_iye) { return ẹyọ_ọ̀rọ̀_iye <= '9' ? ẹyọ_ọ̀rọ̀_iye - '0' : ẹyọ_ọ̀rọ̀_iye - 'A' + 10; }
    static void SMS(int 가로, int 세로, String Àkóónú_iye, int 색) {
        for (int ẹyọ_ọ̀rọ̀_iye = 0; ẹyọ_ọ̀rọ̀_iye < Àkóónú_iye.length(); ẹyọ_ọ̀rọ̀_iye++) {
            int 찾음 = -1;
            for (int 후보 = 0; 후보 < 문자들.length(); 후보++) if (문자들.charAt(후보) == Àkóónú_iye.charAt(ẹyọ_ọ̀rọ̀_iye)) 찾음 = 후보;
            if (찾음 < 0) continue;
            for (int ìlà_ìbú_iye = 0; ìlà_ìbú_iye < 7; ìlà_ìbú_iye++) {
                int 위치 = 찾음 * 14 + ìlà_ìbú_iye * 2;
                int bíìtì_iye = díjììtì_iye(모양들.charAt(위치)) * 16 + díjììtì_iye(모양들.charAt(위치 + 1));
                for (int ìlà_òró_iye = 0; ìlà_òró_iye < 5; ìlà_òró_iye++) if ((bíìtì_iye & (16 >> ìlà_òró_iye)) != 0)
                    kánẹ́ẹ̀lì.사각형(가로 + ẹyọ_ọ̀rọ̀_iye * 12 + ìlà_òró_iye * 2, 세로 + ìlà_ìbú_iye * 2, 2, 2, 색);
            }
        }
    }
    static void 그리기(int ẹ̀yàn_iye, String ipò_iye) {
        kánẹ́ẹ̀lì.사각형(0, 0, 보드.화면너비(), 보드.화면높이(), 0x302018);
        kánẹ́ẹ̀lì.사각형(32, 24, 576, 432, 0xefe8e2);
        kánẹ́ẹ̀lì.사각형(32, 24, 576, 48, 0x905020);
        SMS(52, 40, "JKOROS PROGRAMS", 0xffffff);
        for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < 5; wá_atọ̀ka_àkóónú++) {
            kánẹ́ẹ̀lì.사각형(64, 112 + wá_atọ̀ka_àkóónú * 52, 512, 40, wá_atọ̀ka_àkóónú == ẹ̀yàn_iye ? 0xd0a040 : 0xd8d0c8);
            SMS(84, 128 + wá_atọ̀ka_àkóónú * 52, wá_atọ̀ka_àkóónú == 0 ? "RUN C++ FILE PROGRAM" : wá_atọ̀ka_àkóónú == 1 ? "RUN UDP LOOPBACK" : wá_atọ̀ka_àkóónú == 2 ? "COMPILE AND RUN JAVA" : wá_atọ̀ka_àkóónú == 3 ? "RUN MICROPYTHON" : "OPEN TERMINAL", 0x201810);
        }
        SMS(68, 384, ipò_iye, 0x205020);
        SMS(52, 420, "TAB SELECT  ENTER RUN  Q EXIT", 0x302018);
    }
    public static void ṣiṣẹ́_àṣẹ() {
        if (보드.화면준비() == 0) { 단말.Kọ("GUI unavailable\n"); return; }
        int ẹ̀yàn_iye = 0;
        String ipò_iye = "READY";
        boolean 앞줄 = 명령해석기.앞줄;
        그리기(ẹ̀yàn_iye, ipò_iye);
        단말.Kọ("GUI READY: UART TAB selects, ENTER runs, Q exits\n");
        while (true) {
            int 입력 = 보드.직렬읽기();
            if (입력 < 0) { 보드.ti_dádúró_díẹ̀_CPU(); continue; }
            if (입력 == 10 && 앞줄) { 앞줄 = false; continue; }
            앞줄 = 입력 == 13;
            if (입력 >= '1' && 입력 <= '5') { ẹ̀yàn_iye = 입력 - '1'; 입력 = 13; }
            if (입력 == 't' || 입력 == 'T') { 명령해석기.터미널(false); return; }
            if (입력 == 'q' || 입력 == 'Q' || 입력 == 27) break;
            if (입력 == 9 || 입력 == 'j') {
                ẹ̀yàn_iye = (ẹ̀yàn_iye + 1) % 5; 그리기(ẹ̀yàn_iye, ipò_iye); 단말.Kọ("GUI FOCUS "); 단말.수(ẹ̀yàn_iye); 단말.문자(10);
            } else if (입력 == 13 || 입력 == 10) {
                if (ẹ̀yàn_iye == 4) { 명령해석기.터미널(false); return; }
                int 결과;
                if (ẹ̀yàn_iye < 2) 결과 = 보드.ṣiṣẹ́_aṣàmúlò_àtòjọ_ètò(ẹ̀yàn_iye == 0 ? 0 : 9);
                else if (ẹ̀yàn_iye == 2) {
                    결과 = 명령해석기.예제실행(10, "Hello.java");
                    if (결과 == 0) 결과 = 명령해석기.예제실행(11, "Hello");
                } else 결과 = 명령해석기.예제실행(12, "hello.py");
                ipò_iye = 결과 != 0 ? "PROGRAM FAILED" : ẹ̀yàn_iye == 0 ? "C++ FILE OK" : ẹ̀yàn_iye == 1 ? "UDP LOOPBACK OK" : ẹ̀yàn_iye == 2 ? "JAVA OK" : "MICROPYTHON OK";
                그리기(ẹ̀yàn_iye, ipò_iye);
                단말.Kọ("GUI ACTION "); 단말.수(ẹ̀yàn_iye); 단말.Kọ(" RESULT "); 단말.수(결과); 단말.문자(10);
            }
        }
        kánẹ́ẹ̀lì.화면();
        단말.Kọ("GUI EXIT\n");
    }
}
