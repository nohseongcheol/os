// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 使用最大長度與奇數長度的資料報，測試真實 RTL8139 接收環的繞回。 */
public final class 網路循環 {
    public static int 運行() {
        if (使用者.參數列個數() != 1) { 使用者.寫入("Usage: run stress PORT\n"); return 2; }
        String 文本 = 使用者.實參(0);
        int 埠值 = 0;
        for (int 編號 = 0; 編號 < 文本.length(); 編號++) {
            if (文本.charAt(編號) < '0' || 文本.charAt(編號) > '9' || 埠值 > 6553) return 2;
            埠值 = 埠值 * 10 + 文本.charAt(編號) - '0';
        }
        if (埠值 < 1 || 埠值 > 65535) return 2;
        int 句柄值 = 使用者.打開網路(0);
        if (句柄值 < 0) return 3;
        int[] 資料 = new int[1024];
        for (int 迭代序數 = 0; 迭代序數 < 24; 迭代序數++) {
            int 長度 = 1024 - (迭代序數 & 1);
            for (int 編號 = 0; 編號 < 長度; 編號++) 資料[編號] = (編號 + 迭代序數) & 255;
            if (使用者.發送資料(句柄值, 0x0a000202, 埠值, 資料, 長度) != 長度) return 4;
            if (使用者.接收資料(句柄值, 資料, 300) != 長度) return 5;
            for (int 編號 = 0; 編號 < 長度; 編號++) if (資料[編號] != ((編號 + 迭代序數) & 255)) return 6;
        }
        使用者.關閉網路(句柄值);
        使用者.寫入("UDP STRESS PASS: 24 full/odd datagrams\n");
        return 0;
    }
}
