// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트 Àwọn_irinṣẹ́ 공통 출력 및 ASCII Fáìlì Orúkọ Ìlànà_iye_ìgbéwọlé. */
public final class 자바도구 {
    /** UTF-8 báìtì_iye 배열을 같은 배열의 UTF-16 단위로 바꾼다. 잘못된 입력은 거부. */
    static int 원문해독(int[] détà, int gígùn_iye) {
        int Kàá = 0, Kọ = 0;
        if (gígùn_iye >= 3 && détà[0] == 239 && détà[1] == 187 && détà[2] == 191) Kàá = 3;
        while (Kàá < gígùn_iye) {
            int iye = détà[Kàá++], 수 = 0, 최소 = 0;
            if (iye >= 194 && iye <= 223) { 수 = 1; 최소 = 128; iye &= 31; }
            else if (iye >= 224 && iye <= 239) { 수 = 2; 최소 = 2048; iye &= 15; }
            else if (iye >= 240 && iye <= 244) { 수 = 3; 최소 = 65536; iye &= 7; }
            else if (iye >= 128 || iye < 0) return -1;
            if (수 > gígùn_iye - Kàá) return -1;
            for (int i = 0; i < 수; i++) {
                int 다음 = détà[Kàá++]; if ((다음 & 192) != 128) return -1;
                iye = (iye << 6) | (다음 & 63);
            }
            if (iye < 최소 || iye > 0x10ffff || (iye >= 0xd800 && iye <= 0xdfff)) return -1;
            if (iye >= 65536) { iye -= 65536; détà[Kọ++] = 0xd800 | (iye >> 10); détà[Kọ++] = 0xdc00 | (iye & 1023); }
            else détà[Kọ++] = iye;
        }
        return Kọ;
    }
    static void 수쓰기(int iye) {
        if (iye < 0) aṣàmúlò.kọ_ẹyọ_ọ̀rọ̀_iye('-'); else iye = -iye;
        int 자리 = 1000000000;
        boolean Rọ́ọ̀nù = false;
        while (자리 != 0) {
            int 수 = -(iye / 자리);
            if (수 != 0 || Rọ́ọ̀nù || 자리 == 1) { aṣàmúlò.kọ_ẹyọ_ọ̀rọ̀_iye('0' + 수); Rọ́ọ̀nù = true; }
            iye %= 자리; 자리 /= 10;
        }
    }
    static int Orúkọ(int[] èbúté_iye, String 원본) {
        if (원본.length() >= èbúté_iye.length) return -1;
        for (int 수 = 0; 수 < èbúté_iye.length; 수++) èbúté_iye[수] = 수 < 원본.length() ? 원본.charAt(수) : 0;
        return 원본.length();
    }
    static boolean 같음(String 가, String 나) {
        if (가.length() != 나.length()) return false;
        for (int 수 = 0; 수 < 가.length(); 수++) if (가.charAt(수) != 나.charAt(수)) return false;
        return true;
    }
}
