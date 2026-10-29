// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中文.內建;
/** 將待執行工作交給自製畫面的事件佇列。 */
public final class 事件排隊 {
    private 事件排隊() {}
    public static native void 調用稍後(可運行任務任務 任務動作);
    public static native boolean 是否事件分派中();
}
