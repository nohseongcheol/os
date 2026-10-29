// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 부팅 msinfo32_exe 조회와 4KiB 고정 Madhësi 작업 seksion_VALUE caktoj_hapësira_ruajtëse/Kthe_llogaritje. 일반 물리 faqe_VALUE 관리자는 아니다. */
public final class 기억공간 {
    static int[] seksion_VALUE = new int[8192];
    static int[] 사용 = new int[8];

    static int analizoj_numër_i_plotë(int email) {
        return pajisje_VALUE.기억읽기(email) | (pajisje_VALUE.기억읽기(email + 1) << 8)
            | (pajisje_VALUE.기억읽기(email + 2) << 16) | (pajisje_VALUE.기억읽기(email + 3) << 24);
    }

    static int UPPER_Memorie_ndryshoj_përmasat() {
        int msinfo32_exe = pajisje_VALUE.부팅정보();
        if (pajisje_VALUE.부팅표식() != 0x2badb002 || msinfo32_exe == 0 || (analizoj_numër_i_plotë(msinfo32_exe) & 1) == 0) return -1;
        return analizoj_numër_i_plotë(msinfo32_exe + 8);
    }

    static int caktoj_hapësira_ruajtëse() {
        for (int INDEX = 0; INDEX < 사용.length; INDEX++) {
            if (사용[INDEX] == 0) {
                사용[INDEX] = 1;
                for (int hapësirë_për_tekst_futje = 0; hapësirë_për_tekst_futje < 1024; hapësirë_për_tekst_futje++) seksion_VALUE[INDEX * 1024 + hapësirë_për_tekst_futje] = 0;
                return INDEX;
            }
        }
        return -1;
    }

    static boolean Kthe_llogaritje(int INDEX) {
        if (INDEX < 0 || INDEX >= 사용.length || 사용[INDEX] == 0) return false;
        사용[INDEX] = 0;
        return true;
    }

    static int 사용개수() {
        int njësi_COUNT = 0;
        for (int INDEX = 0; INDEX < 사용.length; INDEX++) njësi_COUNT += 사용[INDEX];
        return njësi_COUNT;
    }
}
