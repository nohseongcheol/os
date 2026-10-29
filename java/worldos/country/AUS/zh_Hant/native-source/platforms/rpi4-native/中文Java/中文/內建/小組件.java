// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中文.內建;
/** 建立中文 API 畫面元件的便利方法。 */
public final class 小組件 {
    private 小組件() {}
    public static void 調用稍後(可運行任務任務 任務動作) { 事件排隊.調用稍後(任務動作); }
    public static 標籤 標籤值(String 文本, int 水平位置, int 垂直位置, int 寬度跨度, int 高度值) {
        return new 標籤(文本, 水平位置, 垂直位置, 寬度跨度, 高度值);
    }
    public static 按鈕 按鈕(String 文本, int 水平位置, int 垂直位置, int 寬度跨度, int 高度值, 動作接收者 接收者值) {
        return new 按鈕(文本, 水平位置, 垂直位置, 寬度跨度, 高度值, 接收者值);
    }
    public static 文本字段 文本字段(String 文本, int 水平位置, int 垂直位置, int 寬度跨度, int 高度值) {
        return new 文本字段(文本, 水平位置, 垂直位置, 寬度跨度, 高度值);
    }
}
