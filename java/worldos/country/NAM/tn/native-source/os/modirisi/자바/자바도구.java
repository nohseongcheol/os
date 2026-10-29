// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트 Thuluse 공통 출력 및 ASCII faele leina Thulaganyo_Boleng_tsenyo. */
public final class 자바도구 {
    /** UTF-8 baete_Boleng 배열을 같은 배열의 UTF-16 단위로 바꾼다. 잘못된 입력은 거부. */
    static int 원문해독(int[] tshedimosetso, int boleele_Boleng) {
        int 읽기 = 0, kwala = 0;
        if (boleele_Boleng >= 3 && tshedimosetso[0] == 239 && tshedimosetso[1] == 187 && tshedimosetso[2] == 191) 읽기 = 3;
        while (읽기 < boleele_Boleng) {
            int Boleng = tshedimosetso[읽기++], 수 = 0, 최소 = 0;
            if (Boleng >= 194 && Boleng <= 223) { 수 = 1; 최소 = 128; Boleng &= 31; }
            else if (Boleng >= 224 && Boleng <= 239) { 수 = 2; 최소 = 2048; Boleng &= 15; }
            else if (Boleng >= 240 && Boleng <= 244) { 수 = 3; 최소 = 65536; Boleng &= 7; }
            else if (Boleng >= 128 || Boleng < 0) return -1;
            if (수 > boleele_Boleng - 읽기) return -1;
            for (int i = 0; i < 수; i++) {
                int 다음 = tshedimosetso[읽기++]; if ((다음 & 192) != 128) return -1;
                Boleng = (Boleng << 6) | (다음 & 63);
            }
            if (Boleng < 최소 || Boleng > 0x10ffff || (Boleng >= 0xd800 && Boleng <= 0xdfff)) return -1;
            if (Boleng >= 65536) { Boleng -= 65536; tshedimosetso[kwala++] = 0xd800 | (Boleng >> 10); tshedimosetso[kwala++] = 0xdc00 | (Boleng & 1023); }
            else tshedimosetso[kwala++] = Boleng;
        }
        return kwala;
    }
    static void 수쓰기(int Boleng) {
        if (Boleng < 0) modirisi.kwala_Letshwao_Boleng('-'); else Boleng = -Boleng;
        int 자리 = 1000000000;
        boolean dirisa = false;
        while (자리 != 0) {
            int 수 = -(Boleng / 자리);
            if (수 != 0 || dirisa || 자리 == 1) { modirisi.kwala_Letshwao_Boleng('0' + 수); dirisa = true; }
            Boleng %= 자리; 자리 /= 10;
        }
    }
    static int leina(int[] bogorogelo_Boleng, String 원본) {
        if (원본.length() >= bogorogelo_Boleng.length) return -1;
        for (int 수 = 0; 수 < bogorogelo_Boleng.length; 수++) bogorogelo_Boleng[수] = 수 < 원본.length() ? 원본.charAt(수) : 0;
        return 원본.length();
    }
    static boolean 같음(String 가, String 나) {
        if (가.length() != 나.length()) return false;
        for (int 수 = 0; 수 < 가.length(); 수++) if (가.charAt(수) != 나.charAt(수)) return false;
        return true;
    }
}
