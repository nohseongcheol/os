// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package فارسی.بومی;

/** 한국어로 اعلامیه·던지기·잡기를 할 수 있는 بی_اعتبار_آرگومان_استثنا. */
public class بی_اعتبار_آرگومان_استثنا extends java.lang.IllegalArgumentException {
    public بی_اعتبار_آرگومان_استثنا() { super(); }
    public بی_اعتبار_آرگومان_استثنا(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
