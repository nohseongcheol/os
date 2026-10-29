// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 蘇利南.JSurOS.輸入值;

public final class 輸入事件 {
    public enum 種類值 {
        鍵向下,
        鍵向上,
        鼠標移動量,
        鼠標按鈕已按下,
        鼠標按鈕已釋放
    }

    private final 種類值 事件種類;
    private final int 首位值;
    private final int 第二值;

    public 輸入事件(種類值 事件種類, int 首位值, int 第二值) {
        this.事件種類 = 事件種類;
        this.首位值 = 首位值;
        this.第二值 = 第二值;
    }

    public 種類值 事件種類() {
        return 事件種類;
    }

    public int 首位值() {
        return 首位值;
    }

    public int 第二值() {
        return 第二值;
    }
}

