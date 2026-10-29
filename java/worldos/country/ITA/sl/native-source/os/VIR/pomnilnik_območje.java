// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 부팅 msinfo32_exe 조회와 4KiB 고정 Velikost 작업 odsek_VALUE dodeliti_Senzor_prostora/vrni_KR. 일반 물리 stran_VALUE 관리자는 아니다. */
public final class pomnilnik_območje {
    static int[] odsek_VALUE = new int[8192];
    static int[] uporaba_VALUE = new int[8];

    static int razčlenjevati_celo_število(int naslov) {
        return naprava_VALUE.기억읽기(naslov) | (naprava_VALUE.기억읽기(naslov + 1) << 8)
            | (naprava_VALUE.기억읽기(naslov + 2) << 16) | (naprava_VALUE.기억읽기(naslov + 3) << 24);
    }

    static int UPPER_pomnilnik_spremeniti_velikost() {
        int msinfo32_exe = naprava_VALUE.부팅정보();
        if (naprava_VALUE.부팅표식() != 0x2badb002 || msinfo32_exe == 0 || (razčlenjevati_celo_število(msinfo32_exe) & 1) == 0) return -1;
        return razčlenjevati_celo_število(msinfo32_exe + 8);
    }

    static int dodeliti_Senzor_prostora() {
        for (int INDEX = 0; INDEX < uporaba_VALUE.length; INDEX++) {
            if (uporaba_VALUE[INDEX] == 0) {
                uporaba_VALUE[INDEX] = 1;
                for (int 칸 = 0; 칸 < 1024; 칸++) odsek_VALUE[INDEX * 1024 + 칸] = 0;
                return INDEX;
            }
        }
        return -1;
    }

    static boolean vrni_KR(int INDEX) {
        if (INDEX < 0 || INDEX >= uporaba_VALUE.length || uporaba_VALUE[INDEX] == 0) return false;
        uporaba_VALUE[INDEX] = 0;
        return true;
    }

    static int 사용개수() {
        int element_COUNT = 0;
        for (int INDEX = 0; INDEX < uporaba_VALUE.length; INDEX++) element_COUNT += uporaba_VALUE[INDEX];
        return element_COUNT;
    }
}
