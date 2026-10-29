// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 부팅 msinfo32_exe 조회와 4KiB 고정 promeniti_veličinu 작업 odeljak_VALUE dodeliti_Skladište/vratiti_KR. 일반 물리 stranica_VALUE 관리자는 아니다. */
public final class Memorija_oblast {
    static int[] odeljak_VALUE = new int[8192];
    static int[] koristiti_VALUE = new int[8];

    static int raščlaniti_ceo_broj(int adresa) {
        return uređaj_VALUE.기억읽기(adresa) | (uređaj_VALUE.기억읽기(adresa + 1) << 8)
            | (uređaj_VALUE.기억읽기(adresa + 2) << 16) | (uređaj_VALUE.기억읽기(adresa + 3) << 24);
    }

    static int UPPER_Memorija_promeniti_veličinu() {
        int msinfo32_exe = uređaj_VALUE.부팅정보();
        if (uređaj_VALUE.부팅표식() != 0x2badb002 || msinfo32_exe == 0 || (raščlaniti_ceo_broj(msinfo32_exe) & 1) == 0) return -1;
        return raščlaniti_ceo_broj(msinfo32_exe + 8);
    }

    static int dodeliti_Skladište() {
        for (int INDEX = 0; INDEX < koristiti_VALUE.length; INDEX++) {
            if (koristiti_VALUE[INDEX] == 0) {
                koristiti_VALUE[INDEX] = 1;
                for (int 칸 = 0; 칸 < 1024; 칸++) odeljak_VALUE[INDEX * 1024 + 칸] = 0;
                return INDEX;
            }
        }
        return -1;
    }

    static boolean vratiti_KR(int INDEX) {
        if (INDEX < 0 || INDEX >= koristiti_VALUE.length || koristiti_VALUE[INDEX] == 0) return false;
        koristiti_VALUE[INDEX] = 0;
        return true;
    }

    static int 사용개수() {
        int stavka_COUNT = 0;
        for (int INDEX = 0; INDEX < koristiti_VALUE.length; INDEX++) stavka_COUNT += koristiti_VALUE[INDEX];
        return stavka_COUNT;
    }
}
