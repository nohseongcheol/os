// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ゲスト道具に共通する出力と ASCII ファイル名の処理。 */
public final class Java道具 {
    /** UTF-8 バイト配列を同じ配列内の UTF-16 単位へ変換する。不正な入力は拒否する。 */
    static int ソース復号(int[] データ, int 長さ) {
        int 読取 = 0, 書込 = 0;
        if (長さ >= 3 && データ[0] == 239 && データ[1] == 187 && データ[2] == 191) 読取 = 3;
        while (読取 < 長さ) {
            int 値 = データ[読取++], 数 = 0, 最小値 = 0;
            if (値 >= 194 && 値 <= 223) { 数 = 1; 最小値 = 128; 値 &= 31; }
            else if (値 >= 224 && 値 <= 239) { 数 = 2; 最小値 = 2048; 値 &= 15; }
            else if (値 >= 240 && 値 <= 244) { 数 = 3; 最小値 = 65536; 値 &= 7; }
            else if (値 >= 128 || 値 < 0) return -1;
            if (数 > 長さ - 読取) return -1;
            for (int i = 0; i < 数; i++) {
                int 次回項目 = データ[読取++]; if ((次回項目 & 192) != 128) return -1;
                値 = (値 << 6) | (次回項目 & 63);
            }
            if (値 < 最小値 || 値 > 0x10ffff || (値 >= 0xd800 && 値 <= 0xdfff)) return -1;
            if (値 >= 65536) { 値 -= 65536; データ[書込++] = 0xd800 | (値 >> 10); データ[書込++] = 0xdc00 | (値 & 1023); }
            else データ[書込++] = 値;
        }
        return 書込;
    }
    static void 番号書込(int 値) {
        if (値 < 0) 利用者.文字値書込('-'); else 値 = -値;
        int 位置添字 = 1000000000;
        boolean 起動処理 = false;
        while (位置添字 != 0) {
            int 数 = -(値 / 位置添字);
            if (数 != 0 || 起動処理 || 位置添字 == 1) { 利用者.文字値書込('0' + 数); 起動処理 = true; }
            値 %= 位置添字; 位置添字 /= 10;
        }
    }
    static int 名前(int[] 宛先値, String 原本) {
        if (原本.length() >= 宛先値.length) return -1;
        for (int 数 = 0; 数 < 宛先値.length; 数++) 宛先値[数] = 数 < 原本.length() ? 原本.charAt(数) : 0;
        return 原本.length();
    }
    static boolean 等価本文(String 先頭位置被演算子, String 第二被演算子) {
        if (先頭位置被演算子.length() != 第二被演算子.length()) return false;
        for (int 数 = 0; 数 < 先頭位置被演算子.length(); 数++) if (先頭位置被演算子.charAt(数) != 第二被演算子.charAt(数)) return false;
        return true;
    }
}
