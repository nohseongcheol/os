// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package नेपाल.JNplOS.입력;

import java.util.ArrayDeque;
import java.util.Queue;

/** 인터럽트와 관리 कोड_मान 사이에서 입력 사건을 안전하게 넘긴다. */
public final class 입력관리자 {
    private final Queue<입력사건> ईवेंट्स_सूची = new ArrayDeque<입력사건>();
    private final int 최대사건수;
    private int 버린사건수;

    public 입력관리자(int 최대사건수) {
        if (최대사건수 <= 0) {
            throw new IllegalArgumentException("घटना 수가 올바르지 않습니다.");
        }
        this.최대사건수 = 최대사건수;
    }

    public synchronized void कुंजी_बंद(int कुंजी_डेटा) {
        넣기(new 입력사건(입력사건.종류.कुंजी_बंद, कुंजी_डेटा & 0xff, 0));
    }

    public synchronized void 키놓음(int कुंजी_डेटा) {
        넣기(new 입력사건(입력사건.종류.키놓음, कुंजी_डेटा & 0xff, 0));
    }

    public synchronized void 쥐이동(int 가로, int अनुलंब_पद) {
        넣기(new 입력사건(입력사건.종류.쥐이동, 가로, अनुलंब_पद));
    }

    public synchronized 입력사건 अगला_घटना() {
        return ईवेंट्स_सूची.poll();
    }

    public synchronized int 버린사건수() {
        return 버린사건수;
    }

    private void 넣기(입력사건 घटना) {
        if (ईवेंट्स_सूची.size() == 최대사건수) {
            ईवेंट्स_सूची.poll();
            버린사건수++;
        }
        ईवेंट्स_सूची.offer(घटना);
    }
}

