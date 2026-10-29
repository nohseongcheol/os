// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Reo_Māori.자체.문자;
import Reo_Māori.자체.Kōnae;
import Reo_Māori.자체.tāurunga_Rārangi;
import Reo_Māori.자체.papakupu;
import Reo_Māori.자체.출력;
public class 한글시험 {
    public static void main(String[] a) throws Exception {
        String 인사 = "안녕하세요 · 日本語 · العربية · 😀";
        출력.tuhi_hononga(문자.wetemuna_raraunga(문자.부호화(인사))); 출력.수쓰기(문자.waehere_pūāhua_COUNT("한글😀"));
        Kōnae.Tuhia("한글자료.txt", 인사); 출력.tuhi_hononga(Kōnae.Pānuitia("한글자료.txt"));
        tāurunga_Rārangi 이름들 = new tāurunga_Rārangi(); 이름들.더하기("가람"); 이름들.더하기("누리"); 출력.tuhi_hononga(이름들.Pānuitia(1));
        papakupu 뜻 = new papakupu(); 뜻.넣기("가람", "강"); System.gc(); 출력.tuhi_hononga(뜻.FIND_tāurunga("가람"));
        try { 문자.wetemuna_raraunga(new byte[] {(byte)0xc0, (byte)0xaf}); } catch (IllegalArgumentException e) { 출력.tuhi_hononga("UTF-8 Pōhēhē 거부"); }
        출력.tuhi_hononga("Reo_Māori puna 완료");
    }
}
