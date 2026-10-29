// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 管線按 16 KiB 分塊依序執行，不模擬行程或並行管線。 */
public final class 命令殼輸入輸出 {
    static int[] 輸入資料 = new int[16384], 輸出資料 = new int[16384];
    static int 輸入長度, 輸入位置, 輸出長度, 輸入檔案 = -1, 輸出檔案 = -1;
    static boolean 管道輸入, 管道輸出;
    static int 失敗值;
    static boolean 允許交互式 = true;
    public static int 是否交互式() { return 允許交互式 && 輸入檔案 < 3 && 輸出檔案 < 3 && !管道輸入 && !管道輸出 ? 1 : 0; }
    public static int 輸出(int 信道值, int 值) {
        if (信道值 != 1) return 0;
        if (輸出檔案 >= 3) { int 已處理值 = 記憶體檔案集.寫入(輸出檔案, 值); if (已處理值 < 0) 失敗值 = 已處理值; return 1; }
        if (!管道輸出) return 0;
        if (輸出長度 == 輸出資料.length) 失敗值 = -28;
        else 輸出資料[輸出長度++] = 值;
        return 1;
    }
    public static int 輸入值() {
        if (輸入檔案 >= 3) { int 已處理值 = 記憶體檔案集.讀取(輸入檔案); return 已處理值 == 256 ? -2 : 已處理值; }
        if (管道輸入) return 輸入位置 < 輸入長度 ? 輸入資料[輸入位置++] : -2;
        return -3; // 轉送至 UART。
    }
    static void 運行(boolean 前導管道, boolean 尾隨管道) {
        管道輸入 = 前導管道; 管道輸出 = 尾隨管道;
        輸入位置 = 0; 輸出長度 = 0; 輸入檔案 = -1; 輸出檔案 = -1; 失敗值 = 0;
    }
    static void 結尾() {
        板.切換輸入輸出(0);
        if (輸入檔案 >= 3) 記憶體檔案集.關閉(輸入檔案);
        if (輸出檔案 >= 3) 記憶體檔案集.關閉(輸出檔案);
        if (管道輸出) { 輸入長度 = 輸出長度; for (int 循環索引 = 0; 循環索引 < 輸出長度; 循環索引++) 輸入資料[循環索引] = 輸出資料[循環索引]; }
        輸入檔案 = -1; 輸出檔案 = -1; 管道輸入 = false; 管道輸出 = false;
    }
}
