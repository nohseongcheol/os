// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.문자;
import 한국어.자체.bara_denc;
import 한국어.자체.dugal_xabaar_lim;
import 한국어.자체.téereb_Tekki_baat;
import 한국어.자체.출력;
public class 한글시험 {
    public static void main(String[] a) throws Exception {
        String 인사 = "안녕하세요 · 日本語 · العربية · 😀";
        출력.biir_buum(문자.fecci_mbir(문자.부호화(인사))); 출력.수쓰기(문자.코드포인트수("한글😀"));
        bara_denc.biir("한글자료.txt", 인사); 출력.biir_buum(bara_denc.읽기("한글자료.txt"));
        dugal_xabaar_lim 이름들 = new dugal_xabaar_lim(); 이름들.더하기("가람"); 이름들.더하기("누리"); 출력.biir_buum(이름들.읽기(1));
        téereb_Tekki_baat 뜻 = new téereb_Tekki_baat(); 뜻.넣기("가람", "강"); System.gc(); 출력.biir_buum(뜻.seet_dugal_xabaar("가람"));
        try { 문자.fecci_mbir(new byte[] {(byte)0xc0, (byte)0xaf}); } catch (IllegalArgumentException e) { 출력.biir_buum("UTF-8 njumte 거부"); }
        출력.biir_buum("한국어 daaray_téere 완료");
    }
}
