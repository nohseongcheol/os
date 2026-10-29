// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 부팅 msinfo32_exe 조회와 4KiB 고정 atharraich_am_meud 작업 earrann_VALUE sònraich_stòras/return_tomhas. 일반 물리 duilleag_VALUE 관리자는 아니다. */
public final class 기억공간 {
    static int[] earrann_VALUE = new int[8192];
    static int[] 사용 = new int[8];

    static int 정수읽기(int ADDRESS) {
        return uidheam_VALUE.기억읽기(ADDRESS) | (uidheam_VALUE.기억읽기(ADDRESS + 1) << 8)
            | (uidheam_VALUE.기억읽기(ADDRESS + 2) << 16) | (uidheam_VALUE.기억읽기(ADDRESS + 3) << 24);
    }

    static int UPPER_cuimhne_atharraich_am_meud() {
        int msinfo32_exe = uidheam_VALUE.부팅정보();
        if (uidheam_VALUE.부팅표식() != 0x2badb002 || msinfo32_exe == 0 || (정수읽기(msinfo32_exe) & 1) == 0) return -1;
        return 정수읽기(msinfo32_exe + 8);
    }

    static int sònraich_stòras() {
        for (int INDEX = 0; INDEX < 사용.length; INDEX++) {
            if (사용[INDEX] == 0) {
                사용[INDEX] = 1;
                for (int slot_cur_a_steach = 0; slot_cur_a_steach < 1024; slot_cur_a_steach++) earrann_VALUE[INDEX * 1024 + slot_cur_a_steach] = 0;
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
        int nì_COUNT = 0;
        for (int INDEX = 0; INDEX < 사용.length; INDEX++) nì_COUNT += 사용[INDEX];
        return nì_COUNT;
    }
}
