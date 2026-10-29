// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package કેનેડા.JCanOS.입력;

import java.util.ArrayDeque;
import java.util.Queue;

/** 인터럽트와 관리 코드 사이에서 입력 사건을 안전하게 넘긴다. */
public final class 입력관리자 {
    private final Queue<입력사건> ધટનાઓ_સૂચી = new ArrayDeque<입력사건>();
    private final int 최대사건수;
    private int 버린사건수;

    public 입력관리자(int 최대사건수) {
        if (최대사건수 <= 0) {
            throw new IllegalArgumentException("ઇવેંટ 수가 올바르지 않습니다.");
        }
        this.최대사건수 = 최대사건수;
    }

    public synchronized void 키누름(int કી_ડેટા) {
        넣기(new 입력사건(입력사건.종류.키누름, કી_ડેટા & 0xff, 0));
    }

    public synchronized void 키놓음(int કી_ડેટા) {
        넣기(new 입력사건(입력사건.종류.키놓음, કી_ડેટા & 0xff, 0));
    }

    public synchronized void 쥐이동(int 가로, int ઊભી_સ્થિતિ) {
        넣기(new 입력사건(입력사건.종류.쥐이동, 가로, ઊભી_સ્થિતિ));
    }

    public synchronized 입력사건 આગલું_ઇવેંટ() {
        return ધટનાઓ_સૂચી.poll();
    }

    public synchronized int 버린사건수() {
        return 버린사건수;
    }

    private void 넣기(입력사건 ઇવેંટ) {
        if (ધટનાઓ_સૂચી.size() == 최대사건수) {
            ધટનાઓ_સૂચી.poll();
            버린사건수++;
        }
        ધટનાઓ_સૂચી.offer(ઇવેંટ);
    }
}

