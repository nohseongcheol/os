// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Татарча.자체.문자;
import Татарча.자체.Birem;
import Татарча.자체.кертү_Исемлек;
import Татарча.자체.сүзлек;
import Татарча.자체.출력;
public class 한글시험 {
    public static void main(String[] a) throws Exception {
        String 인사 = "안녕하세요 · 日本語 · العربية · 😀";
        출력.язу_юл(문자.шифрны_ачу_мәгълүмат(문자.부호화(인사))); 출력.수쓰기(문자.символ_коды_COUNT("한글😀"));
        Birem.язу("한글자료.txt", 인사); 출력.язу_юл(Birem.읽기("한글자료.txt"));
        кертү_Исемлек 이름들 = new кертү_Исемлек(); 이름들.더하기("가람"); 이름들.더하기("누리"); 출력.язу_юл(이름들.읽기(1));
        сүзлек 뜻 = new сүзлек(); 뜻.넣기("가람", "강"); System.gc(); 출력.язу_юл(뜻.FIND_кертү("가람"));
        try { 문자.шифрны_ачу_мәгълүмат(new byte[] {(byte)0xc0, (byte)0xaf}); } catch (IllegalArgumentException e) { 출력.язу_юл("UTF-8 Хата 거부"); }
        출력.язу_юл("Татарча библиотека 완료");
    }
}
