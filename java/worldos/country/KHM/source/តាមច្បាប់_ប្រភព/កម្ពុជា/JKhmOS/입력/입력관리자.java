// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package កម្ពុជា.JKhmOS.입력;

import java.util.ArrayDeque;
import java.util.Queue;

/** 인터럽트와 관리 កូដ_តំលៃ 사이에서 입력 사건을 안전하게 넘긴다. */
public final class 입력관리자 {
    private final Queue<입력사건> ព្រឹត្តិការណ៍_បញ្ជី = new ArrayDeque<입력사건>();
    private final int 최대사건수;
    private int 버린사건수;

    public 입력관리자(int 최대사건수) {
        if (최대사건수 <= 0) {
            throw new IllegalArgumentException("ព្រឹត្តិការណ៍ 수가 올바르지 않습니다.");
        }
        this.최대사건수 = 최대사건수;
    }

    public synchronized void 키누름(int ឃី_ទិន្នន័យ) {
        넣기(new 입력사건(입력사건.종류.키누름, ឃី_ទិន្នន័យ & 0xff, 0));
    }

    public synchronized void 키놓음(int ឃី_ទិន្នន័យ) {
        넣기(new 입력사건(입력사건.종류.키놓음, ឃី_ទិន្នន័យ & 0xff, 0));
    }

    public synchronized void 쥐이동(int 가로, int បញ្ឈរ_កំណត់ទីតាំង) {
        넣기(new 입력사건(입력사건.종류.쥐이동, 가로, បញ្ឈរ_កំណត់ទីតាំង));
    }

    public synchronized 입력사건 បន្ទាប់_ព្រឹត្តិការណ៍() {
        return ព្រឹត្តិការណ៍_បញ្ជី.poll();
    }

    public synchronized int 버린사건수() {
        return 버린사건수;
    }

    private void 넣기(입력사건 ព្រឹត្តិការណ៍) {
        if (ព្រឹត្តិការណ៍_បញ្ជី.size() == 최대사건수) {
            ព្រឹត្តិការណ៍_បញ្ជី.poll();
            버린사건수++;
        }
        ព្រឹត្តិការណ៍_បញ្ជី.offer(ព្រឹត្តិការណ៍);
    }
}

