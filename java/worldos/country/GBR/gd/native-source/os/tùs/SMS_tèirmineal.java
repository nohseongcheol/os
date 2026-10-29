// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** COM1 직렬 출력과 VGA 80x25 문자 화면. 한글은 직렬 단말에 UTF-8로 출력한다. */
public final class SMS_tèirmineal {
    static int slot_cur_a_steach = 0;
    static int 색 = 7;

    static void Ullaich() {
        uidheam_VALUE.입출력바이트쓰기(0x3f9, 0);
        uidheam_VALUE.입출력바이트쓰기(0x3fb, 0x80);
        uidheam_VALUE.입출력바이트쓰기(0x3f8, 1);
        uidheam_VALUE.입출력바이트쓰기(0x3f9, 0);
        uidheam_VALUE.입출력바이트쓰기(0x3fb, 3);
        uidheam_VALUE.입출력바이트쓰기(0x3fa, 0xc7);
        uidheam_VALUE.입출력바이트쓰기(0x3fc, 0x0b);
        지우기();
    }

    static void 직렬바이트(int VALUE) {
        int 횟수 = 100000;
        while ((uidheam_VALUE.입출력바이트읽기(0x3fd) & 0x20) == 0 && 횟수 > 0) 횟수--;
        if (횟수 > 0) uidheam_VALUE.입출력바이트쓰기(0x3f8, VALUE);
    }

    static void 지우기() {
        for (int INDEX = 0; INDEX < 2000; INDEX++) {
            uidheam_VALUE.sgrìobh_cuimhne(0xb8000 + INDEX * 2, 32);
            uidheam_VALUE.sgrìobh_cuimhne(0xb8001 + INDEX * 2, 색);
        }
        slot_cur_a_steach = 0;
        cursair_VALUE();
    }

    static void cursair_VALUE() {
        uidheam_VALUE.입출력바이트쓰기(0x3d4, 14);
        uidheam_VALUE.입출력바이트쓰기(0x3d5, slot_cur_a_steach >> 8);
        uidheam_VALUE.입출력바이트쓰기(0x3d4, 15);
        uidheam_VALUE.입출력바이트쓰기(0x3d5, slot_cur_a_steach & 255);
    }

    static void 화면문자(int VALUE) {
        if (VALUE == 13) return;
        if (VALUE == 10) {
            slot_cur_a_steach = (slot_cur_a_steach / 80 + 1) * 80;
        } else if (VALUE == 8) {
            if (slot_cur_a_steach > 0) {
                slot_cur_a_steach--;
                uidheam_VALUE.sgrìobh_cuimhne(0xb8000 + slot_cur_a_steach * 2, 32);
            }
        } else {
            uidheam_VALUE.sgrìobh_cuimhne(0xb8000 + slot_cur_a_steach * 2, VALUE < 128 ? VALUE : '?');
            uidheam_VALUE.sgrìobh_cuimhne(0xb8001 + slot_cur_a_steach * 2, 색);
            slot_cur_a_steach++;
        }
        if (slot_cur_a_steach >= 2000) {
            for (int INDEX = 0; INDEX < 3840; INDEX++)
                uidheam_VALUE.sgrìobh_cuimhne(0xb8000 + INDEX, uidheam_VALUE.기억읽기(0xb80a0 + INDEX));
            for (int INDEX = 1920; INDEX < 2000; INDEX++) {
                uidheam_VALUE.sgrìobh_cuimhne(0xb8000 + INDEX * 2, 32);
                uidheam_VALUE.sgrìobh_cuimhne(0xb8001 + INDEX * 2, 색);
            }
            slot_cur_a_steach = 1920;
        }
        cursair_VALUE();
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

    static void sgrìobh(String susbaint_VALUE) {
        for (int INDEX = 0; INDEX < susbaint_VALUE.length(); INDEX++) 문자(susbaint_VALUE.charAt(INDEX));
    }

    static void 수쓰기(int VALUE) {
        // 양수로 바꾸지 않으므로 Integer.MIN_VALUE도 안전하다.
        if (VALUE < 0) 문자('-');
        else VALUE = -VALUE;
        int suidhich_INDEX = 1000000000;
        boolean ruith = false;
        while (suidhich_INDEX > 0) {
            int figear_VALUE = -(VALUE / suidhich_INDEX);
            if (figear_VALUE != 0 || ruith || suidhich_INDEX == 1) {
                문자('0' + figear_VALUE);
                ruith = true;
            }
            VALUE %= suidhich_INDEX;
            suidhich_INDEX /= 10;
        }
    }

    static int 직렬읽기() {
        if ((uidheam_VALUE.입출력바이트읽기(0x3fd) & 1) != 0) return uidheam_VALUE.입출력바이트읽기(0x3f8);
        return -1;
    }
}
