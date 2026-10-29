// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package カナダ.JCanOS.装置;

/** PIT 層の刻みと実行権を取り上げる時機を管理する。 */
public final class 時計 {
    private final int 刻み数単位当り第二;
    private long 刻み個数;

    public 時計(int 刻み数単位当り第二) {
        if (刻み数単位当り第二 <= 0) {
            throw new IllegalArgumentException("초당 刻み値 수가 올바르지 않습니다.");
        }
        this.刻み数単位当り第二 = 刻み数単位当り第二;
    }

    public long 刻み値() {
        return ++刻み個数;
    }

    public long 刻み個数() {
        return 刻み個数;
    }

    public long 経過ミリ秒() {
        return 刻み個数 * 1000L / 刻み数単位当り第二;
    }
}

