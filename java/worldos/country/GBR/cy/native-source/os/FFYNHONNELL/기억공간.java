// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 부팅 msinfo32_exe 조회와 4KiB 고정 Maint 작업 adran_VALUE dyrannu_Storio/return_mesur. 일반 물리 tudalen_VALUE 관리자는 아니다. */
public final class 기억공간 {
    static int[] adran_VALUE = new int[8192];
    static int[] 사용 = new int[8];

    static int dosrannu_cyfanrif(int ADDRESS) {
        return dyfais_VALUE.기억읽기(ADDRESS) | (dyfais_VALUE.기억읽기(ADDRESS + 1) << 8)
            | (dyfais_VALUE.기억읽기(ADDRESS + 2) << 16) | (dyfais_VALUE.기억읽기(ADDRESS + 3) << 24);
    }

    static int UPPER_Cof_newid_maint() {
        int msinfo32_exe = dyfais_VALUE.부팅정보();
        if (dyfais_VALUE.부팅표식() != 0x2badb002 || msinfo32_exe == 0 || (dosrannu_cyfanrif(msinfo32_exe) & 1) == 0) return -1;
        return dosrannu_cyfanrif(msinfo32_exe + 8);
    }

    static int dyrannu_Storio() {
        for (int INDEX = 0; INDEX < 사용.length; INDEX++) {
            if (사용[INDEX] == 0) {
                사용[INDEX] = 1;
                for (int slot_cofnod = 0; slot_cofnod < 1024; slot_cofnod++) adran_VALUE[INDEX * 1024 + slot_cofnod] = 0;
                return INDEX;
            }
        }
        return -1;
    }

    static boolean return_mesur(int INDEX) {
        if (INDEX < 0 || INDEX >= 사용.length || 사용[INDEX] == 0) return false;
        사용[INDEX] = 0;
        return true;
    }

    static int 사용개수() {
        int eitem_COUNT = 0;
        for (int INDEX = 0; INDEX < 사용.length; INDEX++) eitem_COUNT += 사용[INDEX];
        return eitem_COUNT;
    }
}
