// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트 도구 공통 출력 및 ASCII ini atiq Pivallianiq_atuutilik_Iliniku. */
public final class 자바도구 {
    /** UTF-8 byte_atuutilik 배열을 같은 배열의 UTF-16 단위로 바꾼다. 잘못된 입력은 거부. */
    static int 원문해독(int[] titiqqat, int takininga_atuutilik) {
        int 읽기 = 0, titiraq = 0;
        if (takininga_atuutilik >= 3 && titiqqat[0] == 239 && titiqqat[1] == 187 && titiqqat[2] == 191) 읽기 = 3;
        while (읽기 < takininga_atuutilik) {
            int atuutilik = titiqqat[읽기++], 수 = 0, 최소 = 0;
            if (atuutilik >= 194 && atuutilik <= 223) { 수 = 1; 최소 = 128; atuutilik &= 31; }
            else if (atuutilik >= 224 && atuutilik <= 239) { 수 = 2; 최소 = 2048; atuutilik &= 15; }
            else if (atuutilik >= 240 && atuutilik <= 244) { 수 = 3; 최소 = 65536; atuutilik &= 7; }
            else if (atuutilik >= 128 || atuutilik < 0) return -1;
            if (수 > takininga_atuutilik - 읽기) return -1;
            for (int i = 0; i < 수; i++) {
                int 다음 = titiqqat[읽기++]; if ((다음 & 192) != 128) return -1;
                atuutilik = (atuutilik << 6) | (다음 & 63);
            }
            if (atuutilik < 최소 || atuutilik > 0x10ffff || (atuutilik >= 0xd800 && atuutilik <= 0xdfff)) return -1;
            if (atuutilik >= 65536) { atuutilik -= 65536; titiqqat[titiraq++] = 0xd800 | (atuutilik >> 10); titiqqat[titiraq++] = 0xdc00 | (atuutilik & 1023); }
            else titiqqat[titiraq++] = atuutilik;
        }
        return titiraq;
    }
    static void 수쓰기(int atuutilik) {
        if (atuutilik < 0) atuqtuq.titiraq_immikkuuqtuq_atuutilik('-'); else atuutilik = -atuutilik;
        int 자리 = 1000000000;
        boolean 시작 = false;
        while (자리 != 0) {
            int 수 = -(atuutilik / 자리);
            if (수 != 0 || 시작 || 자리 == 1) { atuqtuq.titiraq_immikkuuqtuq_atuutilik('0' + 수); 시작 = true; }
            atuutilik %= 자리; 자리 /= 10;
        }
    }
    static int atiq(int[] namunngarvik_atuutilik, String 원본) {
        if (원본.length() >= namunngarvik_atuutilik.length) return -1;
        for (int 수 = 0; 수 < namunngarvik_atuutilik.length; 수++) namunngarvik_atuutilik[수] = 수 < 원본.length() ? 원본.charAt(수) : 0;
        return 원본.length();
    }
    static boolean 같음(String 가, String 나) {
        if (가.length() != 나.length()) return false;
        for (int 수 = 0; 수 < 가.length(); 수++) if (가.charAt(수) != 나.charAt(수)) return false;
        return true;
    }
}
