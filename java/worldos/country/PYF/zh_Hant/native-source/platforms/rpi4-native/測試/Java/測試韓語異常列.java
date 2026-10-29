// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 中文.內建.*;

public class 測試韓語異常列 {
    static void 默認超時() throws java.io.IOException {
        throw new java.net.SocketTimeoutException("원래 異常");
    }
    public static void main(String[] 實參) throws 輸入輸出異常 {
        try { throw new 等待狀態超時異常("等待狀態狀態 結尾"); }
        catch (等待狀態超時異常 錯誤) { 輸出.寫入行(錯誤.說明()); }
        try { throw new 地址查找異常("地址 失敗值"); }
        catch (輸入輸出異常 錯誤) { 輸出.寫入行(錯誤.說明()); }
        try { throw new 缺失檔案異常("檔案 失敗值"); }
        catch (java.io.IOException 錯誤) { 輸出.寫入行("표준 상위 異常 호환"); }
        try { 默認超時(); }
        catch (等待狀態超時異常 曾經已捕獲錯誤地) { 輸出.寫入行("잘못된 備用名稱"); }
        catch (java.io.IOException 原始錯誤) { 輸出.寫入行("中文 예외의 독립된 類型分類"); }
        try { 檔案.讀取("없는한글파일"); }
        catch (缺失檔案異常 錯誤) { 輸出.寫入行("檔案 錯誤 中文 轉換值"); }
        try { 字元.解析整數("숫자가아님"); }
        catch (編號格式失敗 錯誤) { 輸出.寫入行("數字值 錯誤 中文 轉換值"); }
        try { 檢查項.確認真值(false, "檢查項 失敗值"); }
        catch (無效實際參數異常 錯誤) { 輸出.寫入行(錯誤.說明()); }
        try { throw new 陣列邊界異常("裁剪 失敗值"); }
        catch (邊界異常 錯誤) { 輸出.寫入行(錯誤.說明()); }
        try { throw new 空引用引用異常("빈 引用"); }
        catch (java.lang.RuntimeException 錯誤) { 輸出.寫入行("執行命令 異常 호환"); }
        try { throw new 異常("직접 정의한 說明"); }
        catch (異常 錯誤) { 輸出.寫入行(錯誤.說明()); }
        try { throw new 執行緒狀態異常("執行緒狀態異常"); }
        catch (執行緒狀態異常 錯誤) { 輸出.寫入行(錯誤.說明()); }
        try { throw new 等待狀態超時異常("等待狀態超時異常"); }
        catch (等待狀態超時異常 錯誤) { 輸出.寫入行(錯誤.說明()); }
        try { throw new 等待狀態已中斷異常("等待狀態已中斷異常"); }
        catch (等待狀態已中斷異常 錯誤) { 輸出.寫入行(錯誤.說明()); }
        try { throw new 字符串邊界異常("字符串邊界異常"); }
        catch (字符串邊界異常 錯誤) { 輸出.寫入行(錯誤.說明()); }
        try { throw new 陣列邊界異常("陣列邊界異常"); }
        catch (陣列邊界異常 錯誤) { 輸出.寫入行(錯誤.說明()); }
        try { throw new 陣列存儲失敗("陣列存儲失敗"); }
        catch (陣列存儲失敗 錯誤) { 輸出.寫入行(錯誤.說明()); }
        try { throw new 邊界異常("邊界異常"); }
        catch (邊界異常 錯誤) { 輸出.寫入行(錯誤.說明()); }
        try { throw new 空引用引用異常("空引用引用異常"); }
        catch (空引用引用異常 錯誤) { 輸出.寫入行(錯誤.說明()); }
        try { throw new 算術失敗("算術失敗"); }
        catch (算術失敗 錯誤) { 輸出.寫入行(錯誤.說明()); }
        try { throw new 狀態異常("狀態異常"); }
        catch (狀態異常 錯誤) { 輸出.寫入行(錯誤.說明()); }
        try { throw new 編號格式失敗("編號格式失敗"); }
        catch (編號格式失敗 錯誤) { 輸出.寫入行(錯誤.說明()); }
        try { throw new 執行狀態異常("執行狀態異常"); }
        catch (執行狀態異常 錯誤) { 輸出.寫入行(錯誤.說明()); }
        try { throw new 異常("異常"); }
        catch (異常 錯誤) { 輸出.寫入行(錯誤.說明()); }
        try { throw new 負數陣列大小失敗("負數陣列大小失敗"); }
        catch (負數陣列大小失敗 錯誤) { 輸出.寫入行(錯誤.說明()); }
        try { throw new 輸入輸出異常("輸入輸出異常"); }
        catch (輸入輸出異常 錯誤) { 輸出.寫入行(錯誤.說明()); }
        try { throw new 無效實際參數異常("無效實際參數異常"); }
        catch (無效實際參數異常 錯誤) { 輸出.寫入行(錯誤.說明()); }
        try { throw new 地址查找異常("地址查找異常"); }
        catch (地址查找異常 錯誤) { 輸出.寫入行(錯誤.說明()); }
        try { throw new 通信異常("通信異常"); }
        catch (通信異常 錯誤) { 輸出.寫入行(錯誤.說明()); }
        try { throw new 缺失檔案異常("缺失檔案異常"); }
        catch (缺失檔案異常 錯誤) { 輸出.寫入行(錯誤.說明()); }
        try { throw new 類型類型轉換異常("類型類型轉換異常"); }
        catch (類型類型轉換異常 錯誤) { 輸出.寫入行(錯誤.說明()); }
        輸出.寫入行("中文 異常 程序值條目 是否完成");
    }
}
