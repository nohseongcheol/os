// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트 Verktøy 공통 Utdata 및 ASCII Fil Namn Prosess_VALUE_oppføring. */
public final class 자바도구 {
    /** UTF-8 byte_VALUE 배열을 같은 배열의 UTF-16 단위로 바꾼다. 잘못된 입력은 avvise_VALUE. */
    static int 원문해독(int[] data, int lengd_VALUE) {
        int Les = 0, Skriv = 0;
        if (lengd_VALUE >= 3 && data[0] == 239 && data[1] == 187 && data[2] == 191) Les = 3;
        while (Les < lengd_VALUE) {
            int VALUE = data[Les++], 수 = 0, 최소 = 0;
            if (VALUE >= 194 && VALUE <= 223) { 수 = 1; 최소 = 128; VALUE &= 31; }
            else if (VALUE >= 224 && VALUE <= 239) { 수 = 2; 최소 = 2048; VALUE &= 15; }
            else if (VALUE >= 240 && VALUE <= 244) { 수 = 3; 최소 = 65536; VALUE &= 7; }
            else if (VALUE >= 128 || VALUE < 0) return -1;
            if (수 > lengd_VALUE - Les) return -1;
            for (int i = 0; i < 수; i++) {
                int Neste_vare = data[Les++]; if ((Neste_vare & 192) != 128) return -1;
                VALUE = (VALUE << 6) | (Neste_vare & 63);
            }
            if (VALUE < 최소 || VALUE > 0x10ffff || (VALUE >= 0xd800 && VALUE <= 0xdfff)) return -1;
            if (VALUE >= 65536) { VALUE -= 65536; data[Skriv++] = 0xd800 | (VALUE >> 10); data[Skriv++] = 0xdc00 | (VALUE & 1023); }
            else data[Skriv++] = VALUE;
        }
        return Skriv;
    }
    static void 수쓰기(int VALUE) {
        if (VALUE < 0) brukar.skrive_teikn_VALUE('-'); else VALUE = -VALUE;
        int plassere_INDEX = 1000000000;
        boolean Køyr_2 = false;
        while (plassere_INDEX != 0) {
            int 수 = -(VALUE / plassere_INDEX);
            if (수 != 0 || Køyr_2 || plassere_INDEX == 1) { brukar.skrive_teikn_VALUE('0' + 수); Køyr_2 = true; }
            VALUE %= plassere_INDEX; plassere_INDEX /= 10;
        }
    }
    static int Namn(int[] mål_VALUE, String 원본) {
        if (원본.length() >= mål_VALUE.length) return -1;
        for (int 수 = 0; 수 < mål_VALUE.length; 수++) mål_VALUE[수] = 수 < 원본.length() ? 원본.charAt(수) : 0;
        return 원본.length();
    }
    static boolean 같음(String 가, String 나) {
        if (가.length() != 나.length()) return false;
        for (int 수 = 0; 수 < 가.length(); 수++) if (가.charAt(수) != 나.charAt(수)) return false;
        return true;
    }
}
