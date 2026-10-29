// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package カナダ.JCanOS.入力値;

public final class 入力イベント {
    public enum 種別値 {
        キー下方,
        キー上方,
        マウス移動量,
        マウスボタン押下済み,
        マウスボタン解放済み
    }

    private final 種別値 イベント種別;
    private final int 先頭位置値;
    private final int 第二値;

    public 入力イベント(種別値 イベント種別, int 先頭位置値, int 第二値) {
        this.イベント種別 = イベント種別;
        this.先頭位置値 = 先頭位置値;
        this.第二値 = 第二値;
    }

    public 種別値 イベント種別() {
        return イベント種別;
    }

    public int 先頭位置値() {
        return 先頭位置値;
    }

    public int 第二値() {
        return 第二値;
    }
}

