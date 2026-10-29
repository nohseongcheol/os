// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 부팅 msinfo32_exe 조회와 4KiB 고정 Méid 작업 rannán_VALUE leithdháil_Stóras/return_tomhas. 일반 물리 leathanach_VALUE 관리자는 아니다. */
public final class 기억공간 {
    static int[] rannán_VALUE = new int[8192];
    static int[] 사용 = new int[8];

    static int parsáil_slánuimhir(int ADDRESS) {
        return gléas_VALUE.기억읽기(ADDRESS) | (gléas_VALUE.기억읽기(ADDRESS + 1) << 8)
            | (gléas_VALUE.기억읽기(ADDRESS + 2) << 16) | (gléas_VALUE.기억읽기(ADDRESS + 3) << 24);
    }

    static int UPPER_Cuimhne_socraigh_méid() {
        int msinfo32_exe = gléas_VALUE.부팅정보();
        if (gléas_VALUE.부팅표식() != 0x2badb002 || msinfo32_exe == 0 || (parsáil_slánuimhir(msinfo32_exe) & 1) == 0) return -1;
        return parsáil_slánuimhir(msinfo32_exe + 8);
    }

    static int leithdháil_Stóras() {
        for (int INDEX = 0; INDEX < 사용.length; INDEX++) {
            if (사용[INDEX] == 0) {
                사용[INDEX] = 1;
                for (int spás_iontráil = 0; spás_iontráil < 1024; spás_iontráil++) rannán_VALUE[INDEX * 1024 + spás_iontráil] = 0;
                return INDEX;
            }
        }
        return -1;
    }

    static boolean return_tomhas(int INDEX) {
        if (INDEX < 0 || INDEX >= 사용.length || 사용[INDEX] == 0) return false;
        사용[INDEX] = 0;
        return true;
    }

    static int 사용개수() {
        int mír_COUNT = 0;
        for (int INDEX = 0; INDEX < 사용.length; INDEX++) mír_COUNT += 사용[INDEX];
        return mír_COUNT;
    }
}
