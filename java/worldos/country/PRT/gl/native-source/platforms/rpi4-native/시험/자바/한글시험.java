// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Galego.자체.문자;
import Galego.자체.Ficheiro;
import Galego.자체.introdución_Lista;
import Galego.자체.dicionario;
import Galego.자체.Saída;
public class 한글시험 {
    public static void main(String[] a) throws Exception {
        String 인사 = "안녕하세요 · 日本語 · العربية · 😀";
        Saída.escribir_liña(문자.descifrar_datos(문자.부호화(인사))); Saída.수쓰기(문자.código_de_carácter_CONTAR("한글😀"));
        Ficheiro.Escritura("한글자료.txt", 인사); Saída.escribir_liña(Ficheiro.Lectura("한글자료.txt"));
        introdución_Lista 이름들 = new introdución_Lista(); 이름들.더하기("가람"); 이름들.더하기("누리"); Saída.escribir_liña(이름들.Lectura(1));
        dicionario 뜻 = new dicionario(); 뜻.넣기("가람", "강"); System.gc(); Saída.escribir_liña(뜻.Busca_introdución("가람"));
        try { 문자.descifrar_datos(new byte[] {(byte)0xc0, (byte)0xaf}); } catch (IllegalArgumentException e) { Saída.escribir_liña("UTF-8 ERRO rexeitar_VALOR_e3ecc00b"); }
        Saída.escribir_liña("Galego biblioteca 완료");
    }
}
