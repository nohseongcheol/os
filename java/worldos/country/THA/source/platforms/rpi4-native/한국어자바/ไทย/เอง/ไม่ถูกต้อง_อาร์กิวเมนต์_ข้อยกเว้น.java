// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ไทย.เอง;

/** 한국어로 การประกาศ·던지기·잡기를 할 หมายเลข 있는 ไม่ถูกต้อง_อาร์กิวเมนต์_ข้อยกเว้น. */
public class ไม่ถูกต้อง_อาร์กิวเมนต์_ข้อยกเว้น extends java.lang.IllegalArgumentException {
    public ไม่ถูกต้อง_อาร์กิวเมนต์_ข้อยกเว้น() { super(); }
    public ไม่ถูกต้อง_อาร์กิวเมนต์_ข้อยกเว้น(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
