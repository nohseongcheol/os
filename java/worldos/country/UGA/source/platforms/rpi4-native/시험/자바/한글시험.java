// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.문자;
import 한국어.자체.faili;
import 한국어.자체.ingizo_Orodha;
import 한국어.자체.kamusi;
import 한국어.자체.출력;
public class 한글시험 {
    public static void main(String[] a) throws Exception {
        String 인사 = "안녕하세요 · 日本語 · العربية · 😀";
        출력.andika_laini(문자.simbua_fiche_data(문자.부호화(인사))); 출력.수쓰기(문자.코드포인트수("한글😀"));
        faili.andika("한글자료.txt", 인사); 출력.andika_laini(faili.읽기("한글자료.txt"));
        ingizo_Orodha 이름들 = new ingizo_Orodha(); 이름들.더하기("가람"); 이름들.더하기("누리"); 출력.andika_laini(이름들.읽기(1));
        kamusi 뜻 = new kamusi(); 뜻.넣기("가람", "강"); System.gc(); 출력.andika_laini(뜻.gundua_ingizo("가람"));
        try { 문자.simbua_fiche_data(new byte[] {(byte)0xc0, (byte)0xaf}); } catch (IllegalArgumentException e) { 출력.andika_laini("UTF-8 kosa kataa_thamani"); }
        출력.andika_laini("한국어 maktaba 완료");
    }
}
