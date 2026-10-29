// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 Java 工具專用的 SVC 橋接，與現有 x86 工具原始碼一同建置。 */
public final class 使用者 {
    public static native int 打開檔案描述符(int[] 名稱, int 設置);
    public static native int 讀取一檔案位元組(int 描述符條目);
    public static native int 寫入一檔案位元組(int 描述符條目, int 值);
    public static native int 關閉檔案描述符(int 描述符條目);
    public static native int 讀取檔案(int[] 名稱, int[] 資料);
    public static native int 寫入檔案(int[] 名稱, int[] 資料, int 長度);
    public static native int 寫入(String 文本);
    public static native int 寫入字元值(int 值);
    public static native int 參數列個數();
    public static native String 實參(int 編號);
    public static native int 工具編號();
    public static native int 屏幕連接狀態(int 動作, int 編號, int 首位操作數, int 第二操作數, int 第三操作數, int 第四操作數);
    public static native int 屏幕文本(int 編號, int[] 文本, int 長度);
    public static native int 屏幕寬度();
    public static native int 屏幕高度();
    public static native int 流控制(int 動作, int 描述符條目, int 值);
    public static native int 連接流(int 描述符條目, int 地址, int 埠值);
    public static native int 打開網路(int 埠值);
    public static native int 發送網路(int 描述符條目, int 地址, int 埠值, int[] 資料, int 長度);
    public static native int 接收網路(int 描述符條目, int[] 資料, int 長度);
    public static native int 網路埠(int 描述符條目);
    public static native int 毫秒();
    public static native int 等待狀態用於映像();
    public static native int 矩形(int 水平位置, int 垂直位置, int 寬度跨度, int 高度值, int 顏色值);
}
