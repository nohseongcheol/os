// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트 መሳርሒታት 공통 출력 및 ASCII ፋይል ሽም መስርሕ_ዋጋ_ምእታው. */
public final class 자바도구 {
    /** UTF-8 ባይት_ዋጋ 배열을 같은 배열의 UTF-16 단위로 바꾼다. 잘못된 입력은 거부. */
    static int 원문해독(int[] ሓበሬታ, int ንውሓት_ዋጋ) {
        int 읽기 = 0, ጸሓፍ = 0;
        if (ንውሓት_ዋጋ >= 3 && ሓበሬታ[0] == 239 && ሓበሬታ[1] == 187 && ሓበሬታ[2] == 191) 읽기 = 3;
        while (읽기 < ንውሓት_ዋጋ) {
            int ዋጋ = ሓበሬታ[읽기++], 수 = 0, 최소 = 0;
            if (ዋጋ >= 194 && ዋጋ <= 223) { 수 = 1; 최소 = 128; ዋጋ &= 31; }
            else if (ዋጋ >= 224 && ዋጋ <= 239) { 수 = 2; 최소 = 2048; ዋጋ &= 15; }
            else if (ዋጋ >= 240 && ዋጋ <= 244) { 수 = 3; 최소 = 65536; ዋጋ &= 7; }
            else if (ዋጋ >= 128 || ዋጋ < 0) return -1;
            if (수 > ንውሓት_ዋጋ - 읽기) return -1;
            for (int i = 0; i < 수; i++) {
                int 다음 = ሓበሬታ[읽기++]; if ((다음 & 192) != 128) return -1;
                ዋጋ = (ዋጋ << 6) | (다음 & 63);
            }
            if (ዋጋ < 최소 || ዋጋ > 0x10ffff || (ዋጋ >= 0xd800 && ዋጋ <= 0xdfff)) return -1;
            if (ዋጋ >= 65536) { ዋጋ -= 65536; ሓበሬታ[ጸሓፍ++] = 0xd800 | (ዋጋ >> 10); ሓበሬታ[ጸሓፍ++] = 0xdc00 | (ዋጋ & 1023); }
            else ሓበሬታ[ጸሓፍ++] = ዋጋ;
        }
        return ጸሓፍ;
    }
    static void 수쓰기(int ዋጋ) {
        if (ዋጋ < 0) ተጠቃሚ.ጸሓፍ_ፊደል_ዋጋ('-'); else ዋጋ = -ዋጋ;
        int 자리 = 1000000000;
        boolean ኣኺድ = false;
        while (자리 != 0) {
            int 수 = -(ዋጋ / 자리);
            if (수 != 0 || ኣኺድ || 자리 == 1) { ተጠቃሚ.ጸሓፍ_ፊደል_ዋጋ('0' + 수); ኣኺድ = true; }
            ዋጋ %= 자리; 자리 /= 10;
        }
    }
    static int ሽም(int[] መዓልቦ_ዋጋ, String 원본) {
        if (원본.length() >= መዓልቦ_ዋጋ.length) return -1;
        for (int 수 = 0; 수 < መዓልቦ_ዋጋ.length; 수++) መዓልቦ_ዋጋ[수] = 수 < 원본.length() ? 원본.charAt(수) : 0;
        return 원본.length();
    }
    static boolean 같음(String 가, String 나) {
        if (가.length() != 나.length()) return false;
        for (int 수 = 0; 수 < 가.length(); 수++) if (가.charAt(수) != 나.charAt(수)) return false;
        return true;
    }
}
