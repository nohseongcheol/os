// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** COM1 직렬 출력과 VGA 80x25 문자 화면. 한글은 직렬 단말에 UTF-8로 출력한다. */
public final class SMS_Teirminéal {
    static int spás_iontráil = 0;
    static int 색 = 7;

    static void Ullmhaigh() {
        gléas_VALUE.입출력바이트쓰기(0x3f9, 0);
        gléas_VALUE.입출력바이트쓰기(0x3fb, 0x80);
        gléas_VALUE.입출력바이트쓰기(0x3f8, 1);
        gléas_VALUE.입출력바이트쓰기(0x3f9, 0);
        gléas_VALUE.입출력바이트쓰기(0x3fb, 3);
        gléas_VALUE.입출력바이트쓰기(0x3fa, 0xc7);
        gléas_VALUE.입출력바이트쓰기(0x3fc, 0x0b);
        지우기();
    }

    static void 직렬바이트(int VALUE) {
        int 횟수 = 100000;
        while ((gléas_VALUE.입출력바이트읽기(0x3fd) & 0x20) == 0 && 횟수 > 0) 횟수--;
        if (횟수 > 0) gléas_VALUE.입출력바이트쓰기(0x3f8, VALUE);
    }

    static void 지우기() {
        for (int INDEX = 0; INDEX < 2000; INDEX++) {
            gléas_VALUE.scríobh_Cuimhne(0xb8000 + INDEX * 2, 32);
            gléas_VALUE.scríobh_Cuimhne(0xb8001 + INDEX * 2, 색);
        }
        spás_iontráil = 0;
        cúrsóir_VALUE();
    }

    static void cúrsóir_VALUE() {
        gléas_VALUE.입출력바이트쓰기(0x3d4, 14);
        gléas_VALUE.입출력바이트쓰기(0x3d5, spás_iontráil >> 8);
        gléas_VALUE.입출력바이트쓰기(0x3d4, 15);
        gléas_VALUE.입출력바이트쓰기(0x3d5, spás_iontráil & 255);
    }

    static void 화면문자(int VALUE) {
        if (VALUE == 13) return;
        if (VALUE == 10) {
            spás_iontráil = (spás_iontráil / 80 + 1) * 80;
        } else if (VALUE == 8) {
            if (spás_iontráil > 0) {
                spás_iontráil--;
                gléas_VALUE.scríobh_Cuimhne(0xb8000 + spás_iontráil * 2, 32);
            }
        } else {
            gléas_VALUE.scríobh_Cuimhne(0xb8000 + spás_iontráil * 2, VALUE < 128 ? VALUE : '?');
            gléas_VALUE.scríobh_Cuimhne(0xb8001 + spás_iontráil * 2, 색);
            spás_iontráil++;
        }
        if (spás_iontráil >= 2000) {
            for (int INDEX = 0; INDEX < 3840; INDEX++)
                gléas_VALUE.scríobh_Cuimhne(0xb8000 + INDEX, gléas_VALUE.기억읽기(0xb80a0 + INDEX));
            for (int INDEX = 1920; INDEX < 2000; INDEX++) {
                gléas_VALUE.scríobh_Cuimhne(0xb8000 + INDEX * 2, 32);
                gléas_VALUE.scríobh_Cuimhne(0xb8001 + INDEX * 2, 색);
            }
            spás_iontráil = 1920;
        }
        cúrsóir_VALUE();
    }

    static void 문자(int VALUE) {
        if (VALUE < 128) {
            if (VALUE == 10) 직렬바이트(13);
            직렬바이트(VALUE);
        } else if (VALUE < 2048) {
            직렬바이트(0xc0 | (VALUE >> 6));
            직렬바이트(0x80 | (VALUE & 63));
        } else {
            직렬바이트(0xe0 | (VALUE >> 12));
            직렬바이트(0x80 | ((VALUE >> 6) & 63));
            직렬바이트(0x80 | (VALUE & 63));
        }
        화면문자(VALUE);
    }

    static void Scríobh(String Inneachar_VALUE) {
        for (int INDEX = 0; INDEX < Inneachar_VALUE.length(); INDEX++) 문자(Inneachar_VALUE.charAt(INDEX));
    }

    static void 수쓰기(int VALUE) {
        // 양수로 바꾸지 않으므로 Integer.MIN_VALUE도 안전하다.
        if (VALUE < 0) 문자('-');
        else VALUE = -VALUE;
        int suíomh_INDEX = 1000000000;
        boolean Rith_2 = false;
        while (suíomh_INDEX > 0) {
            int digit_VALUE = -(VALUE / suíomh_INDEX);
            if (digit_VALUE != 0 || Rith_2 || suíomh_INDEX == 1) {
                문자('0' + digit_VALUE);
                Rith_2 = true;
            }
            VALUE %= suíomh_INDEX;
            suíomh_INDEX /= 10;
        }
    }

    static int 직렬읽기() {
        if ((gléas_VALUE.입출력바이트읽기(0x3fd) & 1) != 0) return gléas_VALUE.입출력바이트읽기(0x3f8);
        return -1;
    }
}
