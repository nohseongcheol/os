// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 中文.內建.窗口;
import 中文.內建.標籤;
import 中文.內建.文本字段;
import 中文.內建.按鈕;
import 中文.內建.事件排隊;
import 中文.內建.輸出;
import 中文.內建.可運行任務任務;
import 中文.內建.動作接收者;
import 中文.內建.動作通知;

/** 獨立核心上的 Swing 視窗：輸入中文、按下按鈕、更新提示標籤。 */
public class 窗口例 implements 可運行任務任務, 動作接收者 {
    private 窗口 問候語窗口;
    private 文本字段 名稱字段;
    private 標籤 問候語;
    private int 問候語個數;

    public void 打開窗口() {
        問候語窗口 = new 窗口("zh_Hant Swing", 460, 300);
        問候語窗口.添加元素(new 標籤("您好", 20, 20, 420, 28));
        名稱字段 = new 文本字段("zh_Hant", 20, 64, 420, 30);
        問候語 = new 標籤("您好", 20, 152, 420, 28);
        問候語窗口.添加元素(名稱字段);
        問候語窗口.添加元素(new 按鈕("問候", 20, 108, 180, 32, this));
        問候語窗口.添加元素(問候語);
        問候語窗口.添加元素(new 標籤("F9 / Shift+Space | X", 20, 204, 420, 28));
        問候語窗口.顯示窗口();
        輸出.寫入行("GUI 範例 準備: 窗口例");
    }

    public void 問候() {
        問候語個數++;
        問候語.寫入文本("您好, " + 名稱字段.讀取文本() + "님! (" + 問候語個數 + ")");
        輸出.寫入行("GUI 問候例: " + 問候語.讀取文本());
    }

    public void 執行任務() { 打開窗口(); }
    public void 接收動作(動作通知 通知) {
        輸出.寫入行("動作 通知: " + 通知.命令文本());
        問候();
    }
    public static void 運行() {
        事件排隊.調用稍後(new 窗口例());
    }
}
