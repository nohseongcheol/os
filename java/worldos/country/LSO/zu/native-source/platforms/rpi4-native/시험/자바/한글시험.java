// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Isi_Zulu.자체.문자;
import Isi_Zulu.자체.Ihele;
import Isi_Zulu.자체.okufakwayo_Uhlu;
import Isi_Zulu.자체.iqoqo_lokhiye;
import Isi_Zulu.자체.출력;
public class 한글시험 {
    public static void main(String[] a) throws Exception {
        String 인사 = "안녕하세요 · 日本語 · العربية · 😀";
        출력.bhala_umugqa(문자.guqulela_imininingwane(문자.부호화(인사))); 출력.수쓰기(문자.코드포인트수("한글😀"));
        Ihele.Bhala("한글자료.txt", 인사); 출력.bhala_umugqa(Ihele.Funda("한글자료.txt"));
        okufakwayo_Uhlu 이름들 = new okufakwayo_Uhlu(); 이름들.더하기("가람"); 이름들.더하기("누리"); 출력.bhala_umugqa(이름들.Funda(1));
        iqoqo_lokhiye 뜻 = new iqoqo_lokhiye(); 뜻.넣기("가람", "강"); System.gc(); 출력.bhala_umugqa(뜻.thola_okufakwayo("가람"));
        try { 문자.guqulela_imininingwane(new byte[] {(byte)0xc0, (byte)0xaf}); } catch (IllegalArgumentException e) { 출력.bhala_umugqa("UTF-8 Iphutha 거부"); }
        출력.bhala_umugqa("Isi_Zulu umtapo 완료");
    }
}
