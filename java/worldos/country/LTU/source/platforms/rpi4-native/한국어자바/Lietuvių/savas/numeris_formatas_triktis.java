// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Lietuvių.savas;

/** 한국어로 deklaracija·던지기·잡기를 할 numeris 있는 numeris_formatas_triktis. */
public class numeris_formatas_triktis extends neleistinas_argumentas_išimtis {
    public numeris_formatas_triktis() { super(); }
    public numeris_formatas_triktis(String aprašas) { super(aprašas); }
    public String aprašas() { return getMessage(); }
}
