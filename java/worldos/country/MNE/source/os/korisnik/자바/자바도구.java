// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트 Alatke 공통 출력 및 ASCII Datoteka ime Proces_VALUE_stavka. */
public final class 자바도구 {
    /** UTF-8 bajt_VALUE 배열을 같은 배열의 UTF-16 단위로 바꾼다. 잘못된 입력은 odbaciti_VALUE_e3ecc00b. */
    static int 원문해독(int[] podaci, int 길이) {
        int 읽기 = 0, 쓰기 = 0;
        if (길이 >= 3 && podaci[0] == 239 && podaci[1] == 187 && podaci[2] == 191) 읽기 = 3;
        while (읽기 < 길이) {
            int VALUE = podaci[읽기++], 수 = 0, 최소 = 0;
            if (VALUE >= 194 && VALUE <= 223) { 수 = 1; 최소 = 128; VALUE &= 31; }
            else if (VALUE >= 224 && VALUE <= 239) { 수 = 2; 최소 = 2048; VALUE &= 15; }
            else if (VALUE >= 240 && VALUE <= 244) { 수 = 3; 최소 = 65536; VALUE &= 7; }
            else if (VALUE >= 128 || VALUE < 0) return -1;
            if (수 > 길이 - 읽기) return -1;
            for (int i = 0; i < 수; i++) {
                int Dalje_stavka = podaci[읽기++]; if ((Dalje_stavka & 192) != 128) return -1;
                VALUE = (VALUE << 6) | (Dalje_stavka & 63);
            }
            if (VALUE < 최소 || VALUE > 0x10ffff || (VALUE >= 0xd800 && VALUE <= 0xdfff)) return -1;
            if (VALUE >= 65536) { VALUE -= 65536; podaci[쓰기++] = 0xd800 | (VALUE >> 10); podaci[쓰기++] = 0xdc00 | (VALUE & 1023); }
            else podaci[쓰기++] = VALUE;
        }
        return 쓰기;
    }
    static void 수쓰기(int VALUE) {
        if (VALUE < 0) korisnik.문자쓰기('-'); else VALUE = -VALUE;
        int indeks_pozicije = 1000000000;
        boolean koristiti = false;
        while (indeks_pozicije != 0) {
            int 수 = -(VALUE / indeks_pozicije);
            if (수 != 0 || koristiti || indeks_pozicije == 1) { korisnik.문자쓰기('0' + 수); koristiti = true; }
            VALUE %= indeks_pozicije; indeks_pozicije /= 10;
        }
    }
    static int ime(int[] odredište_VALUE, String 원본) {
        if (원본.length() >= odredište_VALUE.length) return -1;
        for (int 수 = 0; 수 < odredište_VALUE.length; 수++) odredište_VALUE[수] = 수 < 원본.length() ? 원본.charAt(수) : 0;
        return 원본.length();
    }
    static boolean 같음(String 가, String SECOND_operand) {
        if (가.length() != SECOND_operand.length()) return false;
        for (int 수 = 0; 수 < 가.length(); 수++) if (가.charAt(수) != SECOND_operand.charAt(수)) return false;
        return true;
    }
}
