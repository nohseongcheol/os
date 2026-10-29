// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ไทย.เอง;

/** 한국어로 การประกาศ·던지기·잡기를 할 หมายเลข 있는 대기시간초과예외. */
public class 대기시간초과예외 extends รับเข้า_ส่งออก_ข้อยกเว้น {
    public 대기시간초과예외() { super(); }
    public 대기시간초과예외(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
