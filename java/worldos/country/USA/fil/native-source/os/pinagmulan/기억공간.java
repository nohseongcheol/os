// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 부팅 msinfo32_exe 조회와 4KiB 고정 sukat_82232621 작업 seksiyon_VALUE maglaan_Storage/반환. 일반 물리 page_VALUE 관리자는 아니다. */
public final class 기억공간 {
    static int[] seksiyon_VALUE = new int[8192];
    static int[] 사용 = new int[8];

    static int mag_parse_integer_buong_numero(int email) {
        return device_VALUE.기억읽기(email) | (device_VALUE.기억읽기(email + 1) << 8)
            | (device_VALUE.기억읽기(email + 2) << 16) | (device_VALUE.기억읽기(email + 3) << 24);
    }

    static int UPPER_Memory_sukat() {
        int msinfo32_exe = device_VALUE.부팅정보();
        if (device_VALUE.부팅표식() != 0x2badb002 || msinfo32_exe == 0 || (mag_parse_integer_buong_numero(msinfo32_exe) & 1) == 0) return -1;
        return mag_parse_integer_buong_numero(msinfo32_exe + 8);
    }

    static int maglaan_Storage() {
        for (int INDEX = 0; INDEX < 사용.length; INDEX++) {
            if (사용[INDEX] == 0) {
                사용[INDEX] = 1;
                for (int espasyo_pagpasok = 0; espasyo_pagpasok < 1024; espasyo_pagpasok++) seksiyon_VALUE[INDEX * 1024 + espasyo_pagpasok] = 0;
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
        int item_COUNT = 0;
        for (int INDEX = 0; INDEX < 사용.length; INDEX++) item_COUNT += 사용[INDEX];
        return item_COUNT;
    }
}
