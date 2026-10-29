// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.문자;
import 한국어.자체.فائل;
import 한국어.자체.داخلہ_فرست;
import 한국어.자체.لغت;
import 한국어.자체.출력;
public class 한글시험 {
    public static void main(String[] a) throws Exception {
        String 인사 = "안녕하세요 · 日本語 · العربية · 😀";
        출력.لکھو_لائن(문자.ضابطہ_کشائی_کرو_کوائف(문자.부호화(인사))); 출력.수쓰기(문자.코드포인트수("한글😀"));
        فائل.لکھو("한글자료.txt", 인사); 출력.لکھو_لائن(فائل.읽기("한글자료.txt"));
        داخلہ_فرست 이름들 = new داخلہ_فرست(); 이름들.더하기("가람"); 이름들.더하기("누리"); 출력.لکھو_لائن(이름들.읽기(1));
        لغت 뜻 = new لغت(); 뜻.넣기("가람", "강"); System.gc(); 출력.لکھو_لائن(뜻.ڈھونڈو_داخلہ("가람"));
        try { 문자.ضابطہ_کشائی_کرو_کوائف(new byte[] {(byte)0xc0, (byte)0xaf}); } catch (IllegalArgumentException e) { 출력.لکھو_لائن("UTF-8 نقص 거부"); }
        출력.لکھو_لائن("한국어 لائبریری 완료");
    }
}
