// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 부팅 msinfo32_exe 조회와 4KiB 고정 Ululyk 작업 bölüm_baha_366e0bfa bölüp_aýyr_Ammar/반환. 일반 물리 sahypa_baha 관리자는 아니다. */
public final class 기억공간 {
    static int[] bölüm_baha_366e0bfa = new int[8192];
    static int[] 사용 = new int[8];

    static int seljer_bitin(int salgy) {
        return enjam_baha.기억읽기(salgy) | (enjam_baha.기억읽기(salgy + 1) << 8)
            | (enjam_baha.기억읽기(salgy + 2) << 16) | (enjam_baha.기억읽기(salgy + 3) << 24);
    }

    static int 위쪽기억크기() {
        int msinfo32_exe = enjam_baha.부팅정보();
        if (enjam_baha.부팅표식() != 0x2badb002 || msinfo32_exe == 0 || (seljer_bitin(msinfo32_exe) & 1) == 0) return -1;
        return seljer_bitin(msinfo32_exe + 8);
    }

    static int bölüp_aýyr_Ammar() {
        for (int indeks = 0; indeks < 사용.length; indeks++) {
            if (사용[indeks] == 0) {
                사용[indeks] = 1;
                for (int ýer_girizmeklik = 0; ýer_girizmeklik < 1024; ýer_girizmeklik++) bölüm_baha_366e0bfa[indeks * 1024 + ýer_girizmeklik] = 0;
                return indeks;
            }
        }
        return -1;
    }

    static boolean 반환(int indeks) {
        if (indeks < 0 || indeks >= 사용.length || 사용[indeks] == 0) return false;
        사용[indeks] = 0;
        return true;
    }

    static int 사용개수() {
        int 개수 = 0;
        for (int indeks = 0; indeks < 사용.length; indeks++) 개수 += 사용[indeks];
        return 개수;
    }
}
