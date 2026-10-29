// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Eesti.oma.문자;
import Eesti.oma.Fail;
import Eesti.oma.kirje_Loend;
import Eesti.oma.sõnastik;
import Eesti.oma.Väljund;
public class 한글시험 {
    public static void main(String[] a) throws Exception {
        String 인사 = "안녕하세요 · 日本語 · العربية · 😀";
        Väljund.kirjutamine_liin(문자.dekrüptima_andmed(문자.kodeerima(인사))); Väljund.kirjutamine_number(문자.koodipunkt_COUNT("한글😀"));
        Fail.Kirjutamine("한글자료.txt", 인사); Väljund.kirjutamine_liin(Fail.Lugemine("한글자료.txt"));
        kirje_Loend 이름들 = new kirje_Loend(); 이름들.더하기("가람"); 이름들.더하기("누리"); Väljund.kirjutamine_liin(이름들.Lugemine(1));
        sõnastik 뜻 = new sõnastik(); 뜻.넣기("가람", "강"); System.gc(); Väljund.kirjutamine_liin(뜻.FIND_kirje("가람"));
        try { 문자.dekrüptima_andmed(new byte[] {(byte)0xc0, (byte)0xaf}); } catch (IllegalArgumentException e) { Väljund.kirjutamine_liin("UTF-8 VIGA keelduma_VALUE"); }
        Väljund.kirjutamine_liin("Eesti teek 완료");
    }
}
