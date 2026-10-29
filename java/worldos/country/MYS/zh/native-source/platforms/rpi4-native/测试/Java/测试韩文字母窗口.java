// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 中文.内置.窗口;
import 中文.内置.小组件;
import 中文.内置.*;

public class 测试韩文字母窗口 implements 可运行任务任务, 动作接收者 {
    窗口 屏幕;
    标签 指南;
    文本字段 输入值;
    public void 执行任务() {
        检查项.确认真值(事件排队.是否事件分派中(), "中文 屏幕 任务 큐");
        屏幕 = new 窗口("中文 库 窗口", 400, 280);
        指南 = 小组件.标签值("한글로 Java 코딩", 20, 20, 340, 30);
        输入值 = 小组件.文本字段("名称", 20, 65, 340, 30);
        屏幕.添加元素(指南);
        屏幕.添加元素(输入值);
        屏幕.添加元素(小组件.按钮("问候", 20, 110, 180, 32, this));
        屏幕.显示窗口();
        输出.写入行("KOREAN SWING READY");
    }
    public void 接收动作(动作通知 事件) {
        检查项.确认真值(事件排队.是否事件分派中(), "中文 动作 되부름");
        检查项.确认真值(事件.编号() == 1001 && 事件.事件源代码() instanceof 按钮, "中文 事件 객체와 原点值");
        检查项.确认真值(!((Object)事件.事件源代码() instanceof javax.swing.JButton), "표준 단추와 독립된 格式值");
        检查项.确认真值(!((Object)事件 instanceof java.awt.event.ActionEvent), "표준 사건과 독립된 格式值");
        指南.写入文本("안녕하세요 " + 输入值.读取文本());
        输出.写入行("KOREAN SWING CLICK " + 输入值.读取文本());
    }
    public static void main(String[] 实参) {
        事件排队.调用稍后(new 测试韩文字母窗口());
    }
}
