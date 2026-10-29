// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 부팅 msinfo32_exe 조회와 4KiB 고정 Tamaina 작업 sekzio_balio esleitu_biltegi/itzuli_neurria. 일반 물리 orri_balio 관리자는 아니다. */
public final class 기억공간 {
    static int[] sekzio_balio = new int[8192];
    static int[] 사용 = new int[8];

    static int analizatu_osoko_zenbaki(int helbide) {
        return gailu_balio.기억읽기(helbide) | (gailu_balio.기억읽기(helbide + 1) << 8)
            | (gailu_balio.기억읽기(helbide + 2) << 16) | (gailu_balio.기억읽기(helbide + 3) << 24);
    }

    static int 위쪽기억크기() {
        int msinfo32_exe = gailu_balio.부팅정보();
        if (gailu_balio.부팅표식() != 0x2badb002 || msinfo32_exe == 0 || (analizatu_osoko_zenbaki(msinfo32_exe) & 1) == 0) return -1;
        return analizatu_osoko_zenbaki(msinfo32_exe + 8);
    }

    static int esleitu_biltegi() {
        for (int INDIZE = 0; INDIZE < 사용.length; INDIZE++) {
            if (사용[INDIZE] == 0) {
                사용[INDIZE] = 1;
                for (int 칸 = 0; 칸 < 1024; 칸++) sekzio_balio[INDIZE * 1024 + 칸] = 0;
                return INDIZE;
            }
        }
        return -1;
    }

    static boolean itzuli_neurria(int INDIZE) {
        if (INDIZE < 0 || INDIZE >= 사용.length || 사용[INDIZE] == 0) return false;
        사용[INDIZE] = 0;
        return true;
    }

    static int 사용개수() {
        int elementu_ZENBATU = 0;
        for (int INDIZE = 0; INDIZE < 사용.length; INDIZE++) elementu_ZENBATU += 사용[INDIZE];
        return elementu_ZENBATU;
    }
}
