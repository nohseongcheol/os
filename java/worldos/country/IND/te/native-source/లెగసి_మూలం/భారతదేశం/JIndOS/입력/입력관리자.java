// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package భారతదేశం.JIndOS.입력;

import java.util.ArrayDeque;
import java.util.Queue;

/** 인터럽트와 관리 కోడ్_మూల్యం 사이에서 입력 사건을 안전하게 넘긴다. */
public final class 입력관리자 {
    private final Queue<입력사건> ఈవెంట్లు_జాబితా = new ArrayDeque<입력사건>();
    private final int 최대사건수;
    private int 버린사건수;

    public 입력관리자(int 최대사건수) {
        if (최대사건수 <= 0) {
            throw new IllegalArgumentException("ఈవెంట్ 수가 올바르지 않습니다.");
        }
        this.최대사건수 = 최대사건수;
    }

    public synchronized void 키누름(int కీ_డేటా) {
        넣기(new 입력사건(입력사건.종류.키누름, కీ_డేటా & 0xff, 0));
    }

    public synchronized void 키놓음(int కీ_డేటా) {
        넣기(new 입력사건(입력사건.종류.키놓음, కీ_డేటా & 0xff, 0));
    }

    public synchronized void 쥐이동(int 가로, int నిలువు_స్థాయి) {
        넣기(new 입력사건(입력사건.종류.쥐이동, 가로, నిలువు_స్థాయి));
    }

    public synchronized 입력사건 తదుపరి_ఈవెంట్() {
        return ఈవెంట్లు_జాబితా.poll();
    }

    public synchronized int 버린사건수() {
        return 버린사건수;
    }

    private void 넣기(입력사건 ఈవెంట్) {
        if (ఈవెంట్లు_జాబితా.size() == 최대사건수) {
            ఈవెంట్లు_జాబితా.poll();
            버린사건수++;
        }
        ఈవెంట్లు_జాబితా.offer(ఈవెంట్);
    }
}

