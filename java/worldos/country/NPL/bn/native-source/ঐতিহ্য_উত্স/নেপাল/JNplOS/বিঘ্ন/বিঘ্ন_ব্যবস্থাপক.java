// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package নেপাল.JNplOS.বিঘ্ন;

import java.util.Arrays;

/** IDT의 Java 관리 측 처리기 등록과 분배를 담당한다. */
public final class বিঘ্ন_ব্যবস্থাপক {
    private final 개입중단처리기[] 처리기들 = new 개입중단처리기[256];
    private boolean হাজির;

    public void নিবন্ধন_করুন_ভুক্তি(int সূচি, 개입중단처리기 처리기) {
        번호확인(সূচি);
        처리기들[সূচি] = 처리기;
    }

    public void রিলিজ_স্টোরেজ(int সূচি) {
        번호확인(সূচি);
        처리기들[সূচি] = null;
    }

    public int বিতরণ_মান(int সূচি, int 저장된쌓임주소) {
        번호확인(সূচি);
        if (!হাজির) {
            return 저장된쌓임주소;
        }
        개입중단처리기 처리기 = 처리기들[সূচি];
        return 처리기 == null ? 저장된쌓임주소 : 처리기.প্রসেসর_মান_ভুক্তি(저장된쌓임주소);
    }

    public void চালু_করুন() {
        হাজির = true;
    }

    public void নিষ্ক্রিয়() {
        হাজির = false;
    }

    public boolean তথ্য_প্রযুক্তি_হাজির() {
        return হাজির;
    }

    public void 모두해제() {
        Arrays.fill(처리기들, null);
    }

    private void 번호확인(int সূচি) {
        if (সূচি < 0 || সূচি >= 처리기들.length) {
            throw new IllegalArgumentException("বিঘ্ন 번호가 올바르지 않습니다.");
        }
    }
}

