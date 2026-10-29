// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package নেপাল.JNplOS.হোস্ট;

import java.util.HashMap;
import java.util.Map;
import নেপাল.JNplOS.কারনেল.হার্ডওয়্যার_মান;

/** 일반 JVM에서 관리 커널을 결정적으로 시험하는 হার্ডওয়্যার_মান 대역이다. */
public final class হোস্ট_হার্ডওয়্যার implements হার্ডওয়্যার_মান {
    private final Map<Integer, Integer> হার্ডওয়্যার_পোর্ট_মান = new HashMap<Integer, Integer>();
    private final StringBuilder 직렬기록 = new StringBuilder();

    @Override
    public void 직렬출력(String সামগ্রি_মান) {
        직렬기록.append(সামগ্রি_মান);
        System.out.print(সামগ্রি_মান);
    }

    @Override
    public int 포트바이트읽기(int হার্ডওয়্যার_পোর্ট_নম্বর) {
        Integer মান = হার্ডওয়্যার_পোর্ট_মান.get(Integer.valueOf(হার্ডওয়্যার_পোর্ট_নম্বর));
        return মান == null ? 0 : মান.intValue();
    }

    @Override
    public void লেখা_পোর্ট_বাইট(int হার্ডওয়্যার_পোর্ট_নম্বর, int মান) {
        হার্ডওয়্যার_পোর্ট_মান.put(Integer.valueOf(হার্ডওয়্যার_পোর্ট_নম্বর), Integer.valueOf(মান & 0xff));
    }

    @Override
    public void 중앙처리장치멈춤() {
        // হোস্ট 시험에서는 পরবর্তী_দফা 사건을 기다리지 않고 즉시 반환한다.
    }

    public String 직렬기록() {
        return 직렬기록.toString();
    }
}

