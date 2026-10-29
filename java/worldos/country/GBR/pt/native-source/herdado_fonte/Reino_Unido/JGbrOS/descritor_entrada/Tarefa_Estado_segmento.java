// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Reino_Unido.JGbrOS.descritor_entrada;

/** x86 작업 mudar_MODO 때 특권 쌓임공간을 제공하는 TSS 관리 표현이다. */
public final class Tarefa_Estado_segmento {
    private int pilha_zero_bloco;
    private int pilha_zero_email;
    private int 입출력허용표위치 = 104;

    public void 특권쌓임공간설정(int fragmento_VALOR, int Endereço) {
        pilha_zero_bloco = fragmento_VALOR;
        pilha_zero_email = Endereço;
    }

    public int pilha_zero_bloco() { return pilha_zero_bloco; }
    public int pilha_zero_email() { return pilha_zero_email; }
    public int 입출력허용표위치() { return 입출력허용표위치; }
}

