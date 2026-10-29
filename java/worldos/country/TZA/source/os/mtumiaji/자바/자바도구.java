// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트 Zana 공통 출력 및 ASCII faili Jina Mchakato_thamani_ingizo. */
public final class 자바도구 {
    /** UTF-8 baiti_thamani 배열을 같은 배열의 UTF-16 단위로 바꾼다. 잘못된 입력은 kataa_thamani. */
    static int 원문해독(int[] data, int urefu_thamani) {
        int 읽기 = 0, andika = 0;
        if (urefu_thamani >= 3 && data[0] == 239 && data[1] == 187 && data[2] == 191) 읽기 = 3;
        while (읽기 < urefu_thamani) {
            int thamani = data[읽기++], 수 = 0, 최소 = 0;
            if (thamani >= 194 && thamani <= 223) { 수 = 1; 최소 = 128; thamani &= 31; }
            else if (thamani >= 224 && thamani <= 239) { 수 = 2; 최소 = 2048; thamani &= 15; }
            else if (thamani >= 240 && thamani <= 244) { 수 = 3; 최소 = 65536; thamani &= 7; }
            else if (thamani >= 128 || thamani < 0) return -1;
            if (수 > urefu_thamani - 읽기) return -1;
            for (int i = 0; i < 수; i++) {
                int 다음 = data[읽기++]; if ((다음 & 192) != 128) return -1;
                thamani = (thamani << 6) | (다음 & 63);
            }
            if (thamani < 최소 || thamani > 0x10ffff || (thamani >= 0xd800 && thamani <= 0xdfff)) return -1;
            if (thamani >= 65536) { thamani -= 65536; data[andika++] = 0xd800 | (thamani >> 10); data[andika++] = 0xdc00 | (thamani & 1023); }
            else data[andika++] = thamani;
        }
        return andika;
    }
    static void 수쓰기(int thamani) {
        if (thamani < 0) mtumiaji.andika_kibambo_thamani('-'); else thamani = -thamani;
        int 자리 = 1000000000;
        boolean endesha = false;
        while (자리 != 0) {
            int 수 = -(thamani / 자리);
            if (수 != 0 || endesha || 자리 == 1) { mtumiaji.andika_kibambo_thamani('0' + 수); endesha = true; }
            thamani %= 자리; 자리 /= 10;
        }
    }
    static int Jina(int[] fikio_thamani, String 원본) {
        if (원본.length() >= fikio_thamani.length) return -1;
        for (int 수 = 0; 수 < fikio_thamani.length; 수++) fikio_thamani[수] = 수 < 원본.length() ? 원본.charAt(수) : 0;
        return 원본.length();
    }
    static boolean 같음(String 가, String 나) {
        if (가.length() != 나.length()) return false;
        for (int 수 = 0; 수 < 가.length(); 수++) if (가.charAt(수) != 나.charAt(수)) return false;
        return true;
    }
}
