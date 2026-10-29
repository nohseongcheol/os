// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트 도구 공통 Eligo 및 ASCII Dosiero Nomo 처리. */
public final class 자바도구 {
    /** UTF-8 바이트 배열을 같은 배열의 UTF-16 단위로 바꾼다. 잘못된 입력은 거부. */
    static int 원문해독(int[] 자료, int 길이) {
        int Lego = 0, Skribo = 0;
        if (길이 >= 3 && 자료[0] == 239 && 자료[1] == 187 && 자료[2] == 191) Lego = 3;
        while (Lego < 길이) {
            int 값 = 자료[Lego++], 수 = 0, 최소 = 0;
            if (값 >= 194 && 값 <= 223) { 수 = 1; 최소 = 128; 값 &= 31; }
            else if (값 >= 224 && 값 <= 239) { 수 = 2; 최소 = 2048; 값 &= 15; }
            else if (값 >= 240 && 값 <= 244) { 수 = 3; 최소 = 65536; 값 &= 7; }
            else if (값 >= 128 || 값 < 0) return -1;
            if (수 > 길이 - Lego) return -1;
            for (int i = 0; i < 수; i++) {
                int 다음 = 자료[Lego++]; if ((다음 & 192) != 128) return -1;
                값 = (값 << 6) | (다음 & 63);
            }
            if (값 < 최소 || 값 > 0x10ffff || (값 >= 0xd800 && 값 <= 0xdfff)) return -1;
            if (값 >= 65536) { 값 -= 65536; 자료[Skribo++] = 0xd800 | (값 >> 10); 자료[Skribo++] = 0xdc00 | (값 & 1023); }
            else 자료[Skribo++] = 값;
        }
        return Skribo;
    }
    static void 수쓰기(int 값) {
        if (값 < 0) 사용자.문자쓰기('-'); else 값 = -값;
        int 자리 = 1000000000;
        boolean Ruli = false;
        while (자리 != 0) {
            int 수 = -(값 / 자리);
            if (수 != 0 || Ruli || 자리 == 1) { 사용자.문자쓰기('0' + 수); Ruli = true; }
            값 %= 자리; 자리 /= 10;
        }
    }
    static int Nomo(int[] 목적, String 원본) {
        if (원본.length() >= 목적.length) return -1;
        for (int 수 = 0; 수 < 목적.length; 수++) 목적[수] = 수 < 원본.length() ? 원본.charAt(수) : 0;
        return 원본.length();
    }
    static boolean 같음(String 가, String 나) {
        if (가.length() != 나.length()) return false;
        for (int 수 = 0; 수 < 가.length(); 수++) if (가.charAt(수) != 나.charAt(수)) return false;
        return true;
    }
}
