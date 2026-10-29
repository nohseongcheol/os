// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** COM1 직렬 출력과 VGA 80x25 문자 화면. 한글은 직렬 단말에 UTF-8로 출력한다. */
public final class SMS_Terminál {
    static int přihrádka_položka = 0;
    static int 색 = 7;

    static void Připravit() {
        mobilní_HODNOTA.입출력바이트쓰기(0x3f9, 0);
        mobilní_HODNOTA.입출력바이트쓰기(0x3fb, 0x80);
        mobilní_HODNOTA.입출력바이트쓰기(0x3f8, 1);
        mobilní_HODNOTA.입출력바이트쓰기(0x3f9, 0);
        mobilní_HODNOTA.입출력바이트쓰기(0x3fb, 3);
        mobilní_HODNOTA.입출력바이트쓰기(0x3fa, 0xc7);
        mobilní_HODNOTA.입출력바이트쓰기(0x3fc, 0x0b);
        vymazat_položka();
    }

    static void 직렬바이트(int HODNOTA) {
        int opakování_POČET = 100000;
        while ((mobilní_HODNOTA.입출력바이트읽기(0x3fd) & 0x20) == 0 && opakování_POČET > 0) opakování_POČET--;
        if (opakování_POČET > 0) mobilní_HODNOTA.입출력바이트쓰기(0x3f8, HODNOTA);
    }

    static void vymazat_položka() {
        for (int INDEX = 0; INDEX < 2000; INDEX++) {
            mobilní_HODNOTA.zápis_Paměť(0xb8000 + INDEX * 2, 32);
            mobilní_HODNOTA.zápis_Paměť(0xb8001 + INDEX * 2, 색);
        }
        přihrádka_položka = 0;
        kurzor_HODNOTA();
    }

    static void kurzor_HODNOTA() {
        mobilní_HODNOTA.입출력바이트쓰기(0x3d4, 14);
        mobilní_HODNOTA.입출력바이트쓰기(0x3d5, přihrádka_položka >> 8);
        mobilní_HODNOTA.입출력바이트쓰기(0x3d4, 15);
        mobilní_HODNOTA.입출력바이트쓰기(0x3d5, přihrádka_položka & 255);
    }

    static void 화면문자(int HODNOTA) {
        if (HODNOTA == 13) return;
        if (HODNOTA == 10) {
            přihrádka_položka = (přihrádka_položka / 80 + 1) * 80;
        } else if (HODNOTA == 8) {
            if (přihrádka_položka > 0) {
                přihrádka_položka--;
                mobilní_HODNOTA.zápis_Paměť(0xb8000 + přihrádka_položka * 2, 32);
            }
        } else {
            mobilní_HODNOTA.zápis_Paměť(0xb8000 + přihrádka_položka * 2, HODNOTA < 128 ? HODNOTA : '?');
            mobilní_HODNOTA.zápis_Paměť(0xb8001 + přihrádka_položka * 2, 색);
            přihrádka_položka++;
        }
        if (přihrádka_položka >= 2000) {
            for (int INDEX = 0; INDEX < 3840; INDEX++)
                mobilní_HODNOTA.zápis_Paměť(0xb8000 + INDEX, mobilní_HODNOTA.기억읽기(0xb80a0 + INDEX));
            for (int INDEX = 1920; INDEX < 2000; INDEX++) {
                mobilní_HODNOTA.zápis_Paměť(0xb8000 + INDEX * 2, 32);
                mobilní_HODNOTA.zápis_Paměť(0xb8001 + INDEX * 2, 색);
            }
            přihrádka_položka = 1920;
        }
        kurzor_HODNOTA();
    }

    static void 문자(int HODNOTA) {
        if (HODNOTA < 128) {
            if (HODNOTA == 10) 직렬바이트(13);
            직렬바이트(HODNOTA);
        } else if (HODNOTA < 2048) {
            직렬바이트(0xc0 | (HODNOTA >> 6));
            직렬바이트(0x80 | (HODNOTA & 63));
        } else {
            직렬바이트(0xe0 | (HODNOTA >> 12));
            직렬바이트(0x80 | ((HODNOTA >> 6) & 63));
            직렬바이트(0x80 | (HODNOTA & 63));
        }
        화면문자(HODNOTA);
    }

    static void Zápis(String Obsah_HODNOTA) {
        for (int INDEX = 0; INDEX < Obsah_HODNOTA.length(); INDEX++) 문자(Obsah_HODNOTA.charAt(INDEX));
    }

    static void zápis_číslo(int HODNOTA) {
        // 양수로 바꾸지 않으므로 Integer.MIN_VALUE도 안전하다.
        if (HODNOTA < 0) 문자('-');
        else HODNOTA = -HODNOTA;
        int poziční_index = 1000000000;
        boolean Spustit_2 = false;
        while (poziční_index > 0) {
            int číslice_HODNOTA = -(HODNOTA / poziční_index);
            if (číslice_HODNOTA != 0 || Spustit_2 || poziční_index == 1) {
                문자('0' + číslice_HODNOTA);
                Spustit_2 = true;
            }
            HODNOTA %= poziční_index;
            poziční_index /= 10;
        }
    }

    static int 직렬읽기() {
        if ((mobilní_HODNOTA.입출력바이트읽기(0x3fd) & 1) != 0) return mobilní_HODNOTA.입출력바이트읽기(0x3f8);
        return -1;
    }
}
