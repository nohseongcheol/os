// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import čeština.vlastní.문자;
import čeština.vlastní.název_souboru;
import čeština.vlastní.položka_Seznam;
import čeština.vlastní.slovník;
import čeština.vlastní.výstupní_pozice;
public class 한글시험 {
    public static void main(String[] a) throws Exception {
        String 인사 = "안녕하세요 · 日本語 · العربية · 😀";
        výstupní_pozice.zápis_čára(문자.dešifrovat_data(문자.kódovat(인사))); výstupní_pozice.zápis_číslo(문자.bod_kódu_POČET("한글😀"));
        název_souboru.Zápis("한글자료.txt", 인사); výstupní_pozice.zápis_čára(název_souboru.Čtení("한글자료.txt"));
        položka_Seznam 이름들 = new položka_Seznam(); 이름들.더하기("가람"); 이름들.더하기("누리"); výstupní_pozice.zápis_čára(이름들.Čtení(1));
        slovník 뜻 = new slovník(); 뜻.넣기("가람", "강"); System.gc(); výstupní_pozice.zápis_čára(뜻.NAJÍT_položka("가람"));
        try { 문자.dešifrovat_data(new byte[] {(byte)0xc0, (byte)0xaf}); } catch (IllegalArgumentException e) { výstupní_pozice.zápis_čára("UTF-8 chyba odmítnout_HODNOTA"); }
        výstupní_pozice.zápis_čára("čeština knihovna 완료");
    }
}
