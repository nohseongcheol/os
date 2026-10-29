// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class pruebaConexiónRed {
    public static int ponerEnMarcha() {
        int ordinalPrimero = Usuario.abrirRed(45000);
        if (ordinalPrimero < 0) { Usuario.escribir("NETWORK UNAVAILABLE\n"); return 3; }
        int[] Datos = new int[8];
        boolean valorPaso = Usuario.abrirRed(45000) == -98
            && Usuario.recibirDatos(ordinalPrimero, Datos, 0) == -11
            && Usuario.recibirDatos(ordinalPrimero, Datos, 50) == -110
            && Usuario.recibirDatos(ordinalPrimero, Datos, 3000) == -22
            && Usuario.enviarDatos(ordinalPrimero, 0x0a000202, 9, Datos, 9) == -90
            && Usuario.recibirDatos(ordinalPrimero, null, 0) == -14
            && Usuario.cerrarRed(ordinalPrimero) == 0 && Usuario.cerrarRed(ordinalPrimero) == -9;
        Usuario.escribir(valorPaso ? "UDP API CHECK PASS\n" : "UDP API CHECK FAIL\n");
        return valorPaso ? 0 : 1;
    }
}
