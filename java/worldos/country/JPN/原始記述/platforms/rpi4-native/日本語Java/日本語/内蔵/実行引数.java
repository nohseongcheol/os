// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 日本語.内蔵;
/** 独自 JVM が入口メソッドへ渡す命令行引数。クラス名は含めない。 */
public final class 実行引数 {
    private 実行引数() {}
    public static native int 項目個数();
    public static native String 文(int 序数添字) throws 境界例外;
}
