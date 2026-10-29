// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 한국어로 declaration·던지기·잡기를 할 수 있는 ARRAY_Store_pagpalya. */
public class ARRAY_Store_pagpalya extends java.lang.ArrayStoreException {
    public ARRAY_Store_pagpalya() { super(); }
    public ARRAY_Store_pagpalya(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
