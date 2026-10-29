// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 프레임버퍼 위의 작은 köra_kommando skärmbild. 입력은 UART의 TAB/ENTER/Q를 사용한다.
 * eget 5x7 영문 글꼴의 제한된 UI이며 Swing, USB HID, 한글 입력기는 아니다.
 */
public final class Dator {
    static String 문자들 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+-.:";
    // 문자마다 7행 × 두 positionsindex 16진수. 프로젝트가 직접 정의한 5x7 teckensnitt_värde.
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
    static int siffra_värde(int tecken_värde) { return tecken_värde <= '9' ? tecken_värde - '0' : tecken_värde - 'A' + 10; }
    static void text(int 가로, int bransch_placera, String Innehåll_värde, int 색) {
        for (int tecken_värde = 0; tecken_värde < Innehåll_värde.length(); tecken_värde++) {
            int 찾음 = -1;
            for (int kandidat = 0; kandidat < 문자들.length(); kandidat++) if (문자들.charAt(kandidat) == Innehåll_värde.charAt(tecken_värde)) 찾음 = kandidat;
            if (찾음 < 0) continue;
            for (int RAD_värde = 0; RAD_värde < 7; RAD_värde++) {
                int position = 찾음 * 14 + RAD_värde * 2;
                int bit_värde = siffra_värde(모양들.charAt(position)) * 16 + siffra_värde(모양들.charAt(position + 1));
                for (int spalt_värde = 0; spalt_värde < 5; spalt_värde++) if ((bit_värde & (16 >> spalt_värde)) != 0)
                    kärna.rektangel(가로 + tecken_värde * 12 + spalt_värde * 2, bransch_placera + RAD_värde * 2, 2, 2, 색);
            }
        }
    }
    static void Paint_skärmbild(int markering_värde, String status_värde) {
        kärna.rektangel(0, 0, Tavla.화면너비(), Tavla.화면높이(), 0x302018);
        kärna.rektangel(32, 24, 576, 432, 0xefe8e2);
        kärna.rektangel(32, 24, 576, 48, 0x905020);
        text(52, 40, "JKOROS PROGRAMS", 0xffffff);
        for (int INDEX = 0; INDEX < 5; INDEX++) {
            kärna.rektangel(64, 112 + INDEX * 52, 512, 40, INDEX == markering_värde ? 0xd0a040 : 0xd8d0c8);
            text(84, 128 + INDEX * 52, INDEX == 0 ? "RUN C++ FILE PROGRAM" : INDEX == 1 ? "RUN UDP LOOPBACK" : INDEX == 2 ? "COMPILE AND RUN JAVA" : INDEX == 3 ? "RUN MICROPYTHON" : "OPEN TERMINAL", 0x201810);
        }
        text(68, 384, status_värde, 0x205020);
        text(52, 420, "TAB SELECT  ENTER RUN  Q EXIT", 0x302018);
    }
    public static void köra_kommando() {
        if (Tavla.Förbereda_skärmbild() == 0) { 단말.Skriv("GUI unavailable\n"); return; }
        int markering_värde = 0;
        String status_värde = "READY";
        boolean Föregående_rad = 명령해석기.Föregående_rad;
        Paint_skärmbild(markering_värde, status_värde);
        단말.Skriv("GUI READY: UART TAB selects, ENTER runs, Q exits\n");
        while (true) {
            int indata_värde = Tavla.직렬읽기();
            if (indata_värde < 0) { Tavla.NOMAVK_CPU(); continue; }
            if (indata_värde == 10 && Föregående_rad) { Föregående_rad = false; continue; }
            Föregående_rad = indata_värde == 13;
            if (indata_värde >= '1' && indata_värde <= '5') { markering_värde = indata_värde - '1'; indata_värde = 13; }
            if (indata_värde == 't' || indata_värde == 'T') { 명령해석기.kommandotolk(false); return; }
            if (indata_värde == 'q' || indata_värde == 'Q' || indata_värde == 27) break;
            if (indata_värde == 9 || indata_värde == 'j') {
                markering_värde = (markering_värde + 1) % 5; Paint_skärmbild(markering_värde, status_värde); 단말.Skriv("GUI FOCUS "); 단말.nummer(markering_värde); 단말.문자(10);
            } else if (indata_värde == 13 || indata_värde == 10) {
                if (markering_värde == 4) { 명령해석기.kommandotolk(false); return; }
                int RESULTAT;
                if (markering_värde < 2) RESULTAT = Tavla.köra_användare_app(markering_värde == 0 ? 0 : 9);
                else if (markering_värde == 2) {
                    RESULTAT = 명령해석기.예제실행(10, "Hello.java");
                    if (RESULTAT == 0) RESULTAT = 명령해석기.예제실행(11, "Hello");
                } else RESULTAT = 명령해석기.예제실행(12, "hello.py");
                status_värde = RESULTAT != 0 ? "PROGRAM FAILED" : markering_värde == 0 ? "C++ FILE OK" : markering_värde == 1 ? "UDP LOOPBACK OK" : markering_värde == 2 ? "JAVA OK" : "MICROPYTHON OK";
                Paint_skärmbild(markering_värde, status_värde);
                단말.Skriv("GUI ACTION "); 단말.nummer(markering_värde); 단말.Skriv(" RESULT "); 단말.nummer(RESULTAT); 단말.문자(10);
            }
        }
        kärna.skärmbild();
        단말.Skriv("GUI EXIT\n");
    }
}
