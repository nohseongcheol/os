// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Română.propriu.문자;
import Română.propriu.Fișier;
import Română.propriu.intrare_Listă;
import Română.propriu.dicționar;
import Română.propriu.Rezultat;
public class 한글시험 {
    public static void main(String[] a) throws Exception {
        String 인사 = "안녕하세요 · 日本語 · العربية · 😀";
        Rezultat.scriere_linie(문자.decripta_date(문자.codifica(인사))); Rezultat.수쓰기(문자.cod_caracter_COUNT("한글😀"));
        Fișier.Scriere("한글자료.txt", 인사); Rezultat.scriere_linie(Fișier.Citire("한글자료.txt"));
        intrare_Listă 이름들 = new intrare_Listă(); 이름들.더하기("가람"); 이름들.더하기("누리"); Rezultat.scriere_linie(이름들.Citire(1));
        dicționar 뜻 = new dicționar(); 뜻.넣기("가람", "강"); System.gc(); Rezultat.scriere_linie(뜻.FIND_intrare("가람"));
        try { 문자.decripta_date(new byte[] {(byte)0xc0, (byte)0xaf}); } catch (IllegalArgumentException e) { Rezultat.scriere_linie("UTF-8 eroare respinge_VALUE"); }
        Rezultat.scriere_linie("Română bibliotecă 완료");
    }
}
