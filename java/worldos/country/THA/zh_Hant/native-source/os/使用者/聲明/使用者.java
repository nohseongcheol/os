// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros 使用者 ELF 專用 API，不是 Linux/JVM 的 JNI 或 java.net API。 */
public final class 使用者 {
    public static native int 打開檔案描述符(int[] 檔案條目名稱, int 打開設置);
    public static native int 讀取一檔案位元組(int 檔案描述符);
    public static native int 寫入一檔案位元組(int 檔案描述符, int 位元組值);
    public static native int 關閉檔案描述符(int 檔案描述符);
    public static native int 提交檔案存儲裝置(int 檔案描述符);
    public static native int 讀取檔案(int[] 名稱, int[] 資料);
    public static native int 寫入字元值(int 字元);
    public static native int 寫入檔案(int[] 名稱, int[] 資料, int 長度);
    public static native int 寫入(String 內容值);
    public static native int 參數列個數();
    public static native String 實參(int 編號);
    public static native int 執行狀態權限();
    public static native int 打開網路(int 局部埠);
    public static native int 發送資料(int 句柄值, int 地址, int 目的地址埠, int[] 資料, int 長度);
    public static native int 接收資料(int 句柄值, int[] 資料, int 限制毫秒);
    public static native int 關閉網路(int 句柄值);
    public static native int 自有對象地址();
    public static native int 已發送地址(int 句柄值);
    public static native int 已發送埠(int 句柄值);
}
