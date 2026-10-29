// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 越南.JVnmOS.設備;

/** 管理 PIT 時脈刻度與搶先執行時機。 */
public final class 時鐘 {
    private final int 時鐘滴答數每第二;
    private long 時鐘週期個數;

    public 時鐘(int 時鐘滴答數每第二) {
        if (時鐘滴答數每第二 <= 0) {
            throw new IllegalArgumentException("초당 時鐘週期值 수가 올바르지 않습니다.");
        }
        this.時鐘滴答數每第二 = 時鐘滴答數每第二;
    }

    public long 時鐘週期值() {
        return ++時鐘週期個數;
    }

    public long 時鐘週期個數() {
        return 時鐘週期個數;
    }

    public long 已過時間毫秒() {
        return 時鐘週期個數 * 1000L / 時鐘滴答數每第二;
    }
}

