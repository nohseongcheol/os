// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import magyar.saját.문자;
import magyar.saját.Fájl;
import magyar.saját.bejegyzés_Lista;
import magyar.saját.szótár;
import magyar.saját.Kimenet;
public class 한글시험 {
    public static void main(String[] a) throws Exception {
        String 인사 = "안녕하세요 · 日本語 · العربية · 😀";
        Kimenet.ír_sor(문자.visszafejt_adat(문자.kódolás(인사))); Kimenet.ír_szám(문자.kódpont_DARAB("한글😀"));
        Fájl.Írás("한글자료.txt", 인사); Kimenet.ír_sor(Fájl.Olvasás("한글자료.txt"));
        bejegyzés_Lista 이름들 = new bejegyzés_Lista(); 이름들.더하기("가람"); 이름들.더하기("누리"); Kimenet.ír_sor(이름들.Olvasás(1));
        szótár 뜻 = new szótár(); 뜻.넣기("가람", "강"); System.gc(); Kimenet.ír_sor(뜻.keres_bejegyzés("가람"));
        try { 문자.visszafejt_adat(new byte[] {(byte)0xc0, (byte)0xaf}); } catch (IllegalArgumentException e) { Kimenet.ír_sor("UTF-8 HIBA elutasít_ÉRTÉK"); }
        Kimenet.ír_sor("magyar kódtár 완료");
    }
}
