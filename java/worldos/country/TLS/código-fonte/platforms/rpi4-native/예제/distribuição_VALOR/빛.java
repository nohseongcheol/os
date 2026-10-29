// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 빛 {
    public static void main(String[] argumentos) throws Exception {
        int SUM_VALOR = 0;
        int número = 1;
        while (número <= 10) {
            SUM_VALOR = SUM_VALOR + número;
            número = número + 1;
        }
        Português.nativo.saídaTexto.gravar_número(SUM_VALOR);
        Português.nativo.ficheiro.Escrita("aot.txt", "한글 AOT ficheiro 😀");
        Português.nativo.saídaTexto.gravar_linha(Português.nativo.ficheiro.Leitura("aot.txt"));
    }
}
