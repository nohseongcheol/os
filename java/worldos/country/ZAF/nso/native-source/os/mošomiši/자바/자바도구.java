// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트 Ditholosi 공통 출력 및 ASCII Faele Leina tiragalo_boleng_go_tsenya_tshedimošo. */
public final class 자바도구 {
    /** UTF-8 paete_boleng 배열을 같은 배열의 UTF-16 단위로 바꾼다. 잘못된 입력은 거부. */
    static int 원문해독(int[] data, int botelele_boleng) {
        int Bala = 0, Ngwala = 0;
        if (botelele_boleng >= 3 && data[0] == 239 && data[1] == 187 && data[2] == 191) Bala = 3;
        while (Bala < botelele_boleng) {
            int boleng = data[Bala++], 수 = 0, 최소 = 0;
            if (boleng >= 194 && boleng <= 223) { 수 = 1; 최소 = 128; boleng &= 31; }
            else if (boleng >= 224 && boleng <= 239) { 수 = 2; 최소 = 2048; boleng &= 15; }
            else if (boleng >= 240 && boleng <= 244) { 수 = 3; 최소 = 65536; boleng &= 7; }
            else if (boleng >= 128 || boleng < 0) return -1;
            if (수 > botelele_boleng - Bala) return -1;
            for (int i = 0; i < 수; i++) {
                int 다음 = data[Bala++]; if ((다음 & 192) != 128) return -1;
                boleng = (boleng << 6) | (다음 & 63);
            }
            if (boleng < 최소 || boleng > 0x10ffff || (boleng >= 0xd800 && boleng <= 0xdfff)) return -1;
            if (boleng >= 65536) { boleng -= 65536; data[Ngwala++] = 0xd800 | (boleng >> 10); data[Ngwala++] = 0xdc00 | (boleng & 1023); }
            else data[Ngwala++] = boleng;
        }
        return Ngwala;
    }
    static void 수쓰기(int boleng) {
        if (boleng < 0) mošomiši.ngwala_tlhaka_boleng('-'); else boleng = -boleng;
        int 자리 = 1000000000;
        boolean Diriša = false;
        while (자리 != 0) {
            int 수 = -(boleng / 자리);
            if (수 != 0 || Diriša || 자리 == 1) { mošomiši.ngwala_tlhaka_boleng('0' + 수); Diriša = true; }
            boleng %= 자리; 자리 /= 10;
        }
    }
    static int Leina(int[] boyo_boleng, String 원본) {
        if (원본.length() >= boyo_boleng.length) return -1;
        for (int 수 = 0; 수 < boyo_boleng.length; 수++) boyo_boleng[수] = 수 < 원본.length() ? 원본.charAt(수) : 0;
        return 원본.length();
    }
    static boolean 같음(String 가, String 나) {
        if (가.length() != 나.length()) return false;
        for (int 수 = 0; 수 < 가.length(); 수++) if (가.charAt(수) != 나.charAt(수)) return false;
        return true;
    }
}
