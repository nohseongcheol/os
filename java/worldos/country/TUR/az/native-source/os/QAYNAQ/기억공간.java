// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 부팅 msinfo32_exe 조회와 4KiB 고정 Böyüklük 작업 bölmə_VALUE_366e0bfa ayırmaq_Yaddaş/geri_qaytarmaq_ölçü. 일반 물리 səhifə_VALUE 관리자는 아니다. */
public final class 기억공간 {
    static int[] bölmə_VALUE_366e0bfa = new int[8192];
    static int[] 사용 = new int[8];

    static int parselləmək_tam_ədəd(int ünvan) {
        return cihaz_VALUE.기억읽기(ünvan) | (cihaz_VALUE.기억읽기(ünvan + 1) << 8)
            | (cihaz_VALUE.기억읽기(ünvan + 2) << 16) | (cihaz_VALUE.기억읽기(ünvan + 3) << 24);
    }

    static int UPPER_Yaddaş_ölçünü_dəyişmək() {
        int msinfo32_exe = cihaz_VALUE.부팅정보();
        if (cihaz_VALUE.부팅표식() != 0x2badb002 || msinfo32_exe == 0 || (parselləmək_tam_ədəd(msinfo32_exe) & 1) == 0) return -1;
        return parselləmək_tam_ədəd(msinfo32_exe + 8);
    }

    static int ayırmaq_Yaddaş() {
        for (int INDEX = 0; INDEX < 사용.length; INDEX++) {
            if (사용[INDEX] == 0) {
                사용[INDEX] = 1;
                for (int slot_daxiletmə = 0; slot_daxiletmə < 1024; slot_daxiletmə++) bölmə_VALUE_366e0bfa[INDEX * 1024 + slot_daxiletmə] = 0;
                return INDEX;
            }
        }
        return -1;
    }

    static boolean geri_qaytarmaq_ölçü(int INDEX) {
        if (INDEX < 0 || INDEX >= 사용.length || 사용[INDEX] == 0) return false;
        사용[INDEX] = 0;
        return true;
    }

    static int 사용개수() {
        int element_COUNT = 0;
        for (int INDEX = 0; INDEX < 사용.length; INDEX++) element_COUNT += 사용[INDEX];
        return element_COUNT;
    }
}
