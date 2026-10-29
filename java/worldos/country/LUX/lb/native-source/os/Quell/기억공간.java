// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 부팅 msinfo32_exe 조회와 4KiB 고정 d_Gréisst_veränneren 작업 Beräich_VALUE zouweisen_Späicher/반환. 일반 물리 Säit_VALUE 관리자는 아니다. */
public final class 기억공간 {
    static int[] Beräich_VALUE = new int[8192];
    static int[] 사용 = new int[8];

    static int analyséieren_Ganzzuel(int Adress) {
        return Mobil_VALUE.기억읽기(Adress) | (Mobil_VALUE.기억읽기(Adress + 1) << 8)
            | (Mobil_VALUE.기억읽기(Adress + 2) << 16) | (Mobil_VALUE.기억읽기(Adress + 3) << 24);
    }

    static int UPPER_Späicher_d_Gréisst_veränneren() {
        int msinfo32_exe = Mobil_VALUE.부팅정보();
        if (Mobil_VALUE.부팅표식() != 0x2badb002 || msinfo32_exe == 0 || (analyséieren_Ganzzuel(msinfo32_exe) & 1) == 0) return -1;
        return analyséieren_Ganzzuel(msinfo32_exe + 8);
    }

    static int zouweisen_Späicher() {
        for (int INDEX = 0; INDEX < 사용.length; INDEX++) {
            if (사용[INDEX] == 0) {
                사용[INDEX] = 1;
                for (int Slot_Agab = 0; Slot_Agab < 1024; Slot_Agab++) Beräich_VALUE[INDEX * 1024 + Slot_Agab] = 0;
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
        int Element_COUNT = 0;
        for (int INDEX = 0; INDEX < 사용.length; INDEX++) Element_COUNT += 사용[INDEX];
        return Element_COUNT;
    }
}
