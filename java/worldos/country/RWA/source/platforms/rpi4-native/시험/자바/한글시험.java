// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Ikinyarwanda.자체.문자;
import Ikinyarwanda.자체.Idosiye;
import Ikinyarwanda.자체.icyinjizwa_Urutonde;
import Ikinyarwanda.자체.inkoranyamagambo;
import Ikinyarwanda.자체.출력;
public class 한글시험 {
    public static void main(String[] a) throws Exception {
        String 인사 = "안녕하세요 · 日本語 · العربية · 😀";
        출력.kwandika_umurongo(문자.gusobanura_amakurushingiro(문자.부호화(인사))); 출력.수쓰기(문자.코드포인트수("한글😀"));
        Idosiye.kwandika("한글자료.txt", 인사); 출력.kwandika_umurongo(Idosiye.읽기("한글자료.txt"));
        icyinjizwa_Urutonde 이름들 = new icyinjizwa_Urutonde(); 이름들.더하기("가람"); 이름들.더하기("누리"); 출력.kwandika_umurongo(이름들.읽기(1));
        inkoranyamagambo 뜻 = new inkoranyamagambo(); 뜻.넣기("가람", "강"); System.gc(); 출력.kwandika_umurongo(뜻.gushaka_icyinjizwa("가람"));
        try { 문자.gusobanura_amakurushingiro(new byte[] {(byte)0xc0, (byte)0xaf}); } catch (IllegalArgumentException e) { 출력.kwandika_umurongo("UTF-8 IKOSA 거부"); }
        출력.kwandika_umurongo("Ikinyarwanda isomero 완료");
    }
}
