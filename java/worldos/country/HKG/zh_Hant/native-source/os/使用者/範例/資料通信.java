// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 資料通信 {
    static int 數字值(String 文本) {
        if (文本 == null || 文本.length() == 0) return -1;
        int 結果 = 0;
        for (int 編號 = 0; 編號 < 文本.length(); 編號++) {
            int 值 = 文本.charAt(編號) - '0';
            if (值 < 0 || 值 > 9 || 結果 > 6553) return -1;
            結果 = 結果 * 10 + 值;
            if (結果 > 65535) return -1;
        }
        return 結果;
    }
    static int 地址(String 文本) {
        if (文本 == null) return 0;
        int 值 = 0, 結果 = 0, 子部分值 = 0, 位數 = 0;
        for (int 編號 = 0; 編號 <= 文本.length(); 編號++) {
            int 字元 = 編號 == 文本.length() ? '.' : 文本.charAt(編號);
            if (字元 == '.') {
                if (位數 == 0 || 子部分值 == 4) return 0;
                結果 = (結果 << 8) | 值; 子部分值++; 值 = 0; 位數 = 0;
            } else {
                if (字元 < '0' || 字元 > '9') return 0;
                值 = 值 * 10 + 字元 - '0';
                if (++位數 > 3 || 值 > 255) return 0;
            }
        }
        return 子部分值 == 4 ? 結果 : 0;
    }
    public static int 運行() {
        if (使用者.參數列個數() != 3) { 使用者.寫入("Usage: run udp IP PORT TEXT\n"); return 2; }
        int 地址 = 地址(使用者.實參(0)), 埠值 = 數字值(使用者.實參(1));
        String 內容值 = 使用者.實參(2);
        if (地址 == 0 || 埠值 < 1 || 內容值.length() > 1024) { 使用者.寫入("Bad destination\n"); return 2; }
        int 句柄值 = 使用者.打開網路(0);
        if (句柄值 < 0) { 使用者.寫入("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] 資料 = new int[1024];
        for (int 編號 = 0; 編號 < 內容值.length(); 編號++) 資料[編號] = 內容值.charAt(編號);
        if (使用者.發送資料(句柄值, 地址, 埠值, 資料, 內容值.length()) < 0) {
            使用者.寫入("UDP SEND FAILED\n"); 使用者.關閉網路(句柄值); return 4;
        }
        使用者.寫入("UDP SENT\n");
        int 已接收長度 = 使用者.接收資料(句柄值, 資料, 1500);
        boolean 相等文本 = 已接收長度 == 內容值.length() && 使用者.已發送地址(句柄值) == 地址 && 使用者.已發送埠(句柄值) == 埠值;
        if (相等文本) for (int 編號 = 0; 編號 < 已接收長度; 編號++) if (資料[編號] != 內容值.charAt(編號)) 相等文本 = false;
        使用者.關閉網路(句柄值);
        if (已接收長度 < 0) { 使用者.寫入("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        使用者.寫入(相等文本 ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return 相等文本 ? 0 : 6;
    }
}
