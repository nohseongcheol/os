// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트 Jumtukaay_yi 공통 출력 및 ASCII bara_denc tur_253d1510 yokkute_xëyma_dugal_xabaar. */
public final class 자바도구 {
    /** UTF-8 okte_xëyma 배열을 같은 배열의 UTF-16 단위로 바꾼다. 잘못된 입력은 거부. */
    static int 원문해독(int[] mbir, int diir_xëyma) {
        int 읽기 = 0, biir = 0;
        if (diir_xëyma >= 3 && mbir[0] == 239 && mbir[1] == 187 && mbir[2] == 191) 읽기 = 3;
        while (읽기 < diir_xëyma) {
            int xëyma = mbir[읽기++], 수 = 0, 최소 = 0;
            if (xëyma >= 194 && xëyma <= 223) { 수 = 1; 최소 = 128; xëyma &= 31; }
            else if (xëyma >= 224 && xëyma <= 239) { 수 = 2; 최소 = 2048; xëyma &= 15; }
            else if (xëyma >= 240 && xëyma <= 244) { 수 = 3; 최소 = 65536; xëyma &= 7; }
            else if (xëyma >= 128 || xëyma < 0) return -1;
            if (수 > diir_xëyma - 읽기) return -1;
            for (int i = 0; i < 수; i++) {
                int 다음 = mbir[읽기++]; if ((다음 & 192) != 128) return -1;
                xëyma = (xëyma << 6) | (다음 & 63);
            }
            if (xëyma < 최소 || xëyma > 0x10ffff || (xëyma >= 0xd800 && xëyma <= 0xdfff)) return -1;
            if (xëyma >= 65536) { xëyma -= 65536; mbir[biir++] = 0xd800 | (xëyma >> 10); mbir[biir++] = 0xdc00 | (xëyma & 1023); }
            else mbir[biir++] = xëyma;
        }
        return biir;
    }
    static void 수쓰기(int xëyma) {
        if (xëyma < 0) kiy_jariñoo_internet.biir_Araf_xëyma('-'); else xëyma = -xëyma;
        int 자리 = 1000000000;
        boolean daw = false;
        while (자리 != 0) {
            int 수 = -(xëyma / 자리);
            if (수 != 0 || daw || 자리 == 1) { kiy_jariñoo_internet.biir_Araf_xëyma('0' + 수); daw = true; }
            xëyma %= 자리; 자리 /= 10;
        }
    }
    static int tur_253d1510(int[] jëmmukaay_xëyma, String 원본) {
        if (원본.length() >= jëmmukaay_xëyma.length) return -1;
        for (int 수 = 0; 수 < jëmmukaay_xëyma.length; 수++) jëmmukaay_xëyma[수] = 수 < 원본.length() ? 원본.charAt(수) : 0;
        return 원본.length();
    }
    static boolean 같음(String 가, String 나) {
        if (가.length() != 나.length()) return false;
        for (int 수 = 0; 수 < 가.length(); 수++) if (가.charAt(수) != 나.charAt(수)) return false;
        return true;
    }
}
