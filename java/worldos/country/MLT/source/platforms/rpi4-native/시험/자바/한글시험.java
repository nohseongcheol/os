// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Malti.자체.문자;
import Malti.자체.fajl;
import Malti.자체.entrata_Lista;
import Malti.자체.dizzjunarju;
import Malti.자체.출력;
public class 한글시험 {
    public static void main(String[] a) throws Exception {
        String 인사 = "안녕하세요 · 日本語 · العربية · 😀";
        출력.kiteb_linja(문자.ddeċifra_data(문자.부호화(인사))); 출력.수쓰기(문자.kodiċi_tal_karattru_COUNT("한글😀"));
        fajl.kiteb("한글자료.txt", 인사); 출력.kiteb_linja(fajl.읽기("한글자료.txt"));
        entrata_Lista 이름들 = new entrata_Lista(); 이름들.더하기("가람"); 이름들.더하기("누리"); 출력.kiteb_linja(이름들.읽기(1));
        dizzjunarju 뜻 = new dizzjunarju(); 뜻.넣기("가람", "강"); System.gc(); 출력.kiteb_linja(뜻.sab_entrata("가람"));
        try { 문자.ddeċifra_data(new byte[] {(byte)0xc0, (byte)0xaf}); } catch (IllegalArgumentException e) { 출력.kiteb_linja("UTF-8 żball 거부"); }
        출력.kiteb_linja("Malti librerija 완료");
    }
}
