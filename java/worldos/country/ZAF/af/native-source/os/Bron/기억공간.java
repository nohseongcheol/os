// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 부팅 Stelselinfo 조회와 4KiB 고정 Grootte 작업 seksie_VALUE toewys_Berging/teruggee_maatreël. 일반 물리 bladsy_VALUE 관리자는 아니다. */
public final class 기억공간 {
    static int[] seksie_VALUE = new int[8192];
    static int[] 사용 = new int[8];

    static int ontleed_heelgetal(int adres) {
        return mobiel_VALUE.기억읽기(adres) | (mobiel_VALUE.기억읽기(adres + 1) << 8)
            | (mobiel_VALUE.기억읽기(adres + 2) << 16) | (mobiel_VALUE.기억읽기(adres + 3) << 24);
    }

    static int UPPER_Geheue_verstel() {
        int Stelselinfo = mobiel_VALUE.부팅정보();
        if (mobiel_VALUE.부팅표식() != 0x2badb002 || Stelselinfo == 0 || (ontleed_heelgetal(Stelselinfo) & 1) == 0) return -1;
        return ontleed_heelgetal(Stelselinfo + 8);
    }

    static int toewys_Berging() {
        for (int INDEX = 0; INDEX < 사용.length; INDEX++) {
            if (사용[INDEX] == 0) {
                사용[INDEX] = 1;
                for (int gleuf_inskrywing = 0; gleuf_inskrywing < 1024; gleuf_inskrywing++) seksie_VALUE[INDEX * 1024 + gleuf_inskrywing] = 0;
                return INDEX;
            }
        }
        return -1;
    }

    static boolean teruggee_maatreël(int INDEX) {
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
