// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 부팅 msinfo32_exe 조회와 4KiB 고정 Izmērs 작업 sadaļa_VALUE piešķirt_Krātuve/atdot_mērs. 일반 물리 lapa_VALUE 관리자는 아니다. */
public final class atmiņa_reģions {
    static int[] sadaļa_VALUE = new int[8192];
    static int[] lietot_VALUE = new int[8];

    static int parsēt_vesels_skaitlis(int adrese) {
        return ierīce_VALUE.기억읽기(adrese) | (ierīce_VALUE.기억읽기(adrese + 1) << 8)
            | (ierīce_VALUE.기억읽기(adrese + 2) << 16) | (ierīce_VALUE.기억읽기(adrese + 3) << 24);
    }

    static int UPPER_atmiņa_mainīt_izmērus() {
        int msinfo32_exe = ierīce_VALUE.부팅정보();
        if (ierīce_VALUE.부팅표식() != 0x2badb002 || msinfo32_exe == 0 || (parsēt_vesels_skaitlis(msinfo32_exe) & 1) == 0) return -1;
        return parsēt_vesels_skaitlis(msinfo32_exe + 8);
    }

    static int piešķirt_Krātuve() {
        for (int INDEX = 0; INDEX < lietot_VALUE.length; INDEX++) {
            if (lietot_VALUE[INDEX] == 0) {
                lietot_VALUE[INDEX] = 1;
                for (int 칸 = 0; 칸 < 1024; 칸++) sadaļa_VALUE[INDEX * 1024 + 칸] = 0;
                return INDEX;
            }
        }
        return -1;
    }

    static boolean atdot_mērs(int INDEX) {
        if (INDEX < 0 || INDEX >= lietot_VALUE.length || lietot_VALUE[INDEX] == 0) return false;
        lietot_VALUE[INDEX] = 0;
        return true;
    }

    static int 사용개수() {
        int krājums_COUNT = 0;
        for (int INDEX = 0; INDEX < lietot_VALUE.length; INDEX++) krājums_COUNT += lietot_VALUE[INDEX];
        return krājums_COUNT;
    }
}
