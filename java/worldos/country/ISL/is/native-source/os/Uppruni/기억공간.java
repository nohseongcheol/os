// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 부팅 msinfo32_exe 조회와 4KiB 고정 Stærð 작업 hluti_VALUE úthluta_geymsla/skila_mæld_stærð. 일반 물리 síða_VALUE 관리자는 아니다. */
public final class 기억공간 {
    static int[] hluti_VALUE = new int[8192];
    static int[] 사용 = new int[8];

    static int þátta_heiltala(int slóð) {
        return tæki_VALUE.기억읽기(slóð) | (tæki_VALUE.기억읽기(slóð + 1) << 8)
            | (tæki_VALUE.기억읽기(slóð + 2) << 16) | (tæki_VALUE.기억읽기(slóð + 3) << 24);
    }

    static int UPPER_Minni_breyta_stærð() {
        int msinfo32_exe = tæki_VALUE.부팅정보();
        if (tæki_VALUE.부팅표식() != 0x2badb002 || msinfo32_exe == 0 || (þátta_heiltala(msinfo32_exe) & 1) == 0) return -1;
        return þátta_heiltala(msinfo32_exe + 8);
    }

    static int úthluta_geymsla() {
        for (int INDEX = 0; INDEX < 사용.length; INDEX++) {
            if (사용[INDEX] == 0) {
                사용[INDEX] = 1;
                for (int rauf_færsla = 0; rauf_færsla < 1024; rauf_færsla++) hluti_VALUE[INDEX * 1024 + rauf_færsla] = 0;
                return INDEX;
            }
        }
        return -1;
    }

    static boolean skila_mæld_stærð(int INDEX) {
        if (INDEX < 0 || INDEX >= 사용.length || 사용[INDEX] == 0) return false;
        사용[INDEX] = 0;
        return true;
    }

    static int 사용개수() {
        int vara_COUNT = 0;
        for (int INDEX = 0; INDEX < 사용.length; INDEX++) vara_COUNT += 사용[INDEX];
        return vara_COUNT;
    }
}
