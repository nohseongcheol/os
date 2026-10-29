// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中文.内置;

/** 检查示例和测试是否满足预期条件。 */
public final class 检查项 {
    private 检查项() {}
    public static void 确认真值(boolean 条件, String 原因值) {
        if (!条件) throw new 无效参数异常(原因值);
    }
}
