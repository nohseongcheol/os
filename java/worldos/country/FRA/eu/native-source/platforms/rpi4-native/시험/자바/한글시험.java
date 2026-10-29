// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Euskara.자체.문자;
import Euskara.자체.Fitxategia;
import Euskara.자체.sarrera_Zerrenda;
import Euskara.자체.hiztegi;
import Euskara.자체.Irteera;
public class 한글시험 {
    public static void main(String[] a) throws Exception {
        String 인사 = "안녕하세요 · 日本語 · العربية · 😀";
        Irteera.idatzi_lerro(문자.desenkriptatu_datuak(문자.부호화(인사))); Irteera.수쓰기(문자.karaktere_kode_ZENBATU("한글😀"));
        Fitxategia.Idatzi("한글자료.txt", 인사); Irteera.idatzi_lerro(Fitxategia.Irakurri("한글자료.txt"));
        sarrera_Zerrenda 이름들 = new sarrera_Zerrenda(); 이름들.더하기("가람"); 이름들.더하기("누리"); Irteera.idatzi_lerro(이름들.Irakurri(1));
        hiztegi 뜻 = new hiztegi(); 뜻.넣기("가람", "강"); System.gc(); Irteera.idatzi_lerro(뜻.Bilatu_sarrera("가람"));
        try { 문자.desenkriptatu_datuak(new byte[] {(byte)0xc0, (byte)0xaf}); } catch (IllegalArgumentException e) { Irteera.idatzi_lerro("UTF-8 errorea baztertu_balio"); }
        Irteera.idatzi_lerro("Euskara liburutegi 완료");
    }
}
