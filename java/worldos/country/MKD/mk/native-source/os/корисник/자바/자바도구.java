// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트 Алатки 공통 출력 및 ASCII Датотека Име Процес_VALUE_внес. */
public final class 자바도구 {
    /** UTF-8 бајт_VALUE 배열을 같은 배열의 UTF-16 단위로 바꾼다. 잘못된 입력은 одбива_VALUE. */
    static int 원문해독(int[] податоци, int должина_VALUE) {
        int Читај = 0, Запиши = 0;
        if (должина_VALUE >= 3 && податоци[0] == 239 && податоци[1] == 187 && податоци[2] == 191) Читај = 3;
        while (Читај < должина_VALUE) {
            int VALUE = податоци[Читај++], 수 = 0, 최소 = 0;
            if (VALUE >= 194 && VALUE <= 223) { 수 = 1; 최소 = 128; VALUE &= 31; }
            else if (VALUE >= 224 && VALUE <= 239) { 수 = 2; 최소 = 2048; VALUE &= 15; }
            else if (VALUE >= 240 && VALUE <= 244) { 수 = 3; 최소 = 65536; VALUE &= 7; }
            else if (VALUE >= 128 || VALUE < 0) return -1;
            if (수 > должина_VALUE - Читај) return -1;
            for (int i = 0; i < 수; i++) {
                int Следно_ставка = податоци[Читај++]; if ((Следно_ставка & 192) != 128) return -1;
                VALUE = (VALUE << 6) | (Следно_ставка & 63);
            }
            if (VALUE < 최소 || VALUE > 0x10ffff || (VALUE >= 0xd800 && VALUE <= 0xdfff)) return -1;
            if (VALUE >= 65536) { VALUE -= 65536; податоци[Запиши++] = 0xd800 | (VALUE >> 10); податоци[Запиши++] = 0xdc00 | (VALUE & 1023); }
            else податоци[Запиши++] = VALUE;
        }
        return Запиши;
    }
    static void 수쓰기(int VALUE) {
        if (VALUE < 0) корисник.запиши_знак_VALUE('-'); else VALUE = -VALUE;
        int позиционирање_INDEX = 1000000000;
        boolean Изврши_2 = false;
        while (позиционирање_INDEX != 0) {
            int 수 = -(VALUE / позиционирање_INDEX);
            if (수 != 0 || Изврши_2 || позиционирање_INDEX == 1) { корисник.запиши_знак_VALUE('0' + 수); Изврши_2 = true; }
            VALUE %= позиционирање_INDEX; позиционирање_INDEX /= 10;
        }
    }
    static int Име(int[] одредиште_VALUE, String 원본) {
        if (원본.length() >= одредиште_VALUE.length) return -1;
        for (int 수 = 0; 수 < одредиште_VALUE.length; 수++) одредиште_VALUE[수] = 수 < 원본.length() ? 원본.charAt(수) : 0;
        return 원본.length();
    }
    static boolean 같음(String 가, String 나) {
        if (가.length() != 나.length()) return false;
        for (int 수 = 0; 수 < 가.length(); 수++) if (가.charAt(수) != 나.charAt(수)) return false;
        return true;
    }
}
