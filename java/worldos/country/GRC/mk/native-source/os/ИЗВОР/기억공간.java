// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 부팅 msinfo32_exe 조회와 4KiB 고정 Големина 작업 секција_VALUE додели_Склад/반환. 일반 물리 страница_VALUE 관리자는 아니다. */
public final class 기억공간 {
    static int[] секција_VALUE = new int[8192];
    static int[] 사용 = new int[8];

    static int разложи_цел_број(int адреса) {
        return уред_VALUE.기억읽기(адреса) | (уред_VALUE.기억읽기(адреса + 1) << 8)
            | (уред_VALUE.기억읽기(адреса + 2) << 16) | (уред_VALUE.기억읽기(адреса + 3) << 24);
    }

    static int UPPER_Меморија_големина() {
        int msinfo32_exe = уред_VALUE.부팅정보();
        if (уред_VALUE.부팅표식() != 0x2badb002 || msinfo32_exe == 0 || (разложи_цел_број(msinfo32_exe) & 1) == 0) return -1;
        return разложи_цел_број(msinfo32_exe + 8);
    }

    static int додели_Склад() {
        for (int INDEX = 0; INDEX < 사용.length; INDEX++) {
            if (사용[INDEX] == 0) {
                사용[INDEX] = 1;
                for (int отвор_внес = 0; отвор_внес < 1024; отвор_внес++) секција_VALUE[INDEX * 1024 + отвор_внес] = 0;
                return INDEX;
            }
        }
        return -1;
    }

    static boolean 반환(int INDEX) {
        if (INDEX < 0 || INDEX >= 사용.length || 사용[INDEX] == 0) return false;
        사용[INDEX] = 0;
        return true;
    }

    static int 사용개수() {
        int ставка_COUNT = 0;
        for (int INDEX = 0; INDEX < 사용.length; INDEX++) ставка_COUNT += 사용[INDEX];
        return ставка_COUNT;
    }
}
