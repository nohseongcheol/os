// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Svenska.eget.문자;
import Svenska.eget.filnamn;
import Svenska.eget.post_ange;
import Svenska.eget.ordlista;
import Svenska.eget.utmatningsposition;
public class 한글시험 {
    public static void main(String[] a) throws Exception {
        String 인사 = "안녕하세요 · 日本語 · العربية · 😀";
        utmatningsposition.skriva_rad(문자.avkryptera_data(문자.koda(인사))); utmatningsposition.skriva_nummer(문자.kodpunkt_ANTAL("한글😀"));
        filnamn.Skriv("한글자료.txt", 인사); utmatningsposition.skriva_rad(filnamn.Läs("한글자료.txt"));
        post_ange 이름들 = new post_ange(); 이름들.더하기("가람"); 이름들.더하기("누리"); utmatningsposition.skriva_rad(이름들.Läs(1));
        ordlista 뜻 = new ordlista(); 뜻.넣기("가람", "강"); System.gc(); utmatningsposition.skriva_rad(뜻.Sök_post("가람"));
        try { 문자.avkryptera_data(new byte[] {(byte)0xc0, (byte)0xaf}); } catch (IllegalArgumentException e) { utmatningsposition.skriva_rad("UTF-8 fel avvisa_värde"); }
        utmatningsposition.skriva_rad("Svenska bibliotek 완료");
    }
}
