// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.문자;
import 한국어.자체.Fíla;
import 한국어.자체.목록;
import 한국어.자체.사전;
import 한국어.자체.출력;
public class 한글시험 {
    public static void main(String[] a) throws Exception {
        String 인사 = "안녕하세요 · 日本語 · العربية · 😀";
        출력.줄쓰기(문자.복호화(문자.부호화(인사))); 출력.수쓰기(문자.코드포인트수("한글😀"));
        Fíla.쓰기("한글자료.txt", 인사); 출력.줄쓰기(Fíla.읽기("한글자료.txt"));
        목록 이름들 = new 목록(); 이름들.더하기("가람"); 이름들.더하기("누리"); 출력.줄쓰기(이름들.읽기(1));
        사전 뜻 = new 사전(); 뜻.넣기("가람", "강"); System.gc(); 출력.줄쓰기(뜻.찾기("가람"));
        try { 문자.복호화(new byte[] {(byte)0xc0, (byte)0xaf}); } catch (IllegalArgumentException e) { 출력.줄쓰기("UTF-8 Brek 거부"); }
        출력.줄쓰기("한국어 라이브러리 완료");
    }
}
