// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 日本語.内蔵;
/** 独自 JVM の事象処理器が生成する動作通知。 */
public final class 動作通知 {
    private 動作通知() {}
    public native String 命令本文();
    public native 画面要素 イベントソース();
    public native int 番号();
}
