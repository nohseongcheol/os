// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.문자;
import 한국어.자체.फाइल;
import 한국어.자체.목록;
import 한국어.자체.사전;
import 한국어.자체.आउटपुट;
public class 한글시험 {
    public static void main(String[] a) throws Exception {
        String 인사 = "안녕하세요 · 日本語 · العربية · 😀";
        आउटपुट.줄쓰기(문자.복호화(문자.부호화(인사))); आउटपुट.수쓰기(문자.코드포인트수("한글😀"));
        फाइल.लिखू("한글자료.txt", 인사); आउटपुट.줄쓰기(फाइल.पढ़ू("한글자료.txt"));
        목록 이름들 = new 목록(); 이름들.더하기("가람"); 이름들.더하기("누리"); आउटपुट.줄쓰기(이름들.पढ़ू(1));
        사전 뜻 = new 사전(); 뜻.넣기("가람", "강"); System.gc(); आउटपुट.줄쓰기(뜻.찾기("가람"));
        try { 문자.복호화(new byte[] {(byte)0xc0, (byte)0xaf}); } catch (IllegalArgumentException e) { आउटपुट.줄쓰기("UTF-8 त्रुटि 거부"); }
        आउटपुट.줄쓰기("한국어 라이브러리 완료");
    }
}
