// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트 Rīki 공통 Izvade 및 ASCII Fails Nosaukums Process_VALUE_ievade. */
public final class 자바도구 {
    /** UTF-8 byte_VALUE 배열을 같은 배열의 UTF-16 단위로 바꾼다. 잘못된 입력은 noraidīt_VALUE. */
    static int 원문해독(int[] dati, int 길이) {
        int Lasīt = 0, Rakstīt = 0;
        if (길이 >= 3 && dati[0] == 239 && dati[1] == 187 && dati[2] == 191) Lasīt = 3;
        while (Lasīt < 길이) {
            int VALUE = dati[Lasīt++], numurs = 0, 최소 = 0;
            if (VALUE >= 194 && VALUE <= 223) { numurs = 1; 최소 = 128; VALUE &= 31; }
            else if (VALUE >= 224 && VALUE <= 239) { numurs = 2; 최소 = 2048; VALUE &= 15; }
            else if (VALUE >= 240 && VALUE <= 244) { numurs = 3; 최소 = 65536; VALUE &= 7; }
            else if (VALUE >= 128 || VALUE < 0) return -1;
            if (numurs > 길이 - Lasīt) return -1;
            for (int i = 0; i < numurs; i++) {
                int Tālāk_krājums = dati[Lasīt++]; if ((Tālāk_krājums & 192) != 128) return -1;
                VALUE = (VALUE << 6) | (Tālāk_krājums & 63);
            }
            if (VALUE < 최소 || VALUE > 0x10ffff || (VALUE >= 0xd800 && VALUE <= 0xdfff)) return -1;
            if (VALUE >= 65536) { VALUE -= 65536; dati[Rakstīt++] = 0xd800 | (VALUE >> 10); dati[Rakstīt++] = 0xdc00 | (VALUE & 1023); }
            else dati[Rakstīt++] = VALUE;
        }
        return Rakstīt;
    }
    static void rakstīšana_numurs(int VALUE) {
        if (VALUE < 0) lietotājs.rakstīšana_rakstzīme_VALUE('-'); else VALUE = -VALUE;
        int pozīcijas_indekss = 1000000000;
        boolean Palaist = false;
        while (pozīcijas_indekss != 0) {
            int numurs = -(VALUE / pozīcijas_indekss);
            if (numurs != 0 || Palaist || pozīcijas_indekss == 1) { lietotājs.rakstīšana_rakstzīme_VALUE('0' + numurs); Palaist = true; }
            VALUE %= pozīcijas_indekss; pozīcijas_indekss /= 10;
        }
    }
    static int Nosaukums(int[] mērķis_VALUE, String 원본) {
        if (원본.length() >= mērķis_VALUE.length) return -1;
        for (int numurs = 0; numurs < mērķis_VALUE.length; numurs++) mērķis_VALUE[numurs] = numurs < 원본.length() ? 원본.charAt(numurs) : 0;
        return 원본.length();
    }
    static boolean 같음(String 가, String SECOND_operands) {
        if (가.length() != SECOND_operands.length()) return false;
        for (int numurs = 0; numurs < 가.length(); numurs++) if (가.charAt(numurs) != SECOND_operands.charAt(numurs)) return false;
        return true;
    }
}
