// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 프레임버퍼 위의 작은 Izpildīt_komanda 화면. 입력은 UART의 TAB/ENTER/Q를 사용한다.
 * savs 5x7 영문 글꼴의 제한된 UI이며 Swing, USB HID, 한글 입력기는 아니다.
 */
public final class dators {
    static String 문자들 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+-.:";
    // 문자마다 7행 × 두 pozīcijas_indekss 16진수. 프로젝트가 직접 정의한 5x7 fonts_VALUE.
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
    static int cipars_VALUE(int rakstzīme_VALUE) { return rakstzīme_VALUE <= '9' ? rakstzīme_VALUE - '0' : rakstzīme_VALUE - 'A' + 10; }
    static void Teksts(int 가로, int vertikāle_amats, String Saturs_VALUE, int 색) {
        for (int rakstzīme_VALUE = 0; rakstzīme_VALUE < Saturs_VALUE.length(); rakstzīme_VALUE++) {
            int 찾음 = -1;
            for (int 후보 = 0; 후보 < 문자들.length(); 후보++) if (문자들.charAt(후보) == Saturs_VALUE.charAt(rakstzīme_VALUE)) 찾음 = 후보;
            if (찾음 < 0) continue;
            for (int ROW_VALUE = 0; ROW_VALUE < 7; ROW_VALUE++) {
                int Novietojums = 찾음 * 14 + ROW_VALUE * 2;
                int bit_VALUE = cipars_VALUE(모양들.charAt(Novietojums)) * 16 + cipars_VALUE(모양들.charAt(Novietojums + 1));
                for (int COLUMN_VALUE = 0; COLUMN_VALUE < 5; COLUMN_VALUE++) if ((bit_VALUE & (16 >> COLUMN_VALUE)) != 0)
                    kodols.taisnstūris(가로 + rakstzīme_VALUE * 12 + COLUMN_VALUE * 2, vertikāle_amats + ROW_VALUE * 2, 2, 2, 색);
            }
        }
    }
    static void 그리기(int atlase_VALUE, String Statuss_VALUE) {
        kodols.taisnstūris(0, 0, Panelis.화면너비(), Panelis.화면높이(), 0x302018);
        kodols.taisnstūris(32, 24, 576, 432, 0xefe8e2);
        kodols.taisnstūris(32, 24, 576, 48, 0x905020);
        Teksts(52, 40, "JKOROS PROGRAMS", 0xffffff);
        for (int INDEX = 0; INDEX < 5; INDEX++) {
            kodols.taisnstūris(64, 112 + INDEX * 52, 512, 40, INDEX == atlase_VALUE ? 0xd0a040 : 0xd8d0c8);
            Teksts(84, 128 + INDEX * 52, INDEX == 0 ? "RUN C++ FILE PROGRAM" : INDEX == 1 ? "RUN UDP LOOPBACK" : INDEX == 2 ? "COMPILE AND RUN JAVA" : INDEX == 3 ? "RUN MICROPYTHON" : "OPEN TERMINAL", 0x201810);
        }
        Teksts(68, 384, Statuss_VALUE, 0x205020);
        Teksts(52, 420, "TAB SELECT  ENTER RUN  Q EXIT", 0x302018);
    }
    public static void Izpildīt_komanda() {
        if (Panelis.화면준비() == 0) { 단말.Rakstīt("GUI unavailable\n"); return; }
        int atlase_VALUE = 0;
        String Statuss_VALUE = "READY";
        boolean 앞줄 = 명령해석기.앞줄;
        그리기(atlase_VALUE, Statuss_VALUE);
        단말.Rakstīt("GUI READY: UART TAB selects, ENTER runs, Q exits\n");
        while (true) {
            int 입력 = Panelis.직렬읽기();
            if (입력 < 0) { Panelis.YIELD_apstrādātājs(); continue; }
            if (입력 == 10 && 앞줄) { 앞줄 = false; continue; }
            앞줄 = 입력 == 13;
            if (입력 >= '1' && 입력 <= '5') { atlase_VALUE = 입력 - '1'; 입력 = 13; }
            if (입력 == 't' || 입력 == 'T') { 명령해석기.Terminālis(false); return; }
            if (입력 == 'q' || 입력 == 'Q' || 입력 == 27) break;
            if (입력 == 9 || 입력 == 'j') {
                atlase_VALUE = (atlase_VALUE + 1) % 5; 그리기(atlase_VALUE, Statuss_VALUE); 단말.Rakstīt("GUI FOCUS "); 단말.numurs(atlase_VALUE); 단말.문자(10);
            } else if (입력 == 13 || 입력 == 10) {
                if (atlase_VALUE == 4) { 명령해석기.Terminālis(false); return; }
                int mērs;
                if (atlase_VALUE < 2) mērs = Panelis.virkne_lietotājs_programma(atlase_VALUE == 0 ? 0 : 9);
                else if (atlase_VALUE == 2) {
                    mērs = 명령해석기.예제실행(10, "Hello.java");
                    if (mērs == 0) mērs = 명령해석기.예제실행(11, "Hello");
                } else mērs = 명령해석기.예제실행(12, "hello.py");
                Statuss_VALUE = mērs != 0 ? "PROGRAM FAILED" : atlase_VALUE == 0 ? "C++ FILE OK" : atlase_VALUE == 1 ? "UDP LOOPBACK OK" : atlase_VALUE == 2 ? "JAVA OK" : "MICROPYTHON OK";
                그리기(atlase_VALUE, Statuss_VALUE);
                단말.Rakstīt("GUI ACTION "); 단말.numurs(atlase_VALUE); 단말.Rakstīt(" RESULT "); 단말.numurs(mērs); 단말.문자(10);
            }
        }
        kodols.화면();
        단말.Rakstīt("GUI EXIT\n");
    }
}
