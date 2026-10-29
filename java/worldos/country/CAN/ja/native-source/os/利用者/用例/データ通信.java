// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class データ通信 {
    static int 桁値(String 文) {
        if (文 == null || 文.length() == 0) return -1;
        int 結果 = 0;
        for (int 番号 = 0; 番号 < 文.length(); 番号++) {
            int 値 = 文.charAt(番号) - '0';
            if (値 < 0 || 値 > 9 || 結果 > 6553) return -1;
            結果 = 結果 * 10 + 値;
            if (結果 > 65535) return -1;
        }
        return 結果;
    }
    static int 番地(String 文) {
        if (文 == null) return 0;
        int 値 = 0, 結果 = 0, 部分要素値 = 0, 桁数 = 0;
        for (int 番号 = 0; 番号 <= 文.length(); 番号++) {
            int 文字 = 番号 == 文.length() ? '.' : 文.charAt(番号);
            if (文字 == '.') {
                if (桁数 == 0 || 部分要素値 == 4) return 0;
                結果 = (結果 << 8) | 値; 部分要素値++; 値 = 0; 桁数 = 0;
            } else {
                if (文字 < '0' || 文字 > '9') return 0;
                値 = 値 * 10 + 文字 - '0';
                if (++桁数 > 3 || 値 > 255) return 0;
            }
        }
        return 部分要素値 == 4 ? 結果 : 0;
    }
    public static int 起動処理() {
        if (利用者.引数列個数() != 3) { 利用者.書込("Usage: run udp IP PORT TEXT\n"); return 2; }
        int 番地 = 番地(利用者.引数(0)), ポート値 = 桁値(利用者.引数(1));
        String 内容物値 = 利用者.引数(2);
        if (番地 == 0 || ポート値 < 1 || 内容物値.length() > 1024) { 利用者.書込("Bad destination\n"); return 2; }
        int 取扱い値 = 利用者.通信網開放(0);
        if (取扱い値 < 0) { 利用者.書込("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] データ = new int[1024];
        for (int 番号 = 0; 番号 < 内容物値.length(); 番号++) データ[番号] = 内容物値.charAt(番号);
        if (利用者.データ送信(取扱い値, 番地, ポート値, データ, 内容物値.length()) < 0) {
            利用者.書込("UDP SEND FAILED\n"); 利用者.通信網閉鎖(取扱い値); return 4;
        }
        利用者.書込("UDP SENT\n");
        int 受信済み長さ = 利用者.データ受取(取扱い値, データ, 1500);
        boolean 等価本文 = 受信済み長さ == 内容物値.length() && 利用者.送信済み番地(取扱い値) == 番地 && 利用者.送信済みポート(取扱い値) == ポート値;
        if (等価本文) for (int 番号 = 0; 番号 < 受信済み長さ; 番号++) if (データ[番号] != 内容物値.charAt(番号)) 等価本文 = false;
        利用者.通信網閉鎖(取扱い値);
        if (受信済み長さ < 0) { 利用者.書込("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        利用者.書込(等価本文 ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return 等価本文 ? 0 : 6;
    }
}
