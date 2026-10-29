// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.문자;
import 한국어.자체.faele;
import 한국어.자체.tsenyo_lenaane;
import 한국어.자체.bukantswe;
import 한국어.자체.출력;
public class 한글시험 {
    public static void main(String[] a) throws Exception {
        String 인사 = "안녕하세요 · 日本語 · العربية · 😀";
        출력.kwala_Mola(문자.Sirolola_tshedimosetso(문자.부호화(인사))); 출력.수쓰기(문자.코드포인트수("한글😀"));
        faele.kwala("한글자료.txt", 인사); 출력.kwala_Mola(faele.읽기("한글자료.txt"));
        tsenyo_lenaane 이름들 = new tsenyo_lenaane(); 이름들.더하기("가람"); 이름들.더하기("누리"); 출력.kwala_Mola(이름들.읽기(1));
        bukantswe 뜻 = new bukantswe(); 뜻.넣기("가람", "강"); System.gc(); 출력.kwala_Mola(뜻.batla_tsenyo("가람"));
        try { 문자.Sirolola_tshedimosetso(new byte[] {(byte)0xc0, (byte)0xaf}); } catch (IllegalArgumentException e) { 출력.kwala_Mola("UTF-8 phoso 거부"); }
        출력.kwala_Mola("한국어 laeborari 완료");
    }
}
