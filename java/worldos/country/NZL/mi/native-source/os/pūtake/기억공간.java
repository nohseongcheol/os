// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 부팅 msinfo32_exe 조회와 4KiB 고정 rahi 작업 wāhanga_uara tiritiri_Rokiroki/반환. 일반 물리 whārangi_uara 관리자는 아니다. */
public final class 기억공간 {
    static int[] wāhanga_uara = new int[8192];
    static int[] 사용 = new int[8];

    static int poroporo_tau_tōpū(int ADDRESS) {
        return pūkoro_uara.기억읽기(ADDRESS) | (pūkoro_uara.기억읽기(ADDRESS + 1) << 8)
            | (pūkoro_uara.기억읽기(ADDRESS + 2) << 16) | (pūkoro_uara.기억읽기(ADDRESS + 3) << 24);
    }

    static int UPPER_Pūmahara_rahi() {
        int msinfo32_exe = pūkoro_uara.부팅정보();
        if (pūkoro_uara.부팅표식() != 0x2badb002 || msinfo32_exe == 0 || (poroporo_tau_tōpū(msinfo32_exe) & 1) == 0) return -1;
        return poroporo_tau_tōpū(msinfo32_exe + 8);
    }

    static int tiritiri_Rokiroki() {
        for (int INDEX = 0; INDEX < 사용.length; INDEX++) {
            if (사용[INDEX] == 0) {
                사용[INDEX] = 1;
                for (int kāniwha_tāurunga = 0; kāniwha_tāurunga < 1024; kāniwha_tāurunga++) wāhanga_uara[INDEX * 1024 + kāniwha_tāurunga] = 0;
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
        int tuemi_COUNT = 0;
        for (int INDEX = 0; INDEX < 사용.length; INDEX++) tuemi_COUNT += 사용[INDEX];
        return tuemi_COUNT;
    }
}
