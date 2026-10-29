// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 부팅 msinfo32_exe 조회와 4KiB 고정 Mărime 작업 secțiune_VALUE aloca_Stocare/restitui_KR. 일반 물리 pagina_VALUE 관리자는 아니다. */
public final class Memorie_regiune {
    static int[] secțiune_VALUE = new int[8192];
    static int[] utiliza_VALUE = new int[8];

    static int analiza_întreg(int adresa) {
        return mobil_VALUE.기억읽기(adresa) | (mobil_VALUE.기억읽기(adresa + 1) << 8)
            | (mobil_VALUE.기억읽기(adresa + 2) << 16) | (mobil_VALUE.기억읽기(adresa + 3) << 24);
    }

    static int UPPER_Memorie_dimensiona() {
        int msinfo32_exe = mobil_VALUE.부팅정보();
        if (mobil_VALUE.부팅표식() != 0x2badb002 || msinfo32_exe == 0 || (analiza_întreg(msinfo32_exe) & 1) == 0) return -1;
        return analiza_întreg(msinfo32_exe + 8);
    }

    static int aloca_Stocare() {
        for (int INDEX = 0; INDEX < utiliza_VALUE.length; INDEX++) {
            if (utiliza_VALUE[INDEX] == 0) {
                utiliza_VALUE[INDEX] = 1;
                for (int 칸 = 0; 칸 < 1024; 칸++) secțiune_VALUE[INDEX * 1024 + 칸] = 0;
                return INDEX;
            }
        }
        return -1;
    }

    static boolean restitui_KR(int INDEX) {
        if (INDEX < 0 || INDEX >= utiliza_VALUE.length || utiliza_VALUE[INDEX] == 0) return false;
        utiliza_VALUE[INDEX] = 0;
        return true;
    }

    static int 사용개수() {
        int element_COUNT = 0;
        for (int INDEX = 0; INDEX < utiliza_VALUE.length; INDEX++) element_COUNT += utiliza_VALUE[INDEX];
        return element_COUNT;
    }
}
