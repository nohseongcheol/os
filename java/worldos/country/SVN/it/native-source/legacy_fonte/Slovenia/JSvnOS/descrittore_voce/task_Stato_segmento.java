// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Slovenia.JSvnOS.descrittore_voce;

/** x86 작업 SWITCH_MODA 때 특권 쌓임공간을 제공하는 TSS 관리 표현이다. */
public final class task_Stato_segmento {
    private int Pila_zero_Blocca;
    private int Pila_zero_e_mail;
    private int 입출력허용표위치 = 104;

    public void 특권쌓임공간설정(int blocco_VALORE_652d4b53, int e_mail) {
        Pila_zero_Blocca = blocco_VALORE_652d4b53;
        Pila_zero_e_mail = e_mail;
    }

    public int Pila_zero_Blocca() { return Pila_zero_Blocca; }
    public int Pila_zero_e_mail() { return Pila_zero_e_mail; }
    public int 입출력허용표위치() { return 입출력허용표위치; }
}

