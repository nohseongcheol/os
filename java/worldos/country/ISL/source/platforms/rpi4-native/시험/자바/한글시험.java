// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Íslenska.eigin.문자;
import Íslenska.eigin.Skrá;
import Íslenska.eigin.færsla_Listi;
import Íslenska.eigin.orðabók;
import Íslenska.eigin.úttak;
public class 한글시험 {
    public static void main(String[] a) throws Exception {
        String 인사 = "안녕하세요 · 日本語 · العربية · 😀";
        úttak.skrifa_lína(문자.dulráða_gögn(문자.부호화(인사))); úttak.skrifa_númer(문자.stafkóði_COUNT("한글😀"));
        Skrá.Skrift("한글자료.txt", 인사); úttak.skrifa_lína(Skrá.Lestur("한글자료.txt"));
        færsla_Listi 이름들 = new færsla_Listi(); 이름들.더하기("가람"); 이름들.더하기("누리"); úttak.skrifa_lína(이름들.Lestur(1));
        orðabók 뜻 = new orðabók(); 뜻.넣기("가람", "강"); System.gc(); úttak.skrifa_lína(뜻.FIND_færsla("가람"));
        try { 문자.dulráða_gögn(new byte[] {(byte)0xc0, (byte)0xaf}); } catch (IllegalArgumentException e) { úttak.skrifa_lína("UTF-8 Villa hafna_VALUE"); }
        úttak.skrifa_lína("Íslenska safn 완료");
    }
}
