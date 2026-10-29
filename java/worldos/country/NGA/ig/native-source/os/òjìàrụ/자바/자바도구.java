// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트 Ngwaọrụ 공통 출력 및 ASCII Faịlụ Aha ùsòrò_valuu_ndebà. */
public final class 자바도구 {
    /** UTF-8 baịtị_valuu 배열을 같은 배열의 UTF-16 단위로 바꾼다. 잘못된 입력은 거부. */
    static int 원문해독(int[] datà, int ogologo_valuu) {
        int Wepụta_ọzi = 0, Chekwaa_ozi = 0;
        if (ogologo_valuu >= 3 && datà[0] == 239 && datà[1] == 187 && datà[2] == 191) Wepụta_ọzi = 3;
        while (Wepụta_ọzi < ogologo_valuu) {
            int valuu = datà[Wepụta_ọzi++], 수 = 0, 최소 = 0;
            if (valuu >= 194 && valuu <= 223) { 수 = 1; 최소 = 128; valuu &= 31; }
            else if (valuu >= 224 && valuu <= 239) { 수 = 2; 최소 = 2048; valuu &= 15; }
            else if (valuu >= 240 && valuu <= 244) { 수 = 3; 최소 = 65536; valuu &= 7; }
            else if (valuu >= 128 || valuu < 0) return -1;
            if (수 > ogologo_valuu - Wepụta_ọzi) return -1;
            for (int i = 0; i < 수; i++) {
                int 다음 = datà[Wepụta_ọzi++]; if ((다음 & 192) != 128) return -1;
                valuu = (valuu << 6) | (다음 & 63);
            }
            if (valuu < 최소 || valuu > 0x10ffff || (valuu >= 0xd800 && valuu <= 0xdfff)) return -1;
            if (valuu >= 65536) { valuu -= 65536; datà[Chekwaa_ozi++] = 0xd800 | (valuu >> 10); datà[Chekwaa_ozi++] = 0xdc00 | (valuu & 1023); }
            else datà[Chekwaa_ozi++] = valuu;
        }
        return Chekwaa_ozi;
    }
    static void 수쓰기(int valuu) {
        if (valuu < 0) òjìàrụ.dee_mkpụrụedemede_valuu('-'); else valuu = -valuu;
        int 자리 = 1000000000;
        boolean Bido = false;
        while (자리 != 0) {
            int 수 = -(valuu / 자리);
            if (수 != 0 || Bido || 자리 == 1) { òjìàrụ.dee_mkpụrụedemede_valuu('0' + 수); Bido = true; }
            valuu %= 자리; 자리 /= 10;
        }
    }
    static int Aha(int[] ebemwèga_valuu, String 원본) {
        if (원본.length() >= ebemwèga_valuu.length) return -1;
        for (int 수 = 0; 수 < ebemwèga_valuu.length; 수++) ebemwèga_valuu[수] = 수 < 원본.length() ? 원본.charAt(수) : 0;
        return 원본.length();
    }
    static boolean 같음(String 가, String 나) {
        if (가.length() != 나.length()) return false;
        for (int 수 = 0; 수 < 가.length(); 수++) if (가.charAt(수) != 나.charAt(수)) return false;
        return true;
    }
}
