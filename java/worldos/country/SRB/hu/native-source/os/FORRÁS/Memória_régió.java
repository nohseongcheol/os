// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 부팅 msinfo32_exe 조회와 4KiB 고정 Méret 작업 szakasz_ÉRTÉK kioszt_tár/visszaküld_KR. 일반 물리 lap_ÉRTÉK 관리자는 아니다. */
public final class Memória_régió {
    static int[] szakasz_ÉRTÉK = new int[8192];
    static int[] használ_ÉRTÉK = new int[8];

    static int elemez_egész_szám(int CÍM) {
        return mobil_ÉRTÉK.기억읽기(CÍM) | (mobil_ÉRTÉK.기억읽기(CÍM + 1) << 8)
            | (mobil_ÉRTÉK.기억읽기(CÍM + 2) << 16) | (mobil_ÉRTÉK.기억읽기(CÍM + 3) << 24);
    }

    static int NAGYBETŰS_Memória_méretez() {
        int msinfo32_exe = mobil_ÉRTÉK.부팅정보();
        if (mobil_ÉRTÉK.부팅표식() != 0x2badb002 || msinfo32_exe == 0 || (elemez_egész_szám(msinfo32_exe) & 1) == 0) return -1;
        return elemez_egész_szám(msinfo32_exe + 8);
    }

    static int kioszt_tár() {
        for (int INDEX = 0; INDEX < használ_ÉRTÉK.length; INDEX++) {
            if (használ_ÉRTÉK[INDEX] == 0) {
                használ_ÉRTÉK[INDEX] = 1;
                for (int tárolóhely_bejegyzés = 0; tárolóhely_bejegyzés < 1024; tárolóhely_bejegyzés++) szakasz_ÉRTÉK[INDEX * 1024 + tárolóhely_bejegyzés] = 0;
                return INDEX;
            }
        }
        return -1;
    }

    static boolean visszaküld_KR(int INDEX) {
        if (INDEX < 0 || INDEX >= használ_ÉRTÉK.length || használ_ÉRTÉK[INDEX] == 0) return false;
        használ_ÉRTÉK[INDEX] = 0;
        return true;
    }

    static int 사용개수() {
        int cikk_DARAB = 0;
        for (int INDEX = 0; INDEX < használ_ÉRTÉK.length; INDEX++) cikk_DARAB += használ_ÉRTÉK[INDEX];
        return cikk_DARAB;
    }
}
