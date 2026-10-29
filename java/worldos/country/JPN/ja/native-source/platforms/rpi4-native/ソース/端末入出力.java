// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 端末入出力 {
    static void 文字(int 値) {
        if (値 < 0x80) 基板.直列書込(値);
        else if (値 < 0x800) {
            基板.直列書込(0xc0 | (値 >> 6)); 基板.直列書込(0x80 | (値 & 63));
        } else if (値 < 0x10000) {
            基板.直列書込(0xe0 | (値 >> 12)); 基板.直列書込(0x80 | ((値 >> 6) & 63)); 基板.直列書込(0x80 | (値 & 63));
        } else {
            基板.直列書込(0xf0 | (値 >> 18)); 基板.直列書込(0x80 | ((値 >> 12) & 63));
            基板.直列書込(0x80 | ((値 >> 6) & 63)); 基板.直列書込(0x80 | (値 & 63));
        }
    }
    static void 書込(String 文) {
        for (int 番号 = 0; 番号 < 文.length(); 番号++) {
            int 値 = 文.charAt(番号);
            if (値 >= 0xd800 && 値 <= 0xdbff && 番号 + 1 < 文.length()) {
                int 下端値 = 文.charAt(番号 + 1);
                if (下端値 >= 0xdc00 && 下端値 <= 0xdfff) {
                    値 = 0x10000 + ((値 - 0xd800) << 10) + 下端値 - 0xdc00; 番号++;
                }
            }
            if (値 >= 0xd800 && 値 <= 0xdfff) 値 = 0xfffd;
            文字(値);
        }
    }
    static void 数(int 値) {
        if (値 < 0) 文字('-'); else 値 = -値;
        int 位置添字 = 1000000000;
        boolean 起動処理 = false;
        while (位置添字 > 0) {
            int 桁値 = -(値 / 位置添字);
            if (桁値 != 0 || 起動処理 || 位置添字 == 1) { 文字('0' + 桁値); 起動処理 = true; }
            値 %= 位置添字; 位置添字 /= 10;
        }
    }
}
