// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트 Instrumente 공통 Rezultat 및 ASCII Fișier Nume Proces_VALUE_intrare. */
public final class 자바도구 {
    /** UTF-8 byte_VALUE 배열을 같은 배열의 UTF-16 단위로 바꾼다. 잘못된 입력은 respinge_VALUE. */
    static int 원문해독(int[] date, int lungime_VALUE) {
        int Citire = 0, Scriere = 0;
        if (lungime_VALUE >= 3 && date[0] == 239 && date[1] == 187 && date[2] == 191) Citire = 3;
        while (Citire < lungime_VALUE) {
            int VALUE = date[Citire++], 수 = 0, 최소 = 0;
            if (VALUE >= 194 && VALUE <= 223) { 수 = 1; 최소 = 128; VALUE &= 31; }
            else if (VALUE >= 224 && VALUE <= 239) { 수 = 2; 최소 = 2048; VALUE &= 15; }
            else if (VALUE >= 240 && VALUE <= 244) { 수 = 3; 최소 = 65536; VALUE &= 7; }
            else if (VALUE >= 128 || VALUE < 0) return -1;
            if (수 > lungime_VALUE - Citire) return -1;
            for (int i = 0; i < 수; i++) {
                int Următorul_element = date[Citire++]; if ((Următorul_element & 192) != 128) return -1;
                VALUE = (VALUE << 6) | (Următorul_element & 63);
            }
            if (VALUE < 최소 || VALUE > 0x10ffff || (VALUE >= 0xd800 && VALUE <= 0xdfff)) return -1;
            if (VALUE >= 65536) { VALUE -= 65536; date[Scriere++] = 0xd800 | (VALUE >> 10); date[Scriere++] = 0xdc00 | (VALUE & 1023); }
            else date[Scriere++] = VALUE;
        }
        return Scriere;
    }
    static void 수쓰기(int VALUE) {
        if (VALUE < 0) utilizator.scriere_caracter_VALUE('-'); else VALUE = -VALUE;
        int index_de_poziție = 1000000000;
        boolean Pornește = false;
        while (index_de_poziție != 0) {
            int 수 = -(VALUE / index_de_poziție);
            if (수 != 0 || Pornește || index_de_poziție == 1) { utilizator.scriere_caracter_VALUE('0' + 수); Pornește = true; }
            VALUE %= index_de_poziție; index_de_poziție /= 10;
        }
    }
    static int Nume(int[] destinație_VALUE, String 원본) {
        if (원본.length() >= destinație_VALUE.length) return -1;
        for (int 수 = 0; 수 < destinație_VALUE.length; 수++) destinație_VALUE[수] = 수 < 원본.length() ? 원본.charAt(수) : 0;
        return 원본.length();
    }
    static boolean 같음(String 가, String SECOND_operand) {
        if (가.length() != SECOND_operand.length()) return false;
        for (int 수 = 0; 수 < 가.length(); 수++) if (가.charAt(수) != SECOND_operand.charAt(수)) return false;
        return true;
    }
}
