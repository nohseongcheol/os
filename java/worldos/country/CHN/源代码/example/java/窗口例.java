// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 中文.内置.窗口;
import 中文.内置.标签;
import 中文.内置.文本字段;
import 中文.内置.按钮;
import 中文.内置.事件排队;
import 中文.内置.输出;
import 中文.内置.可运行任务任务;
import 中文.内置.动作接收者;
import 中文.内置.动作通知;

/** 独立内核上的 Swing 窗口：输入中文、点击按钮、更新提示标签。 */
public class 窗口例 implements 可运行任务任务, 动作接收者 {
    private 窗口 问候语窗口;
    private 文本字段 名称字段;
    private 标签 问候语;
    private int 问候语个数;

    public void 打开窗口() {
        问候语窗口 = new 窗口("Chinese Swing", 460, 300);
        问候语窗口.添加元素(new 标签("你好", 20, 20, 420, 28));
        名称字段 = new 文本字段("Chinese", 20, 64, 420, 30);
        问候语 = new 标签("你好", 20, 152, 420, 28);
        问候语窗口.添加元素(名称字段);
        问候语窗口.添加元素(new 按钮("问候", 20, 108, 180, 32, this));
        问候语窗口.添加元素(问候语);
        问候语窗口.添加元素(new 标签("F9 / Shift+Space | X", 20, 204, 420, 28));
        问候语窗口.显示窗口();
        输出.写入行("GUI 用例 准备: 窗口例");
    }

    public void 问候() {
        问候语个数++;
        问候语.写入文本("你好, " + 名称字段.读取文本() + "님! (" + 问候语个数 + ")");
        输出.写入行("GUI 问候例: " + 问候语.读取文本());
    }

    public void 执行任务() { 打开窗口(); }
    public void 接收动作(动作通知 通知) {
        输出.写入行("动作 通知: " + 通知.命令文本());
        问候();
    }
    public static void 运行() {
        事件排队.调用稍后(new 窗口例());
    }
}
