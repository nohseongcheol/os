// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트 Ibikoresho 공통 출력 및 ASCII Idosiye Izina Inzira_agaciro_icyinjizwa. */
public final class 자바도구 {
    /** UTF-8 bayiti_agaciro 배열을 같은 배열의 UTF-16 단위로 바꾼다. 잘못된 입력은 거부. */
    static int 원문해독(int[] amakurushingiro, int uburebure_agaciro) {
        int 읽기 = 0, kwandika = 0;
        if (uburebure_agaciro >= 3 && amakurushingiro[0] == 239 && amakurushingiro[1] == 187 && amakurushingiro[2] == 191) 읽기 = 3;
        while (읽기 < uburebure_agaciro) {
            int agaciro = amakurushingiro[읽기++], 수 = 0, 최소 = 0;
            if (agaciro >= 194 && agaciro <= 223) { 수 = 1; 최소 = 128; agaciro &= 31; }
            else if (agaciro >= 224 && agaciro <= 239) { 수 = 2; 최소 = 2048; agaciro &= 15; }
            else if (agaciro >= 240 && agaciro <= 244) { 수 = 3; 최소 = 65536; agaciro &= 7; }
            else if (agaciro >= 128 || agaciro < 0) return -1;
            if (수 > uburebure_agaciro - 읽기) return -1;
            for (int i = 0; i < 수; i++) {
                int 다음 = amakurushingiro[읽기++]; if ((다음 & 192) != 128) return -1;
                agaciro = (agaciro << 6) | (다음 & 63);
            }
            if (agaciro < 최소 || agaciro > 0x10ffff || (agaciro >= 0xd800 && agaciro <= 0xdfff)) return -1;
            if (agaciro >= 65536) { agaciro -= 65536; amakurushingiro[kwandika++] = 0xd800 | (agaciro >> 10); amakurushingiro[kwandika++] = 0xdc00 | (agaciro & 1023); }
            else amakurushingiro[kwandika++] = agaciro;
        }
        return kwandika;
    }
    static void 수쓰기(int agaciro) {
        if (agaciro < 0) ukoresha.kwandika_inyuguti_agaciro('-'); else agaciro = -agaciro;
        int 자리 = 1000000000;
        boolean ihuriro = false;
        while (자리 != 0) {
            int 수 = -(agaciro / 자리);
            if (수 != 0 || ihuriro || 자리 == 1) { ukoresha.kwandika_inyuguti_agaciro('0' + 수); ihuriro = true; }
            agaciro %= 자리; 자리 /= 10;
        }
    }
    static int Izina(int[] aho_ijya_agaciro, String 원본) {
        if (원본.length() >= aho_ijya_agaciro.length) return -1;
        for (int 수 = 0; 수 < aho_ijya_agaciro.length; 수++) aho_ijya_agaciro[수] = 수 < 원본.length() ? 원본.charAt(수) : 0;
        return 원본.length();
    }
    static boolean 같음(String 가, String 나) {
        if (가.length() != 나.length()) return false;
        for (int 수 = 0; 수 < 가.length(); 수++) if (가.charAt(수) != 나.charAt(수)) return false;
        return true;
    }
}
