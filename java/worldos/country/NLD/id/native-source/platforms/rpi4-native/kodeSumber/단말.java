// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 단말 {
    static void 문자(int VALUE) {
        if (VALUE < 0x80) Papan.직렬쓰기(VALUE);
        else if (VALUE < 0x800) {
            Papan.직렬쓰기(0xc0 | (VALUE >> 6)); Papan.직렬쓰기(0x80 | (VALUE & 63));
        } else if (VALUE < 0x10000) {
            Papan.직렬쓰기(0xe0 | (VALUE >> 12)); Papan.직렬쓰기(0x80 | ((VALUE >> 6) & 63)); Papan.직렬쓰기(0x80 | (VALUE & 63));
        } else {
            Papan.직렬쓰기(0xf0 | (VALUE >> 18)); Papan.직렬쓰기(0x80 | ((VALUE >> 12) & 63));
            Papan.직렬쓰기(0x80 | ((VALUE >> 6) & 63)); Papan.직렬쓰기(0x80 | (VALUE & 63));
        }
    }
    static void Tulis(String teks) {
        for (int INDEX = 0; INDEX < teks.length(); INDEX++) {
            int VALUE = teks.charAt(INDEX);
            if (VALUE >= 0xd800 && VALUE <= 0xdbff && INDEX + 1 < teks.length()) {
                int 아래 = teks.charAt(INDEX + 1);
                if (아래 >= 0xdc00 && 아래 <= 0xdfff) {
                    VALUE = 0x10000 + ((VALUE - 0xd800) << 10) + 아래 - 0xdc00; INDEX++;
                }
            }
            if (VALUE >= 0xd800 && VALUE <= 0xdfff) VALUE = 0xfffd;
            문자(VALUE);
        }
    }
    static void 수(int VALUE) {
        if (VALUE < 0) 문자('-'); else VALUE = -VALUE;
        int posisi_INDEX = 1000000000;
        boolean jalankan = false;
        while (posisi_INDEX > 0) {
            int angka_VALUE = -(VALUE / posisi_INDEX);
            if (angka_VALUE != 0 || jalankan || posisi_INDEX == 1) { 문자('0' + angka_VALUE); jalankan = true; }
            VALUE %= posisi_INDEX; posisi_INDEX /= 10;
        }
    }
}
