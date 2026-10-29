// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트 hulpmiddelen 공통 tekstuitvoer 및 ASCII bestand Naam Proces_WAARDE_invoer. */
public final class 자바도구 {
    /** UTF-8 byte_WAARDE 배열을 같은 배열의 UTF-16 단위로 바꾼다. 잘못된 입력은 weigeren_WAARDE. */
    static int 원문해독(int[] gegevens, int tijdsduur_WAARDE) {
        int Lezen = 0, Schrijven = 0;
        if (tijdsduur_WAARDE >= 3 && gegevens[0] == 239 && gegevens[1] == 187 && gegevens[2] == 191) Lezen = 3;
        while (Lezen < tijdsduur_WAARDE) {
            int WAARDE = gegevens[Lezen++], nummer = 0, 최소 = 0;
            if (WAARDE >= 194 && WAARDE <= 223) { nummer = 1; 최소 = 128; WAARDE &= 31; }
            else if (WAARDE >= 224 && WAARDE <= 239) { nummer = 2; 최소 = 2048; WAARDE &= 15; }
            else if (WAARDE >= 240 && WAARDE <= 244) { nummer = 3; 최소 = 65536; WAARDE &= 7; }
            else if (WAARDE >= 128 || WAARDE < 0) return -1;
            if (nummer > tijdsduur_WAARDE - Lezen) return -1;
            for (int i = 0; i < nummer; i++) {
                int Volgende_item = gegevens[Lezen++]; if ((Volgende_item & 192) != 128) return -1;
                WAARDE = (WAARDE << 6) | (Volgende_item & 63);
            }
            if (WAARDE < 최소 || WAARDE > 0x10ffff || (WAARDE >= 0xd800 && WAARDE <= 0xdfff)) return -1;
            if (WAARDE >= 65536) { WAARDE -= 65536; gegevens[Schrijven++] = 0xd800 | (WAARDE >> 10); gegevens[Schrijven++] = 0xdc00 | (WAARDE & 1023); }
            else gegevens[Schrijven++] = WAARDE;
        }
        return Schrijven;
    }
    static void schrijven_nummer(int WAARDE) {
        if (WAARDE < 0) gebruikersruimte.schrijven_teken_WAARDE('-'); else WAARDE = -WAARDE;
        int plaatsingsindex = 1000000000;
        boolean starten = false;
        while (plaatsingsindex != 0) {
            int nummer = -(WAARDE / plaatsingsindex);
            if (nummer != 0 || starten || plaatsingsindex == 1) { gebruikersruimte.schrijven_teken_WAARDE('0' + nummer); starten = true; }
            WAARDE %= plaatsingsindex; plaatsingsindex /= 10;
        }
    }
    static int Naam(int[] doel_WAARDE, String 원본) {
        if (원본.length() >= doel_WAARDE.length) return -1;
        for (int nummer = 0; nummer < doel_WAARDE.length; nummer++) doel_WAARDE[nummer] = nummer < 원본.length() ? 원본.charAt(nummer) : 0;
        return 원본.length();
    }
    static boolean 같음(String 가, String SECONDE_operand) {
        if (가.length() != SECONDE_operand.length()) return false;
        for (int nummer = 0; nummer < 가.length(); nummer++) if (가.charAt(nummer) != SECONDE_operand.charAt(nummer)) return false;
        return true;
    }
}
