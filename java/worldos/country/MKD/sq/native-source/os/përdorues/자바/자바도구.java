// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트 Mjete 공통 출력 및 ASCII Kartelë Emër Proces_VALUE_futje. */
public final class 자바도구 {
    /** UTF-8 bajt_VALUE 배열을 같은 배열의 UTF-16 단위로 바꾼다. 잘못된 입력은 refuzo_VALUE. */
    static int 원문해독(int[] të_dhëna, int gjatësi_VALUE) {
        int Leximi = 0, Shkrimi = 0;
        if (gjatësi_VALUE >= 3 && të_dhëna[0] == 239 && të_dhëna[1] == 187 && të_dhëna[2] == 191) Leximi = 3;
        while (Leximi < gjatësi_VALUE) {
            int VALUE = të_dhëna[Leximi++], 수 = 0, 최소 = 0;
            if (VALUE >= 194 && VALUE <= 223) { 수 = 1; 최소 = 128; VALUE &= 31; }
            else if (VALUE >= 224 && VALUE <= 239) { 수 = 2; 최소 = 2048; VALUE &= 15; }
            else if (VALUE >= 240 && VALUE <= 244) { 수 = 3; 최소 = 65536; VALUE &= 7; }
            else if (VALUE >= 128 || VALUE < 0) return -1;
            if (수 > gjatësi_VALUE - Leximi) return -1;
            for (int i = 0; i < 수; i++) {
                int Tjetër_njësi = të_dhëna[Leximi++]; if ((Tjetër_njësi & 192) != 128) return -1;
                VALUE = (VALUE << 6) | (Tjetër_njësi & 63);
            }
            if (VALUE < 최소 || VALUE > 0x10ffff || (VALUE >= 0xd800 && VALUE <= 0xdfff)) return -1;
            if (VALUE >= 65536) { VALUE -= 65536; të_dhëna[Shkrimi++] = 0xd800 | (VALUE >> 10); të_dhëna[Shkrimi++] = 0xdc00 | (VALUE & 1023); }
            else të_dhëna[Shkrimi++] = VALUE;
        }
        return Shkrimi;
    }
    static void 수쓰기(int VALUE) {
        if (VALUE < 0) përdorues.shkruaj_karakter_VALUE('-'); else VALUE = -VALUE;
        int pozicioni_INDEX = 1000000000;
        boolean Ekzekuto = false;
        while (pozicioni_INDEX != 0) {
            int 수 = -(VALUE / pozicioni_INDEX);
            if (수 != 0 || Ekzekuto || pozicioni_INDEX == 1) { përdorues.shkruaj_karakter_VALUE('0' + 수); Ekzekuto = true; }
            VALUE %= pozicioni_INDEX; pozicioni_INDEX /= 10;
        }
    }
    static int Emër(int[] vendmbërritje_VALUE, String 원본) {
        if (원본.length() >= vendmbërritje_VALUE.length) return -1;
        for (int 수 = 0; 수 < vendmbërritje_VALUE.length; 수++) vendmbërritje_VALUE[수] = 수 < 원본.length() ? 원본.charAt(수) : 0;
        return 원본.length();
    }
    static boolean 같음(String 가, String 나) {
        if (가.length() != 나.length()) return false;
        for (int 수 = 0; 수 < 가.length(); 수++) if (가.charAt(수) != 나.charAt(수)) return false;
        return true;
    }
}
