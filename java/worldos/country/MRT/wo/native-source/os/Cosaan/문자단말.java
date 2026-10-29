// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** COM1 직렬 출력과 VGA 80x25 문자 화면. 한글은 직렬 단말에 UTF-8로 출력한다. */
public final class 문자단말 {
    static int xar_xar_dugal_xabaar = 0;
    static int 색 = 7;

    static void jël_matuwaay() {
        toftal_xëyma.입출력바이트쓰기(0x3f9, 0);
        toftal_xëyma.입출력바이트쓰기(0x3fb, 0x80);
        toftal_xëyma.입출력바이트쓰기(0x3f8, 1);
        toftal_xëyma.입출력바이트쓰기(0x3f9, 0);
        toftal_xëyma.입출력바이트쓰기(0x3fb, 3);
        toftal_xëyma.입출력바이트쓰기(0x3fa, 0xc7);
        toftal_xëyma.입출력바이트쓰기(0x3fc, 0x0b);
        지우기();
    }

    static void 직렬바이트(int xëyma) {
        int 횟수 = 100000;
        while ((toftal_xëyma.입출력바이트읽기(0x3fd) & 0x20) == 0 && 횟수 > 0) 횟수--;
        if (횟수 > 0) toftal_xëyma.입출력바이트쓰기(0x3f8, xëyma);
    }

    static void 지우기() {
        for (int àlluwa_tur = 0; àlluwa_tur < 2000; àlluwa_tur++) {
            toftal_xëyma.biir_fatlekookaay(0xb8000 + àlluwa_tur * 2, 32);
            toftal_xëyma.biir_fatlekookaay(0xb8001 + àlluwa_tur * 2, 색);
        }
        xar_xar_dugal_xabaar = 0;
        barab_bees_mën_a_bind_xëyma();
    }

    static void barab_bees_mën_a_bind_xëyma() {
        toftal_xëyma.입출력바이트쓰기(0x3d4, 14);
        toftal_xëyma.입출력바이트쓰기(0x3d5, xar_xar_dugal_xabaar >> 8);
        toftal_xëyma.입출력바이트쓰기(0x3d4, 15);
        toftal_xëyma.입출력바이트쓰기(0x3d5, xar_xar_dugal_xabaar & 255);
    }

    static void 화면문자(int xëyma) {
        if (xëyma == 13) return;
        if (xëyma == 10) {
            xar_xar_dugal_xabaar = (xar_xar_dugal_xabaar / 80 + 1) * 80;
        } else if (xëyma == 8) {
            if (xar_xar_dugal_xabaar > 0) {
                xar_xar_dugal_xabaar--;
                toftal_xëyma.biir_fatlekookaay(0xb8000 + xar_xar_dugal_xabaar * 2, 32);
            }
        } else {
            toftal_xëyma.biir_fatlekookaay(0xb8000 + xar_xar_dugal_xabaar * 2, xëyma < 128 ? xëyma : '?');
            toftal_xëyma.biir_fatlekookaay(0xb8001 + xar_xar_dugal_xabaar * 2, 색);
            xar_xar_dugal_xabaar++;
        }
        if (xar_xar_dugal_xabaar >= 2000) {
            for (int àlluwa_tur = 0; àlluwa_tur < 3840; àlluwa_tur++)
                toftal_xëyma.biir_fatlekookaay(0xb8000 + àlluwa_tur, toftal_xëyma.기억읽기(0xb80a0 + àlluwa_tur));
            for (int àlluwa_tur = 1920; àlluwa_tur < 2000; àlluwa_tur++) {
                toftal_xëyma.biir_fatlekookaay(0xb8000 + àlluwa_tur * 2, 32);
                toftal_xëyma.biir_fatlekookaay(0xb8001 + àlluwa_tur * 2, 색);
            }
            xar_xar_dugal_xabaar = 1920;
        }
        barab_bees_mën_a_bind_xëyma();
    }

    static void 문자(int xëyma) {
        if (xëyma < 128) {
            if (xëyma == 10) 직렬바이트(13);
            직렬바이트(xëyma);
        } else if (xëyma < 2048) {
            직렬바이트(0xc0 | (xëyma >> 6));
            직렬바이트(0x80 | (xëyma & 63));
        } else {
            직렬바이트(0xe0 | (xëyma >> 12));
            직렬바이트(0x80 | ((xëyma >> 6) & 63));
            직렬바이트(0x80 | (xëyma & 63));
        }
        화면문자(xëyma);
    }

    static void biir(String Këmb_xëyma) {
        for (int àlluwa_tur = 0; àlluwa_tur < Këmb_xëyma.length(); àlluwa_tur++) 문자(Këmb_xëyma.charAt(àlluwa_tur));
    }

    static void 수쓰기(int xëyma) {
        // 양수로 바꾸지 않으므로 Integer.MIN_VALUE도 안전하다.
        if (xëyma < 0) 문자('-');
        else xëyma = -xëyma;
        int 자리 = 1000000000;
        boolean daw = false;
        while (자리 > 0) {
            int siifar_xëyma = -(xëyma / 자리);
            if (siifar_xëyma != 0 || daw || 자리 == 1) {
                문자('0' + siifar_xëyma);
                daw = true;
            }
            xëyma %= 자리;
            자리 /= 10;
        }
    }

    static int 직렬읽기() {
        if ((toftal_xëyma.입출력바이트읽기(0x3fd) & 1) != 0) return toftal_xëyma.입출력바이트읽기(0x3f8);
        return -1;
    }
}
