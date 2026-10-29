// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 부팅 msinfo32_exe 조회와 4KiB 고정 daqqas 작업 taqsima_VALUE_366e0bfa alloka_Ħażna/반환. 일반 물리 paġna_VALUE 관리자는 아니다. */
public final class 기억공간 {
    static int[] taqsima_VALUE_366e0bfa = new int[8192];
    static int[] 사용 = new int[8];

    static int analizza_numru_sħiħ(int ADDRESS) {
        return mowbajl_VALUE.기억읽기(ADDRESS) | (mowbajl_VALUE.기억읽기(ADDRESS + 1) << 8)
            | (mowbajl_VALUE.기억읽기(ADDRESS + 2) << 16) | (mowbajl_VALUE.기억읽기(ADDRESS + 3) << 24);
    }

    static int UPPER_Memorja_daqqas() {
        int msinfo32_exe = mowbajl_VALUE.부팅정보();
        if (mowbajl_VALUE.부팅표식() != 0x2badb002 || msinfo32_exe == 0 || (analizza_numru_sħiħ(msinfo32_exe) & 1) == 0) return -1;
        return analizza_numru_sħiħ(msinfo32_exe + 8);
    }

    static int alloka_Ħażna() {
        for (int INDEX = 0; INDEX < 사용.length; INDEX++) {
            if (사용[INDEX] == 0) {
                사용[INDEX] = 1;
                for (int slott_entrata = 0; slott_entrata < 1024; slott_entrata++) taqsima_VALUE_366e0bfa[INDEX * 1024 + slott_entrata] = 0;
                return INDEX;
            }
        }
        return -1;
    }

    static boolean 반환(int INDEX) {
        if (INDEX < 0 || INDEX >= 사용.length || 사용[INDEX] == 0) return false;
        사용[INDEX] = 0;
        return true;
    }

    static int 사용개수() {
        int element_COUNT = 0;
        for (int INDEX = 0; INDEX < 사용.length; INDEX++) element_COUNT += 사용[INDEX];
        return element_COUNT;
    }
}
