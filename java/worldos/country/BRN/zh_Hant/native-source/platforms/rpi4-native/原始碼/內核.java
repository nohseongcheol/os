// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 獨立 Java 核心的 Pi4 初始移植版，不在 Linux 或主機 JVM 上執行。 */
public final class 內核 {
    static int[] 任務迭代次數 = new int[3];
    static int[] 任務總和 = new int[3];
    static int 任務排序;
    static int 任務錯誤;
    static int 隨機種子 = 17;

    static void 驗證(boolean 條件, int 編號) {
        if (!條件) { 終端輸入輸出.寫入("FAIL "); 終端輸入輸出.數(編號); 板.停止(編號); }
    }
    static int 分支(int 值) {
        switch (值) { case -100: return 7; case 2: return 9; case 1000: return 11; default: return 3; }
    }
    static int 稠密切換(int 值) {
        switch (值) { case 0: return 9; case 1: return 12; case 2: return 17; case 3: return 20; default: return -1; }
    }
    static int[] 發回陣列(int[] 陣列值) { return 陣列值; }
    static void 測試算術() {
        int 值 = 隨機種子;
        驗證(值 * 7 - 值 == 102 && 值 / 3 == 5 && 值 % 3 == 2, 1);
        int 最小整數 = 0x80000000, 負數一 = -1;
        驗證(最小整數 / 負數一 == 最小整數 && 最小整數 % 負數一 == 0, 2);
        驗證(最小整數 + 最小整數 == 0 && -最小整數 == 最小整數, 3);
        驗證((-值 >> 2) == -5 && (-值 >>> 2) == 1073741819 && (值 << 33) == 34, 4);
        驗證((byte)(值 * 16) == 16 && (short)65535 == -1 && (char)負數一 == 65535, 5);
        int[] 陣列值 = new int[5];
        for (int 循環索引 = 0; 循環索引 < 陣列值.length; 循環索引++) 陣列值[循環索引] = 循環索引 * 值;
        陣列值[2]++;
        驗證(發回陣列(陣列值) == 陣列值 && 陣列值[2] == 35 && 陣列值[4] == 68, 6);
        驗證(分支(值 - 117) == 7 && 分支(值 - 15) == 9 && 分支(值) == 3 && 稠密切換(值 - 15) == 17, 7);
        String 文本 = "한글 😀";
        驗證(文本.length() == 5 && 文本.charAt(0) == '한' && 文本.charAt(3) == 0xd83d, 8);
        驗證(板.CPU特權級別() == 1, 9);
        終端輸入輸出.寫入("JAVA AOT PASS int32/ref64/array/string/switch EL1\n");
    }
    public static void 任務(int 編號) {
        // 檢查交出執行權前後區域變數是否保持不變；每個工作使用獨立的機器堆疊。
        int 局部值 = 編號 * 100;
        for (int 循環索引 = 0; 循環索引 < 10; 循環索引++) {
            if (任務排序 % 2 + 1 != 編號) 任務錯誤++;
            任務排序++;
            局部值 += 循環索引 + 編號;
            任務總和[編號] = 局部值;
            任務迭代次數[編號]++;
            板.掛起處理器();
            if (局部值 != 任務總和[編號]) 任務錯誤++;
        }
    }
    static void 測試任務列() {
        任務排序 = 0; 任務錯誤 = 0;
        任務迭代次數[1] = 0; 任務迭代次數[2] = 0;
        驗證(板.創建任務(1) == 0 && 板.創建任務(2) == 0, 20);
        int 旋轉個數 = 0;
        while (板.任務狀態(1) != 0 || 板.任務狀態(2) != 0) {
            板.掛起處理器();
            驗證(++旋轉個數 < 100, 21);
        }
        驗證(任務迭代次數[1] == 10 && 任務迭代次數[2] == 10 && 任務排序 == 20 && 任務錯誤 == 0, 22);
        驗證(任務總和[1] == 155 && 任務總和[2] == 265, 23);
        終端輸入輸出.寫入("TASK PASS two stacks / 20 alternating steps (cooperative)\n");
    }
    static void 矩形(int 水平位置, int 垂直位置, int 寬度值, int 高度值, int 顏色值) {
        for (int Y_按鈕座標 = 垂直位置; Y_按鈕座標 < 垂直位置 + 高度值; Y_按鈕座標++)
            for (int 橫座標座標 = 水平位置; 橫座標座標 < 水平位置 + 寬度值; 橫座標座標++) 板.放入屏幕像素(橫座標座標, Y_按鈕座標, 顏色值);
    }
    static void 屏幕() {
        if (板.準備屏幕() == 0) { 終端輸入輸出.寫入("FRAMEBUFFER unavailable\n"); return; }
        矩形(0, 0, 板.屏幕寬度(), 板.屏幕高度(), 0x302018);
        矩形(40, 40, 560, 400, 0xefe8e2);
        矩形(40, 40, 560, 40, 0x905020);
        矩形(60, 110, 240, 140, 0x90b050);
        矩形(320, 110, 260, 140, 0xd0a040);
        矩形(60, 290, 520, 120, 0xd8d0c8);
        終端輸入輸出.寫入("FRAMEBUFFER PASS "); 終端輸入輸出.數(板.屏幕寬度()); 終端輸入輸出.字元('x');
        終端輸入輸出.數(板.屏幕高度()); 終端輸入輸出.寫入(" RGB32 (drawing only)\n");
    }
    static void 測試C() {
        int 結果 = 板.測試Cpp();
        驗證(結果 == 0, 100 + 結果);
        終端輸入輸出.寫入("C++ POSIX-KOR PASS direct Java RAM file API\n");
    }
    static void 測試用戶程式列() {
        驗證(板.檢查用戶程式() == 0, 200);
        終端輸入輸出.寫入("ELF64 REJECT PASS malformed / ABI / bounds / W^X\n");
        int 初始結果 = 板.運行用戶程式(0);
        if (初始結果 != 0) { 終端輸入輸出.寫入("USER DEMO RESULT "); 終端輸入輸出.數(初始結果); 終端輸入輸出.字元(10); }
        驗證(初始結果 == 0, 201);
        終端輸入輸出.寫入("EL0 C++ PASS constructors / RAII / file / heap / syscall pointers\n");
        int[] 預期值列 = new int[]{-1001, -1001, -1002, -1001, -1003, -1004, -1001, -1002};
        for (int 編號 = 0; 編號 < 預期值列.length; 編號++) {
            終端輸入輸出.寫入("USER CHECK "); 終端輸入輸出.數(編號); 終端輸入輸出.字元(10);
            int 結果 = 板.運行用戶程式(編號 + 1);
            if (結果 != 預期值列[編號]) { 終端輸入輸出.寫入("USER RESULT "); 終端輸入輸出.數(結果); 終端輸入輸出.字元(10); }
            驗證(結果 == 預期值列[編號], 210 + 編號);
        }
        驗證(板.運行用戶程式(0) == 0, 220);
        終端輸入輸出.寫入("USER PROTECTION PASS kernel/text/MMIO/stack/NX/privilege/timer; kernel recovered\n");
    }
    static void 測試聯網() {
        int 結果 = 板.運行用戶程式(9);
        if (結果 != 0) { 終端輸入輸出.寫入("UDP RESULT "); 終端輸入輸出.數(結果); 終端輸入輸出.字元(10); }
        驗證(結果 == 0, 230);
    }
    static void 系統信息() {
        終端輸入輸出.寫入("Own Java AOT kernel / AArch64 EL1 / Raspberry Pi 4\n");
        終端輸入輸出.寫入("No Linux kernel. Java subset + MicroPython; no full OpenJDK/CPython/Swing.\n");
        終端輸入輸出.寫入("EL0 ELF64 / MMU / W^X / SVC ABI v1 / 2-second user deadline\n");
        終端輸入輸出.寫入("IPv4 TCP/UDP: lwIP over auxiliary UART SLIP; guest FTP. No GENET/Wi-Fi/DNS/TLS yet.\n");
        終端輸入輸出.寫入("Guest TinyCC and static-subset jaot. No SD filesystem or full OpenJDK/pthread.\n");
    }
    public static void 運行() {
        終端輸入輸出.寫入("WorldOS zh_Hant · 您好 · 😀\n");
        測試算術();
        測試C();
        測試任務列();
        屏幕();
        測試用戶程式列();
        測試聯網();
        終端輸入輸出.寫入("NATIVE READY\n");
        命令解釋器.執行命令();
    }
}
