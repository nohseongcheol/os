// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트 Verkfæri 공통 úttak 및 ASCII Skrá Heiti Ferli_VALUE_færsla. */
public final class 자바도구 {
    /** UTF-8 bæti_VALUE 배열을 같은 배열의 UTF-16 단위로 바꾼다. 잘못된 입력은 hafna_VALUE. */
    static int 원문해독(int[] gögn, int lengd_VALUE) {
        int Lestur = 0, Skrift = 0;
        if (lengd_VALUE >= 3 && gögn[0] == 239 && gögn[1] == 187 && gögn[2] == 191) Lestur = 3;
        while (Lestur < lengd_VALUE) {
            int VALUE = gögn[Lestur++], númer = 0, 최소 = 0;
            if (VALUE >= 194 && VALUE <= 223) { númer = 1; 최소 = 128; VALUE &= 31; }
            else if (VALUE >= 224 && VALUE <= 239) { númer = 2; 최소 = 2048; VALUE &= 15; }
            else if (VALUE >= 240 && VALUE <= 244) { númer = 3; 최소 = 65536; VALUE &= 7; }
            else if (VALUE >= 128 || VALUE < 0) return -1;
            if (númer > lengd_VALUE - Lestur) return -1;
            for (int i = 0; i < númer; i++) {
                int Áfram_vara = gögn[Lestur++]; if ((Áfram_vara & 192) != 128) return -1;
                VALUE = (VALUE << 6) | (Áfram_vara & 63);
            }
            if (VALUE < 최소 || VALUE > 0x10ffff || (VALUE >= 0xd800 && VALUE <= 0xdfff)) return -1;
            if (VALUE >= 65536) { VALUE -= 65536; gögn[Skrift++] = 0xd800 | (VALUE >> 10); gögn[Skrift++] = 0xdc00 | (VALUE & 1023); }
            else gögn[Skrift++] = VALUE;
        }
        return Skrift;
    }
    static void skrifa_númer(int VALUE) {
        if (VALUE < 0) notandi.skrifa_stafur_VALUE('-'); else VALUE = -VALUE;
        int staða_INDEX = 1000000000;
        boolean Keyra_2 = false;
        while (staða_INDEX != 0) {
            int númer = -(VALUE / staða_INDEX);
            if (númer != 0 || Keyra_2 || staða_INDEX == 1) { notandi.skrifa_stafur_VALUE('0' + númer); Keyra_2 = true; }
            VALUE %= staða_INDEX; staða_INDEX /= 10;
        }
    }
    static int Heiti(int[] endastaður_VALUE, String 원본) {
        if (원본.length() >= endastaður_VALUE.length) return -1;
        for (int númer = 0; númer < endastaður_VALUE.length; númer++) endastaður_VALUE[númer] = númer < 원본.length() ? 원본.charAt(númer) : 0;
        return 원본.length();
    }
    static boolean 같음(String 가, String 나) {
        if (가.length() != 나.length()) return false;
        for (int númer = 0; númer < 가.length(); númer++) if (가.charAt(númer) != 나.charAt(númer)) return false;
        return true;
    }
}
