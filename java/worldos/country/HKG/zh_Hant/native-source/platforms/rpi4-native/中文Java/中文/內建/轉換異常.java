// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中文.內建;

/** 在中文 API 邊界轉換標準 Java 錯誤，不改變標準 catch 子句的含義。 */
final class 轉換異常 {
    private 轉換異常() {}
    public static 輸入輸出異常 輸入輸出(java.io.IOException 錯誤) {
        if (錯誤 instanceof 輸入輸出異常) return (輸入輸出異常)錯誤;
        if (錯誤 instanceof java.net.SocketTimeoutException) return new 等待狀態超時異常("通訊等待逾時。");
        if (錯誤 instanceof java.net.UnknownHostException) return new 地址查找異常("無法解析位址。目前請使用數字形式的 IPv4 位址。");
        if (錯誤 instanceof java.io.FileNotFoundException) return new 缺失檔案異常("無法開啟檔案。");
        if (錯誤 instanceof java.net.SocketException) return new 通信異常("通訊連線操作失敗: " + 錯誤.getMessage());
        return new 輸入輸出異常("輸入輸出操作失敗: " + 錯誤.getMessage());
    }
    public static RuntimeException 執行命令(RuntimeException 錯誤) {
        if (錯誤 instanceof java.lang.NumberFormatException) return new 編號格式失敗("請檢查數字格式和範圍。");
        if (錯誤 instanceof java.lang.IllegalArgumentException) return new 無效實際參數異常("請檢查引數的值和範圍。");
        if (錯誤 instanceof java.lang.ArrayIndexOutOfBoundsException) return new 陣列邊界異常("超出陣列範圍。");
        if (錯誤 instanceof java.lang.StringIndexOutOfBoundsException) return new 字符串邊界異常("超出字串範圍。");
        if (錯誤 instanceof java.lang.IndexOutOfBoundsException) return new 邊界異常("超出允許範圍。");
        if (錯誤 instanceof java.lang.NullPointerException) return new 空引用引用異常("參照為空。");
        return new 執行狀態異常(錯誤.getMessage());
    }
}
