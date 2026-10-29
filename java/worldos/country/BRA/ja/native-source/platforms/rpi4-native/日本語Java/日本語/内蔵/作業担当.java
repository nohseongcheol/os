// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 日本語.内蔵;
/** 独自 JVM のスケジューラーが管理する実行の流れ。標準 Thread は包まない。 */
public final class 作業担当 {
    public 作業担当(実行可能処理作業 作業動作) {
        throw new 状況例外("自前の JVM に日本語 API の実行の流れを作成する機能が必要です。");
    }
    public native void 作業開始処理() throws スレッド状況例外;
    public native void 待機() throws 待合中断済み例外;
    public native boolean 判定稼働中();
    public static native void 作業実行権譲渡();
}
