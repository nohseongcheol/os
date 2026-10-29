// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트 Nástroje 공통 Výstup 및 ASCII Súbor Názov Proces_VALUE_položka. */
public final class 자바도구 {
    /** UTF-8 Byte_VALUE 배열을 같은 배열의 UTF-16 단위로 바꾼다. 잘못된 입력은 odmietnuť_VALUE. */
    static int 원문해독(int[] údaje, int dĺžka_VALUE) {
        int Čítanie = 0, Zápis = 0;
        if (dĺžka_VALUE >= 3 && údaje[0] == 239 && údaje[1] == 187 && údaje[2] == 191) Čítanie = 3;
        while (Čítanie < dĺžka_VALUE) {
            int VALUE = údaje[Čítanie++], 수 = 0, 최소 = 0;
            if (VALUE >= 194 && VALUE <= 223) { 수 = 1; 최소 = 128; VALUE &= 31; }
            else if (VALUE >= 224 && VALUE <= 239) { 수 = 2; 최소 = 2048; VALUE &= 15; }
            else if (VALUE >= 240 && VALUE <= 244) { 수 = 3; 최소 = 65536; VALUE &= 7; }
            else if (VALUE >= 128 || VALUE < 0) return -1;
            if (수 > dĺžka_VALUE - Čítanie) return -1;
            for (int i = 0; i < 수; i++) {
                int Ďalej_položka = údaje[Čítanie++]; if ((Ďalej_položka & 192) != 128) return -1;
                VALUE = (VALUE << 6) | (Ďalej_položka & 63);
            }
            if (VALUE < 최소 || VALUE > 0x10ffff || (VALUE >= 0xd800 && VALUE <= 0xdfff)) return -1;
            if (VALUE >= 65536) { VALUE -= 65536; údaje[Zápis++] = 0xd800 | (VALUE >> 10); údaje[Zápis++] = 0xdc00 | (VALUE & 1023); }
            else údaje[Zápis++] = VALUE;
        }
        return Zápis;
    }
    static void 수쓰기(int VALUE) {
        if (VALUE < 0) používateľ.zapísať_znak_VALUE('-'); else VALUE = -VALUE;
        int pozičný_index = 1000000000;
        boolean Spustiť_2 = false;
        while (pozičný_index != 0) {
            int 수 = -(VALUE / pozičný_index);
            if (수 != 0 || Spustiť_2 || pozičný_index == 1) { používateľ.zapísať_znak_VALUE('0' + 수); Spustiť_2 = true; }
            VALUE %= pozičný_index; pozičný_index /= 10;
        }
    }
    static int Názov(int[] cieľ_VALUE, String 원본) {
        if (원본.length() >= cieľ_VALUE.length) return -1;
        for (int 수 = 0; 수 < cieľ_VALUE.length; 수++) cieľ_VALUE[수] = 수 < 원본.length() ? 원본.charAt(수) : 0;
        return 원본.length();
    }
    static boolean 같음(String 가, String SECOND_operand) {
        if (가.length() != SECOND_operand.length()) return false;
        for (int 수 = 0; 수 < 가.length(); 수++) if (가.charAt(수) != SECOND_operand.charAt(수)) return false;
        return true;
    }
}
