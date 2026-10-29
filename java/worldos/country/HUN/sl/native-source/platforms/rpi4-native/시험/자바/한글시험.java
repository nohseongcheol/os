// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import slovenščina.lastno.문자;
import slovenščina.lastno.Datoteka;
import slovenščina.lastno.vnos_Seznam;
import slovenščina.lastno.slovar;
import slovenščina.lastno.Izpis;
public class 한글시험 {
    public static void main(String[] a) throws Exception {
        String 인사 = "안녕하세요 · 日本語 · العربية · 😀";
        Izpis.pisati_linija(문자.dešifrirati_podatki(문자.kodirati(인사))); Izpis.수쓰기(문자.koda_znaka_COUNT("한글😀"));
        Datoteka.Pisanje("한글자료.txt", 인사); Izpis.pisati_linija(Datoteka.Branje("한글자료.txt"));
        vnos_Seznam 이름들 = new vnos_Seznam(); 이름들.더하기("가람"); 이름들.더하기("누리"); Izpis.pisati_linija(이름들.Branje(1));
        slovar 뜻 = new slovar(); 뜻.넣기("가람", "강"); System.gc(); Izpis.pisati_linija(뜻.FIND_vnos("가람"));
        try { 문자.dešifrirati_podatki(new byte[] {(byte)0xc0, (byte)0xaf}); } catch (IllegalArgumentException e) { Izpis.pisati_linija("UTF-8 NAPAKA zavrniti_VALUE"); }
        Izpis.pisati_linija("slovenščina knjižnica 완료");
    }
}
