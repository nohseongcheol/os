// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import norsk.eget.문자;
import norsk.eget.Fil;
import norsk.eget.oppføring_Liste;
import norsk.eget.ordliste;
import norsk.eget.Utgang;
public class 한글시험 {
    public static void main(String[] a) throws Exception {
        String 인사 = "안녕하세요 · 日本語 · العربية · 😀";
        Utgang.skrive_linje(문자.dekryptere_data(문자.부호화(인사))); Utgang.skrive_nummer(문자.tegnkode_ANTALL("한글😀"));
        Fil.Skriv("한글자료.txt", 인사); Utgang.skrive_linje(Fil.Les("한글자료.txt"));
        oppføring_Liste 이름들 = new oppføring_Liste(); 이름들.더하기("가람"); 이름들.더하기("누리"); Utgang.skrive_linje(이름들.Les(1));
        ordliste 뜻 = new ordliste(); 뜻.넣기("가람", "강"); System.gc(); Utgang.skrive_linje(뜻.Søk_oppføring("가람"));
        try { 문자.dekryptere_data(new byte[] {(byte)0xc0, (byte)0xaf}); } catch (IllegalArgumentException e) { Utgang.skrive_linje("UTF-8 feil avvise_VERDI"); }
        Utgang.skrive_linje("norsk bibliotek 완료");
    }
}
