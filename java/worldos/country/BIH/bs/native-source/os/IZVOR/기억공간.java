// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 부팅 msinfo32_exe 조회와 4KiB 고정 Veličina 작업 sekcija_VALUE dodijeliti_Pohrana/vratiti_mjera. 일반 물리 stranica_VALUE 관리자는 아니다. */
public final class 기억공간 {
    static int[] sekcija_VALUE = new int[8192];
    static int[] 사용 = new int[8];

    static int raščlanjivati_cijeli_broj(int adresa) {
        return uređaj_VALUE.기억읽기(adresa) | (uređaj_VALUE.기억읽기(adresa + 1) << 8)
            | (uređaj_VALUE.기억읽기(adresa + 2) << 16) | (uređaj_VALUE.기억읽기(adresa + 3) << 24);
    }

    static int UPPER_Memorija_podesiti_veličinu() {
        int msinfo32_exe = uređaj_VALUE.부팅정보();
        if (uređaj_VALUE.부팅표식() != 0x2badb002 || msinfo32_exe == 0 || (raščlanjivati_cijeli_broj(msinfo32_exe) & 1) == 0) return -1;
        return raščlanjivati_cijeli_broj(msinfo32_exe + 8);
    }

    static int dodijeliti_Pohrana() {
        for (int INDEX = 0; INDEX < 사용.length; INDEX++) {
            if (사용[INDEX] == 0) {
                사용[INDEX] = 1;
                for (int prostor_za_unos_unos = 0; prostor_za_unos_unos < 1024; prostor_za_unos_unos++) sekcija_VALUE[INDEX * 1024 + prostor_za_unos_unos] = 0;
                return INDEX;
            }
        }
        return -1;
    }

    static boolean vratiti_mjera(int INDEX) {
        if (INDEX < 0 || INDEX >= 사용.length || 사용[INDEX] == 0) return false;
        사용[INDEX] = 0;
        return true;
    }

    static int 사용개수() {
        int stavka_COUNT = 0;
        for (int INDEX = 0; INDEX < 사용.length; INDEX++) stavka_COUNT += 사용[INDEX];
        return stavka_COUNT;
    }
}
