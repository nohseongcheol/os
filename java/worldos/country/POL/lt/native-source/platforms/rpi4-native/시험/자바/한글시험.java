// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Lietuvių.savas.문자;
import Lietuvių.savas.Failas;
import Lietuvių.savas.įrašas_Sąrašas;
import Lietuvių.savas.žodynas;
import Lietuvių.savas.Išvestis;
public class 한글시험 {
    public static void main(String[] a) throws Exception {
        String 인사 = "안녕하세요 · 日本語 · العربية · 😀";
        Išvestis.rašymas_eilutė(문자.iššifruoti_duomenys(문자.koduoti(인사))); Išvestis.rašymas_numeris(문자.kodo_elementas_COUNT("한글😀"));
        Failas.Rašymas("한글자료.txt", 인사); Išvestis.rašymas_eilutė(Failas.Skaitymas("한글자료.txt"));
        įrašas_Sąrašas 이름들 = new įrašas_Sąrašas(); 이름들.더하기("가람"); 이름들.더하기("누리"); Išvestis.rašymas_eilutė(이름들.Skaitymas(1));
        žodynas 뜻 = new žodynas(); 뜻.넣기("가람", "강"); System.gc(); Išvestis.rašymas_eilutė(뜻.FIND_įrašas("가람"));
        try { 문자.iššifruoti_duomenys(new byte[] {(byte)0xc0, (byte)0xaf}); } catch (IllegalArgumentException e) { Išvestis.rašymas_eilutė("UTF-8 KLAIDA atmesti_VALUE"); }
        Išvestis.rašymas_eilutė("Lietuvių biblioteka 완료");
    }
}
