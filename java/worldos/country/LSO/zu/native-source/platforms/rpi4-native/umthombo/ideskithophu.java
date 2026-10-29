// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 프레임버퍼 위의 작은 yenza_umyalo 화면. 입력은 UART의 TAB/ENTER/Q를 사용한다.
 * 자체 5x7 영문 글꼴의 제한된 UI이며 Swing, USB HID, 한글 입력기는 아니다.
 */
public final class ideskithophu {
    static String 문자들 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+-.:";
    // 문자마다 7행 × 두 자리 16진수. 프로젝트가 직접 정의한 5x7 ubuso_bohlamvu_ifonti_inani.
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
    static int idijithi_inani(int uhlamvusimo_inani) { return uhlamvusimo_inani <= '9' ? uhlamvusimo_inani - '0' : uhlamvusimo_inani - 'A' + 10; }
    static void Itekisi(int 가로, int 세로, String Okuqukethwe_inani, int 색) {
        for (int uhlamvusimo_inani = 0; uhlamvusimo_inani < Okuqukethwe_inani.length(); uhlamvusimo_inani++) {
            int 찾음 = -1;
            for (int 후보 = 0; 후보 < 문자들.length(); 후보++) if (문자들.charAt(후보) == Okuqukethwe_inani.charAt(uhlamvusimo_inani)) 찾음 = 후보;
            if (찾음 < 0) continue;
            for (int umugqa_inani = 0; umugqa_inani < 7; umugqa_inani++) {
                int 위치 = 찾음 * 14 + umugqa_inani * 2;
                int ibhithi_inani = idijithi_inani(모양들.charAt(위치)) * 16 + idijithi_inani(모양들.charAt(위치 + 1));
                for (int ikholomu_inani = 0; ikholomu_inani < 5; ikholomu_inani++) if ((ibhithi_inani & (16 >> ikholomu_inani)) != 0)
                    ikhenela.사각형(가로 + uhlamvusimo_inani * 12 + ikholomu_inani * 2, 세로 + umugqa_inani * 2, 2, 2, 색);
            }
        }
    }
    static void 그리기(int okukhethiwe_inani, String isimo_inani) {
        ikhenela.사각형(0, 0, 보드.화면너비(), 보드.화면높이(), 0x302018);
        ikhenela.사각형(32, 24, 576, 432, 0xefe8e2);
        ikhenela.사각형(32, 24, 576, 48, 0x905020);
        Itekisi(52, 40, "JKOROS PROGRAMS", 0xffffff);
        for (int thola_inkomba = 0; thola_inkomba < 5; thola_inkomba++) {
            ikhenela.사각형(64, 112 + thola_inkomba * 52, 512, 40, thola_inkomba == okukhethiwe_inani ? 0xd0a040 : 0xd8d0c8);
            Itekisi(84, 128 + thola_inkomba * 52, thola_inkomba == 0 ? "RUN C++ FILE PROGRAM" : thola_inkomba == 1 ? "RUN UDP LOOPBACK" : thola_inkomba == 2 ? "COMPILE AND RUN JAVA" : thola_inkomba == 3 ? "RUN MICROPYTHON" : "OPEN TERMINAL", 0x201810);
        }
        Itekisi(68, 384, isimo_inani, 0x205020);
        Itekisi(52, 420, "TAB SELECT  ENTER RUN  Q EXIT", 0x302018);
    }
    public static void yenza_umyalo() {
        if (보드.화면준비() == 0) { 단말.Bhala("GUI unavailable\n"); return; }
        int okukhethiwe_inani = 0;
        String isimo_inani = "READY";
        boolean 앞줄 = 명령해석기.앞줄;
        그리기(okukhethiwe_inani, isimo_inani);
        단말.Bhala("GUI READY: UART TAB selects, ENTER runs, Q exits\n");
        while (true) {
            int 입력 = 보드.직렬읽기();
            if (입력 < 0) { 보드.misa_okwesikhashana_i_CPU(); continue; }
            if (입력 == 10 && 앞줄) { 앞줄 = false; continue; }
            앞줄 = 입력 == 13;
            if (입력 >= '1' && 입력 <= '5') { okukhethiwe_inani = 입력 - '1'; 입력 = 13; }
            if (입력 == 't' || 입력 == 'T') { 명령해석기.터미널(false); return; }
            if (입력 == 'q' || 입력 == 'Q' || 입력 == 27) break;
            if (입력 == 9 || 입력 == 'j') {
                okukhethiwe_inani = (okukhethiwe_inani + 1) % 5; 그리기(okukhethiwe_inani, isimo_inani); 단말.Bhala("GUI FOCUS "); 단말.수(okukhethiwe_inani); 단말.문자(10);
            } else if (입력 == 13 || 입력 == 10) {
                if (okukhethiwe_inani == 4) { 명령해석기.터미널(false); return; }
                int 결과;
                if (okukhethiwe_inani < 2) 결과 = 보드.sebenzisa_umsebenzisi_i_app(okukhethiwe_inani == 0 ? 0 : 9);
                else if (okukhethiwe_inani == 2) {
                    결과 = 명령해석기.예제실행(10, "Hello.java");
                    if (결과 == 0) 결과 = 명령해석기.예제실행(11, "Hello");
                } else 결과 = 명령해석기.예제실행(12, "hello.py");
                isimo_inani = 결과 != 0 ? "PROGRAM FAILED" : okukhethiwe_inani == 0 ? "C++ FILE OK" : okukhethiwe_inani == 1 ? "UDP LOOPBACK OK" : okukhethiwe_inani == 2 ? "JAVA OK" : "MICROPYTHON OK";
                그리기(okukhethiwe_inani, isimo_inani);
                단말.Bhala("GUI ACTION "); 단말.수(okukhethiwe_inani); 단말.Bhala(" RESULT "); 단말.수(결과); 단말.문자(10);
            }
        }
        ikhenela.화면();
        단말.Bhala("GUI EXIT\n");
    }
}
