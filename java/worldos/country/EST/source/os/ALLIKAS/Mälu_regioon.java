// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 부팅 msinfo32_exe 조회와 4KiB 고정 Suurus 작업 jaotis_VALUE lisama_salvesti/tagasi_saatma_näitaja. 일반 물리 leht_VALUE 관리자는 아니다. */
public final class Mälu_regioon {
    static int[] jaotis_VALUE = new int[8192];
    static int[] kasutus_VALUE = new int[8];

    static int sõeluma_täisarv(int ADDRESS) {
        return seade_VALUE.기억읽기(ADDRESS) | (seade_VALUE.기억읽기(ADDRESS + 1) << 8)
            | (seade_VALUE.기억읽기(ADDRESS + 2) << 16) | (seade_VALUE.기억읽기(ADDRESS + 3) << 24);
    }

    static int UPPER_Mälu_suurust_muutma() {
        int msinfo32_exe = seade_VALUE.부팅정보();
        if (seade_VALUE.부팅표식() != 0x2badb002 || msinfo32_exe == 0 || (sõeluma_täisarv(msinfo32_exe) & 1) == 0) return -1;
        return sõeluma_täisarv(msinfo32_exe + 8);
    }

    static int lisama_salvesti() {
        for (int INDEX = 0; INDEX < kasutus_VALUE.length; INDEX++) {
            if (kasutus_VALUE[INDEX] == 0) {
                kasutus_VALUE[INDEX] = 1;
                for (int 칸 = 0; 칸 < 1024; 칸++) jaotis_VALUE[INDEX * 1024 + 칸] = 0;
                return INDEX;
            }
        }
        return -1;
    }

    static boolean tagasi_saatma_näitaja(int INDEX) {
        if (INDEX < 0 || INDEX >= kasutus_VALUE.length || kasutus_VALUE[INDEX] == 0) return false;
        kasutus_VALUE[INDEX] = 0;
        return true;
    }

    static int 사용개수() {
        int kaup_COUNT = 0;
        for (int INDEX = 0; INDEX < kasutus_VALUE.length; INDEX++) kaup_COUNT += kasutus_VALUE[INDEX];
        return kaup_COUNT;
    }
}
