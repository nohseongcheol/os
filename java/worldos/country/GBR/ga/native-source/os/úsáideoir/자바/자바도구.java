// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트 Uirlisí 공통 Aschur 및 ASCII Comhad Ainm Próiseas_VALUE_iontráil. */
public final class 자바도구 {
    /** UTF-8 beart_VALUE 배열을 같은 배열의 UTF-16 단위로 바꾼다. 잘못된 입력은 diúltaigh_VALUE. */
    static int 원문해독(int[] sonraí, int fad_VALUE) {
        int Léigh = 0, Scríobh = 0;
        if (fad_VALUE >= 3 && sonraí[0] == 239 && sonraí[1] == 187 && sonraí[2] == 191) Léigh = 3;
        while (Léigh < fad_VALUE) {
            int VALUE = sonraí[Léigh++], 수 = 0, 최소 = 0;
            if (VALUE >= 194 && VALUE <= 223) { 수 = 1; 최소 = 128; VALUE &= 31; }
            else if (VALUE >= 224 && VALUE <= 239) { 수 = 2; 최소 = 2048; VALUE &= 15; }
            else if (VALUE >= 240 && VALUE <= 244) { 수 = 3; 최소 = 65536; VALUE &= 7; }
            else if (VALUE >= 128 || VALUE < 0) return -1;
            if (수 > fad_VALUE - Léigh) return -1;
            for (int i = 0; i < 수; i++) {
                int Ar_aghaidh_mír = sonraí[Léigh++]; if ((Ar_aghaidh_mír & 192) != 128) return -1;
                VALUE = (VALUE << 6) | (Ar_aghaidh_mír & 63);
            }
            if (VALUE < 최소 || VALUE > 0x10ffff || (VALUE >= 0xd800 && VALUE <= 0xdfff)) return -1;
            if (VALUE >= 65536) { VALUE -= 65536; sonraí[Scríobh++] = 0xd800 | (VALUE >> 10); sonraí[Scríobh++] = 0xdc00 | (VALUE & 1023); }
            else sonraí[Scríobh++] = VALUE;
        }
        return Scríobh;
    }
    static void 수쓰기(int VALUE) {
        if (VALUE < 0) úsáideoir.scríobh_carachtar_VALUE('-'); else VALUE = -VALUE;
        int suíomh_INDEX = 1000000000;
        boolean Rith_2 = false;
        while (suíomh_INDEX != 0) {
            int 수 = -(VALUE / suíomh_INDEX);
            if (수 != 0 || Rith_2 || suíomh_INDEX == 1) { úsáideoir.scríobh_carachtar_VALUE('0' + 수); Rith_2 = true; }
            VALUE %= suíomh_INDEX; suíomh_INDEX /= 10;
        }
    }
    static int Ainm(int[] sprioc_VALUE, String 원본) {
        if (원본.length() >= sprioc_VALUE.length) return -1;
        for (int 수 = 0; 수 < sprioc_VALUE.length; 수++) sprioc_VALUE[수] = 수 < 원본.length() ? 원본.charAt(수) : 0;
        return 원본.length();
    }
    static boolean 같음(String 가, String 나) {
        if (가.length() != 나.length()) return false;
        for (int 수 = 0; 수 < 가.length(); 수++) if (가.charAt(수) != 나.charAt(수)) return false;
        return true;
    }
}
