// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 부팅 msinfo32_exe 조회와 4KiB 고정 Ingano 작업 igice_agaciro kugenera_Ububiko/반환. 일반 물리 paji_agaciro 관리자는 아니다. */
public final class 기억공간 {
    static int[] igice_agaciro = new int[8192];
    static int[] 사용 = new int[8];

    static int gusesengura_umubare_wuzuye(int aderesi) {
        return igendanwa_agaciro.기억읽기(aderesi) | (igendanwa_agaciro.기억읽기(aderesi + 1) << 8)
            | (igendanwa_agaciro.기억읽기(aderesi + 2) << 16) | (igendanwa_agaciro.기억읽기(aderesi + 3) << 24);
    }

    static int 위쪽기억크기() {
        int msinfo32_exe = igendanwa_agaciro.부팅정보();
        if (igendanwa_agaciro.부팅표식() != 0x2badb002 || msinfo32_exe == 0 || (gusesengura_umubare_wuzuye(msinfo32_exe) & 1) == 0) return -1;
        return gusesengura_umubare_wuzuye(msinfo32_exe + 8);
    }

    static int kugenera_Ububiko() {
        for (int umugerekashakiro = 0; umugerekashakiro < 사용.length; umugerekashakiro++) {
            if (사용[umugerekashakiro] == 0) {
                사용[umugerekashakiro] = 1;
                for (int umwanya_icyinjizwa = 0; umwanya_icyinjizwa < 1024; umwanya_icyinjizwa++) igice_agaciro[umugerekashakiro * 1024 + umwanya_icyinjizwa] = 0;
                return umugerekashakiro;
            }
        }
        return -1;
    }

    static boolean 반환(int umugerekashakiro) {
        if (umugerekashakiro < 0 || umugerekashakiro >= 사용.length || 사용[umugerekashakiro] == 0) return false;
        사용[umugerekashakiro] = 0;
        return true;
    }

    static int 사용개수() {
        int 개수 = 0;
        for (int umugerekashakiro = 0; umugerekashakiro < 사용.length; umugerekashakiro++) 개수 += 사용[umugerekashakiro];
        return 개수;
    }
}
