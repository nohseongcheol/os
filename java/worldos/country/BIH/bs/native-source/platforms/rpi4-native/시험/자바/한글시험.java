// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.문자;
import 한국어.자체.Fajl;
import 한국어.자체.unos_spisak;
import 한국어.자체.rječnik;
import 한국어.자체.Ispis;
public class 한글시험 {
    public static void main(String[] a) throws Exception {
        String 인사 = "안녕하세요 · 日本語 · العربية · 😀";
        Ispis.pisati_redak(문자.dešifrirati_podaci(문자.부호화(인사))); Ispis.수쓰기(문자.kôd_znaka_COUNT("한글😀"));
        Fajl.Piši("한글자료.txt", 인사); Ispis.pisati_redak(Fajl.Čitaj("한글자료.txt"));
        unos_spisak 이름들 = new unos_spisak(); 이름들.더하기("가람"); 이름들.더하기("누리"); Ispis.pisati_redak(이름들.Čitaj(1));
        rječnik 뜻 = new rječnik(); 뜻.넣기("가람", "강"); System.gc(); Ispis.pisati_redak(뜻.FIND_unos("가람"));
        try { 문자.dešifrirati_podaci(new byte[] {(byte)0xc0, (byte)0xaf}); } catch (IllegalArgumentException e) { Ispis.pisati_redak("UTF-8 GRESKA odbiti_VALUE"); }
        Ispis.pisati_redak("한국어 biblioteka 완료");
    }
}
