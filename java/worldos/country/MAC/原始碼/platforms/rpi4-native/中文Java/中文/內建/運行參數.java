// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中文.內建;
/** 自製 JVM 傳給進入方法的命令列引數，不包含類別名稱。 */
public final class 運行參數 {
    private 運行參數() {}
    public static native int 項目個數();
    public static native String 文本(int 序數索引) throws 邊界異常;
}
