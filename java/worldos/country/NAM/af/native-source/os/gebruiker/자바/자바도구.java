// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트 Nutsmiddels 공통 Afvoer 및 ASCII Lêer Naam Proses_VALUE_inskrywing. */
public final class 자바도구 {
    /** UTF-8 greep_VALUE 배열을 같은 배열의 UTF-16 단위로 바꾼다. 잘못된 입력은 거부. */
    static int 원문해독(int[] data, int lengte_VALUE) {
        int Lees = 0, Skryf = 0;
        if (lengte_VALUE >= 3 && data[0] == 239 && data[1] == 187 && data[2] == 191) Lees = 3;
        while (Lees < lengte_VALUE) {
            int VALUE = data[Lees++], 수 = 0, 최소 = 0;
            if (VALUE >= 194 && VALUE <= 223) { 수 = 1; 최소 = 128; VALUE &= 31; }
            else if (VALUE >= 224 && VALUE <= 239) { 수 = 2; 최소 = 2048; VALUE &= 15; }
            else if (VALUE >= 240 && VALUE <= 244) { 수 = 3; 최소 = 65536; VALUE &= 7; }
            else if (VALUE >= 128 || VALUE < 0) return -1;
            if (수 > lengte_VALUE - Lees) return -1;
            for (int i = 0; i < 수; i++) {
                int Volgende_item = data[Lees++]; if ((Volgende_item & 192) != 128) return -1;
                VALUE = (VALUE << 6) | (Volgende_item & 63);
            }
            if (VALUE < 최소 || VALUE > 0x10ffff || (VALUE >= 0xd800 && VALUE <= 0xdfff)) return -1;
            if (VALUE >= 65536) { VALUE -= 65536; data[Skryf++] = 0xd800 | (VALUE >> 10); data[Skryf++] = 0xdc00 | (VALUE & 1023); }
            else data[Skryf++] = VALUE;
        }
        return Skryf;
    }
    static void 수쓰기(int VALUE) {
        if (VALUE < 0) gebruiker.skryf_karakter_VALUE('-'); else VALUE = -VALUE;
        int plaas_INDEX = 1000000000;
        boolean Loop = false;
        while (plaas_INDEX != 0) {
            int 수 = -(VALUE / plaas_INDEX);
            if (수 != 0 || Loop || plaas_INDEX == 1) { gebruiker.skryf_karakter_VALUE('0' + 수); Loop = true; }
            VALUE %= plaas_INDEX; plaas_INDEX /= 10;
        }
    }
    static int Naam(int[] bestemming_VALUE, String 원본) {
        if (원본.length() >= bestemming_VALUE.length) return -1;
        for (int 수 = 0; 수 < bestemming_VALUE.length; 수++) bestemming_VALUE[수] = 수 < 원본.length() ? 원본.charAt(수) : 0;
        return 원본.length();
    }
    static boolean 같음(String 가, String 나) {
        if (가.length() != 나.length()) return false;
        for (int 수 = 0; 수 < 가.length(); 수++) if (가.charAt(수) != 나.charAt(수)) return false;
        return true;
    }
}
