// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.문자;
import 한국어.자체.فائل;
import 한국어.자체.داخلا_فهرست;
import 한국어.자체.ڊڪشنري;
import 한국어.자체.출력;
public class 한글시험 {
    public static void main(String[] a) throws Exception {
        String 인사 = "안녕하세요 · 日本語 · العربية · 😀";
        출력.لکو_لڪير(문자.طئي_ٿيل_ڪوائف(문자.부호화(인사))); 출력.수쓰기(문자.코드포인트수("한글😀"));
        فائل.لکو("한글자료.txt", 인사); 출력.لکو_لڪير(فائل.읽기("한글자료.txt"));
        داخلا_فهرست 이름들 = new داخلا_فهرست(); 이름들.더하기("가람"); 이름들.더하기("누리"); 출력.لکو_لڪير(이름들.읽기(1));
        ڊڪشنري 뜻 = new ڊڪشنري(); 뜻.넣기("가람", "강"); System.gc(); 출력.لکو_لڪير(뜻.ڳوليو_داخلا("가람"));
        try { 문자.طئي_ٿيل_ڪوائف(new byte[] {(byte)0xc0, (byte)0xaf}); } catch (IllegalArgumentException e) { 출력.لکو_لڪير("UTF-8 نقص 거부"); }
        출력.لکو_لڪير("한국어 لائبريري 완료");
    }
}
