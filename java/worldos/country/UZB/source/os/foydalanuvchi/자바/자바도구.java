// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트 Vositalar 공통 출력 및 ASCII Fayl Nomi Jarayon_VALUE_kiritish. */
public final class 자바도구 {
    /** UTF-8 bayt_VALUE 배열을 같은 배열의 UTF-16 단위로 바꾼다. 잘못된 입력은 거부. */
    static int 원문해독(int[] ma_lumotlar, int uzunlik_VALUE) {
        int Oʻqish = 0, Yozish = 0;
        if (uzunlik_VALUE >= 3 && ma_lumotlar[0] == 239 && ma_lumotlar[1] == 187 && ma_lumotlar[2] == 191) Oʻqish = 3;
        while (Oʻqish < uzunlik_VALUE) {
            int VALUE = ma_lumotlar[Oʻqish++], 수 = 0, 최소 = 0;
            if (VALUE >= 194 && VALUE <= 223) { 수 = 1; 최소 = 128; VALUE &= 31; }
            else if (VALUE >= 224 && VALUE <= 239) { 수 = 2; 최소 = 2048; VALUE &= 15; }
            else if (VALUE >= 240 && VALUE <= 244) { 수 = 3; 최소 = 65536; VALUE &= 7; }
            else if (VALUE >= 128 || VALUE < 0) return -1;
            if (수 > uzunlik_VALUE - Oʻqish) return -1;
            for (int i = 0; i < 수; i++) {
                int Keyingi_element = ma_lumotlar[Oʻqish++]; if ((Keyingi_element & 192) != 128) return -1;
                VALUE = (VALUE << 6) | (Keyingi_element & 63);
            }
            if (VALUE < 최소 || VALUE > 0x10ffff || (VALUE >= 0xd800 && VALUE <= 0xdfff)) return -1;
            if (VALUE >= 65536) { VALUE -= 65536; ma_lumotlar[Yozish++] = 0xd800 | (VALUE >> 10); ma_lumotlar[Yozish++] = 0xdc00 | (VALUE & 1023); }
            else ma_lumotlar[Yozish++] = VALUE;
        }
        return Yozish;
    }
    static void 수쓰기(int VALUE) {
        if (VALUE < 0) foydalanuvchi.yozmoq_belgi_VALUE('-'); else VALUE = -VALUE;
        int holat_INDEX = 1000000000;
        boolean Bajarish = false;
        while (holat_INDEX != 0) {
            int 수 = -(VALUE / holat_INDEX);
            if (수 != 0 || Bajarish || holat_INDEX == 1) { foydalanuvchi.yozmoq_belgi_VALUE('0' + 수); Bajarish = true; }
            VALUE %= holat_INDEX; holat_INDEX /= 10;
        }
    }
    static int Nomi(int[] ko_chirish_joyi_VALUE, String 원본) {
        if (원본.length() >= ko_chirish_joyi_VALUE.length) return -1;
        for (int 수 = 0; 수 < ko_chirish_joyi_VALUE.length; 수++) ko_chirish_joyi_VALUE[수] = 수 < 원본.length() ? 원본.charAt(수) : 0;
        return 원본.length();
    }
    static boolean 같음(String 가, String 나) {
        if (가.length() != 나.length()) return false;
        for (int 수 = 0; 수 < 가.length(); 수++) if (가.charAt(수) != 나.charAt(수)) return false;
        return true;
    }
}
