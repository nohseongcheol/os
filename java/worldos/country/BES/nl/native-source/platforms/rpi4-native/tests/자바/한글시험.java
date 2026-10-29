// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Nederlands.Eigen.문자;
import Nederlands.Eigen.bestand;
import Nederlands.Eigen.invoer_Lijst_f07b3200;
import Nederlands.Eigen.woordenlijst;
import Nederlands.Eigen.tekstuitvoer;
public class 한글시험 {
    public static void main(String[] a) throws Exception {
        String 인사 = "안녕하세요 · 日本語 · العربية · 😀";
        tekstuitvoer.schrijven_lijn(문자.ontsleutelen_gegevens(문자.coderen(인사))); tekstuitvoer.schrijven_nummer(문자.codepoint_AANTAL("한글😀"));
        bestand.Schrijven("한글자료.txt", 인사); tekstuitvoer.schrijven_lijn(bestand.Lezen("한글자료.txt"));
        invoer_Lijst_f07b3200 이름들 = new invoer_Lijst_f07b3200(); 이름들.더하기("가람"); 이름들.더하기("누리"); tekstuitvoer.schrijven_lijn(이름들.Lezen(1));
        woordenlijst 뜻 = new woordenlijst(); 뜻.넣기("가람", "강"); System.gc(); tekstuitvoer.schrijven_lijn(뜻.Zoeken_invoer("가람"));
        try { 문자.ontsleutelen_gegevens(new byte[] {(byte)0xc0, (byte)0xaf}); } catch (IllegalArgumentException e) { tekstuitvoer.schrijven_lijn("UTF-8 fout weigeren_WAARDE"); }
        tekstuitvoer.schrijven_lijn("Nederlands bibliotheek 완료");
    }
}
