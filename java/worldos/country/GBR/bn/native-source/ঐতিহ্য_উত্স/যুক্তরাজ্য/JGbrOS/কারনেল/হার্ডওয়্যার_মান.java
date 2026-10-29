// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package যুক্তরাজ্য.JGbrOS.কারনেল;

/** Java 관리 커널과 CPU 고유 কোড_মান 사이의 유일한 경계다. */
public interface হার্ডওয়্যার_মান {
    void 직렬출력(String সামগ্রি_মান);

    int 포트바이트읽기(int হার্ডওয়্যার_পোর্ট_নম্বর);

    void লেখা_পোর্ট_বাইট(int হার্ডওয়্যার_পোর্ট_নম্বর, int মান);

    void 중앙처리장치멈춤();
}

