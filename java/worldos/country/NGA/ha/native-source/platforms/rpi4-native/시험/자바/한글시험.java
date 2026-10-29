// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.문자;
import 한국어.자체.Fayil;
import 한국어.자체.Mashigar_bayanai_Jeri;
import 한국어.자체.kamus;
import 한국어.자체.출력;
public class 한글시험 {
    public static void main(String[] a) throws Exception {
        String 인사 = "안녕하세요 · 日本語 · العربية · 😀";
        출력.Rubuta_Layi(문자.Bude_Tarin_bayani(문자.부호화(인사))); 출력.수쓰기(문자.코드포인트수("한글😀"));
        Fayil.Yi_Rubutu("한글자료.txt", 인사); 출력.Rubuta_Layi(Fayil.Yi_Karatu("한글자료.txt"));
        Mashigar_bayanai_Jeri 이름들 = new Mashigar_bayanai_Jeri(); 이름들.더하기("가람"); 이름들.더하기("누리"); 출력.Rubuta_Layi(이름들.Yi_Karatu(1));
        kamus 뜻 = new kamus(); 뜻.넣기("가람", "강"); System.gc(); 출력.Rubuta_Layi(뜻.nema_Mashigar_bayanai("가람"));
        try { 문자.Bude_Tarin_bayani(new byte[] {(byte)0xc0, (byte)0xaf}); } catch (IllegalArgumentException e) { 출력.Rubuta_Layi("UTF-8 Kuskure kore_Daraja"); }
        출력.Rubuta_Layi("한국어 laburare 완료");
    }
}
