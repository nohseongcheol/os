// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 日本語.内蔵;
/** 独自 JVM が接続する固定 ABI。JNI や任意の native メソッドの読込み器ではない。 */
public final class 中核値 {
    private 中核値() {}
    public static native int ミリ秒();
    public static native int 対象イメージ待合();
    public static native int 画面幅();
    public static native int 画面高さ();
    public static native int 矩形(int 水平位置, int 垂直位置, int 幅跨域, int 高さ値, int 色値);
}
