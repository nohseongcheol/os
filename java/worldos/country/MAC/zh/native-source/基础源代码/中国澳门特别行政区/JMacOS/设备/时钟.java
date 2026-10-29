// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中国澳门特别行政区.JMacOS.设备;

/** 管理 PIT 时钟滴答和抢占时机。 */
public final class 时钟 {
    private final int 时钟滴答数每第二;
    private long 时钟周期个数;

    public 时钟(int 时钟滴答数每第二) {
        if (时钟滴答数每第二 <= 0) {
            throw new IllegalArgumentException("초당 时钟周期值 수가 올바르지 않습니다.");
        }
        this.时钟滴答数每第二 = 时钟滴答数每第二;
    }

    public long 时钟周期值() {
        return ++时钟周期个数;
    }

    public long 时钟周期个数() {
        return 时钟周期个数;
    }

    public long 已过时间毫秒() {
        return 时钟周期个数 * 1000L / 时钟滴答数每第二;
    }
}

