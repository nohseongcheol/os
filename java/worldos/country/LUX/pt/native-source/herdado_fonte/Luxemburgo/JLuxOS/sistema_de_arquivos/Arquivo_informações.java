// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Luxemburgo.JLuxOS.sistema_de_arquivos;

public final class Arquivo_informações {
    private final int Tamanho;
    private final int forma_Tipo;

    public Arquivo_informações(int Tamanho, int forma_Tipo) {
        this.Tamanho = Tamanho;
        this.forma_Tipo = forma_Tipo;
    }

    public int Tamanho() {
        return Tamanho;
    }

    public int forma_Tipo() {
        return forma_Tipo;
    }
}

