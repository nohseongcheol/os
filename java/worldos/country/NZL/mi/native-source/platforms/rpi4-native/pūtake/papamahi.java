// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 프레임버퍼 위의 작은 kawe_tono 화면. 입력은 UART의 TAB/ENTER/Q를 사용한다.
 * 자체 5x7 영문 글꼴의 제한된 UI이며 Swing, USB HID, 한글 입력기는 아니다.
 */
public final class papamahi {
    static String 문자들 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+-.:";
    // 문자마다 7행 × 두 tūranga_INDEX 16진수. 프로젝트가 직접 정의한 5x7 momotuhi_uara.
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
    static int mati_uara(int pūāhua_uara) { return pūāhua_uara <= '9' ? pūāhua_uara - '0' : pūāhua_uara - 'A' + 10; }
    static void Ngā_kupu(int 가로, int Poutū_tūranga, String Ihirangi_uara, int 색) {
        for (int pūāhua_uara = 0; pūāhua_uara < Ihirangi_uara.length(); pūāhua_uara++) {
            int 찾음 = -1;
            for (int 후보 = 0; 후보 < 문자들.length(); 후보++) if (문자들.charAt(후보) == Ihirangi_uara.charAt(pūāhua_uara)) 찾음 = 후보;
            if (찾음 < 0) continue;
            for (int ROW_uara = 0; ROW_uara < 7; ROW_uara++) {
                int tūranga = 찾음 * 14 + ROW_uara * 2;
                int moka_uara = mati_uara(모양들.charAt(tūranga)) * 16 + mati_uara(모양들.charAt(tūranga + 1));
                for (int tīwae_uara = 0; tīwae_uara < 5; tīwae_uara++) if ((moka_uara & (16 >> tīwae_uara)) != 0)
                    kākano.사각형(가로 + pūāhua_uara * 12 + tīwae_uara * 2, Poutū_tūranga + ROW_uara * 2, 2, 2, 색);
            }
        }
    }
    static void 그리기(int tīpakonga_uara, String tūnga_uara) {
        kākano.사각형(0, 0, papa.화면너비(), papa.화면높이(), 0x302018);
        kākano.사각형(32, 24, 576, 432, 0xefe8e2);
        kākano.사각형(32, 24, 576, 48, 0x905020);
        Ngā_kupu(52, 40, "JKOROS PROGRAMS", 0xffffff);
        for (int INDEX = 0; INDEX < 5; INDEX++) {
            kākano.사각형(64, 112 + INDEX * 52, 512, 40, INDEX == tīpakonga_uara ? 0xd0a040 : 0xd8d0c8);
            Ngā_kupu(84, 128 + INDEX * 52, INDEX == 0 ? "RUN C++ FILE PROGRAM" : INDEX == 1 ? "RUN UDP LOOPBACK" : INDEX == 2 ? "COMPILE AND RUN JAVA" : INDEX == 3 ? "RUN MICROPYTHON" : "OPEN TERMINAL", 0x201810);
        }
        Ngā_kupu(68, 384, tūnga_uara, 0x205020);
        Ngā_kupu(52, 420, "TAB SELECT  ENTER RUN  Q EXIT", 0x302018);
    }
    public static void kawe_tono() {
        if (papa.화면준비() == 0) { 단말.Tuhia("GUI unavailable\n"); return; }
        int tīpakonga_uara = 0;
        String tūnga_uara = "READY";
        boolean 앞줄 = 명령해석기.앞줄;
        그리기(tīpakonga_uara, tūnga_uara);
        단말.Tuhia("GUI READY: UART TAB selects, ENTER runs, Q exits\n");
        while (true) {
            int 입력 = papa.직렬읽기();
            if (입력 < 0) { papa.YIELD_PTM(); continue; }
            if (입력 == 10 && 앞줄) { 앞줄 = false; continue; }
            앞줄 = 입력 == 13;
            if (입력 >= '1' && 입력 <= '5') { tīpakonga_uara = 입력 - '1'; 입력 = 13; }
            if (입력 == 't' || 입력 == 'T') { 명령해석기.Tauranga(false); return; }
            if (입력 == 'q' || 입력 == 'Q' || 입력 == 27) break;
            if (입력 == 9 || 입력 == 'j') {
                tīpakonga_uara = (tīpakonga_uara + 1) % 5; 그리기(tīpakonga_uara, tūnga_uara); 단말.Tuhia("GUI FOCUS "); 단말.수(tīpakonga_uara); 단말.문자(10);
            } else if (입력 == 13 || 입력 == 10) {
                if (tīpakonga_uara == 4) { 명령해석기.Tauranga(false); return; }
                int mēhua;
                if (tīpakonga_uara < 2) mēhua = papa.whakahaere_kaiwhakamahi_kaupapa(tīpakonga_uara == 0 ? 0 : 9);
                else if (tīpakonga_uara == 2) {
                    mēhua = 명령해석기.예제실행(10, "Hello.java");
                    if (mēhua == 0) mēhua = 명령해석기.예제실행(11, "Hello");
                } else mēhua = 명령해석기.예제실행(12, "hello.py");
                tūnga_uara = mēhua != 0 ? "PROGRAM FAILED" : tīpakonga_uara == 0 ? "C++ FILE OK" : tīpakonga_uara == 1 ? "UDP LOOPBACK OK" : tīpakonga_uara == 2 ? "JAVA OK" : "MICROPYTHON OK";
                그리기(tīpakonga_uara, tūnga_uara);
                단말.Tuhia("GUI ACTION "); 단말.수(tīpakonga_uara); 단말.Tuhia(" RESULT "); 단말.수(mēhua); 단말.문자(10);
            }
        }
        kākano.화면();
        단말.Tuhia("GUI EXIT\n");
    }
}
