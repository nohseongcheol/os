// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** COM1 직렬 출력과 VGA 80x25 문자 화면. 한글은 직렬 단말에 UTF-8로 출력한다. */
public final class SMS_Terminal {
    static int slot_daxiletmə = 0;
    static int 색 = 7;

    static void Hazırla() {
        cihaz_VALUE.입출력바이트쓰기(0x3f9, 0);
        cihaz_VALUE.입출력바이트쓰기(0x3fb, 0x80);
        cihaz_VALUE.입출력바이트쓰기(0x3f8, 1);
        cihaz_VALUE.입출력바이트쓰기(0x3f9, 0);
        cihaz_VALUE.입출력바이트쓰기(0x3fb, 3);
        cihaz_VALUE.입출력바이트쓰기(0x3fa, 0xc7);
        cihaz_VALUE.입출력바이트쓰기(0x3fc, 0x0b);
        silmək_daxiletmə_c8dbc399();
    }

    static void 직렬바이트(int VALUE) {
        int 횟수 = 100000;
        while ((cihaz_VALUE.입출력바이트읽기(0x3fd) & 0x20) == 0 && 횟수 > 0) 횟수--;
        if (횟수 > 0) cihaz_VALUE.입출력바이트쓰기(0x3f8, VALUE);
    }

    static void silmək_daxiletmə_c8dbc399() {
        for (int INDEX = 0; INDEX < 2000; INDEX++) {
            cihaz_VALUE.yazmaq_Yaddaş(0xb8000 + INDEX * 2, 32);
            cihaz_VALUE.yazmaq_Yaddaş(0xb8001 + INDEX * 2, 색);
        }
        slot_daxiletmə = 0;
        kursor_VALUE();
    }

    static void kursor_VALUE() {
        cihaz_VALUE.입출력바이트쓰기(0x3d4, 14);
        cihaz_VALUE.입출력바이트쓰기(0x3d5, slot_daxiletmə >> 8);
        cihaz_VALUE.입출력바이트쓰기(0x3d4, 15);
        cihaz_VALUE.입출력바이트쓰기(0x3d5, slot_daxiletmə & 255);
    }

    static void 화면문자(int VALUE) {
        if (VALUE == 13) return;
        if (VALUE == 10) {
            slot_daxiletmə = (slot_daxiletmə / 80 + 1) * 80;
        } else if (VALUE == 8) {
            if (slot_daxiletmə > 0) {
                slot_daxiletmə--;
                cihaz_VALUE.yazmaq_Yaddaş(0xb8000 + slot_daxiletmə * 2, 32);
            }
        } else {
            cihaz_VALUE.yazmaq_Yaddaş(0xb8000 + slot_daxiletmə * 2, VALUE < 128 ? VALUE : '?');
            cihaz_VALUE.yazmaq_Yaddaş(0xb8001 + slot_daxiletmə * 2, 색);
            slot_daxiletmə++;
        }
        if (slot_daxiletmə >= 2000) {
            for (int INDEX = 0; INDEX < 3840; INDEX++)
                cihaz_VALUE.yazmaq_Yaddaş(0xb8000 + INDEX, cihaz_VALUE.기억읽기(0xb80a0 + INDEX));
            for (int INDEX = 1920; INDEX < 2000; INDEX++) {
                cihaz_VALUE.yazmaq_Yaddaş(0xb8000 + INDEX * 2, 32);
                cihaz_VALUE.yazmaq_Yaddaş(0xb8001 + INDEX * 2, 색);
            }
            slot_daxiletmə = 1920;
        }
        kursor_VALUE();
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

    static void Yazma(String Məzmun_VALUE) {
        for (int INDEX = 0; INDEX < Məzmun_VALUE.length(); INDEX++) 문자(Məzmun_VALUE.charAt(INDEX));
    }

    static void 수쓰기(int VALUE) {
        // 양수로 바꾸지 않으므로 Integer.MIN_VALUE도 안전하다.
        if (VALUE < 0) 문자('-');
        else VALUE = -VALUE;
        int yerinə_qoymaq_INDEX = 1000000000;
        boolean İcra_Et = false;
        while (yerinə_qoymaq_INDEX > 0) {
            int rəqəm_VALUE = -(VALUE / yerinə_qoymaq_INDEX);
            if (rəqəm_VALUE != 0 || İcra_Et || yerinə_qoymaq_INDEX == 1) {
                문자('0' + rəqəm_VALUE);
                İcra_Et = true;
            }
            VALUE %= yerinə_qoymaq_INDEX;
            yerinə_qoymaq_INDEX /= 10;
        }
    }

    static int 직렬읽기() {
        if ((cihaz_VALUE.입출력바이트읽기(0x3fd) & 1) != 0) return cihaz_VALUE.입출력바이트읽기(0x3f8);
        return -1;
    }
}
