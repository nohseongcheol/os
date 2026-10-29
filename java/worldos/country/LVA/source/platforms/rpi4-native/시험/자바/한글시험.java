// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Latviešu.savs.문자;
import Latviešu.savs.Fails;
import Latviešu.savs.ievade_Saraksts;
import Latviešu.savs.vārdnīca;
import Latviešu.savs.Izvade;
public class 한글시험 {
    public static void main(String[] a) throws Exception {
        String 인사 = "안녕하세요 · 日本語 · العربية · 😀";
        Izvade.rakstīšana_līnija(문자.atšifrēt_dati(문자.kodēt(인사))); Izvade.rakstīšana_numurs(문자.koda_punkts_COUNT("한글😀"));
        Fails.Rakstīt("한글자료.txt", 인사); Izvade.rakstīšana_līnija(Fails.Lasīt("한글자료.txt"));
        ievade_Saraksts 이름들 = new ievade_Saraksts(); 이름들.더하기("가람"); 이름들.더하기("누리"); Izvade.rakstīšana_līnija(이름들.Lasīt(1));
        vārdnīca 뜻 = new vārdnīca(); 뜻.넣기("가람", "강"); System.gc(); Izvade.rakstīšana_līnija(뜻.FIND_ievade("가람"));
        try { 문자.atšifrēt_dati(new byte[] {(byte)0xc0, (byte)0xaf}); } catch (IllegalArgumentException e) { Izvade.rakstīšana_līnija("UTF-8 Kļūda noraidīt_VALUE"); }
        Izvade.rakstīšana_līnija("Latviešu bibliotēka 완료");
    }
}
