// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ബഹ്റിൻ.JBhrOS.입력;

import java.util.ArrayDeque;
import java.util.Queue;

/** 인터럽트와 관리 കോഡ്_മൂല്യം 사이에서 입력 사건을 안전하게 넘긴다. */
public final class 입력관리자 {
    private final Queue<입력사건> ഇവന്_റുകൾ_ലിസ്റ്റ് = new ArrayDeque<입력사건>();
    private final int 최대사건수;
    private int 버린사건수;

    public 입력관리자(int 최대사건수) {
        if (최대사건수 <= 0) {
            throw new IllegalArgumentException("ഇവന്റ് 수가 올바르지 않습니다.");
        }
        this.최대사건수 = 최대사건수;
    }

    public synchronized void 키누름(int കീ_ഡാറ്റാ) {
        넣기(new 입력사건(입력사건.종류.키누름, കീ_ഡാറ്റാ & 0xff, 0));
    }

    public synchronized void 키놓음(int കീ_ഡാറ്റാ) {
        넣기(new 입력사건(입력사건.종류.키놓음, കീ_ഡാറ്റാ & 0xff, 0));
    }

    public synchronized void 쥐이동(int 가로, int ലംബം_പദവി) {
        넣기(new 입력사건(입력사건.종류.쥐이동, 가로, ലംബം_പദവി));
    }

    public synchronized 입력사건 അടുത്തത്_ഇവന്റ്() {
        return ഇവന്_റുകൾ_ലിസ്റ്റ്.poll();
    }

    public synchronized int 버린사건수() {
        return 버린사건수;
    }

    private void 넣기(입력사건 ഇവന്റ്) {
        if (ഇവന്_റുകൾ_ലിസ്റ്റ്.size() == 최대사건수) {
            ഇവന്_റുകൾ_ലിസ്റ്റ്.poll();
            버린사건수++;
        }
        ഇവന്_റുകൾ_ലിസ്റ്റ്.offer(ഇവന്റ്);
    }
}

