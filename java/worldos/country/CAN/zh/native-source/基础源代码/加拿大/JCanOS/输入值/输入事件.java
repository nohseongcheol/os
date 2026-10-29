// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 加拿大.JCanOS.输入值;

public final class 输入事件 {
    public enum 种类值 {
        键向下,
        键向上,
        鼠标移动量,
        鼠标按钮已按下,
        鼠标按钮已释放
    }

    private final 种类值 事件种类;
    private final int 首位值;
    private final int 第二值;

    public 输入事件(种类值 事件种类, int 首位值, int 第二值) {
        this.事件种类 = 事件种类;
        this.首位值 = 首位值;
        this.第二值 = 第二值;
    }

    public 种类值 事件种类() {
        return 事件种类;
    }

    public int 首位值() {
        return 首位值;
    }

    public int 第二值() {
        return 第二值;
    }
}

