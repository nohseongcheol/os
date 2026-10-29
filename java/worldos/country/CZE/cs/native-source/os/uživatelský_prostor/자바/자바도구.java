// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트 nástroje 공통 výstupní_pozice 및 ASCII název_souboru Název Proces_HODNOTA_položka. */
public final class 자바도구 {
    /** UTF-8 bajt_HODNOTA 배열을 같은 배열의 UTF-16 단위로 바꾼다. 잘못된 입력은 odmítnout_HODNOTA. */
    static int 원문해독(int[] data, int délka_HODNOTA) {
        int Čtení = 0, Zápis = 0;
        if (délka_HODNOTA >= 3 && data[0] == 239 && data[1] == 187 && data[2] == 191) Čtení = 3;
        while (Čtení < délka_HODNOTA) {
            int HODNOTA = data[Čtení++], číslo = 0, 최소 = 0;
            if (HODNOTA >= 194 && HODNOTA <= 223) { číslo = 1; 최소 = 128; HODNOTA &= 31; }
            else if (HODNOTA >= 224 && HODNOTA <= 239) { číslo = 2; 최소 = 2048; HODNOTA &= 15; }
            else if (HODNOTA >= 240 && HODNOTA <= 244) { číslo = 3; 최소 = 65536; HODNOTA &= 7; }
            else if (HODNOTA >= 128 || HODNOTA < 0) return -1;
            if (číslo > délka_HODNOTA - Čtení) return -1;
            for (int i = 0; i < číslo; i++) {
                int Další_zboží = data[Čtení++]; if ((Další_zboží & 192) != 128) return -1;
                HODNOTA = (HODNOTA << 6) | (Další_zboží & 63);
            }
            if (HODNOTA < 최소 || HODNOTA > 0x10ffff || (HODNOTA >= 0xd800 && HODNOTA <= 0xdfff)) return -1;
            if (HODNOTA >= 65536) { HODNOTA -= 65536; data[Zápis++] = 0xd800 | (HODNOTA >> 10); data[Zápis++] = 0xdc00 | (HODNOTA & 1023); }
            else data[Zápis++] = HODNOTA;
        }
        return Zápis;
    }
    static void zápis_číslo(int HODNOTA) {
        if (HODNOTA < 0) uživatelský_prostor.zápis_znak_HODNOTA('-'); else HODNOTA = -HODNOTA;
        int poziční_index = 1000000000;
        boolean Spustit_2 = false;
        while (poziční_index != 0) {
            int číslo = -(HODNOTA / poziční_index);
            if (číslo != 0 || Spustit_2 || poziční_index == 1) { uživatelský_prostor.zápis_znak_HODNOTA('0' + číslo); Spustit_2 = true; }
            HODNOTA %= poziční_index; poziční_index /= 10;
        }
    }
    static int Název(int[] cíl_HODNOTA, String 원본) {
        if (원본.length() >= cíl_HODNOTA.length) return -1;
        for (int číslo = 0; číslo < cíl_HODNOTA.length; číslo++) cíl_HODNOTA[číslo] = číslo < 원본.length() ? 원본.charAt(číslo) : 0;
        return 원본.length();
    }
    static boolean 같음(String 가, String SEKUNDA_operand) {
        if (가.length() != SEKUNDA_operand.length()) return false;
        for (int číslo = 0; číslo < 가.length(); číslo++) if (가.charAt(číslo) != SEKUNDA_operand.charAt(číslo)) return false;
        return true;
    }
}
