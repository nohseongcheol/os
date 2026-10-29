// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.문자;
import 한국어.자체.Fichier;
import 한국어.자체.Agab_Lëscht;
import 한국어.자체.Dictionnaire;
import 한국어.자체.출력;
public class 한글시험 {
    public static void main(String[] a) throws Exception {
        String 인사 = "안녕하세요 · 日本語 · العربية · 😀";
        출력.schreiwen_Zeil(문자.decryptéieren_Daten(문자.부호화(인사))); 출력.수쓰기(문자.Zeechecode_COUNT("한글😀"));
        Fichier.schreiwen("한글자료.txt", 인사); 출력.schreiwen_Zeil(Fichier.읽기("한글자료.txt"));
        Agab_Lëscht 이름들 = new Agab_Lëscht(); 이름들.더하기("가람"); 이름들.더하기("누리"); 출력.schreiwen_Zeil(이름들.읽기(1));
        Dictionnaire 뜻 = new Dictionnaire(); 뜻.넣기("가람", "강"); System.gc(); 출력.schreiwen_Zeil(뜻.FIND_Agab("가람"));
        try { 문자.decryptéieren_Daten(new byte[] {(byte)0xc0, (byte)0xaf}); } catch (IllegalArgumentException e) { 출력.schreiwen_Zeil("UTF-8 Feeler 거부"); }
        출력.schreiwen_Zeil("한국어 Bibliothéik 완료");
    }
}
