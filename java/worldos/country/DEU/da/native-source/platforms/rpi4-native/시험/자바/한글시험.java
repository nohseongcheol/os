// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Dansk.eget.문자;
import Dansk.eget.Fil;
import Dansk.eget.post_Liste;
import Dansk.eget.ordbog;
import Dansk.eget.Udgang;
public class 한글시험 {
    public static void main(String[] a) throws Exception {
        String 인사 = "안녕하세요 · 日本語 · العربية · 😀";
        Udgang.skrive_linje(문자.dekryptere_data(문자.kode(인사))); Udgang.skrive_tal(문자.tegnkode_TÆL("한글😀"));
        Fil.Skrive("한글자료.txt", 인사); Udgang.skrive_linje(Fil.Læse("한글자료.txt"));
        post_Liste 이름들 = new post_Liste(); 이름들.더하기("가람"); 이름들.더하기("누리"); Udgang.skrive_linje(이름들.Læse(1));
        ordbog 뜻 = new ordbog(); 뜻.넣기("가람", "강"); System.gc(); Udgang.skrive_linje(뜻.Søg_post("가람"));
        try { 문자.dekryptere_data(new byte[] {(byte)0xc0, (byte)0xaf}); } catch (IllegalArgumentException e) { Udgang.skrive_linje("UTF-8 fejl afvise_VÆRDI"); }
        Udgang.skrive_linje("Dansk bibliotek 완료");
    }
}
