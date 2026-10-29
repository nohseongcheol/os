// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Việt_Nam.JVnmOS.giáTrịVào;

import java.util.ArrayDeque;
import java.util.Queue;

/** Chuyển sự kiện đầu vào an toàn giữa ngắt và mã được quản lý. */
public final class BộQuảnLýĐầuVào {
    private final Queue<sựKiệnĐầuVào> danhSáchCácSựKiện = new ArrayDeque<sựKiệnĐầuVào>();
    private final int sốLượngSựKiệnTốiĐa;
    private int sốLượngSựKiệnĐãBỏ;

    public BộQuảnLýĐầuVào(int sốLượngSựKiệnTốiĐa) {
        if (sốLượngSựKiệnTốiĐa <= 0) {
            throw new IllegalArgumentException("sựKiện 수가 올바르지 않습니다.");
        }
        this.sốLượngSựKiệnTốiĐa = sốLượngSựKiệnTốiĐa;
    }

    public synchronized void xuốngPhím(int dữLiệuPhím) {
        đặtGiáTrị(new sựKiệnĐầuVào(sựKiệnĐầuVào.giáTrịLoại.xuốngPhím, dữLiệuPhím & 0xff, 0));
    }

    public synchronized void lênPhím(int dữLiệuPhím) {
        đặtGiáTrị(new sựKiệnĐầuVào(sựKiệnĐầuVào.giáTrịLoại.lênPhím, dữLiệuPhím & 0xff, 0));
    }

    public synchronized void chuyểnĐộngChuột(int vịTríNgang, int vịTríDọc) {
        đặtGiáTrị(new sựKiệnĐầuVào(sựKiệnĐầuVào.giáTrịLoại.chuyểnĐộngChuột, vịTríNgang, vịTríDọc));
    }

    public synchronized sựKiệnĐầuVào sựKiệnKếTiếp() {
        return danhSáchCácSựKiện.poll();
    }

    public synchronized int sốLượngSựKiệnĐãBỏ() {
        return sốLượngSựKiệnĐãBỏ;
    }

    private void đặtGiáTrị(sựKiệnĐầuVào sựKiện) {
        if (danhSáchCácSựKiện.size() == sốLượngSựKiệnTốiĐa) {
            danhSáchCácSựKiện.poll();
            sốLượngSựKiệnĐãBỏ++;
        }
        danhSáchCácSựKiện.offer(sựKiện);
    }
}

