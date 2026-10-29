// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.문자;
import 한국어.자체.دوتنه;
import 한국어.자체.목록;
import 한국어.자체.사전;
import 한국어.자체.출력;
public class 한글시험 {
    public static void main(String[] a) throws Exception {
        String 인사 = "안녕하세요 · 日本語 · العربية · 😀";
        출력.ليکل_ليکه(문자.کوډ_پرانېستل_اومتوک(문자.부호화(인사))); 출력.수쓰기(문자.코드포인트수("한글😀"));
        دوتنه.لوستل_2("한글자료.txt", 인사); 출력.ليکل_ليکه(دوتنه.لوستل("한글자료.txt"));
        목록 이름들 = new 목록(); 이름들.더하기("가람"); 이름들.더하기("누리"); 출력.ليکل_ليکه(이름들.لوستل(1));
        사전 뜻 = new 사전(); 뜻.넣기("가람", "강"); System.gc(); 출력.ليکل_ليکه(뜻.찾기("가람"));
        try { 문자.کوډ_پرانېستل_اومتوک(new byte[] {(byte)0xc0, (byte)0xaf}); } catch (IllegalArgumentException e) { 출력.ليکل_ليکه("UTF-8 تېروتنه 거부"); }
        출력.ليکل_ليکه("한국어 کتابتون 완료");
    }
}
