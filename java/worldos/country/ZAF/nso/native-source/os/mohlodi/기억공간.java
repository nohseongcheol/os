// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 부팅 msinfo32_exe 조회와 4KiB 고정 Bogolo 작업 karolo_boleng aba_Bobolokelo/반환. 일반 물리 letlakala_boleng 관리자는 아니다. */
public final class 기억공간 {
    static int[] karolo_boleng = new int[8192];
    static int[] 사용 = new int[8];

    static int ripaganya_palotlalo(int atrese) {
        return sedirišwa_boleng.기억읽기(atrese) | (sedirišwa_boleng.기억읽기(atrese + 1) << 8)
            | (sedirišwa_boleng.기억읽기(atrese + 2) << 16) | (sedirišwa_boleng.기억읽기(atrese + 3) << 24);
    }

    static int 위쪽기억크기() {
        int msinfo32_exe = sedirišwa_boleng.부팅정보();
        if (sedirišwa_boleng.부팅표식() != 0x2badb002 || msinfo32_exe == 0 || (ripaganya_palotlalo(msinfo32_exe) & 1) == 0) return -1;
        return ripaganya_palotlalo(msinfo32_exe + 8);
    }

    static int aba_Bobolokelo() {
        for (int lokela = 0; lokela < 사용.length; lokela++) {
            if (사용[lokela] == 0) {
                사용[lokela] = 1;
                for (int sekgobana_go_tsenya_tshedimošo = 0; sekgobana_go_tsenya_tshedimošo < 1024; sekgobana_go_tsenya_tshedimošo++) karolo_boleng[lokela * 1024 + sekgobana_go_tsenya_tshedimošo] = 0;
                return lokela;
            }
        }
        return -1;
    }

    static boolean 반환(int lokela) {
        if (lokela < 0 || lokela >= 사용.length || 사용[lokela] == 0) return false;
        사용[lokela] = 0;
        return true;
    }

    static int 사용개수() {
        int 개수 = 0;
        for (int lokela = 0; lokela < 사용.length; lokela++) 개수 += 사용[lokela];
        return 개수;
    }
}
