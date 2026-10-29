// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 단말 {
    static void 문자(int inani) {
        if (inani < 0x80) 보드.직렬쓰기(inani);
        else if (inani < 0x800) {
            보드.직렬쓰기(0xc0 | (inani >> 6)); 보드.직렬쓰기(0x80 | (inani & 63));
        } else if (inani < 0x10000) {
            보드.직렬쓰기(0xe0 | (inani >> 12)); 보드.직렬쓰기(0x80 | ((inani >> 6) & 63)); 보드.직렬쓰기(0x80 | (inani & 63));
        } else {
            보드.직렬쓰기(0xf0 | (inani >> 18)); 보드.직렬쓰기(0x80 | ((inani >> 12) & 63));
            보드.직렬쓰기(0x80 | ((inani >> 6) & 63)); 보드.직렬쓰기(0x80 | (inani & 63));
        }
    }
    static void Bhala(String Itekisi) {
        for (int thola_inkomba = 0; thola_inkomba < Itekisi.length(); thola_inkomba++) {
            int inani = Itekisi.charAt(thola_inkomba);
            if (inani >= 0xd800 && inani <= 0xdbff && thola_inkomba + 1 < Itekisi.length()) {
                int 아래 = Itekisi.charAt(thola_inkomba + 1);
                if (아래 >= 0xdc00 && 아래 <= 0xdfff) {
                    inani = 0x10000 + ((inani - 0xd800) << 10) + 아래 - 0xdc00; thola_inkomba++;
                }
            }
            if (inani >= 0xd800 && inani <= 0xdfff) inani = 0xfffd;
            문자(inani);
        }
    }
    static void 수(int inani) {
        if (inani < 0) 문자('-'); else inani = -inani;
        int 자리 = 1000000000;
        boolean Sebenzisa = false;
        while (자리 > 0) {
            int idijithi_inani = -(inani / 자리);
            if (idijithi_inani != 0 || Sebenzisa || 자리 == 1) { 문자('0' + idijithi_inani); Sebenzisa = true; }
            inani %= 자리; 자리 /= 10;
        }
    }
}
