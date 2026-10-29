// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 日本語.内蔵;

/** 実行例と試験で、期待する条件が満たされることを確認する。 */
public final class 検査項目 {
    private 検査項目() {}
    public static void 真偽確認(boolean 条件, String 原因値) {
        if (!条件) throw new 無効引数例外(原因値);
    }
}
