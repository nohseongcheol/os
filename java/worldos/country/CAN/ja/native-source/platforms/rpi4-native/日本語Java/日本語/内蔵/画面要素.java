// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 日本語.内蔵;
/** 独自 JVM の画面オブジェクトに共通する契約。標準 Swing オブジェクトは保持しない。 */
public abstract class 画面要素 {
    public native String 本文読取();
    public native void 本文書込(String 文);
    public native void 境界設定(int 水平位置, int 垂直位置, int 幅跨域, int 高さ値);
}
