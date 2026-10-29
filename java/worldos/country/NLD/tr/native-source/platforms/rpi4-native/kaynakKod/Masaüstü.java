// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 프레임버퍼 위의 작은 yürütmek_komut 화면. 입력은 UART의 TAB/ENTER/Q를 사용한다.
 * Öz 5x7 영문 글꼴의 제한된 UI이며 Swing, USB HID, 한글 입력기는 아니다.
 */
public final class Masaüstü {
    static String 문자들 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+-.:";
    // 문자마다 7행 × 두 konum_dizini 16진수. 프로젝트가 직접 정의한 5x7 yazı_tipi_değer.
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
    static int rakam_değer(int karakter_değer) { return karakter_değer <= '9' ? karakter_değer - '0' : karakter_değer - 'A' + 10; }
    static void metin(int 가로, int Dikey_konum, String içerik_değer, int 색) {
        for (int karakter_değer = 0; karakter_değer < içerik_değer.length(); karakter_değer++) {
            int 찾음 = -1;
            for (int aday = 0; aday < 문자들.length(); aday++) if (문자들.charAt(aday) == içerik_değer.charAt(karakter_değer)) 찾음 = aday;
            if (찾음 < 0) continue;
            for (int SATIR_değer = 0; SATIR_değer < 7; SATIR_değer++) {
                int konum = 찾음 * 14 + SATIR_değer * 2;
                int bit_değer = rakam_değer(모양들.charAt(konum)) * 16 + rakam_değer(모양들.charAt(konum + 1));
                for (int SÜTUN_değer = 0; SÜTUN_değer < 5; SÜTUN_değer++) if ((bit_değer & (16 >> SÜTUN_değer)) != 0)
                    Çekirdek.dikdörtgen(가로 + karakter_değer * 12 + SÜTUN_değer * 2, Dikey_konum + SATIR_değer * 2, 2, 2, 색);
            }
        }
    }
    static void 그리기(int seçim_değer, String Durum_değer) {
        Çekirdek.dikdörtgen(0, 0, Pano.화면너비(), Pano.화면높이(), 0x302018);
        Çekirdek.dikdörtgen(32, 24, 576, 432, 0xefe8e2);
        Çekirdek.dikdörtgen(32, 24, 576, 48, 0x905020);
        metin(52, 40, "JKOROS PROGRAMS", 0xffffff);
        for (int Dizin = 0; Dizin < 5; Dizin++) {
            Çekirdek.dikdörtgen(64, 112 + Dizin * 52, 512, 40, Dizin == seçim_değer ? 0xd0a040 : 0xd8d0c8);
            metin(84, 128 + Dizin * 52, Dizin == 0 ? "RUN C++ FILE PROGRAM" : Dizin == 1 ? "RUN UDP LOOPBACK" : Dizin == 2 ? "COMPILE AND RUN JAVA" : Dizin == 3 ? "RUN MICROPYTHON" : "OPEN TERMINAL", 0x201810);
        }
        metin(68, 384, Durum_değer, 0x205020);
        metin(52, 420, "TAB SELECT  ENTER RUN  Q EXIT", 0x302018);
    }
    public static void yürütmek_komut() {
        if (Pano.화면준비() == 0) { 단말.Yazma("GUI unavailable\n"); return; }
        int seçim_değer = 0;
        String Durum_değer = "READY";
        boolean Önceki_hat = KomutYorumlayıcı.Önceki_hat;
        그리기(seçim_değer, Durum_değer);
        단말.Yazma("GUI READY: UART TAB selects, ENTER runs, Q exits\n");
        while (true) {
            int artış_değer = Pano.직렬읽기();
            if (artış_değer < 0) { Pano.ÖDEME_CPU(); continue; }
            if (artış_değer == 10 && Önceki_hat) { Önceki_hat = false; continue; }
            Önceki_hat = artış_değer == 13;
            if (artış_değer >= '1' && artış_değer <= '5') { seçim_değer = artış_değer - '1'; artış_değer = 13; }
            if (artış_değer == 't' || artış_değer == 'T') { KomutYorumlayıcı.uçbirim(false); return; }
            if (artış_değer == 'q' || artış_değer == 'Q' || artış_değer == 27) break;
            if (artış_değer == 9 || artış_değer == 'j') {
                seçim_değer = (seçim_değer + 1) % 5; 그리기(seçim_değer, Durum_değer); 단말.Yazma("GUI FOCUS "); 단말.수(seçim_değer); 단말.문자(10);
            } else if (artış_değer == 13 || artış_değer == 10) {
                if (seçim_değer == 4) { KomutYorumlayıcı.uçbirim(false); return; }
                int sonuç;
                if (seçim_değer < 2) sonuç = Pano.çalıştırma_kullanıcı_program(seçim_değer == 0 ? 0 : 9);
                else if (seçim_değer == 2) {
                    sonuç = KomutYorumlayıcı.예제실행(10, "Hello.java");
                    if (sonuç == 0) sonuç = KomutYorumlayıcı.예제실행(11, "Hello");
                } else sonuç = KomutYorumlayıcı.예제실행(12, "hello.py");
                Durum_değer = sonuç != 0 ? "PROGRAM FAILED" : seçim_değer == 0 ? "C++ FILE OK" : seçim_değer == 1 ? "UDP LOOPBACK OK" : seçim_değer == 2 ? "JAVA OK" : "MICROPYTHON OK";
                그리기(seçim_değer, Durum_değer);
                단말.Yazma("GUI ACTION "); 단말.수(seçim_değer); 단말.Yazma(" RESULT "); 단말.수(sonuç); 단말.문자(10);
            }
        }
        Çekirdek.화면();
        단말.Yazma("GUI EXIT\n");
    }
}
