// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트 Izixhobo 공통 출력 및 ASCII iFayili Igama Inkqubo_ixabiso_ufako_nkcukacha. */
public final class 자바도구 {
    /** UTF-8 ibhayithi_ixabiso 배열을 같은 배열의 UTF-16 단위로 바꾼다. 잘못된 입력은 거부. */
    static int 원문해독(int[] iingcombolo, int ubude_ixabiso) {
        int Funda = 0, Bhala = 0;
        if (ubude_ixabiso >= 3 && iingcombolo[0] == 239 && iingcombolo[1] == 187 && iingcombolo[2] == 191) Funda = 3;
        while (Funda < ubude_ixabiso) {
            int ixabiso = iingcombolo[Funda++], 수 = 0, 최소 = 0;
            if (ixabiso >= 194 && ixabiso <= 223) { 수 = 1; 최소 = 128; ixabiso &= 31; }
            else if (ixabiso >= 224 && ixabiso <= 239) { 수 = 2; 최소 = 2048; ixabiso &= 15; }
            else if (ixabiso >= 240 && ixabiso <= 244) { 수 = 3; 최소 = 65536; ixabiso &= 7; }
            else if (ixabiso >= 128 || ixabiso < 0) return -1;
            if (수 > ubude_ixabiso - Funda) return -1;
            for (int i = 0; i < 수; i++) {
                int 다음 = iingcombolo[Funda++]; if ((다음 & 192) != 128) return -1;
                ixabiso = (ixabiso << 6) | (다음 & 63);
            }
            if (ixabiso < 최소 || ixabiso > 0x10ffff || (ixabiso >= 0xd800 && ixabiso <= 0xdfff)) return -1;
            if (ixabiso >= 65536) { ixabiso -= 65536; iingcombolo[Bhala++] = 0xd800 | (ixabiso >> 10); iingcombolo[Bhala++] = 0xdc00 | (ixabiso & 1023); }
            else iingcombolo[Bhala++] = ixabiso;
        }
        return Bhala;
    }
    static void 수쓰기(int ixabiso) {
        if (ixabiso < 0) umsebenzisi.bhala_ikharakhtha_ixabiso('-'); else ixabiso = -ixabiso;
        int 자리 = 1000000000;
        boolean Phumeza = false;
        while (자리 != 0) {
            int 수 = -(ixabiso / 자리);
            if (수 != 0 || Phumeza || 자리 == 1) { umsebenzisi.bhala_ikharakhtha_ixabiso('0' + 수); Phumeza = true; }
            ixabiso %= 자리; 자리 /= 10;
        }
    }
    static int Igama(int[] indawo_ekuyiwa_kuyo_ixabiso, String 원본) {
        if (원본.length() >= indawo_ekuyiwa_kuyo_ixabiso.length) return -1;
        for (int 수 = 0; 수 < indawo_ekuyiwa_kuyo_ixabiso.length; 수++) indawo_ekuyiwa_kuyo_ixabiso[수] = 수 < 원본.length() ? 원본.charAt(수) : 0;
        return 원본.length();
    }
    static boolean 같음(String 가, String 나) {
        if (가.length() != 나.length()) return false;
        for (int 수 = 0; 수 < 가.length(); 수++) if (가.charAt(수) != 나.charAt(수)) return false;
        return true;
    }
}
