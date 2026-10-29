// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 단말 {
    static void 문자(int VALUE) {
        if (VALUE < 0x80) lövhə.직렬쓰기(VALUE);
        else if (VALUE < 0x800) {
            lövhə.직렬쓰기(0xc0 | (VALUE >> 6)); lövhə.직렬쓰기(0x80 | (VALUE & 63));
        } else if (VALUE < 0x10000) {
            lövhə.직렬쓰기(0xe0 | (VALUE >> 12)); lövhə.직렬쓰기(0x80 | ((VALUE >> 6) & 63)); lövhə.직렬쓰기(0x80 | (VALUE & 63));
        } else {
            lövhə.직렬쓰기(0xf0 | (VALUE >> 18)); lövhə.직렬쓰기(0x80 | ((VALUE >> 12) & 63));
            lövhə.직렬쓰기(0x80 | ((VALUE >> 6) & 63)); lövhə.직렬쓰기(0x80 | (VALUE & 63));
        }
    }
    static void Yazma(String Mətn) {
        for (int INDEX = 0; INDEX < Mətn.length(); INDEX++) {
            int VALUE = Mətn.charAt(INDEX);
            if (VALUE >= 0xd800 && VALUE <= 0xdbff && INDEX + 1 < Mətn.length()) {
                int 아래 = Mətn.charAt(INDEX + 1);
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
        int yerinə_qoymaq_INDEX = 1000000000;
        boolean İcra_Et = false;
        while (yerinə_qoymaq_INDEX > 0) {
            int rəqəm_VALUE = -(VALUE / yerinə_qoymaq_INDEX);
            if (rəqəm_VALUE != 0 || İcra_Et || yerinə_qoymaq_INDEX == 1) { 문자('0' + rəqəm_VALUE); İcra_Et = true; }
            VALUE %= yerinə_qoymaq_INDEX; yerinə_qoymaq_INDEX /= 10;
        }
    }
}
