// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ভাৰত.JIndOS.কাৰ্ণেল;

import ভাৰত.JIndOS.기억공간.মেম_ৰি_মেনেজাৰ;
import ভাৰত.JIndOS.기억공간.পৃষ্ঠা_মেনেজাৰ;
import ভাৰত.JIndOS.입력.입력관리자;
import ভাৰত.JIndOS.작업.প্ৰক্ৰিয়া_মান;
import ভাৰত.JIndOS.작업.অনুসূচক;
import ভাৰত.JIndOS.체계호출.체계호출;
import ভাৰত.JIndOS.ফাইল_ছিষ্টেম.파일서술자표;
import ভাৰত.JIndOS.ফাইল_ছিষ্টেম.ফাইল_ছিষ্টেম;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class কাৰ্ণেল {
    private final 하드웨어 চেলফোন_মান;
    private final মেম_ৰি_মেনেজাৰ 기억공간 = new মেম_ৰি_মেনেজাৰ(32 * 1024 * 1024);
    private final পৃষ্ঠা_মেনেজাৰ 쪽관리 = new পৃষ্ঠা_মেনেজাৰ();
    private final ফাইল_ছিষ্টেম ফাইল_ছিষ্টেম = new ফাইল_ছিষ্টেম();
    private final অনুসূচক অনুসূচক = new অনুসূচক(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final প্ৰক্ৰিয়া_মান 첫과정;
    private final 체계호출 체계호출;

    public কাৰ্ণেল(하드웨어 চেলফোন_মান) {
        this.চেলফোন_মান = চেলফোন_মান;
        첫과정 = অনুসূচক.첫과정(new 파일서술자표(ফাইল_ছিষ্টেম));
        체계호출 = new 체계호출(ফাইল_ছিষ্টেম, 쪽관리, অনুসূচক, চেলফোন_মান, 입력관리);
    }

    public void সঞ্চালন() {
        চেলফোন_মান.직렬출력("=== JIndOS 관리 কাৰ্ণেল_মান ===\n");
    }

    public void 한단계실행() {
        চেলফোন_মান.중앙처리장치멈춤();
    }

    public মেম_ৰি_মেনেজাৰ 기억공간() {
        return 기억공간;
    }

    public পৃষ্ঠা_মেনেজাৰ 쪽관리() {
        return 쪽관리;
    }

    public ফাইল_ছিষ্টেম ফাইল_ছিষ্টেম() {
        return ফাইল_ছিষ্টেম;
    }

    public অনুসূচক অনুসূচক() {
        return অনুসূচক;
    }

    public 입력관리자 입력관리() {
        return 입력관리;
    }

    public প্ৰক্ৰিয়া_মান 첫과정() {
        return 첫과정;
    }

    public 체계호출 체계호출() {
        return 체계호출;
    }
}
