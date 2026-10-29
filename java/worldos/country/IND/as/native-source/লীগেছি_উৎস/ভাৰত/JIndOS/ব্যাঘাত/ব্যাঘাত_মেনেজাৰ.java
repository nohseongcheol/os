// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ভাৰত.JIndOS.ব্যাঘাত;

import java.util.Arrays;

/** IDT의 Java 관리 측 처리기 등록과 분배를 담당한다. */
public final class ব্যাঘাত_মেনেজাৰ {
    private final 개입중단처리기[] 처리기들 = new 개입중단처리기[256];
    private boolean সক্ৰিয়;

    public void পঞ্জীয়ন_কৰক_প্রবিষ্ট(int ইনডেক্স, 개입중단처리기 처리기) {
        번호확인(ইনডেক্স);
        처리기들[ইনডেক্স] = 처리기;
    }

    public void ৰিলিজ_ষ্ট_ৰেজ(int ইনডেক্স) {
        번호확인(ইনডেক্স);
        처리기들[ইনডেক্স] = null;
    }

    public int বিতৰণ_কৰক_মান(int ইনডেক্স, int 저장된쌓임주소) {
        번호확인(ইনডেক্স);
        if (!সক্ৰিয়) {
            return 저장된쌓임주소;
        }
        개입중단처리기 처리기 = 처리기들[ইনডেক্স];
        return 처리기 == null ? 저장된쌓임주소 : 처리기.প্ৰক্ৰিয়া_মান_প্রবিষ্ট(저장된쌓임주소);
    }

    public void সক্ষম_কৰক() {
        সক্ৰিয় = true;
    }

    public void অসক্ৰিয়_কৰক() {
        সক্ৰিয় = false;
    }

    public boolean 활성인가() {
        return সক্ৰিয়;
    }

    public void 모두해제() {
        Arrays.fill(처리기들, null);
    }

    private void 번호확인(int ইনডেক্স) {
        if (ইনডেক্স < 0 || ইনডেক্স >= 처리기들.length) {
            throw new IllegalArgumentException("ব্যাঘাত 번호가 올바르지 않습니다.");
        }
    }
}

