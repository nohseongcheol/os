// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 中文.內建.窗口;
import 中文.內建.小組件;
import 中文.內建.*;

public class 測試韓文字母窗口 implements 可運行任務任務, 動作接收者 {
    窗口 屏幕;
    標籤 指南;
    文本字段 輸入值;
    public void 執行任務() {
        檢查項.確認真值(事件排隊.是否事件分派中(), "中文 屏幕 任務 큐");
        屏幕 = new 窗口("中文 庫 窗口", 400, 280);
        指南 = 小組件.標籤值("한글로 Java 코딩", 20, 20, 340, 30);
        輸入值 = 小組件.文本字段("名稱", 20, 65, 340, 30);
        屏幕.添加元素(指南);
        屏幕.添加元素(輸入值);
        屏幕.添加元素(小組件.按鈕("問候", 20, 110, 180, 32, this));
        屏幕.顯示窗口();
        輸出.寫入行("KOREAN SWING READY");
    }
    public void 接收動作(動作通知 事件) {
        檢查項.確認真值(事件排隊.是否事件分派中(), "中文 動作 되부름");
        檢查項.確認真值(事件.編號() == 1001 && 事件.事件原始碼() instanceof 按鈕, "中文 事件 객체와 原點值");
        檢查項.確認真值(!((Object)事件.事件原始碼() instanceof javax.swing.JButton), "표준 단추와 독립된 格式值");
        檢查項.確認真值(!((Object)事件 instanceof java.awt.event.ActionEvent), "표준 사건과 독립된 格式值");
        指南.寫入文本("안녕하세요 " + 輸入值.讀取文本());
        輸出.寫入行("KOREAN SWING CLICK " + 輸入值.讀取文本());
    }
    public static void main(String[] 實參) {
        事件排隊.調用稍後(new 測試韓文字母窗口());
    }
}
