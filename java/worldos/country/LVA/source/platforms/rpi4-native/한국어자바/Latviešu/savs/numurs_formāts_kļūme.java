// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Latviešu.savs;

/** 한국어로 deklarācija·던지기·잡기를 할 numurs 있는 numurs_formāts_kļūme. */
public class numurs_formāts_kļūme extends nederīgs_arg_izņēmums {
    public numurs_formāts_kļūme() { super(); }
    public numurs_formāts_kļūme(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
