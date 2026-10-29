// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ଭାରତ.JIndOS.입력;

import java.util.ArrayDeque;
import java.util.Queue;

/** 인터럽트와 관리 코드 사이에서 입력 사건을 안전하게 넘긴다. */
public final class 입력관리자 {
    private final Queue<입력사건> ଇଭେଣ୍ଟସମୂହ_ତାଲିକା = new ArrayDeque<입력사건>();
    private final int 최대사건수;
    private int 버린사건수;

    public 입력관리자(int 최대사건수) {
        if (최대사건수 <= 0) {
            throw new IllegalArgumentException("ଘଟଣା 수가 올바르지 않습니다.");
        }
        this.최대사건수 = 최대사건수;
    }

    public synchronized void 키누름(int କୀ_ଡାଟା) {
        넣기(new 입력사건(입력사건.종류.키누름, କୀ_ଡାଟା & 0xff, 0));
    }

    public synchronized void 키놓음(int କୀ_ଡାଟା) {
        넣기(new 입력사건(입력사건.종류.키놓음, କୀ_ଡାଟା & 0xff, 0));
    }

    public synchronized void 쥐이동(int 가로, int ଅନୁଲମ୍ବ_ସ୍ଥିତି) {
        넣기(new 입력사건(입력사건.종류.쥐이동, 가로, ଅନୁଲମ୍ବ_ସ୍ଥିତି));
    }

    public synchronized 입력사건 ପରବର୍ତ୍ତୀ_ଘଟଣା() {
        return ଇଭେଣ୍ଟସମୂହ_ତାଲିକା.poll();
    }

    public synchronized int 버린사건수() {
        return 버린사건수;
    }

    private void 넣기(입력사건 ଘଟଣା) {
        if (ଇଭେଣ୍ଟସମୂହ_ତାଲିକା.size() == 최대사건수) {
            ଇଭେଣ୍ଟସମୂହ_ତାଲିକା.poll();
            버린사건수++;
        }
        ଇଭେଣ୍ଟସମୂହ_ତାଲିକା.offer(ଘଟଣା);
    }
}

