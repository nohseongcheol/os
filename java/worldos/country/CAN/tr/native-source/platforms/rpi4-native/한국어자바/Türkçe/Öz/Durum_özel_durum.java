// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Türkçe.Öz;

/** 한국어로 bildirim·던지기·잡기를 할 수 있는 Durum_özel_durum. */
public class Durum_özel_durum extends java.lang.IllegalStateException {
    public Durum_özel_durum() { super(); }
    public Durum_özel_durum(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
