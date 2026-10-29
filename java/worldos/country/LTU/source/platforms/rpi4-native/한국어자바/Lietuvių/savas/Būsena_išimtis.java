// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Lietuvių.savas;

/** 한국어로 deklaracija·던지기·잡기를 할 numeris 있는 Būsena_išimtis. */
public class Būsena_išimtis extends java.lang.IllegalStateException {
    public Būsena_išimtis() { super(); }
    public Būsena_išimtis(String aprašas) { super(aprašas); }
    public String aprašas() { return getMessage(); }
}
