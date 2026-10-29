// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class saudação_ae353e94 {
    public static int iniciar() {
        espaço_do_utilizador.Escrita("Hello from a separate Java ELF!\n");
        espaço_do_utilizador.Escrita(espaço_do_utilizador.execução_Permissão() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int ÍNDICE = 0; ÍNDICE < espaço_do_utilizador.인수개수(); ÍNDICE++) {
            espaço_do_utilizador.Escrita("arg: "); espaço_do_utilizador.Escrita(espaço_do_utilizador.argumentos(ÍNDICE)); espaço_do_utilizador.Escrita("\n");
        }
        return espaço_do_utilizador.execução_Permissão() == 3 ? 0 : 1;
    }
}
