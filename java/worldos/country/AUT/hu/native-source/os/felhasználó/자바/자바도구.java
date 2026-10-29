// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트 Eszközök 공통 Kimenet 및 ASCII Fájl Név folyamat_ÉRTÉK_bejegyzés. */
public final class 자바도구 {
    /** UTF-8 bájt_ÉRTÉK 배열을 같은 배열의 UTF-16 단위로 바꾼다. 잘못된 입력은 elutasít_ÉRTÉK. */
    static int 원문해독(int[] adat, int hossz_ÉRTÉK) {
        int Olvasás = 0, Írás = 0;
        if (hossz_ÉRTÉK >= 3 && adat[0] == 239 && adat[1] == 187 && adat[2] == 191) Olvasás = 3;
        while (Olvasás < hossz_ÉRTÉK) {
            int ÉRTÉK = adat[Olvasás++], szám = 0, 최소 = 0;
            if (ÉRTÉK >= 194 && ÉRTÉK <= 223) { szám = 1; 최소 = 128; ÉRTÉK &= 31; }
            else if (ÉRTÉK >= 224 && ÉRTÉK <= 239) { szám = 2; 최소 = 2048; ÉRTÉK &= 15; }
            else if (ÉRTÉK >= 240 && ÉRTÉK <= 244) { szám = 3; 최소 = 65536; ÉRTÉK &= 7; }
            else if (ÉRTÉK >= 128 || ÉRTÉK < 0) return -1;
            if (szám > hossz_ÉRTÉK - Olvasás) return -1;
            for (int i = 0; i < szám; i++) {
                int Tovább_cikk = adat[Olvasás++]; if ((Tovább_cikk & 192) != 128) return -1;
                ÉRTÉK = (ÉRTÉK << 6) | (Tovább_cikk & 63);
            }
            if (ÉRTÉK < 최소 || ÉRTÉK > 0x10ffff || (ÉRTÉK >= 0xd800 && ÉRTÉK <= 0xdfff)) return -1;
            if (ÉRTÉK >= 65536) { ÉRTÉK -= 65536; adat[Írás++] = 0xd800 | (ÉRTÉK >> 10); adat[Írás++] = 0xdc00 | (ÉRTÉK & 1023); }
            else adat[Írás++] = ÉRTÉK;
        }
        return Írás;
    }
    static void ír_szám(int ÉRTÉK) {
        if (ÉRTÉK < 0) felhasználó.ír_karakter_ÉRTÉK('-'); else ÉRTÉK = -ÉRTÉK;
        int helyzetindex = 1000000000;
        boolean Futtatás = false;
        while (helyzetindex != 0) {
            int szám = -(ÉRTÉK / helyzetindex);
            if (szám != 0 || Futtatás || helyzetindex == 1) { felhasználó.ír_karakter_ÉRTÉK('0' + szám); Futtatás = true; }
            ÉRTÉK %= helyzetindex; helyzetindex /= 10;
        }
    }
    static int Név(int[] cél_ÉRTÉK, String 원본) {
        if (원본.length() >= cél_ÉRTÉK.length) return -1;
        for (int szám = 0; szám < cél_ÉRTÉK.length; szám++) cél_ÉRTÉK[szám] = szám < 원본.length() ? 원본.charAt(szám) : 0;
        return 원본.length();
    }
    static boolean 같음(String 가, String MPERC_operandus) {
        if (가.length() != MPERC_operandus.length()) return false;
        for (int szám = 0; szám < 가.length(); szám++) if (가.charAt(szám) != MPERC_operandus.charAt(szám)) return false;
        return true;
    }
}
