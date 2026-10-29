// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Gaeilge.자체.문자;
import Gaeilge.자체.Comhad;
import Gaeilge.자체.iontráil_Liosta;
import Gaeilge.자체.foclóir;
import Gaeilge.자체.Aschur;
public class 한글시험 {
    public static void main(String[] a) throws Exception {
        String 인사 = "안녕하세요 · 日本語 · العربية · 😀";
        Aschur.scríobh_líne(문자.díchriptigh_sonraí(문자.부호화(인사))); Aschur.수쓰기(문자.pointe_cóid_COUNT("한글😀"));
        Comhad.Scríobh("한글자료.txt", 인사); Aschur.scríobh_líne(Comhad.Léigh("한글자료.txt"));
        iontráil_Liosta 이름들 = new iontráil_Liosta(); 이름들.더하기("가람"); 이름들.더하기("누리"); Aschur.scríobh_líne(이름들.Léigh(1));
        foclóir 뜻 = new foclóir(); 뜻.넣기("가람", "강"); System.gc(); Aschur.scríobh_líne(뜻.FIND_iontráil("가람"));
        try { 문자.díchriptigh_sonraí(new byte[] {(byte)0xc0, (byte)0xaf}); } catch (IllegalArgumentException e) { Aschur.scríobh_líne("UTF-8 ERREÁID diúltaigh_VALUE"); }
        Aschur.scríobh_líne("Gaeilge leabharlann 완료");
    }
}
