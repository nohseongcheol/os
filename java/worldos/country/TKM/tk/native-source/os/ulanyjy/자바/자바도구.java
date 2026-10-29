// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트 Gurallar 공통 출력 및 ASCII Faýl Ad Proses_baha_girizmeklik. */
public final class 자바도구 {
    /** UTF-8 baýt_baha 배열을 같은 배열의 UTF-16 단위로 바꾼다. 잘못된 입력은 거부. */
    static int 원문해독(int[] maglumat, int dowamlylyk_baha) {
        int Oka = 0, Ýaz = 0;
        if (dowamlylyk_baha >= 3 && maglumat[0] == 239 && maglumat[1] == 187 && maglumat[2] == 191) Oka = 3;
        while (Oka < dowamlylyk_baha) {
            int baha = maglumat[Oka++], 수 = 0, 최소 = 0;
            if (baha >= 194 && baha <= 223) { 수 = 1; 최소 = 128; baha &= 31; }
            else if (baha >= 224 && baha <= 239) { 수 = 2; 최소 = 2048; baha &= 15; }
            else if (baha >= 240 && baha <= 244) { 수 = 3; 최소 = 65536; baha &= 7; }
            else if (baha >= 128 || baha < 0) return -1;
            if (수 > dowamlylyk_baha - Oka) return -1;
            for (int i = 0; i < 수; i++) {
                int 다음 = maglumat[Oka++]; if ((다음 & 192) != 128) return -1;
                baha = (baha << 6) | (다음 & 63);
            }
            if (baha < 최소 || baha > 0x10ffff || (baha >= 0xd800 && baha <= 0xdfff)) return -1;
            if (baha >= 65536) { baha -= 65536; maglumat[Ýaz++] = 0xd800 | (baha >> 10); maglumat[Ýaz++] = 0xdc00 | (baha & 1023); }
            else maglumat[Ýaz++] = baha;
        }
        return Ýaz;
    }
    static void 수쓰기(int baha) {
        if (baha < 0) ulanyjy.ýaz_nyşan_baha('-'); else baha = -baha;
        int 자리 = 1000000000;
        boolean Bitir = false;
        while (자리 != 0) {
            int 수 = -(baha / 자리);
            if (수 != 0 || Bitir || 자리 == 1) { ulanyjy.ýaz_nyşan_baha('0' + 수); Bitir = true; }
            baha %= 자리; 자리 /= 10;
        }
    }
    static int Ad(int[] barylmaly_ýer_baha, String 원본) {
        if (원본.length() >= barylmaly_ýer_baha.length) return -1;
        for (int 수 = 0; 수 < barylmaly_ýer_baha.length; 수++) barylmaly_ýer_baha[수] = 수 < 원본.length() ? 원본.charAt(수) : 0;
        return 원본.length();
    }
    static boolean 같음(String 가, String 나) {
        if (가.length() != 나.length()) return false;
        for (int 수 = 0; 수 < 가.length(); 수++) if (가.charAt(수) != 나.charAt(수)) return false;
        return true;
    }
}
