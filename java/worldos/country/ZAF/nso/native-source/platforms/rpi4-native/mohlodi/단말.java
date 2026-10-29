// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 단말 {
    static void 문자(int boleng) {
        if (boleng < 0x80) 보드.직렬쓰기(boleng);
        else if (boleng < 0x800) {
            보드.직렬쓰기(0xc0 | (boleng >> 6)); 보드.직렬쓰기(0x80 | (boleng & 63));
        } else if (boleng < 0x10000) {
            보드.직렬쓰기(0xe0 | (boleng >> 12)); 보드.직렬쓰기(0x80 | ((boleng >> 6) & 63)); 보드.직렬쓰기(0x80 | (boleng & 63));
        } else {
            보드.직렬쓰기(0xf0 | (boleng >> 18)); 보드.직렬쓰기(0x80 | ((boleng >> 12) & 63));
            보드.직렬쓰기(0x80 | ((boleng >> 6) & 63)); 보드.직렬쓰기(0x80 | (boleng & 63));
        }
    }
    static void Ngwala(String Sengwalwa) {
        for (int lokela = 0; lokela < Sengwalwa.length(); lokela++) {
            int boleng = Sengwalwa.charAt(lokela);
            if (boleng >= 0xd800 && boleng <= 0xdbff && lokela + 1 < Sengwalwa.length()) {
                int 아래 = Sengwalwa.charAt(lokela + 1);
                if (아래 >= 0xdc00 && 아래 <= 0xdfff) {
                    boleng = 0x10000 + ((boleng - 0xd800) << 10) + 아래 - 0xdc00; lokela++;
                }
            }
            if (boleng >= 0xd800 && boleng <= 0xdfff) boleng = 0xfffd;
            문자(boleng);
        }
    }
    static void 수(int boleng) {
        if (boleng < 0) 문자('-'); else boleng = -boleng;
        int 자리 = 1000000000;
        boolean Diriša = false;
        while (자리 > 0) {
            int 숫자 = -(boleng / 자리);
            if (숫자 != 0 || Diriša || 자리 == 1) { 문자('0' + 숫자); Diriša = true; }
            boleng %= 자리; 자리 /= 10;
        }
    }
}
