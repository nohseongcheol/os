// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 부팅 msinfo32_exe 조회와 4KiB 고정 Størrelse 작업 sektion_VÆRDI tildel_Lager/returnere_KR. 일반 물리 side_VÆRDI 관리자는 아니다. */
public final class Hukommelse_område {
    static int[] sektion_VÆRDI = new int[8192];
    static int[] brug_VÆRDI = new int[8];

    static int opdele_tekst_heltal(int mail) {
        return enhed_VÆRDI.기억읽기(mail) | (enhed_VÆRDI.기억읽기(mail + 1) << 8)
            | (enhed_VÆRDI.기억읽기(mail + 2) << 16) | (enhed_VÆRDI.기억읽기(mail + 3) << 24);
    }

    static int STORE_BOGSTAVER_Hukommelse_tilpasse_størrelse() {
        int msinfo32_exe = enhed_VÆRDI.부팅정보();
        if (enhed_VÆRDI.부팅표식() != 0x2badb002 || msinfo32_exe == 0 || (opdele_tekst_heltal(msinfo32_exe) & 1) == 0) return -1;
        return opdele_tekst_heltal(msinfo32_exe + 8);
    }

    static int tildel_Lager() {
        for (int INDEKS = 0; INDEKS < brug_VÆRDI.length; INDEKS++) {
            if (brug_VÆRDI[INDEKS] == 0) {
                brug_VÆRDI[INDEKS] = 1;
                for (int udvidelsesstik_post = 0; udvidelsesstik_post < 1024; udvidelsesstik_post++) sektion_VÆRDI[INDEKS * 1024 + udvidelsesstik_post] = 0;
                return INDEKS;
            }
        }
        return -1;
    }

    static boolean returnere_KR(int INDEKS) {
        if (INDEKS < 0 || INDEKS >= brug_VÆRDI.length || brug_VÆRDI[INDEKS] == 0) return false;
        brug_VÆRDI[INDEKS] = 0;
        return true;
    }

    static int 사용개수() {
        int vare_TÆL = 0;
        for (int INDEKS = 0; INDEKS < brug_VÆRDI.length; INDEKS++) vare_TÆL += brug_VÆRDI[INDEKS];
        return vare_TÆL;
    }
}
