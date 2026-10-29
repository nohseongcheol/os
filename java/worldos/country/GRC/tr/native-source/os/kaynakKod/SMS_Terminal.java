// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** COM1 직렬 출력과 VGA 80x25 문자 화면. 한글은 직렬 단말에 UTF-8로 출력한다. */
public final class SMS_Terminal {
    static int yuva_girdi = 0;
    static int 색 = 7;

    static void Hazırlan() {
        cihaz_değer.입출력바이트쓰기(0x3f9, 0);
        cihaz_değer.입출력바이트쓰기(0x3fb, 0x80);
        cihaz_değer.입출력바이트쓰기(0x3f8, 1);
        cihaz_değer.입출력바이트쓰기(0x3f9, 0);
        cihaz_değer.입출력바이트쓰기(0x3fb, 3);
        cihaz_değer.입출력바이트쓰기(0x3fa, 0xc7);
        cihaz_değer.입출력바이트쓰기(0x3fc, 0x0b);
        silmek_girdi();
    }

    static void 직렬바이트(int değer) {
        int 횟수 = 100000;
        while ((cihaz_değer.입출력바이트읽기(0x3fd) & 0x20) == 0 && 횟수 > 0) 횟수--;
        if (횟수 > 0) cihaz_değer.입출력바이트쓰기(0x3f8, değer);
    }

    static void silmek_girdi() {
        for (int Dizin = 0; Dizin < 2000; Dizin++) {
            cihaz_değer.yazma_Bellek(0xb8000 + Dizin * 2, 32);
            cihaz_değer.yazma_Bellek(0xb8001 + Dizin * 2, 색);
        }
        yuva_girdi = 0;
        imleç_değer();
    }

    static void imleç_değer() {
        cihaz_değer.입출력바이트쓰기(0x3d4, 14);
        cihaz_değer.입출력바이트쓰기(0x3d5, yuva_girdi >> 8);
        cihaz_değer.입출력바이트쓰기(0x3d4, 15);
        cihaz_değer.입출력바이트쓰기(0x3d5, yuva_girdi & 255);
    }

    static void 화면문자(int değer) {
        if (değer == 13) return;
        if (değer == 10) {
            yuva_girdi = (yuva_girdi / 80 + 1) * 80;
        } else if (değer == 8) {
            if (yuva_girdi > 0) {
                yuva_girdi--;
                cihaz_değer.yazma_Bellek(0xb8000 + yuva_girdi * 2, 32);
            }
        } else {
            cihaz_değer.yazma_Bellek(0xb8000 + yuva_girdi * 2, değer < 128 ? değer : '?');
            cihaz_değer.yazma_Bellek(0xb8001 + yuva_girdi * 2, 색);
            yuva_girdi++;
        }
        if (yuva_girdi >= 2000) {
            for (int Dizin = 0; Dizin < 3840; Dizin++)
                cihaz_değer.yazma_Bellek(0xb8000 + Dizin, cihaz_değer.기억읽기(0xb80a0 + Dizin));
            for (int Dizin = 1920; Dizin < 2000; Dizin++) {
                cihaz_değer.yazma_Bellek(0xb8000 + Dizin * 2, 32);
                cihaz_değer.yazma_Bellek(0xb8001 + Dizin * 2, 색);
            }
            yuva_girdi = 1920;
        }
        imleç_değer();
    }

    static void 문자(int değer) {
        if (değer < 128) {
            if (değer == 10) 직렬바이트(13);
            직렬바이트(değer);
        } else if (değer < 2048) {
            직렬바이트(0xc0 | (değer >> 6));
            직렬바이트(0x80 | (değer & 63));
        } else {
            직렬바이트(0xe0 | (değer >> 12));
            직렬바이트(0x80 | ((değer >> 6) & 63));
            직렬바이트(0x80 | (değer & 63));
        }
        화면문자(değer);
    }

    static void Yazma(String içerik_değer) {
        for (int Dizin = 0; Dizin < içerik_değer.length(); Dizin++) 문자(içerik_değer.charAt(Dizin));
    }

    static void 수쓰기(int değer) {
        // 양수로 바꾸지 않으므로 Integer.MIN_VALUE도 안전하다.
        if (değer < 0) 문자('-');
        else değer = -değer;
        int konum_dizini = 1000000000;
        boolean çalıştır = false;
        while (konum_dizini > 0) {
            int rakam_değer = -(değer / konum_dizini);
            if (rakam_değer != 0 || çalıştır || konum_dizini == 1) {
                문자('0' + rakam_değer);
                çalıştır = true;
            }
            değer %= konum_dizini;
            konum_dizini /= 10;
        }
    }

    static int 직렬읽기() {
        if ((cihaz_değer.입출력바이트읽기(0x3fd) & 1) != 0) return cihaz_değer.입출력바이트읽기(0x3f8);
        return -1;
    }
}
