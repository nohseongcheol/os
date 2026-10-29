// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Català.propi.문자;
import Català.propi.Fitxer;
import Català.propi.introducció_Llista;
import Català.propi.diccionari;
import Català.propi.Sortida;
public class 한글시험 {
    public static void main(String[] a) throws Exception {
        String 인사 = "안녕하세요 · 日本語 · العربية · 😀";
        Sortida.escriure_línia(문자.desencriptar_dades(문자.부호화(인사))); Sortida.수쓰기(문자.codi_de_caràcter_COMPT("한글😀"));
        Fitxer.Escriptura("한글자료.txt", 인사); Sortida.escriure_línia(Fitxer.Lectura("한글자료.txt"));
        introducció_Llista 이름들 = new introducció_Llista(); 이름들.더하기("가람"); 이름들.더하기("누리"); Sortida.escriure_línia(이름들.Lectura(1));
        diccionari 뜻 = new diccionari(); 뜻.넣기("가람", "강"); System.gc(); Sortida.escriure_línia(뜻.BUSCA_introducció("가람"));
        try { 문자.desencriptar_dades(new byte[] {(byte)0xc0, (byte)0xaf}); } catch (IllegalArgumentException e) { Sortida.escriure_línia("UTF-8 s_ha_produït_un_error rebutjar_VALOR"); }
        Sortida.escriure_línia("Català biblioteca 완료");
    }
}
