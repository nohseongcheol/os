// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 日本語.内蔵;
/** スレッドは一つの実行の流れ。独自 JVM 内で命令数を基準に交互に実行する。 */
public final class 作業 {
    private 作業() {}
    public static 作業担当 起動処理(実行可能処理作業 作業動作) { 作業担当 スレッド値 = new 作業担当(作業動作); スレッド値.作業開始処理(); return スレッド値; }
    public static void 待機(作業担当 スレッド値) throws 待合中断済み例外 { スレッド値.待機(); }
    public static boolean 判定稼働中(作業担当 スレッド値) { return スレッド値.判定稼働中(); }
    public static void 作業実行権譲渡() { 作業担当.作業実行権譲渡(); }
}
