// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트 Verktøy 공통 Utgang 및 ASCII Fil Navn Prosess_VERDI_oppføring. */
public final class 자바도구 {
    /** UTF-8 byte_VERDI 배열을 같은 배열의 UTF-16 단위로 바꾼다. 잘못된 입력은 avvise_VERDI. */
    static int 원문해독(int[] data, int lengde_VERDI) {
        int Les = 0, Skriv = 0;
        if (lengde_VERDI >= 3 && data[0] == 239 && data[1] == 187 && data[2] == 191) Les = 3;
        while (Les < lengde_VERDI) {
            int VERDI = data[Les++], nummer = 0, 최소 = 0;
            if (VERDI >= 194 && VERDI <= 223) { nummer = 1; 최소 = 128; VERDI &= 31; }
            else if (VERDI >= 224 && VERDI <= 239) { nummer = 2; 최소 = 2048; VERDI &= 15; }
            else if (VERDI >= 240 && VERDI <= 244) { nummer = 3; 최소 = 65536; VERDI &= 7; }
            else if (VERDI >= 128 || VERDI < 0) return -1;
            if (nummer > lengde_VERDI - Les) return -1;
            for (int i = 0; i < nummer; i++) {
                int Neste_vare = data[Les++]; if ((Neste_vare & 192) != 128) return -1;
                VERDI = (VERDI << 6) | (Neste_vare & 63);
            }
            if (VERDI < 최소 || VERDI > 0x10ffff || (VERDI >= 0xd800 && VERDI <= 0xdfff)) return -1;
            if (VERDI >= 65536) { VERDI -= 65536; data[Skriv++] = 0xd800 | (VERDI >> 10); data[Skriv++] = 0xdc00 | (VERDI & 1023); }
            else data[Skriv++] = VERDI;
        }
        return Skriv;
    }
    static void skrive_nummer(int VERDI) {
        if (VERDI < 0) bruker.skrive_tegn_VERDI('-'); else VERDI = -VERDI;
        int posisjonsindeks = 1000000000;
        boolean Kjør_2 = false;
        while (posisjonsindeks != 0) {
            int nummer = -(VERDI / posisjonsindeks);
            if (nummer != 0 || Kjør_2 || posisjonsindeks == 1) { bruker.skrive_tegn_VERDI('0' + nummer); Kjør_2 = true; }
            VERDI %= posisjonsindeks; posisjonsindeks /= 10;
        }
    }
    static int Navn(int[] mål_VERDI, String 원본) {
        if (원본.length() >= mål_VERDI.length) return -1;
        for (int nummer = 0; nummer < mål_VERDI.length; nummer++) mål_VERDI[nummer] = nummer < 원본.length() ? 원본.charAt(nummer) : 0;
        return 원본.length();
    }
    static boolean 같음(String 가, String SEKUND_operand) {
        if (가.length() != SEKUND_operand.length()) return false;
        for (int nummer = 0; nummer < 가.length(); nummer++) if (가.charAt(nummer) != SEKUND_operand.charAt(nummer)) return false;
        return true;
    }
}
