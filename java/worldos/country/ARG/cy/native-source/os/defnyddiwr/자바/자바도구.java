// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트 Offer 공통 Allbwn 및 ASCII Ffeil Enw Proses_VALUE_cofnod. */
public final class 자바도구 {
    /** UTF-8 beit_VALUE 배열을 같은 배열의 UTF-16 단위로 바꾼다. 잘못된 입력은 gwrthod_VALUE. */
    static int 원문해독(int[] data, int hyd_VALUE) {
        int Darllen = 0, Ysgrifennu = 0;
        if (hyd_VALUE >= 3 && data[0] == 239 && data[1] == 187 && data[2] == 191) Darllen = 3;
        while (Darllen < hyd_VALUE) {
            int VALUE = data[Darllen++], 수 = 0, 최소 = 0;
            if (VALUE >= 194 && VALUE <= 223) { 수 = 1; 최소 = 128; VALUE &= 31; }
            else if (VALUE >= 224 && VALUE <= 239) { 수 = 2; 최소 = 2048; VALUE &= 15; }
            else if (VALUE >= 240 && VALUE <= 244) { 수 = 3; 최소 = 65536; VALUE &= 7; }
            else if (VALUE >= 128 || VALUE < 0) return -1;
            if (수 > hyd_VALUE - Darllen) return -1;
            for (int i = 0; i < 수; i++) {
                int Nesaf_eitem = data[Darllen++]; if ((Nesaf_eitem & 192) != 128) return -1;
                VALUE = (VALUE << 6) | (Nesaf_eitem & 63);
            }
            if (VALUE < 최소 || VALUE > 0x10ffff || (VALUE >= 0xd800 && VALUE <= 0xdfff)) return -1;
            if (VALUE >= 65536) { VALUE -= 65536; data[Ysgrifennu++] = 0xd800 | (VALUE >> 10); data[Ysgrifennu++] = 0xdc00 | (VALUE & 1023); }
            else data[Ysgrifennu++] = VALUE;
        }
        return Ysgrifennu;
    }
    static void 수쓰기(int VALUE) {
        if (VALUE < 0) defnyddiwr.ysgrifennu_nod_VALUE('-'); else VALUE = -VALUE;
        int safle_INDEX = 1000000000;
        boolean Gweithredu_2 = false;
        while (safle_INDEX != 0) {
            int 수 = -(VALUE / safle_INDEX);
            if (수 != 0 || Gweithredu_2 || safle_INDEX == 1) { defnyddiwr.ysgrifennu_nod_VALUE('0' + 수); Gweithredu_2 = true; }
            VALUE %= safle_INDEX; safle_INDEX /= 10;
        }
    }
    static int Enw(int[] cyrchfan_VALUE, String 원본) {
        if (원본.length() >= cyrchfan_VALUE.length) return -1;
        for (int 수 = 0; 수 < cyrchfan_VALUE.length; 수++) cyrchfan_VALUE[수] = 수 < 원본.length() ? 원본.charAt(수) : 0;
        return 원본.length();
    }
    static boolean 같음(String 가, String 나) {
        if (가.length() != 나.length()) return false;
        for (int 수 = 0; 수 < 가.length(); 수++) if (가.charAt(수) != 나.charAt(수)) return false;
        return true;
    }
}
