// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** COM1 직렬 출력과 VGA 80x25 문자 화면. 한글은 직렬 단말에 UTF-8로 출력한다. */
public final class SMS_Terminal {
    static int slot_entri = 0;
    static int 색 = 7;

    static void Siapkan() {
        Ponsel_VALUE.입출력바이트쓰기(0x3f9, 0);
        Ponsel_VALUE.입출력바이트쓰기(0x3fb, 0x80);
        Ponsel_VALUE.입출력바이트쓰기(0x3f8, 1);
        Ponsel_VALUE.입출력바이트쓰기(0x3f9, 0);
        Ponsel_VALUE.입출력바이트쓰기(0x3fb, 3);
        Ponsel_VALUE.입출력바이트쓰기(0x3fa, 0xc7);
        Ponsel_VALUE.입출력바이트쓰기(0x3fc, 0x0b);
        hapus_entri_c8dbc399();
    }

    static void 직렬바이트(int VALUE) {
        int pengulangan_COUNT = 100000;
        while ((Ponsel_VALUE.입출력바이트읽기(0x3fd) & 0x20) == 0 && pengulangan_COUNT > 0) pengulangan_COUNT--;
        if (pengulangan_COUNT > 0) Ponsel_VALUE.입출력바이트쓰기(0x3f8, VALUE);
    }

    static void hapus_entri_c8dbc399() {
        for (int INDEX = 0; INDEX < 2000; INDEX++) {
            Ponsel_VALUE.tulis_Memori(0xb8000 + INDEX * 2, 32);
            Ponsel_VALUE.tulis_Memori(0xb8001 + INDEX * 2, 색);
        }
        slot_entri = 0;
        kursor_VALUE();
    }

    static void kursor_VALUE() {
        Ponsel_VALUE.입출력바이트쓰기(0x3d4, 14);
        Ponsel_VALUE.입출력바이트쓰기(0x3d5, slot_entri >> 8);
        Ponsel_VALUE.입출력바이트쓰기(0x3d4, 15);
        Ponsel_VALUE.입출력바이트쓰기(0x3d5, slot_entri & 255);
    }

    static void 화면문자(int VALUE) {
        if (VALUE == 13) return;
        if (VALUE == 10) {
            slot_entri = (slot_entri / 80 + 1) * 80;
        } else if (VALUE == 8) {
            if (slot_entri > 0) {
                slot_entri--;
                Ponsel_VALUE.tulis_Memori(0xb8000 + slot_entri * 2, 32);
            }
        } else {
            Ponsel_VALUE.tulis_Memori(0xb8000 + slot_entri * 2, VALUE < 128 ? VALUE : '?');
            Ponsel_VALUE.tulis_Memori(0xb8001 + slot_entri * 2, 색);
            slot_entri++;
        }
        if (slot_entri >= 2000) {
            for (int INDEX = 0; INDEX < 3840; INDEX++)
                Ponsel_VALUE.tulis_Memori(0xb8000 + INDEX, Ponsel_VALUE.기억읽기(0xb80a0 + INDEX));
            for (int INDEX = 1920; INDEX < 2000; INDEX++) {
                Ponsel_VALUE.tulis_Memori(0xb8000 + INDEX * 2, 32);
                Ponsel_VALUE.tulis_Memori(0xb8001 + INDEX * 2, 색);
            }
            slot_entri = 1920;
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

    static void Tulis(String Isi_VALUE) {
        for (int INDEX = 0; INDEX < Isi_VALUE.length(); INDEX++) 문자(Isi_VALUE.charAt(INDEX));
    }

    static void 수쓰기(int VALUE) {
        // 양수로 바꾸지 않으므로 Integer.MIN_VALUE도 안전하다.
        if (VALUE < 0) 문자('-');
        else VALUE = -VALUE;
        int posisi_INDEX = 1000000000;
        boolean jalankan = false;
        while (posisi_INDEX > 0) {
            int angka_VALUE = -(VALUE / posisi_INDEX);
            if (angka_VALUE != 0 || jalankan || posisi_INDEX == 1) {
                문자('0' + angka_VALUE);
                jalankan = true;
            }
            VALUE %= posisi_INDEX;
            posisi_INDEX /= 10;
        }
    }

    static int 직렬읽기() {
        if ((Ponsel_VALUE.입출력바이트읽기(0x3fd) & 1) != 0) return Ponsel_VALUE.입출력바이트읽기(0x3f8);
        return -1;
    }
}
