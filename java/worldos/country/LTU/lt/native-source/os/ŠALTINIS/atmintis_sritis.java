// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 부팅 msinfo32_exe 조회와 4KiB 고정 Dydis 작업 sekcija_VALUE priskirti_Saugykla/grąžinti_KR. 일반 물리 puslapis_VALUE 관리자는 아니다. */
public final class atmintis_sritis {
    static int[] sekcija_VALUE = new int[8192];
    static int[] naudoti_VALUE = new int[8];

    static int analizuoti_sintaksę_sveikasis_skaičius(int ADDRESS) {
        return įrenginys_VALUE.기억읽기(ADDRESS) | (įrenginys_VALUE.기억읽기(ADDRESS + 1) << 8)
            | (įrenginys_VALUE.기억읽기(ADDRESS + 2) << 16) | (įrenginys_VALUE.기억읽기(ADDRESS + 3) << 24);
    }

    static int UPPER_atmintis_dydis() {
        int msinfo32_exe = įrenginys_VALUE.부팅정보();
        if (įrenginys_VALUE.부팅표식() != 0x2badb002 || msinfo32_exe == 0 || (analizuoti_sintaksę_sveikasis_skaičius(msinfo32_exe) & 1) == 0) return -1;
        return analizuoti_sintaksę_sveikasis_skaičius(msinfo32_exe + 8);
    }

    static int priskirti_Saugykla() {
        for (int INDEX = 0; INDEX < naudoti_VALUE.length; INDEX++) {
            if (naudoti_VALUE[INDEX] == 0) {
                naudoti_VALUE[INDEX] = 1;
                for (int 칸 = 0; 칸 < 1024; 칸++) sekcija_VALUE[INDEX * 1024 + 칸] = 0;
                return INDEX;
            }
        }
        return -1;
    }

    static boolean grąžinti_KR(int INDEX) {
        if (INDEX < 0 || INDEX >= naudoti_VALUE.length || naudoti_VALUE[INDEX] == 0) return false;
        naudoti_VALUE[INDEX] = 0;
        return true;
    }

    static int 사용개수() {
        int prekė_COUNT = 0;
        for (int INDEX = 0; INDEX < naudoti_VALUE.length; INDEX++) prekė_COUNT += naudoti_VALUE[INDEX];
        return prekė_COUNT;
    }
}
