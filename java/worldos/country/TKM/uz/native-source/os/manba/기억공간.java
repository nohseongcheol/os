// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 부팅 msinfo32_exe 조회와 4KiB 고정 Hajmi 작업 bo_lim_VALUE_366e0bfa joylashtirmoq_Xotira/qaytarish_o_lchov. 일반 물리 sahifa_VALUE 관리자는 아니다. */
public final class 기억공간 {
    static int[] bo_lim_VALUE_366e0bfa = new int[8192];
    static int[] 사용 = new int[8];

    static int tahlil_qilmoq_butun_son(int manzil) {
        return qurilma_VALUE.기억읽기(manzil) | (qurilma_VALUE.기억읽기(manzil + 1) << 8)
            | (qurilma_VALUE.기억읽기(manzil + 2) << 16) | (qurilma_VALUE.기억읽기(manzil + 3) << 24);
    }

    static int UPPER_Xotira_o_lcham() {
        int msinfo32_exe = qurilma_VALUE.부팅정보();
        if (qurilma_VALUE.부팅표식() != 0x2badb002 || msinfo32_exe == 0 || (tahlil_qilmoq_butun_son(msinfo32_exe) & 1) == 0) return -1;
        return tahlil_qilmoq_butun_son(msinfo32_exe + 8);
    }

    static int joylashtirmoq_Xotira() {
        for (int INDEX = 0; INDEX < 사용.length; INDEX++) {
            if (사용[INDEX] == 0) {
                사용[INDEX] = 1;
                for (int in_kiritish = 0; in_kiritish < 1024; in_kiritish++) bo_lim_VALUE_366e0bfa[INDEX * 1024 + in_kiritish] = 0;
                return INDEX;
            }
        }
        return -1;
    }

    static boolean qaytarish_o_lchov(int INDEX) {
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
