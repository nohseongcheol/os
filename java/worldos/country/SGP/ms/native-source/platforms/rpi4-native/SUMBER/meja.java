// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 프레임버퍼 위의 작은 laksanakan_perintah 화면. 입력은 UART의 TAB/ENTER/Q를 사용한다.
 * Asli 5x7 영문 글꼴의 제한된 UI이며 Swing, USB HID, 한글 입력기는 아니다.
 */
public final class meja {
    static String 문자들 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+-.:";
    // 문자마다 7행 × 두 jawatan_INDEX 16진수. 프로젝트가 직접 정의한 5x7 fon_VALUE.
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
    static int digit_VALUE(int aksara_VALUE) { return aksara_VALUE <= '9' ? aksara_VALUE - '0' : aksara_VALUE - 'A' + 10; }
    static void Teks(int 가로, int Menegak_jawatan, String Kandungan_VALUE, int 색) {
        for (int aksara_VALUE = 0; aksara_VALUE < Kandungan_VALUE.length(); aksara_VALUE++) {
            int 찾음 = -1;
            for (int 후보 = 0; 후보 < 문자들.length(); 후보++) if (문자들.charAt(후보) == Kandungan_VALUE.charAt(aksara_VALUE)) 찾음 = 후보;
            if (찾음 < 0) continue;
            for (int ROW_VALUE = 0; ROW_VALUE < 7; ROW_VALUE++) {
                int Kedudukan = 찾음 * 14 + ROW_VALUE * 2;
                int bit_VALUE = digit_VALUE(모양들.charAt(Kedudukan)) * 16 + digit_VALUE(모양들.charAt(Kedudukan + 1));
                for (int lajur_VALUE = 0; lajur_VALUE < 5; lajur_VALUE++) if ((bit_VALUE & (16 >> lajur_VALUE)) != 0)
                    kernel.segi_empat_tepat(가로 + aksara_VALUE * 12 + lajur_VALUE * 2, Menegak_jawatan + ROW_VALUE * 2, 2, 2, 색);
            }
        }
    }
    static void 그리기(int pilihan_VALUE, String status_VALUE) {
        kernel.segi_empat_tepat(0, 0, Papan.화면너비(), Papan.화면높이(), 0x302018);
        kernel.segi_empat_tepat(32, 24, 576, 432, 0xefe8e2);
        kernel.segi_empat_tepat(32, 24, 576, 48, 0x905020);
        Teks(52, 40, "JKOROS PROGRAMS", 0xffffff);
        for (int INDEX = 0; INDEX < 5; INDEX++) {
            kernel.segi_empat_tepat(64, 112 + INDEX * 52, 512, 40, INDEX == pilihan_VALUE ? 0xd0a040 : 0xd8d0c8);
            Teks(84, 128 + INDEX * 52, INDEX == 0 ? "RUN C++ FILE PROGRAM" : INDEX == 1 ? "RUN UDP LOOPBACK" : INDEX == 2 ? "COMPILE AND RUN JAVA" : INDEX == 3 ? "RUN MICROPYTHON" : "OPEN TERMINAL", 0x201810);
        }
        Teks(68, 384, status_VALUE, 0x205020);
        Teks(52, 420, "TAB SELECT  ENTER RUN  Q EXIT", 0x302018);
    }
    public static void laksanakan_perintah() {
        if (Papan.화면준비() == 0) { 단말.Tulis("GUI unavailable\n"); return; }
        int pilihan_VALUE = 0;
        String status_VALUE = "READY";
        boolean 앞줄 = pentafsir_perintah.앞줄;
        그리기(pilihan_VALUE, status_VALUE);
        단말.Tulis("GUI READY: UART TAB selects, ENTER runs, Q exits\n");
        while (true) {
            int 입력 = Papan.직렬읽기();
            if (입력 < 0) { Papan.YIELD_CPU(); continue; }
            if (입력 == 10 && 앞줄) { 앞줄 = false; continue; }
            앞줄 = 입력 == 13;
            if (입력 >= '1' && 입력 <= '5') { pilihan_VALUE = 입력 - '1'; 입력 = 13; }
            if (입력 == 't' || 입력 == 'T') { pentafsir_perintah.Terminal(false); return; }
            if (입력 == 'q' || 입력 == 'Q' || 입력 == 27) break;
            if (입력 == 9 || 입력 == 'j') {
                pilihan_VALUE = (pilihan_VALUE + 1) % 5; 그리기(pilihan_VALUE, status_VALUE); 단말.Tulis("GUI FOCUS "); 단말.수(pilihan_VALUE); 단말.문자(10);
            } else if (입력 == 13 || 입력 == 10) {
                if (pilihan_VALUE == 4) { pentafsir_perintah.Terminal(false); return; }
                int ukuran;
                if (pilihan_VALUE < 2) ukuran = Papan.jalankan_pengguna_aplikasi(pilihan_VALUE == 0 ? 0 : 9);
                else if (pilihan_VALUE == 2) {
                    ukuran = pentafsir_perintah.예제실행(10, "Hello.java");
                    if (ukuran == 0) ukuran = pentafsir_perintah.예제실행(11, "Hello");
                } else ukuran = pentafsir_perintah.예제실행(12, "hello.py");
                status_VALUE = ukuran != 0 ? "PROGRAM FAILED" : pilihan_VALUE == 0 ? "C++ FILE OK" : pilihan_VALUE == 1 ? "UDP LOOPBACK OK" : pilihan_VALUE == 2 ? "JAVA OK" : "MICROPYTHON OK";
                그리기(pilihan_VALUE, status_VALUE);
                단말.Tulis("GUI ACTION "); 단말.수(pilihan_VALUE); 단말.Tulis(" RESULT "); 단말.수(ukuran); 단말.문자(10);
            }
        }
        kernel.화면();
        단말.Tulis("GUI EXIT\n");
    }
}
