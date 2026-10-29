// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Việt_Nam.JVnmOS.ThiếtBị;

/** Quản lý nhịp PIT và thời điểm thu hồi quyền chạy. */
public final class ĐồngHồ {
    private final int thứHaiMỗiCácNhịp;
    private long sốLượngNhịp;

    public ĐồngHồ(int thứHaiMỗiCácNhịp) {
        if (thứHaiMỗiCácNhịp <= 0) {
            throw new IllegalArgumentException("초당 giáTrịNhịp 수가 올바르지 않습니다.");
        }
        this.thứHaiMỗiCácNhịp = thứHaiMỗiCácNhịp;
    }

    public long giáTrịNhịp() {
        return ++sốLượngNhịp;
    }

    public long sốLượngNhịp() {
        return sốLượngNhịp;
    }

    public long miliGiâyĐãTrôi() {
        return sốLượngNhịp * 1000L / thứHaiMỗiCácNhịp;
    }
}

