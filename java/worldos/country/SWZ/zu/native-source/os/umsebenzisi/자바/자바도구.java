// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트 Amathuluzi 공통 출력 및 ASCII Ihele Igama Inqubo_inani_okufakwayo. */
public final class 자바도구 {
    /** UTF-8 ibhayithi_inani 배열을 같은 배열의 UTF-16 단위로 바꾼다. 잘못된 입력은 거부. */
    static int 원문해독(int[] imininingwane, int ubude_inani) {
        int Funda = 0, Bhala = 0;
        if (ubude_inani >= 3 && imininingwane[0] == 239 && imininingwane[1] == 187 && imininingwane[2] == 191) Funda = 3;
        while (Funda < ubude_inani) {
            int inani = imininingwane[Funda++], 수 = 0, 최소 = 0;
            if (inani >= 194 && inani <= 223) { 수 = 1; 최소 = 128; inani &= 31; }
            else if (inani >= 224 && inani <= 239) { 수 = 2; 최소 = 2048; inani &= 15; }
            else if (inani >= 240 && inani <= 244) { 수 = 3; 최소 = 65536; inani &= 7; }
            else if (inani >= 128 || inani < 0) return -1;
            if (수 > ubude_inani - Funda) return -1;
            for (int i = 0; i < 수; i++) {
                int 다음 = imininingwane[Funda++]; if ((다음 & 192) != 128) return -1;
                inani = (inani << 6) | (다음 & 63);
            }
            if (inani < 최소 || inani > 0x10ffff || (inani >= 0xd800 && inani <= 0xdfff)) return -1;
            if (inani >= 65536) { inani -= 65536; imininingwane[Bhala++] = 0xd800 | (inani >> 10); imininingwane[Bhala++] = 0xdc00 | (inani & 1023); }
            else imininingwane[Bhala++] = inani;
        }
        return Bhala;
    }
    static void 수쓰기(int inani) {
        if (inani < 0) umsebenzisi.bhala_uhlamvusimo_inani('-'); else inani = -inani;
        int 자리 = 1000000000;
        boolean Sebenzisa = false;
        while (자리 != 0) {
            int 수 = -(inani / 자리);
            if (수 != 0 || Sebenzisa || 자리 == 1) { umsebenzisi.bhala_uhlamvusimo_inani('0' + 수); Sebenzisa = true; }
            inani %= 자리; 자리 /= 10;
        }
    }
    static int Igama(int[] isikhumulo_inani, String 원본) {
        if (원본.length() >= isikhumulo_inani.length) return -1;
        for (int 수 = 0; 수 < isikhumulo_inani.length; 수++) isikhumulo_inani[수] = 수 < 원본.length() ? 원본.charAt(수) : 0;
        return 원본.length();
    }
    static boolean 같음(String 가, String 나) {
        if (가.length() != 나.length()) return false;
        for (int 수 = 0; 수 < 가.length(); 수++) if (가.charAt(수) != 나.charAt(수)) return false;
        return true;
    }
}
