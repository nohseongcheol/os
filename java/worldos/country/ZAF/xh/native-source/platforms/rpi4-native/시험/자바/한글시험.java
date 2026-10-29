// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import isiXhosa.자체.문자;
import isiXhosa.자체.iFayili;
import isiXhosa.자체.ufako_nkcukacha_uludwe;
import isiXhosa.자체.isichazi_magama;
import isiXhosa.자체.출력;
public class 한글시험 {
    public static void main(String[] a) throws Exception {
        String 인사 = "안녕하세요 · 日本語 · العربية · 😀";
        출력.bhala_umgca(문자.buyisela_ubhalo_oluqhelekileyo_iingcombolo(문자.부호화(인사))); 출력.수쓰기(문자.코드포인트수("한글😀"));
        iFayili.Bhala("한글자료.txt", 인사); 출력.bhala_umgca(iFayili.Funda("한글자료.txt"));
        ufako_nkcukacha_uludwe 이름들 = new ufako_nkcukacha_uludwe(); 이름들.더하기("가람"); 이름들.더하기("누리"); 출력.bhala_umgca(이름들.Funda(1));
        isichazi_magama 뜻 = new isichazi_magama(); 뜻.넣기("가람", "강"); System.gc(); 출력.bhala_umgca(뜻.fumana_ufako_nkcukacha("가람"));
        try { 문자.buyisela_ubhalo_oluqhelekileyo_iingcombolo(new byte[] {(byte)0xc0, (byte)0xaf}); } catch (IllegalArgumentException e) { 출력.bhala_umgca("UTF-8 Impazamo 거부"); }
        출력.bhala_umgca("isiXhosa ilayibhrari 완료");
    }
}
