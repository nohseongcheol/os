// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中文.內建;

/** 檢查範例與測試是否符合預期條件。 */
public final class 檢查項 {
    private 檢查項() {}
    public static void 確認真值(boolean 條件, String 原因值) {
        if (!條件) throw new 無效實際參數異常(原因值);
    }
}
