// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 단말 {
    static void 문자(int thamani) {
        if (thamani < 0x80) 보드.직렬쓰기(thamani);
        else if (thamani < 0x800) {
            보드.직렬쓰기(0xc0 | (thamani >> 6)); 보드.직렬쓰기(0x80 | (thamani & 63));
        } else if (thamani < 0x10000) {
            보드.직렬쓰기(0xe0 | (thamani >> 12)); 보드.직렬쓰기(0x80 | ((thamani >> 6) & 63)); 보드.직렬쓰기(0x80 | (thamani & 63));
        } else {
            보드.직렬쓰기(0xf0 | (thamani >> 18)); 보드.직렬쓰기(0x80 | ((thamani >> 12) & 63));
            보드.직렬쓰기(0x80 | ((thamani >> 6) & 63)); 보드.직렬쓰기(0x80 | (thamani & 63));
        }
    }
    static void andika(String SMS) {
        for (int kielezo = 0; kielezo < SMS.length(); kielezo++) {
            int thamani = SMS.charAt(kielezo);
            if (thamani >= 0xd800 && thamani <= 0xdbff && kielezo + 1 < SMS.length()) {
                int 아래 = SMS.charAt(kielezo + 1);
                if (아래 >= 0xdc00 && 아래 <= 0xdfff) {
                    thamani = 0x10000 + ((thamani - 0xd800) << 10) + 아래 - 0xdc00; kielezo++;
                }
            }
            if (thamani >= 0xd800 && thamani <= 0xdfff) thamani = 0xfffd;
            문자(thamani);
        }
    }
    static void 수(int thamani) {
        if (thamani < 0) 문자('-'); else thamani = -thamani;
        int 자리 = 1000000000;
        boolean endesha = false;
        while (자리 > 0) {
            int dijiti_thamani = -(thamani / 자리);
            if (dijiti_thamani != 0 || endesha || 자리 == 1) { 문자('0' + dijiti_thamani); endesha = true; }
            thamani %= 자리; 자리 /= 10;
        }
    }
}
