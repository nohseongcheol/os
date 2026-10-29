// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 부팅 i_msinfo32_exe 조회와 4KiB 고정 Ubukhulu 작업 icandelo_ixabiso yabela_Ugcino/반환. 일반 물리 ikhasi_ixabiso 관리자는 아니다. */
public final class 기억공간 {
    static int[] icandelo_ixabiso = new int[8192];
    static int[] 사용 = new int[8];

    static int ingcaciso_yegama_inani_elipheleleyo(int idilesi) {
        return isixhobo_ixabiso.기억읽기(idilesi) | (isixhobo_ixabiso.기억읽기(idilesi + 1) << 8)
            | (isixhobo_ixabiso.기억읽기(idilesi + 2) << 16) | (isixhobo_ixabiso.기억읽기(idilesi + 3) << 24);
    }

    static int 위쪽기억크기() {
        int i_msinfo32_exe = isixhobo_ixabiso.부팅정보();
        if (isixhobo_ixabiso.부팅표식() != 0x2badb002 || i_msinfo32_exe == 0 || (ingcaciso_yegama_inani_elipheleleyo(i_msinfo32_exe) & 1) == 0) return -1;
        return ingcaciso_yegama_inani_elipheleleyo(i_msinfo32_exe + 8);
    }

    static int yabela_Ugcino() {
        for (int indeksa = 0; indeksa < 사용.length; indeksa++) {
            if (사용[indeksa] == 0) {
                사용[indeksa] = 1;
                for (int isithuba_ufako_nkcukacha = 0; isithuba_ufako_nkcukacha < 1024; isithuba_ufako_nkcukacha++) icandelo_ixabiso[indeksa * 1024 + isithuba_ufako_nkcukacha] = 0;
                return indeksa;
            }
        }
        return -1;
    }

    static boolean 반환(int indeksa) {
        if (indeksa < 0 || indeksa >= 사용.length || 사용[indeksa] == 0) return false;
        사용[indeksa] = 0;
        return true;
    }

    static int 사용개수() {
        int 개수 = 0;
        for (int indeksa = 0; indeksa < 사용.length; indeksa++) 개수 += 사용[indeksa];
        return 개수;
    }
}
