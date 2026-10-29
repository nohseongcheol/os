// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Slovenský.vlastné.문자;
import Slovenský.vlastné.Súbor;
import Slovenský.vlastné.položka_Zoznam;
import Slovenský.vlastné.slovník;
import Slovenský.vlastné.Výstup;
public class 한글시험 {
    public static void main(String[] a) throws Exception {
        String 인사 = "안녕하세요 · 日本語 · العربية · 😀";
        Výstup.zapísať_linka(문자.dešifrovať_údaje(문자.kódovať(인사))); Výstup.수쓰기(문자.bod_kódu_COUNT("한글😀"));
        Súbor.Zápis("한글자료.txt", 인사); Výstup.zapísať_linka(Súbor.Čítanie("한글자료.txt"));
        položka_Zoznam 이름들 = new položka_Zoznam(); 이름들.더하기("가람"); 이름들.더하기("누리"); Výstup.zapísať_linka(이름들.Čítanie(1));
        slovník 뜻 = new slovník(); 뜻.넣기("가람", "강"); System.gc(); Výstup.zapísať_linka(뜻.FIND_položka("가람"));
        try { 문자.dešifrovať_údaje(new byte[] {(byte)0xc0, (byte)0xaf}); } catch (IllegalArgumentException e) { Výstup.zapísať_linka("UTF-8 chyba odmietnuť_VALUE"); }
        Výstup.zapísať_linka("Slovenský knižnica 완료");
    }
}
