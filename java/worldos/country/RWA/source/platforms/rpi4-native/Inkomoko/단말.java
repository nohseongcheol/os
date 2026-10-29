// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 단말 {
    static void 문자(int agaciro) {
        if (agaciro < 0x80) 보드.직렬쓰기(agaciro);
        else if (agaciro < 0x800) {
            보드.직렬쓰기(0xc0 | (agaciro >> 6)); 보드.직렬쓰기(0x80 | (agaciro & 63));
        } else if (agaciro < 0x10000) {
            보드.직렬쓰기(0xe0 | (agaciro >> 12)); 보드.직렬쓰기(0x80 | ((agaciro >> 6) & 63)); 보드.직렬쓰기(0x80 | (agaciro & 63));
        } else {
            보드.직렬쓰기(0xf0 | (agaciro >> 18)); 보드.직렬쓰기(0x80 | ((agaciro >> 12) & 63));
            보드.직렬쓰기(0x80 | ((agaciro >> 6) & 63)); 보드.직렬쓰기(0x80 | (agaciro & 63));
        }
    }
    static void kwandika(String Umwandiko) {
        for (int umugerekashakiro = 0; umugerekashakiro < Umwandiko.length(); umugerekashakiro++) {
            int agaciro = Umwandiko.charAt(umugerekashakiro);
            if (agaciro >= 0xd800 && agaciro <= 0xdbff && umugerekashakiro + 1 < Umwandiko.length()) {
                int 아래 = Umwandiko.charAt(umugerekashakiro + 1);
                if (아래 >= 0xdc00 && 아래 <= 0xdfff) {
                    agaciro = 0x10000 + ((agaciro - 0xd800) << 10) + 아래 - 0xdc00; umugerekashakiro++;
                }
            }
            if (agaciro >= 0xd800 && agaciro <= 0xdfff) agaciro = 0xfffd;
            문자(agaciro);
        }
    }
    static void 수(int agaciro) {
        if (agaciro < 0) 문자('-'); else agaciro = -agaciro;
        int 자리 = 1000000000;
        boolean ihuriro = false;
        while (자리 > 0) {
            int umubare_agaciro = -(agaciro / 자리);
            if (umubare_agaciro != 0 || ihuriro || 자리 == 1) { 문자('0' + umubare_agaciro); ihuriro = true; }
            agaciro %= 자리; 자리 /= 10;
        }
    }
}
