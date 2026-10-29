// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트 Værktøjer 공통 Udgang 및 ASCII Fil Navn Proces_VÆRDI_post. */
public final class 자바도구 {
    /** UTF-8 byte_VÆRDI 배열을 같은 배열의 UTF-16 단위로 바꾼다. 잘못된 입력은 afvise_VÆRDI. */
    static int 원문해독(int[] data, int varighed_VÆRDI) {
        int Læse = 0, Skrive = 0;
        if (varighed_VÆRDI >= 3 && data[0] == 239 && data[1] == 187 && data[2] == 191) Læse = 3;
        while (Læse < varighed_VÆRDI) {
            int VÆRDI = data[Læse++], tal = 0, 최소 = 0;
            if (VÆRDI >= 194 && VÆRDI <= 223) { tal = 1; 최소 = 128; VÆRDI &= 31; }
            else if (VÆRDI >= 224 && VÆRDI <= 239) { tal = 2; 최소 = 2048; VÆRDI &= 15; }
            else if (VÆRDI >= 240 && VÆRDI <= 244) { tal = 3; 최소 = 65536; VÆRDI &= 7; }
            else if (VÆRDI >= 128 || VÆRDI < 0) return -1;
            if (tal > varighed_VÆRDI - Læse) return -1;
            for (int i = 0; i < tal; i++) {
                int Næste_vare = data[Læse++]; if ((Næste_vare & 192) != 128) return -1;
                VÆRDI = (VÆRDI << 6) | (Næste_vare & 63);
            }
            if (VÆRDI < 최소 || VÆRDI > 0x10ffff || (VÆRDI >= 0xd800 && VÆRDI <= 0xdfff)) return -1;
            if (VÆRDI >= 65536) { VÆRDI -= 65536; data[Skrive++] = 0xd800 | (VÆRDI >> 10); data[Skrive++] = 0xdc00 | (VÆRDI & 1023); }
            else data[Skrive++] = VÆRDI;
        }
        return Skrive;
    }
    static void skrive_tal(int VÆRDI) {
        if (VÆRDI < 0) bruger.skrive_tegn_VÆRDI('-'); else VÆRDI = -VÆRDI;
        int positionsindeks = 1000000000;
        boolean Kør_2 = false;
        while (positionsindeks != 0) {
            int tal = -(VÆRDI / positionsindeks);
            if (tal != 0 || Kør_2 || positionsindeks == 1) { bruger.skrive_tegn_VÆRDI('0' + tal); Kør_2 = true; }
            VÆRDI %= positionsindeks; positionsindeks /= 10;
        }
    }
    static int Navn(int[] destination_VÆRDI, String 원본) {
        if (원본.length() >= destination_VÆRDI.length) return -1;
        for (int tal = 0; tal < destination_VÆRDI.length; tal++) destination_VÆRDI[tal] = tal < 원본.length() ? 원본.charAt(tal) : 0;
        return 원본.length();
    }
    static boolean 같음(String 가, String SEKUND_operand) {
        if (가.length() != SEKUND_operand.length()) return false;
        for (int tal = 0; tal < 가.length(); tal++) if (가.charAt(tal) != SEKUND_operand.charAt(tal)) return false;
        return true;
    }
}
