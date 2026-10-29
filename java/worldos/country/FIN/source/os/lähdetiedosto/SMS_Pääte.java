// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** COM1 직렬 출력과 VGA 80x25 문자 화면. 한글은 직렬 단말에 UTF-8로 출력한다. */
public final class SMS_Pääte {
    static int paikka_merkintä = 0;
    static int 색 = 7;

    static void Valmistele() {
        laite_ARVO.입출력바이트쓰기(0x3f9, 0);
        laite_ARVO.입출력바이트쓰기(0x3fb, 0x80);
        laite_ARVO.입출력바이트쓰기(0x3f8, 1);
        laite_ARVO.입출력바이트쓰기(0x3f9, 0);
        laite_ARVO.입출력바이트쓰기(0x3fb, 3);
        laite_ARVO.입출력바이트쓰기(0x3fa, 0xc7);
        laite_ARVO.입출력바이트쓰기(0x3fc, 0x0b);
        poistaa_merkintä_c8dbc399();
    }

    static void 직렬바이트(int ARVO) {
        int toisto_LASKE = 100000;
        while ((laite_ARVO.입출력바이트읽기(0x3fd) & 0x20) == 0 && toisto_LASKE > 0) toisto_LASKE--;
        if (toisto_LASKE > 0) laite_ARVO.입출력바이트쓰기(0x3f8, ARVO);
    }

    static void poistaa_merkintä_c8dbc399() {
        for (int INDEKSI = 0; INDEKSI < 2000; INDEKSI++) {
            laite_ARVO.kirjoitus_Muisti(0xb8000 + INDEKSI * 2, 32);
            laite_ARVO.kirjoitus_Muisti(0xb8001 + INDEKSI * 2, 색);
        }
        paikka_merkintä = 0;
        kohdistin_ARVO();
    }

    static void kohdistin_ARVO() {
        laite_ARVO.입출력바이트쓰기(0x3d4, 14);
        laite_ARVO.입출력바이트쓰기(0x3d5, paikka_merkintä >> 8);
        laite_ARVO.입출력바이트쓰기(0x3d4, 15);
        laite_ARVO.입출력바이트쓰기(0x3d5, paikka_merkintä & 255);
    }

    static void 화면문자(int ARVO) {
        if (ARVO == 13) return;
        if (ARVO == 10) {
            paikka_merkintä = (paikka_merkintä / 80 + 1) * 80;
        } else if (ARVO == 8) {
            if (paikka_merkintä > 0) {
                paikka_merkintä--;
                laite_ARVO.kirjoitus_Muisti(0xb8000 + paikka_merkintä * 2, 32);
            }
        } else {
            laite_ARVO.kirjoitus_Muisti(0xb8000 + paikka_merkintä * 2, ARVO < 128 ? ARVO : '?');
            laite_ARVO.kirjoitus_Muisti(0xb8001 + paikka_merkintä * 2, 색);
            paikka_merkintä++;
        }
        if (paikka_merkintä >= 2000) {
            for (int INDEKSI = 0; INDEKSI < 3840; INDEKSI++)
                laite_ARVO.kirjoitus_Muisti(0xb8000 + INDEKSI, laite_ARVO.lukea_Muisti(0xb80a0 + INDEKSI));
            for (int INDEKSI = 1920; INDEKSI < 2000; INDEKSI++) {
                laite_ARVO.kirjoitus_Muisti(0xb8000 + INDEKSI * 2, 32);
                laite_ARVO.kirjoitus_Muisti(0xb8001 + INDEKSI * 2, 색);
            }
            paikka_merkintä = 1920;
        }
        kohdistin_ARVO();
    }

    static void 문자(int ARVO) {
        if (ARVO < 128) {
            if (ARVO == 10) 직렬바이트(13);
            직렬바이트(ARVO);
        } else if (ARVO < 2048) {
            직렬바이트(0xc0 | (ARVO >> 6));
            직렬바이트(0x80 | (ARVO & 63));
        } else {
            직렬바이트(0xe0 | (ARVO >> 12));
            직렬바이트(0x80 | ((ARVO >> 6) & 63));
            직렬바이트(0x80 | (ARVO & 63));
        }
        화면문자(ARVO);
    }

    static void Kirjoitus(String Sisältö_ARVO) {
        for (int INDEKSI = 0; INDEKSI < Sisältö_ARVO.length(); INDEKSI++) 문자(Sisältö_ARVO.charAt(INDEKSI));
    }

    static void kirjoitus_numero(int ARVO) {
        // 양수로 바꾸지 않으므로 Integer.MIN_VALUE도 안전하다.
        if (ARVO < 0) 문자('-');
        else ARVO = -ARVO;
        int sijainti = 1000000000;
        boolean Suorita_2 = false;
        while (sijainti > 0) {
            int numero_ARVO = -(ARVO / sijainti);
            if (numero_ARVO != 0 || Suorita_2 || sijainti == 1) {
                문자('0' + numero_ARVO);
                Suorita_2 = true;
            }
            ARVO %= sijainti;
            sijainti /= 10;
        }
    }

    static int 직렬읽기() {
        if ((laite_ARVO.입출력바이트읽기(0x3fd) & 1) != 0) return laite_ARVO.입출력바이트읽기(0x3f8);
        return -1;
    }
}
