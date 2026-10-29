// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 最大長と奇数長のデータグラムで、実際の RTL8139 受信リングの折返しを試験する。 */
public final class 通信網ループ {
    public static int 起動処理() {
        if (利用者.引数列個数() != 1) { 利用者.書込("Usage: run stress PORT\n"); return 2; }
        String 文 = 利用者.引数(0);
        int ポート値 = 0;
        for (int 番号 = 0; 番号 < 文.length(); 番号++) {
            if (文.charAt(番号) < '0' || 文.charAt(番号) > '9' || ポート値 > 6553) return 2;
            ポート値 = ポート値 * 10 + 文.charAt(番号) - '0';
        }
        if (ポート値 < 1 || ポート値 > 65535) return 2;
        int 取扱い値 = 利用者.通信網開放(0);
        if (取扱い値 < 0) return 3;
        int[] データ = new int[1024];
        for (int 反復回序数 = 0; 反復回序数 < 24; 反復回序数++) {
            int 長さ = 1024 - (反復回序数 & 1);
            for (int 番号 = 0; 番号 < 長さ; 番号++) データ[番号] = (番号 + 反復回序数) & 255;
            if (利用者.データ送信(取扱い値, 0x0a000202, ポート値, データ, 長さ) != 長さ) return 4;
            if (利用者.データ受取(取扱い値, データ, 300) != 長さ) return 5;
            for (int 番号 = 0; 番号 < 長さ; 番号++) if (データ[番号] != ((番号 + 反復回序数) & 255)) return 6;
        }
        利用者.通信網閉鎖(取扱い値);
        利用者.書込("UDP STRESS PASS: 24 full/odd datagrams\n");
        return 0;
    }
}
