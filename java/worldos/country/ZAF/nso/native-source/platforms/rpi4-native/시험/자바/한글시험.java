// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.문자;
import 한국어.자체.Faele;
import 한국어.자체.go_tsenya_tshedimošo_Lenaneo;
import 한국어.자체.lefelopolokelo;
import 한국어.자체.출력;
public class 한글시험 {
    public static void main(String[] a) throws Exception {
        String 인사 = "안녕하세요 · 日本語 · العربية · 😀";
        출력.ngwala_mothaladi(문자.boetša_sekeng_data(문자.부호화(인사))); 출력.수쓰기(문자.코드포인트수("한글😀"));
        Faele.Ngwala("한글자료.txt", 인사); 출력.ngwala_mothaladi(Faele.Bala("한글자료.txt"));
        go_tsenya_tshedimošo_Lenaneo 이름들 = new go_tsenya_tshedimošo_Lenaneo(); 이름들.더하기("가람"); 이름들.더하기("누리"); 출력.ngwala_mothaladi(이름들.Bala(1));
        lefelopolokelo 뜻 = new lefelopolokelo(); 뜻.넣기("가람", "강"); System.gc(); 출력.ngwala_mothaladi(뜻.hwetša_go_tsenya_tshedimošo("가람"));
        try { 문자.boetša_sekeng_data(new byte[] {(byte)0xc0, (byte)0xaf}); } catch (IllegalArgumentException e) { 출력.ngwala_mothaladi("UTF-8 Phošo 거부"); }
        출력.ngwala_mothaladi("한국어 Bokgobadata 완료");
    }
}
