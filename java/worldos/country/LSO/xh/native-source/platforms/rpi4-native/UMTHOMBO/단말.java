// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 단말 {
    static void 문자(int ixabiso) {
        if (ixabiso < 0x80) 보드.직렬쓰기(ixabiso);
        else if (ixabiso < 0x800) {
            보드.직렬쓰기(0xc0 | (ixabiso >> 6)); 보드.직렬쓰기(0x80 | (ixabiso & 63));
        } else if (ixabiso < 0x10000) {
            보드.직렬쓰기(0xe0 | (ixabiso >> 12)); 보드.직렬쓰기(0x80 | ((ixabiso >> 6) & 63)); 보드.직렬쓰기(0x80 | (ixabiso & 63));
        } else {
            보드.직렬쓰기(0xf0 | (ixabiso >> 18)); 보드.직렬쓰기(0x80 | ((ixabiso >> 12) & 63));
            보드.직렬쓰기(0x80 | ((ixabiso >> 6) & 63)); 보드.직렬쓰기(0x80 | (ixabiso & 63));
        }
    }
    static void Bhala(String Umbhalo) {
        for (int indeksa = 0; indeksa < Umbhalo.length(); indeksa++) {
            int ixabiso = Umbhalo.charAt(indeksa);
            if (ixabiso >= 0xd800 && ixabiso <= 0xdbff && indeksa + 1 < Umbhalo.length()) {
                int 아래 = Umbhalo.charAt(indeksa + 1);
                if (아래 >= 0xdc00 && 아래 <= 0xdfff) {
                    ixabiso = 0x10000 + ((ixabiso - 0xd800) << 10) + 아래 - 0xdc00; indeksa++;
                }
            }
            if (ixabiso >= 0xd800 && ixabiso <= 0xdfff) ixabiso = 0xfffd;
            문자(ixabiso);
        }
    }
    static void 수(int ixabiso) {
        if (ixabiso < 0) 문자('-'); else ixabiso = -ixabiso;
        int 자리 = 1000000000;
        boolean Phumeza = false;
        while (자리 > 0) {
            int inani_ixabiso = -(ixabiso / 자리);
            if (inani_ixabiso != 0 || Phumeza || 자리 == 1) { 문자('0' + inani_ixabiso); Phumeza = true; }
            ixabiso %= 자리; 자리 /= 10;
        }
    }
}
