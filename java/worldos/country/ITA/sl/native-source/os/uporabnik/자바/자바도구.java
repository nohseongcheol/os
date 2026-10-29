// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트 Orodja 공통 Izpis 및 ASCII Datoteka Ime Proces_VALUE_vnos. */
public final class 자바도구 {
    /** UTF-8 bajt_VALUE 배열을 같은 배열의 UTF-16 단위로 바꾼다. 잘못된 입력은 zavrniti_VALUE. */
    static int 원문해독(int[] podatki, int 길이) {
        int Branje = 0, Pisanje = 0;
        if (길이 >= 3 && podatki[0] == 239 && podatki[1] == 187 && podatki[2] == 191) Branje = 3;
        while (Branje < 길이) {
            int VALUE = podatki[Branje++], 수 = 0, 최소 = 0;
            if (VALUE >= 194 && VALUE <= 223) { 수 = 1; 최소 = 128; VALUE &= 31; }
            else if (VALUE >= 224 && VALUE <= 239) { 수 = 2; 최소 = 2048; VALUE &= 15; }
            else if (VALUE >= 240 && VALUE <= 244) { 수 = 3; 최소 = 65536; VALUE &= 7; }
            else if (VALUE >= 128 || VALUE < 0) return -1;
            if (수 > 길이 - Branje) return -1;
            for (int i = 0; i < 수; i++) {
                int Naprej_element = podatki[Branje++]; if ((Naprej_element & 192) != 128) return -1;
                VALUE = (VALUE << 6) | (Naprej_element & 63);
            }
            if (VALUE < 최소 || VALUE > 0x10ffff || (VALUE >= 0xd800 && VALUE <= 0xdfff)) return -1;
            if (VALUE >= 65536) { VALUE -= 65536; podatki[Pisanje++] = 0xd800 | (VALUE >> 10); podatki[Pisanje++] = 0xdc00 | (VALUE & 1023); }
            else podatki[Pisanje++] = VALUE;
        }
        return Pisanje;
    }
    static void 수쓰기(int VALUE) {
        if (VALUE < 0) uporabnik.pisati_znak_VALUE('-'); else VALUE = -VALUE;
        int kazalec_mesta = 1000000000;
        boolean Zaženi = false;
        while (kazalec_mesta != 0) {
            int 수 = -(VALUE / kazalec_mesta);
            if (수 != 0 || Zaženi || kazalec_mesta == 1) { uporabnik.pisati_znak_VALUE('0' + 수); Zaženi = true; }
            VALUE %= kazalec_mesta; kazalec_mesta /= 10;
        }
    }
    static int Ime(int[] cilj_VALUE, String 원본) {
        if (원본.length() >= cilj_VALUE.length) return -1;
        for (int 수 = 0; 수 < cilj_VALUE.length; 수++) cilj_VALUE[수] = 수 < 원본.length() ? 원본.charAt(수) : 0;
        return 원본.length();
    }
    static boolean 같음(String 가, String SECOND_operand) {
        if (가.length() != SECOND_operand.length()) return false;
        for (int 수 = 0; 수 < 가.length(); 수++) if (가.charAt(수) != SECOND_operand.charAt(수)) return false;
        return true;
    }
}
