// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import hrvatski.vlastiti.문자;
import hrvatski.vlastiti.Datoteka;
import hrvatski.vlastiti.unos_Popis;
import hrvatski.vlastiti.rječnik;
import hrvatski.vlastiti.Izlaz;
public class 한글시험 {
    public static void main(String[] a) throws Exception {
        String 인사 = "안녕하세요 · 日本語 · العربية · 😀";
        Izlaz.zapisivanje_red(문자.dešifrirati_podaci(문자.kodirati(인사))); Izlaz.수쓰기(문자.točka_koda_COUNT("한글😀"));
        Datoteka.Zapisuj("한글자료.txt", 인사); Izlaz.zapisivanje_red(Datoteka.Čitaj("한글자료.txt"));
        unos_Popis 이름들 = new unos_Popis(); 이름들.더하기("가람"); 이름들.더하기("누리"); Izlaz.zapisivanje_red(이름들.Čitaj(1));
        rječnik 뜻 = new rječnik(); 뜻.넣기("가람", "강"); System.gc(); Izlaz.zapisivanje_red(뜻.FIND_unos("가람"));
        try { 문자.dešifrirati_podaci(new byte[] {(byte)0xc0, (byte)0xaf}); } catch (IllegalArgumentException e) { Izlaz.zapisivanje_red("UTF-8 GREŠKA odbiti_VALUE"); }
        Izlaz.zapisivanje_red("hrvatski biblioteka 완료");
    }
}
