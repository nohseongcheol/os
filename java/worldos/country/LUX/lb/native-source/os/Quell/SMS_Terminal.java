// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** COM1 직렬 출력과 VGA 80x25 문자 화면. 한글은 직렬 단말에 UTF-8로 출력한다. */
public final class SMS_Terminal {
    static int Slot_Agab = 0;
    static int 색 = 7;

    static void Préparéieren() {
        Mobil_VALUE.입출력바이트쓰기(0x3f9, 0);
        Mobil_VALUE.입출력바이트쓰기(0x3fb, 0x80);
        Mobil_VALUE.입출력바이트쓰기(0x3f8, 1);
        Mobil_VALUE.입출력바이트쓰기(0x3f9, 0);
        Mobil_VALUE.입출력바이트쓰기(0x3fb, 3);
        Mobil_VALUE.입출력바이트쓰기(0x3fa, 0xc7);
        Mobil_VALUE.입출력바이트쓰기(0x3fc, 0x0b);
        지우기();
    }

    static void 직렬바이트(int VALUE) {
        int 횟수 = 100000;
        while ((Mobil_VALUE.입출력바이트읽기(0x3fd) & 0x20) == 0 && 횟수 > 0) 횟수--;
        if (횟수 > 0) Mobil_VALUE.입출력바이트쓰기(0x3f8, VALUE);
    }

    static void 지우기() {
        for (int INDEX = 0; INDEX < 2000; INDEX++) {
            Mobil_VALUE.schreiwen_Späicher(0xb8000 + INDEX * 2, 32);
            Mobil_VALUE.schreiwen_Späicher(0xb8001 + INDEX * 2, 색);
        }
        Slot_Agab = 0;
        Curseur_VALUE();
    }

    static void Curseur_VALUE() {
        Mobil_VALUE.입출력바이트쓰기(0x3d4, 14);
        Mobil_VALUE.입출력바이트쓰기(0x3d5, Slot_Agab >> 8);
        Mobil_VALUE.입출력바이트쓰기(0x3d4, 15);
        Mobil_VALUE.입출력바이트쓰기(0x3d5, Slot_Agab & 255);
    }

    static void 화면문자(int VALUE) {
        if (VALUE == 13) return;
        if (VALUE == 10) {
            Slot_Agab = (Slot_Agab / 80 + 1) * 80;
        } else if (VALUE == 8) {
            if (Slot_Agab > 0) {
                Slot_Agab--;
                Mobil_VALUE.schreiwen_Späicher(0xb8000 + Slot_Agab * 2, 32);
            }
        } else {
            Mobil_VALUE.schreiwen_Späicher(0xb8000 + Slot_Agab * 2, VALUE < 128 ? VALUE : '?');
            Mobil_VALUE.schreiwen_Späicher(0xb8001 + Slot_Agab * 2, 색);
            Slot_Agab++;
        }
        if (Slot_Agab >= 2000) {
            for (int INDEX = 0; INDEX < 3840; INDEX++)
                Mobil_VALUE.schreiwen_Späicher(0xb8000 + INDEX, Mobil_VALUE.기억읽기(0xb80a0 + INDEX));
            for (int INDEX = 1920; INDEX < 2000; INDEX++) {
                Mobil_VALUE.schreiwen_Späicher(0xb8000 + INDEX * 2, 32);
                Mobil_VALUE.schreiwen_Späicher(0xb8001 + INDEX * 2, 색);
            }
            Slot_Agab = 1920;
        }
        Curseur_VALUE();
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

    static void schreiwen(String Inhalt_VALUE) {
        for (int INDEX = 0; INDEX < Inhalt_VALUE.length(); INDEX++) 문자(Inhalt_VALUE.charAt(INDEX));
    }

    static void 수쓰기(int VALUE) {
        // 양수로 바꾸지 않으므로 Integer.MIN_VALUE도 안전하다.
        if (VALUE < 0) 문자('-');
        else VALUE = -VALUE;
        int positionéieren_INDEX = 1000000000;
        boolean Laf = false;
        while (positionéieren_INDEX > 0) {
            int Ziffer_VALUE = -(VALUE / positionéieren_INDEX);
            if (Ziffer_VALUE != 0 || Laf || positionéieren_INDEX == 1) {
                문자('0' + Ziffer_VALUE);
                Laf = true;
            }
            VALUE %= positionéieren_INDEX;
            positionéieren_INDEX /= 10;
        }
    }

    static int 직렬읽기() {
        if ((Mobil_VALUE.입출력바이트읽기(0x3fd) & 1) != 0) return Mobil_VALUE.입출력바이트읽기(0x3f8);
        return -1;
    }
}
