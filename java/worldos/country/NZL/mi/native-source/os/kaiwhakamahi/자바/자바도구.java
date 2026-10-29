// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트 Ngā_Utauta 공통 출력 및 ASCII Kōnae Ingoa Hātepe_uara_tāurunga. */
public final class 자바도구 {
    /** UTF-8 paita_uara 배열을 같은 배열의 UTF-16 단위로 바꾼다. 잘못된 입력은 거부. */
    static int 원문해독(int[] raraunga, int roa_uara) {
        int Pānuitia = 0, Tuhia = 0;
        if (roa_uara >= 3 && raraunga[0] == 239 && raraunga[1] == 187 && raraunga[2] == 191) Pānuitia = 3;
        while (Pānuitia < roa_uara) {
            int uara = raraunga[Pānuitia++], 수 = 0, 최소 = 0;
            if (uara >= 194 && uara <= 223) { 수 = 1; 최소 = 128; uara &= 31; }
            else if (uara >= 224 && uara <= 239) { 수 = 2; 최소 = 2048; uara &= 15; }
            else if (uara >= 240 && uara <= 244) { 수 = 3; 최소 = 65536; uara &= 7; }
            else if (uara >= 128 || uara < 0) return -1;
            if (수 > roa_uara - Pānuitia) return -1;
            for (int i = 0; i < 수; i++) {
                int Panuku_tuemi = raraunga[Pānuitia++]; if ((Panuku_tuemi & 192) != 128) return -1;
                uara = (uara << 6) | (Panuku_tuemi & 63);
            }
            if (uara < 최소 || uara > 0x10ffff || (uara >= 0xd800 && uara <= 0xdfff)) return -1;
            if (uara >= 65536) { uara -= 65536; raraunga[Tuhia++] = 0xd800 | (uara >> 10); raraunga[Tuhia++] = 0xdc00 | (uara & 1023); }
            else raraunga[Tuhia++] = uara;
        }
        return Tuhia;
    }
    static void 수쓰기(int uara) {
        if (uara < 0) kaiwhakamahi.tuhi_pūāhua_uara('-'); else uara = -uara;
        int tūranga_INDEX = 1000000000;
        boolean whakahaere = false;
        while (tūranga_INDEX != 0) {
            int 수 = -(uara / tūranga_INDEX);
            if (수 != 0 || whakahaere || tūranga_INDEX == 1) { kaiwhakamahi.tuhi_pūāhua_uara('0' + 수); whakahaere = true; }
            uara %= tūranga_INDEX; tūranga_INDEX /= 10;
        }
    }
    static int Ingoa(int[] ūnga_uara, String 원본) {
        if (원본.length() >= ūnga_uara.length) return -1;
        for (int 수 = 0; 수 < ūnga_uara.length; 수++) ūnga_uara[수] = 수 < 원본.length() ? 원본.charAt(수) : 0;
        return 원본.length();
    }
    static boolean 같음(String 가, String 나) {
        if (가.length() != 나.length()) return false;
        for (int 수 = 0; 수 < 가.length(); 수++) if (가.charAt(수) != 나.charAt(수)) return false;
        return true;
    }
}
