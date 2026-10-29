// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트 Tools 공통 출력 및 ASCII Fichier Numm Prozess_VALUE_Agab. */
public final class 자바도구 {
    /** UTF-8 Byte_VALUE 배열을 같은 배열의 UTF-16 단위로 바꾼다. 잘못된 입력은 거부. */
    static int 원문해독(int[] Daten, int Längt_VALUE) {
        int 읽기 = 0, schreiwen = 0;
        if (Längt_VALUE >= 3 && Daten[0] == 239 && Daten[1] == 187 && Daten[2] == 191) 읽기 = 3;
        while (읽기 < Längt_VALUE) {
            int VALUE = Daten[읽기++], 수 = 0, 최소 = 0;
            if (VALUE >= 194 && VALUE <= 223) { 수 = 1; 최소 = 128; VALUE &= 31; }
            else if (VALUE >= 224 && VALUE <= 239) { 수 = 2; 최소 = 2048; VALUE &= 15; }
            else if (VALUE >= 240 && VALUE <= 244) { 수 = 3; 최소 = 65536; VALUE &= 7; }
            else if (VALUE >= 128 || VALUE < 0) return -1;
            if (수 > Längt_VALUE - 읽기) return -1;
            for (int i = 0; i < 수; i++) {
                int Weider_Element = Daten[읽기++]; if ((Weider_Element & 192) != 128) return -1;
                VALUE = (VALUE << 6) | (Weider_Element & 63);
            }
            if (VALUE < 최소 || VALUE > 0x10ffff || (VALUE >= 0xd800 && VALUE <= 0xdfff)) return -1;
            if (VALUE >= 65536) { VALUE -= 65536; Daten[schreiwen++] = 0xd800 | (VALUE >> 10); Daten[schreiwen++] = 0xdc00 | (VALUE & 1023); }
            else Daten[schreiwen++] = VALUE;
        }
        return schreiwen;
    }
    static void 수쓰기(int VALUE) {
        if (VALUE < 0) Benotzer.schreiwen_Zeechen_VALUE('-'); else VALUE = -VALUE;
        int positionéieren_INDEX = 1000000000;
        boolean Laf = false;
        while (positionéieren_INDEX != 0) {
            int 수 = -(VALUE / positionéieren_INDEX);
            if (수 != 0 || Laf || positionéieren_INDEX == 1) { Benotzer.schreiwen_Zeechen_VALUE('0' + 수); Laf = true; }
            VALUE %= positionéieren_INDEX; positionéieren_INDEX /= 10;
        }
    }
    static int Numm(int[] Zil_VALUE, String 원본) {
        if (원본.length() >= Zil_VALUE.length) return -1;
        for (int 수 = 0; 수 < Zil_VALUE.length; 수++) Zil_VALUE[수] = 수 < 원본.length() ? 원본.charAt(수) : 0;
        return 원본.length();
    }
    static boolean 같음(String 가, String 나) {
        if (가.length() != 나.length()) return false;
        for (int 수 = 0; 수 < 가.length(); 수++) if (가.charAt(수) != 나.charAt(수)) return false;
        return true;
    }
}
