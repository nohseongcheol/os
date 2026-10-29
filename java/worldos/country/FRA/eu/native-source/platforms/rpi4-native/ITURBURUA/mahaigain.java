// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 프레임버퍼 위의 작은 exekutatu_komando 화면. 입력은 UART의 TAB/ENTER/Q를 사용한다.
 * 자체 5x7 영문 글꼴의 제한된 UI이며 Swing, USB HID, 한글 입력기는 아니다.
 */
public final class mahaigain {
    static String 문자들 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+-.:";
    // 문자마다 7행 × 두 kargu_INDIZE 16진수. 프로젝트가 직접 정의한 5x7 letra_tipo_balio.
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
    static int digitu_balio(int karaktere_balio) { return karaktere_balio <= '9' ? karaktere_balio - '0' : karaktere_balio - 'A' + 10; }
    static void Testua(int 가로, int Bertikala_kargu, String eduki_balio, int 색) {
        for (int karaktere_balio = 0; karaktere_balio < eduki_balio.length(); karaktere_balio++) {
            int 찾음 = -1;
            for (int 후보 = 0; 후보 < 문자들.length(); 후보++) if (문자들.charAt(후보) == eduki_balio.charAt(karaktere_balio)) 찾음 = 후보;
            if (찾음 < 0) continue;
            for (int ERRENKADA_balio = 0; ERRENKADA_balio < 7; ERRENKADA_balio++) {
                int Posizioa = 찾음 * 14 + ERRENKADA_balio * 2;
                int bit_balio = digitu_balio(모양들.charAt(Posizioa)) * 16 + digitu_balio(모양들.charAt(Posizioa + 1));
                for (int zutabe_balio = 0; zutabe_balio < 5; zutabe_balio++) if ((bit_balio & (16 >> zutabe_balio)) != 0)
                    nukleo.사각형(가로 + karaktere_balio * 12 + zutabe_balio * 2, Bertikala_kargu + ERRENKADA_balio * 2, 2, 2, 색);
            }
        }
    }
    static void 그리기(int hautapen_balio, String Egoera_balio) {
        nukleo.사각형(0, 0, arbel.화면너비(), arbel.화면높이(), 0x302018);
        nukleo.사각형(32, 24, 576, 432, 0xefe8e2);
        nukleo.사각형(32, 24, 576, 48, 0x905020);
        Testua(52, 40, "JKOROS PROGRAMS", 0xffffff);
        for (int INDIZE = 0; INDIZE < 5; INDIZE++) {
            nukleo.사각형(64, 112 + INDIZE * 52, 512, 40, INDIZE == hautapen_balio ? 0xd0a040 : 0xd8d0c8);
            Testua(84, 128 + INDIZE * 52, INDIZE == 0 ? "RUN C++ FILE PROGRAM" : INDIZE == 1 ? "RUN UDP LOOPBACK" : INDIZE == 2 ? "COMPILE AND RUN JAVA" : INDIZE == 3 ? "RUN MICROPYTHON" : "OPEN TERMINAL", 0x201810);
        }
        Testua(68, 384, Egoera_balio, 0x205020);
        Testua(52, 420, "TAB SELECT  ENTER RUN  Q EXIT", 0x302018);
    }
    public static void exekutatu_komando() {
        if (arbel.화면준비() == 0) { 단말.Idatzi("GUI unavailable\n"); return; }
        int hautapen_balio = 0;
        String Egoera_balio = "READY";
        boolean 앞줄 = 명령해석기.앞줄;
        그리기(hautapen_balio, Egoera_balio);
        단말.Idatzi("GUI READY: UART TAB selects, ENTER runs, Q exits\n");
        while (true) {
            int 입력 = arbel.직렬읽기();
            if (입력 < 0) { arbel.YIELD_PUZ(); continue; }
            if (입력 == 10 && 앞줄) { 앞줄 = false; continue; }
            앞줄 = 입력 == 13;
            if (입력 >= '1' && 입력 <= '5') { hautapen_balio = 입력 - '1'; 입력 = 13; }
            if (입력 == 't' || 입력 == 'T') { 명령해석기.Terminala(false); return; }
            if (입력 == 'q' || 입력 == 'Q' || 입력 == 27) break;
            if (입력 == 9 || 입력 == 'j') {
                hautapen_balio = (hautapen_balio + 1) % 5; 그리기(hautapen_balio, Egoera_balio); 단말.Idatzi("GUI FOCUS "); 단말.수(hautapen_balio); 단말.문자(10);
            } else if (입력 == 13 || 입력 == 10) {
                if (hautapen_balio == 4) { 명령해석기.Terminala(false); return; }
                int EMAITZA;
                if (hautapen_balio < 2) EMAITZA = arbel.exekutatu_erabiltzaile_aplik(hautapen_balio == 0 ? 0 : 9);
                else if (hautapen_balio == 2) {
                    EMAITZA = 명령해석기.예제실행(10, "Hello.java");
                    if (EMAITZA == 0) EMAITZA = 명령해석기.예제실행(11, "Hello");
                } else EMAITZA = 명령해석기.예제실행(12, "hello.py");
                Egoera_balio = EMAITZA != 0 ? "PROGRAM FAILED" : hautapen_balio == 0 ? "C++ FILE OK" : hautapen_balio == 1 ? "UDP LOOPBACK OK" : hautapen_balio == 2 ? "JAVA OK" : "MICROPYTHON OK";
                그리기(hautapen_balio, Egoera_balio);
                단말.Idatzi("GUI ACTION "); 단말.수(hautapen_balio); 단말.Idatzi(" RESULT "); 단말.수(EMAITZA); 단말.문자(10);
            }
        }
        nukleo.화면();
        단말.Idatzi("GUI EXIT\n");
    }
}
