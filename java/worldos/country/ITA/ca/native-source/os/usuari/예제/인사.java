// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int Executa_2() {
        usuari.Escriptura("Hello from a separate Java ELF!\n");
        usuari.Escriptura(usuari.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int INDEX = 0; INDEX < usuari.인수개수(); INDEX++) {
            usuari.Escriptura("arg: "); usuari.Escriptura(usuari.인수(INDEX)); usuari.Escriptura("\n");
        }
        return usuari.실행권한() == 3 ? 0 : 1;
    }
}
