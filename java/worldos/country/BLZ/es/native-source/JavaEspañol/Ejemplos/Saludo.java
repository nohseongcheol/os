// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import español.Java.*;
import java.nio.file.Path;
import java.awt.GraphicsEnvironment;
import javax.swing.*;

public class Saludo {
    public static void main(String[] argumentos) throws Exception {
        String texto = "안녕하세요 · Hello · 日本語 · العربية · 😀";
        Path ruta = Archivo.ruta("Saludo.txt");
        Archivo.escribir(ruta, texto);
        System.out.println(Archivo.leer(ruta));
        Thread valorTrabajo = Tarea.ponerEnMarcha("Saludo Tarea", () -> System.out.println("Tarea valorHiloEjecución ejecutarComando"));
        Tarea.esperarFin(valorTrabajo);
        if (GraphicsEnvironment.isHeadless()) {
            System.out.println("그래픽 화면이 없어 terminal 출력만 실행했습니다. 창을 보려면 QEMU 데스크톱의 터미널에서 실행하세요.");
        } else {
            Pantalla.valorPosterior(() -> Pantalla.ventana("다국어 Saludo", new JLabel(texto), 700, 160));
        }
    }
}
