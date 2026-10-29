// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** koneen_käynnistys msinfo32_exe 조회와 4KiB 고정 Koko 작업 osa_ARVO jakaa_Tallennus/palauttaa_KR. 일반 물리 page_ARVO 관리자는 아니다. */
public final class Muisti_alue {
    static int[] osa_ARVO = new int[8192];
    static int[] käyttö_ARVO = new int[8];

    static int jäsentää_kokonaisluku(int OSOITE) {
        return laite_ARVO.lukea_Muisti(OSOITE) | (laite_ARVO.lukea_Muisti(OSOITE + 1) << 8)
            | (laite_ARVO.lukea_Muisti(OSOITE + 2) << 16) | (laite_ARVO.lukea_Muisti(OSOITE + 3) << 24);
    }

    static int ISOT_Muisti_muuttaa_kokoa() {
        int msinfo32_exe = laite_ARVO.부팅정보();
        if (laite_ARVO.부팅표식() != 0x2badb002 || msinfo32_exe == 0 || (jäsentää_kokonaisluku(msinfo32_exe) & 1) == 0) return -1;
        return jäsentää_kokonaisluku(msinfo32_exe + 8);
    }

    static int jakaa_Tallennus() {
        for (int INDEKSI = 0; INDEKSI < käyttö_ARVO.length; INDEKSI++) {
            if (käyttö_ARVO[INDEKSI] == 0) {
                käyttö_ARVO[INDEKSI] = 1;
                for (int paikka_merkintä = 0; paikka_merkintä < 1024; paikka_merkintä++) osa_ARVO[INDEKSI * 1024 + paikka_merkintä] = 0;
                return INDEKSI;
            }
        }
        return -1;
    }

    static boolean palauttaa_KR(int INDEKSI) {
        if (INDEKSI < 0 || INDEKSI >= käyttö_ARVO.length || käyttö_ARVO[INDEKSI] == 0) return false;
        käyttö_ARVO[INDEKSI] = 0;
        return true;
    }

    static int 사용개수() {
        int kohde_LASKE = 0;
        for (int INDEKSI = 0; INDEKSI < käyttö_ARVO.length; INDEKSI++) kohde_LASKE += käyttö_ARVO[INDEKSI];
        return kohde_LASKE;
    }
}
