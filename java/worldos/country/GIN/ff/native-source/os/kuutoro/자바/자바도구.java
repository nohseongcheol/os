// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트 도구 공통 출력 및 ASCII fiilde innde Yuɓɓo_golle_njaru_naatnugol. */
public final class 자바도구 {
    /** UTF-8 oktee_njaru 배열을 같은 배열의 UTF-16 단위로 바꾼다. 잘못된 입력은 거부. */
    static int 원문해독(int[] keɓe, int njuuteendi_njaru) {
        int 읽기 = 0, winndude = 0;
        if (njuuteendi_njaru >= 3 && keɓe[0] == 239 && keɓe[1] == 187 && keɓe[2] == 191) 읽기 = 3;
        while (읽기 < njuuteendi_njaru) {
            int njaru = keɓe[읽기++], 수 = 0, 최소 = 0;
            if (njaru >= 194 && njaru <= 223) { 수 = 1; 최소 = 128; njaru &= 31; }
            else if (njaru >= 224 && njaru <= 239) { 수 = 2; 최소 = 2048; njaru &= 15; }
            else if (njaru >= 240 && njaru <= 244) { 수 = 3; 최소 = 65536; njaru &= 7; }
            else if (njaru >= 128 || njaru < 0) return -1;
            if (수 > njuuteendi_njaru - 읽기) return -1;
            for (int i = 0; i < 수; i++) {
                int 다음 = keɓe[읽기++]; if ((다음 & 192) != 128) return -1;
                njaru = (njaru << 6) | (다음 & 63);
            }
            if (njaru < 최소 || njaru > 0x10ffff || (njaru >= 0xd800 && njaru <= 0xdfff)) return -1;
            if (njaru >= 65536) { njaru -= 65536; keɓe[winndude++] = 0xd800 | (njaru >> 10); keɓe[winndude++] = 0xdc00 | (njaru & 1023); }
            else keɓe[winndude++] = njaru;
        }
        return winndude;
    }
    static void 수쓰기(int njaru) {
        if (njaru < 0) kuutoro.winndude_alkulal_njaru('-'); else njaru = -njaru;
        int 자리 = 1000000000;
        boolean huutoraade = false;
        while (자리 != 0) {
            int 수 = -(njaru / 자리);
            if (수 != 0 || huutoraade || 자리 == 1) { kuutoro.winndude_alkulal_njaru('0' + 수); huutoraade = true; }
            njaru %= 자리; 자리 /= 10;
        }
    }
    static int innde(int[] tiindaare_njaru, String 원본) {
        if (원본.length() >= tiindaare_njaru.length) return -1;
        for (int 수 = 0; 수 < tiindaare_njaru.length; 수++) tiindaare_njaru[수] = 수 < 원본.length() ? 원본.charAt(수) : 0;
        return 원본.length();
    }
    static boolean 같음(String 가, String 나) {
        if (가.length() != 나.length()) return false;
        for (int 수 = 0; 수 < 가.length(); 수++) if (가.charAt(수) != 나.charAt(수)) return false;
        return true;
    }
}
