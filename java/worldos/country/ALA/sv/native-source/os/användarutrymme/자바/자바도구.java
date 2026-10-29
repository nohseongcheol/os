// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트 verktyg 공통 utmatningsposition 및 ASCII filnamn Namn Process_värde_post. */
public final class 자바도구 {
    /** UTF-8 byte_värde 배열을 같은 배열의 UTF-16 단위로 바꾼다. 잘못된 입력은 avvisa_värde. */
    static int 원문해독(int[] data, int längd_värde) {
        int Läs = 0, Skriv = 0;
        if (längd_värde >= 3 && data[0] == 239 && data[1] == 187 && data[2] == 191) Läs = 3;
        while (Läs < längd_värde) {
            int värde = data[Läs++], nummer = 0, 최소 = 0;
            if (värde >= 194 && värde <= 223) { nummer = 1; 최소 = 128; värde &= 31; }
            else if (värde >= 224 && värde <= 239) { nummer = 2; 최소 = 2048; värde &= 15; }
            else if (värde >= 240 && värde <= 244) { nummer = 3; 최소 = 65536; värde &= 7; }
            else if (värde >= 128 || värde < 0) return -1;
            if (nummer > längd_värde - Läs) return -1;
            for (int i = 0; i < nummer; i++) {
                int Nästa_objekt = data[Läs++]; if ((Nästa_objekt & 192) != 128) return -1;
                värde = (värde << 6) | (Nästa_objekt & 63);
            }
            if (värde < 최소 || värde > 0x10ffff || (värde >= 0xd800 && värde <= 0xdfff)) return -1;
            if (värde >= 65536) { värde -= 65536; data[Skriv++] = 0xd800 | (värde >> 10); data[Skriv++] = 0xdc00 | (värde & 1023); }
            else data[Skriv++] = värde;
        }
        return Skriv;
    }
    static void skriva_nummer(int värde) {
        if (värde < 0) användarutrymme.skriva_tecken_värde('-'); else värde = -värde;
        int positionsindex = 1000000000;
        boolean Kör = false;
        while (positionsindex != 0) {
            int nummer = -(värde / positionsindex);
            if (nummer != 0 || Kör || positionsindex == 1) { användarutrymme.skriva_tecken_värde('0' + nummer); Kör = true; }
            värde %= positionsindex; positionsindex /= 10;
        }
    }
    static int Namn(int[] mål_värde, String 원본) {
        if (원본.length() >= mål_värde.length) return -1;
        for (int nummer = 0; nummer < mål_värde.length; nummer++) mål_värde[nummer] = nummer < 원본.length() ? 원본.charAt(nummer) : 0;
        return 원본.length();
    }
    static boolean 같음(String 가, String SEKUND_operand) {
        if (가.length() != SEKUND_operand.length()) return false;
        for (int nummer = 0; nummer < 가.length(); nummer++) if (가.charAt(nummer) != SEKUND_operand.charAt(nummer)) return false;
        return true;
    }
}
