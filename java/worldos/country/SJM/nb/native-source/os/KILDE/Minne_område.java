// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 부팅 msinfo32_exe 조회와 4KiB 고정 Størrelse 작업 inndeling_VERDI tildele_lager/return_KR. 일반 물리 page_VERDI 관리자는 아니다. */
public final class Minne_område {
    static int[] inndeling_VERDI = new int[8192];
    static int[] bruk_VERDI = new int[8];

    static int dele_opp_heltall(int e_post) {
        return enhet_VERDI.기억읽기(e_post) | (enhet_VERDI.기억읽기(e_post + 1) << 8)
            | (enhet_VERDI.기억읽기(e_post + 2) << 16) | (enhet_VERDI.기억읽기(e_post + 3) << 24);
    }

    static int STORE_Minne_skalere() {
        int msinfo32_exe = enhet_VERDI.부팅정보();
        if (enhet_VERDI.부팅표식() != 0x2badb002 || msinfo32_exe == 0 || (dele_opp_heltall(msinfo32_exe) & 1) == 0) return -1;
        return dele_opp_heltall(msinfo32_exe + 8);
    }

    static int tildele_lager() {
        for (int INDEKS = 0; INDEKS < bruk_VERDI.length; INDEKS++) {
            if (bruk_VERDI[INDEKS] == 0) {
                bruk_VERDI[INDEKS] = 1;
                for (int åpning_oppføring = 0; åpning_oppføring < 1024; åpning_oppføring++) inndeling_VERDI[INDEKS * 1024 + åpning_oppføring] = 0;
                return INDEKS;
            }
        }
        return -1;
    }

    static boolean return_KR(int INDEKS) {
        if (INDEKS < 0 || INDEKS >= bruk_VERDI.length || bruk_VERDI[INDEKS] == 0) return false;
        bruk_VERDI[INDEKS] = 0;
        return true;
    }

    static int 사용개수() {
        int vare_ANTALL = 0;
        for (int INDEKS = 0; INDEKS < bruk_VERDI.length; INDEKS++) vare_ANTALL += bruk_VERDI[INDEKS];
        return vare_ANTALL;
    }
}
