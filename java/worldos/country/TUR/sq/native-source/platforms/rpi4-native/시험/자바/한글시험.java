// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.문자;
import 한국어.자체.Kartelë;
import 한국어.자체.futje_Listë;
import 한국어.자체.fjalor;
import 한국어.자체.출력;
public class 한글시험 {
    public static void main(String[] a) throws Exception {
        String 인사 = "안녕하세요 · 日本語 · العربية · 😀";
        출력.shkruaj_linjë(문자.dekriptoj_të_dhëna(문자.부호화(인사))); 출력.수쓰기(문자.kodi_i_karakterit_COUNT("한글😀"));
        Kartelë.Shkrimi("한글자료.txt", 인사); 출력.shkruaj_linjë(Kartelë.Leximi("한글자료.txt"));
        futje_Listë 이름들 = new futje_Listë(); 이름들.더하기("가람"); 이름들.더하기("누리"); 출력.shkruaj_linjë(이름들.Leximi(1));
        fjalor 뜻 = new fjalor(); 뜻.넣기("가람", "강"); System.gc(); 출력.shkruaj_linjë(뜻.FIND_futje("가람"));
        try { 문자.dekriptoj_të_dhëna(new byte[] {(byte)0xc0, (byte)0xaf}); } catch (IllegalArgumentException e) { 출력.shkruaj_linjë("UTF-8 GABIM refuzo_VALUE"); }
        출력.shkruaj_linjë("한국어 bibliotekë 완료");
    }
}
