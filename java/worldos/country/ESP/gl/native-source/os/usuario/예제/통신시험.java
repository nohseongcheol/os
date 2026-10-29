// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 통신시험 {
    public static int Executar_2() {
        int 첫째 = usuario.abrir_Rede(45000);
        if (첫째 < 0) { usuario.Escritura("NETWORK UNAVAILABLE\n"); return 3; }
        int[] datos = new int[8];
        boolean pass_VALOR = usuario.abrir_Rede(45000) == -98
            && usuario.자료받기(첫째, datos, 0) == -11
            && usuario.자료받기(첫째, datos, 50) == -110
            && usuario.자료받기(첫째, datos, 3000) == -22
            && usuario.enviar_datos(첫째, 0x0a000202, 9, datos, 9) == -90
            && usuario.자료받기(첫째, null, 0) == -14
            && usuario.peche_Rede(첫째) == 0 && usuario.peche_Rede(첫째) == -9;
        usuario.Escritura(pass_VALOR ? "UDP API CHECK PASS\n" : "UDP API CHECK FAIL\n");
        return pass_VALOR ? 0 : 1;
    }
}
