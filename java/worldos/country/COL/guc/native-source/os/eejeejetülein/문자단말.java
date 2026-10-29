// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** COM1 직렬 출력과 VGA 80x25 문자 화면. 한글은 직렬 단말에 UTF-8로 출력한다. */
public final class 문자단말 {
    static int 칸 = 0;
    static int 색 = 7;

    static void 준비() {
        serulaalü_ajutuu.입출력바이트쓰기(0x3f9, 0);
        serulaalü_ajutuu.입출력바이트쓰기(0x3fb, 0x80);
        serulaalü_ajutuu.입출력바이트쓰기(0x3f8, 1);
        serulaalü_ajutuu.입출력바이트쓰기(0x3f9, 0);
        serulaalü_ajutuu.입출력바이트쓰기(0x3fb, 3);
        serulaalü_ajutuu.입출력바이트쓰기(0x3fa, 0xc7);
        serulaalü_ajutuu.입출력바이트쓰기(0x3fc, 0x0b);
        지우기();
    }

    static void 직렬바이트(int ajutuu) {
        int 횟수 = 100000;
        while ((serulaalü_ajutuu.입출력바이트읽기(0x3fd) & 0x20) == 0 && 횟수 > 0) 횟수--;
        if (횟수 > 0) serulaalü_ajutuu.입출력바이트쓰기(0x3f8, ajutuu);
    }

    static void 지우기() {
        for (int ee_iyatialujuna = 0; ee_iyatialujuna < 2000; ee_iyatialujuna++) {
            serulaalü_ajutuu.기억쓰기(0xb8000 + ee_iyatialujuna * 2, 32);
            serulaalü_ajutuu.기억쓰기(0xb8001 + ee_iyatialujuna * 2, 색);
        }
        칸 = 0;
        ee_iyatiaa_ajutuu();
    }

    static void ee_iyatiaa_ajutuu() {
        serulaalü_ajutuu.입출력바이트쓰기(0x3d4, 14);
        serulaalü_ajutuu.입출력바이트쓰기(0x3d5, 칸 >> 8);
        serulaalü_ajutuu.입출력바이트쓰기(0x3d4, 15);
        serulaalü_ajutuu.입출력바이트쓰기(0x3d5, 칸 & 255);
    }

    static void 화면문자(int ajutuu) {
        if (ajutuu == 13) return;
        if (ajutuu == 10) {
            칸 = (칸 / 80 + 1) * 80;
        } else if (ajutuu == 8) {
            if (칸 > 0) {
                칸--;
                serulaalü_ajutuu.기억쓰기(0xb8000 + 칸 * 2, 32);
            }
        } else {
            serulaalü_ajutuu.기억쓰기(0xb8000 + 칸 * 2, ajutuu < 128 ? ajutuu : '?');
            serulaalü_ajutuu.기억쓰기(0xb8001 + 칸 * 2, 색);
            칸++;
        }
        if (칸 >= 2000) {
            for (int ee_iyatialujuna = 0; ee_iyatialujuna < 3840; ee_iyatialujuna++)
                serulaalü_ajutuu.기억쓰기(0xb8000 + ee_iyatialujuna, serulaalü_ajutuu.기억읽기(0xb80a0 + ee_iyatialujuna));
            for (int ee_iyatialujuna = 1920; ee_iyatialujuna < 2000; ee_iyatialujuna++) {
                serulaalü_ajutuu.기억쓰기(0xb8000 + ee_iyatialujuna * 2, 32);
                serulaalü_ajutuu.기억쓰기(0xb8001 + ee_iyatialujuna * 2, 색);
            }
            칸 = 1920;
        }
        ee_iyatiaa_ajutuu();
    }

    static void 문자(int ajutuu) {
        if (ajutuu < 128) {
            if (ajutuu == 10) 직렬바이트(13);
            직렬바이트(ajutuu);
        } else if (ajutuu < 2048) {
            직렬바이트(0xc0 | (ajutuu >> 6));
            직렬바이트(0x80 | (ajutuu & 63));
        } else {
            직렬바이트(0xe0 | (ajutuu >> 12));
            직렬바이트(0x80 | ((ajutuu >> 6) & 63));
            직렬바이트(0x80 | (ajutuu & 63));
        }
        화면문자(ajutuu);
    }

    static void ashajaa(String alu_ujatüü_ajutuu) {
        for (int ee_iyatialujuna = 0; ee_iyatialujuna < alu_ujatüü_ajutuu.length(); ee_iyatialujuna++) 문자(alu_ujatüü_ajutuu.charAt(ee_iyatialujuna));
    }

    static void 수쓰기(int ajutuu) {
        // 양수로 바꾸지 않으므로 Integer.MIN_VALUE도 안전하다.
        if (ajutuu < 0) 문자('-');
        else ajutuu = -ajutuu;
        int 자리 = 1000000000;
        boolean 시작 = false;
        while (자리 > 0) {
            int 숫자 = -(ajutuu / 자리);
            if (숫자 != 0 || 시작 || 자리 == 1) {
                문자('0' + 숫자);
                시작 = true;
            }
            ajutuu %= 자리;
            자리 /= 10;
        }
    }

    static int 직렬읽기() {
        if ((serulaalü_ajutuu.입출력바이트읽기(0x3fd) & 1) != 0) return serulaalü_ajutuu.입출력바이트읽기(0x3f8);
        return -1;
    }
}
