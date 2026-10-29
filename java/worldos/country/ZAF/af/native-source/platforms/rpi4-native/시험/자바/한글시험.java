// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.문자;
import 한국어.자체.Lêer;
import 한국어.자체.inskrywing_Lys;
import 한국어.자체.woordeboek;
import 한국어.자체.Afvoer;
public class 한글시험 {
    public static void main(String[] a) throws Exception {
        String 인사 = "안녕하세요 · 日本語 · العربية · 😀";
        Afvoer.skryf_lyn(문자.dekripteer_data(문자.부호화(인사))); Afvoer.수쓰기(문자.karakterkode_COUNT("한글😀"));
        Lêer.Skryf("한글자료.txt", 인사); Afvoer.skryf_lyn(Lêer.Lees("한글자료.txt"));
        inskrywing_Lys 이름들 = new inskrywing_Lys(); 이름들.더하기("가람"); 이름들.더하기("누리"); Afvoer.skryf_lyn(이름들.Lees(1));
        woordeboek 뜻 = new woordeboek(); 뜻.넣기("가람", "강"); System.gc(); Afvoer.skryf_lyn(뜻.FIND_inskrywing("가람"));
        try { 문자.dekripteer_data(new byte[] {(byte)0xc0, (byte)0xaf}); } catch (IllegalArgumentException e) { Afvoer.skryf_lyn("UTF-8 Fout 거부"); }
        Afvoer.skryf_lyn("한국어 biblioteek 완료");
    }
}
