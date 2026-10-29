// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 통신시험 {
    public static int Executa_2() {
        int 첫째 = usuari.crear_xarxa(45000);
        if (첫째 < 0) { usuari.Escriptura("NETWORK UNAVAILABLE\n"); return 3; }
        int[] dades = new int[8];
        boolean transmetre_VALOR = usuari.crear_xarxa(45000) == -98
            && usuari.rebre_dades(첫째, dades, 0) == -11
            && usuari.rebre_dades(첫째, dades, 50) == -110
            && usuari.rebre_dades(첫째, dades, 3000) == -22
            && usuari.enviar_dades(첫째, 0x0a000202, 9, dades, 9) == -90
            && usuari.rebre_dades(첫째, null, 0) == -14
            && usuari.Tanca_xarxa(첫째) == 0 && usuari.Tanca_xarxa(첫째) == -9;
        usuari.Escriptura(transmetre_VALOR ? "UDP API CHECK PASS\n" : "UDP API CHECK FAIL\n");
        return transmetre_VALOR ? 0 : 1;
    }
}
