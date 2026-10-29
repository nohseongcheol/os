// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 부팅 Podaci_o_sustavu 조회와 4KiB 고정 Veličina 작업 sekcija_VALUE dodijeli_Pohrana/vratiti_KR. 일반 물리 dojaviti_VALUE 관리자는 아니다. */
public final class Memorija_regije {
    static int[] sekcija_VALUE = new int[8192];
    static int[] uporaba_VALUE = new int[8];

    static int rastavljati_cijeli_broj(int adresa) {
        return uređaj_VALUE.기억읽기(adresa) | (uređaj_VALUE.기억읽기(adresa + 1) << 8)
            | (uređaj_VALUE.기억읽기(adresa + 2) << 16) | (uređaj_VALUE.기억읽기(adresa + 3) << 24);
    }

    static int UPPER_Memorija_promijeniti_veličinu() {
        int Podaci_o_sustavu = uređaj_VALUE.부팅정보();
        if (uređaj_VALUE.부팅표식() != 0x2badb002 || Podaci_o_sustavu == 0 || (rastavljati_cijeli_broj(Podaci_o_sustavu) & 1) == 0) return -1;
        return rastavljati_cijeli_broj(Podaci_o_sustavu + 8);
    }

    static int dodijeli_Pohrana() {
        for (int INDEX = 0; INDEX < uporaba_VALUE.length; INDEX++) {
            if (uporaba_VALUE[INDEX] == 0) {
                uporaba_VALUE[INDEX] = 1;
                for (int 칸 = 0; 칸 < 1024; 칸++) sekcija_VALUE[INDEX * 1024 + 칸] = 0;
                return INDEX;
            }
        }
        return -1;
    }

    static boolean vratiti_KR(int INDEX) {
        if (INDEX < 0 || INDEX >= uporaba_VALUE.length || uporaba_VALUE[INDEX] == 0) return false;
        uporaba_VALUE[INDEX] = 0;
        return true;
    }

    static int 사용개수() {
        int artikl_COUNT = 0;
        for (int INDEX = 0; INDEX < uporaba_VALUE.length; INDEX++) artikl_COUNT += uporaba_VALUE[INDEX];
        return artikl_COUNT;
    }
}
