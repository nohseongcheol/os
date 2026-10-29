// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.문자;
import 한국어.자체.फायल;
import 한국어.자체.प्रवेश_सुची;
import 한국어.자체.डिक्शनरी;
import 한국어.자체.출력;
public class 한글시험 {
    public static void main(String[] a) throws Exception {
        String 인사 = "안녕하세요 · 日本語 · العربية · 😀";
        출력.बरोवचें_रेग(문자.डिक्रिप्ट_डेटा(문자.부호화(인사))); 출력.수쓰기(문자.वर्ण_कोड_COUNT("한글😀"));
        फायल.बरोवचें("한글자료.txt", 인사); 출력.बरोवचें_रेग(फायल.읽기("한글자료.txt"));
        प्रवेश_सुची 이름들 = new प्रवेश_सुची(); 이름들.더하기("가람"); 이름들.더하기("누리"); 출력.बरोवचें_रेग(이름들.읽기(1));
        डिक्शनरी 뜻 = new डिक्शनरी(); 뜻.넣기("가람", "강"); System.gc(); 출력.बरोवचें_रेग(뜻.FIND_प्रवेश("가람"));
        try { 문자.डिक्रिप्ट_डेटा(new byte[] {(byte)0xc0, (byte)0xaf}); } catch (IllegalArgumentException e) { 출력.बरोवचें_रेग("UTF-8 चूक 거부"); }
        출력.बरोवचें_रेग("한국어 लायब्ररी 완료");
    }
}
