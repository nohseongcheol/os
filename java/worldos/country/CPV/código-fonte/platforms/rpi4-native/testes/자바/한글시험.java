// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Português.nativo.문자;
import Português.nativo.ficheiro;
import Português.nativo.entrada_Lista_f07b3200;
import Português.nativo.dicionário;
import Português.nativo.saídaTexto;
public class 한글시험 {
    public static void main(String[] a) throws Exception {
        String saudação_ae353e94 = "안녕하세요 · 日本語 · العربية · 😀";
        saídaTexto.gravar_linha(문자.descriptografar_dados(문자.codificar(saudação_ae353e94))); saídaTexto.gravar_número(문자.ponto_de_código_CONT_NÚM("한글😀"));
        ficheiro.Escrita("한글자료.txt", saudação_ae353e94); saídaTexto.gravar_linha(ficheiro.Leitura("한글자료.txt"));
        entrada_Lista_f07b3200 이름들 = new entrada_Lista_f07b3200(); 이름들.더하기("가람"); 이름들.더하기("누리"); saídaTexto.gravar_linha(이름들.Leitura(1));
        dicionário 뜻 = new dicionário(); 뜻.넣기("가람", "강"); System.gc(); saídaTexto.gravar_linha(뜻.PROCURAR_entrada("가람"));
        try { 문자.descriptografar_dados(new byte[] {(byte)0xc0, (byte)0xaf}); } catch (IllegalArgumentException e) { saídaTexto.gravar_linha("UTF-8 erro rejeitar_VALOR"); }
        saídaTexto.gravar_linha("Português biblioteca 완료");
    }
}
