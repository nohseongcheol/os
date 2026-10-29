// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中文.内置;
/** 创建中文 API 界面组件的便捷方法。 */
public final class 小组件 {
    private 小组件() {}
    public static void 调用稍后(可运行任务任务 任务动作) { 事件排队.调用稍后(任务动作); }
    public static 标签 标签值(String 文本, int 水平位置, int 垂直位置, int 宽度跨度, int 高度值) {
        return new 标签(文本, 水平位置, 垂直位置, 宽度跨度, 高度值);
    }
    public static 按钮 按钮(String 文本, int 水平位置, int 垂直位置, int 宽度跨度, int 高度值, 动作接收者 接收者值) {
        return new 按钮(文本, 水平位置, 垂直位置, 宽度跨度, 高度值, 接收者值);
    }
    public static 文本字段 文本字段(String 文本, int 水平位置, int 垂直位置, int 宽度跨度, int 高度值) {
        return new 文本字段(文本, 水平位置, 垂直位置, 宽度跨度, 高度值);
    }
}
