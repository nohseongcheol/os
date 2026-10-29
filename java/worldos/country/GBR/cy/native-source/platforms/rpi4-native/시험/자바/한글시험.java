// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Cymraeg.자체.문자;
import Cymraeg.자체.Ffeil;
import Cymraeg.자체.cofnod_Rhestr;
import Cymraeg.자체.geiriadur;
import Cymraeg.자체.Allbwn;
public class 한글시험 {
    public static void main(String[] a) throws Exception {
        String 인사 = "안녕하세요 · 日本語 · العربية · 😀";
        Allbwn.ysgrifennu_llinell(문자.dadgryptio_data(문자.부호화(인사))); Allbwn.수쓰기(문자.cod_nod_COUNT("한글😀"));
        Ffeil.Ysgrifennu("한글자료.txt", 인사); Allbwn.ysgrifennu_llinell(Ffeil.Darllen("한글자료.txt"));
        cofnod_Rhestr 이름들 = new cofnod_Rhestr(); 이름들.더하기("가람"); 이름들.더하기("누리"); Allbwn.ysgrifennu_llinell(이름들.Darllen(1));
        geiriadur 뜻 = new geiriadur(); 뜻.넣기("가람", "강"); System.gc(); Allbwn.ysgrifennu_llinell(뜻.FIND_cofnod("가람"));
        try { 문자.dadgryptio_data(new byte[] {(byte)0xc0, (byte)0xaf}); } catch (IllegalArgumentException e) { Allbwn.ysgrifennu_llinell("UTF-8 Gwall gwrthod_VALUE"); }
        Allbwn.ysgrifennu_llinell("Cymraeg llyfrgell 완료");
    }
}
