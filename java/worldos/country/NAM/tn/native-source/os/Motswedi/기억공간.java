// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 부팅 msinfo32_exe 조회와 4KiB 고정 lekanya 작업 karolo_Boleng abela_Polokelo/반환. 일반 물리 tsebe_Boleng 관리자는 아니다. */
public final class 기억공간 {
    static int[] karolo_Boleng = new int[8192];
    static int[] 사용 = new int[8];

    static int go_lokolola_Palotlalo(int aterese) {
        return mobaele_Boleng.기억읽기(aterese) | (mobaele_Boleng.기억읽기(aterese + 1) << 8)
            | (mobaele_Boleng.기억읽기(aterese + 2) << 16) | (mobaele_Boleng.기억읽기(aterese + 3) << 24);
    }

    static int 위쪽기억크기() {
        int msinfo32_exe = mobaele_Boleng.부팅정보();
        if (mobaele_Boleng.부팅표식() != 0x2badb002 || msinfo32_exe == 0 || (go_lokolola_Palotlalo(msinfo32_exe) & 1) == 0) return -1;
        return go_lokolola_Palotlalo(msinfo32_exe + 8);
    }

    static int abela_Polokelo() {
        for (int tshupane = 0; tshupane < 사용.length; tshupane++) {
            if (사용[tshupane] == 0) {
                사용[tshupane] = 1;
                for (int sebaka_tsenyo = 0; sebaka_tsenyo < 1024; sebaka_tsenyo++) karolo_Boleng[tshupane * 1024 + sebaka_tsenyo] = 0;
                return tshupane;
            }
        }
        return -1;
    }

    static boolean 반환(int tshupane) {
        if (tshupane < 0 || tshupane >= 사용.length || 사용[tshupane] == 0) return false;
        사용[tshupane] = 0;
        return true;
    }

    static int 사용개수() {
        int 개수 = 0;
        for (int tshupane = 0; tshupane < 사용.length; tshupane++) 개수 += 사용[tshupane];
        return 개수;
    }
}
