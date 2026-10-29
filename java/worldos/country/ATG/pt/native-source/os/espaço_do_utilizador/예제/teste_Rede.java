// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class teste_Rede {
    public static int iniciar() {
        int 첫째 = espaço_do_utilizador.abrir_rede(45000);
        if (첫째 < 0) { espaço_do_utilizador.Escrita("NETWORK UNAVAILABLE\n"); return 3; }
        int[] dados = new int[8];
        boolean 통과 = espaço_do_utilizador.abrir_rede(45000) == -98
            && espaço_do_utilizador.receber_dados(첫째, dados, 0) == -11
            && espaço_do_utilizador.receber_dados(첫째, dados, 50) == -110
            && espaço_do_utilizador.receber_dados(첫째, dados, 3000) == -22
            && espaço_do_utilizador.enviar_dados(첫째, 0x0a000202, 9, dados, 9) == -90
            && espaço_do_utilizador.receber_dados(첫째, null, 0) == -14
            && espaço_do_utilizador.Close_rede(첫째) == 0 && espaço_do_utilizador.Close_rede(첫째) == -9;
        espaço_do_utilizador.Escrita(통과 ? "UDP API CHECK PASS\n" : "UDP API CHECK FAIL\n");
        return 통과 ? 0 : 1;
    }
}
