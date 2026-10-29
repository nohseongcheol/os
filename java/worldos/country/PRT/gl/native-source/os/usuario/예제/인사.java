// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int Executar_2() {
        usuario.Escritura("Hello from a separate Java ELF!\n");
        usuario.Escritura(usuario.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int ÍNDICE = 0; ÍNDICE < usuario.인수개수(); ÍNDICE++) {
            usuario.Escritura("arg: "); usuario.Escritura(usuario.Argumentos(ÍNDICE)); usuario.Escritura("\n");
        }
        return usuario.실행권한() == 3 ? 0 : 1;
    }
}
