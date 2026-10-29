// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트 도구 공통 출력 및 ASCII anaajaalaa 이름 처리. */
public final class 자바도구 {
    /** UTF-8 waai_ajutuu 배열을 같은 배열의 UTF-16 단위로 바꾼다. 잘못된 입력은 거부. */
    static int 원문해독(int[] atijaaya, int akaliaa_ajutuu) {
        int 읽기 = 0, ashajaa = 0;
        if (akaliaa_ajutuu >= 3 && atijaaya[0] == 239 && atijaaya[1] == 187 && atijaaya[2] == 191) 읽기 = 3;
        while (읽기 < akaliaa_ajutuu) {
            int ajutuu = atijaaya[읽기++], 수 = 0, 최소 = 0;
            if (ajutuu >= 194 && ajutuu <= 223) { 수 = 1; 최소 = 128; ajutuu &= 31; }
            else if (ajutuu >= 224 && ajutuu <= 239) { 수 = 2; 최소 = 2048; ajutuu &= 15; }
            else if (ajutuu >= 240 && ajutuu <= 244) { 수 = 3; 최소 = 65536; ajutuu &= 7; }
            else if (ajutuu >= 128 || ajutuu < 0) return -1;
            if (수 > akaliaa_ajutuu - 읽기) return -1;
            for (int i = 0; i < 수; i++) {
                int 다음 = atijaaya[읽기++]; if ((다음 & 192) != 128) return -1;
                ajutuu = (ajutuu << 6) | (다음 & 63);
            }
            if (ajutuu < 최소 || ajutuu > 0x10ffff || (ajutuu >= 0xd800 && ajutuu <= 0xdfff)) return -1;
            if (ajutuu >= 65536) { ajutuu -= 65536; atijaaya[ashajaa++] = 0xd800 | (ajutuu >> 10); atijaaya[ashajaa++] = 0xdc00 | (ajutuu & 1023); }
            else atijaaya[ashajaa++] = ajutuu;
        }
        return ashajaa;
    }
    static void 수쓰기(int ajutuu) {
        if (ajutuu < 0) ka_yataayakalü.ashajaa_jeerü_ajutuu('-'); else ajutuu = -ajutuu;
        int 자리 = 1000000000;
        boolean 시작 = false;
        while (자리 != 0) {
            int 수 = -(ajutuu / 자리);
            if (수 != 0 || 시작 || 자리 == 1) { ka_yataayakalü.ashajaa_jeerü_ajutuu('0' + 수); 시작 = true; }
            ajutuu %= 자리; 자리 /= 10;
        }
    }
    static int 이름(int[] jalamüinjatü_ajutuu, String 원본) {
        if (원본.length() >= jalamüinjatü_ajutuu.length) return -1;
        for (int 수 = 0; 수 < jalamüinjatü_ajutuu.length; 수++) jalamüinjatü_ajutuu[수] = 수 < 원본.length() ? 원본.charAt(수) : 0;
        return 원본.length();
    }
    static boolean 같음(String 가, String 나) {
        if (가.length() != 나.length()) return false;
        for (int 수 = 0; 수 < 가.length(); 수++) if (가.charAt(수) != 나.charAt(수)) return false;
        return true;
    }
}
