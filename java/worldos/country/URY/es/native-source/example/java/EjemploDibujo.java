// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class EjemploDibujo {
    public static void ponerEnMarcha() {
        // Dibujar rectángulos rojos, verdes y azules a la derecha de la pantalla 640x480.
        español.propio.Pantalla.rectángulo(600, 400, 28, 20, 0x0000ff);
        español.propio.Pantalla.rectángulo(600, 425, 28, 20, 0x00ff00);
        español.propio.Pantalla.rectángulo(600, 450, 28, 20, 0xff0000);
        español.propio.Salida.escribirLínea("JAVA 그래픽: RGB");
        español.propio.Salida.escribirLínea("Enter");
        español.propio.Pantalla.esperarFin();
    }
}
