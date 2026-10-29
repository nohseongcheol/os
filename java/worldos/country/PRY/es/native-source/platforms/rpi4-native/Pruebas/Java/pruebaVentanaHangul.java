// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import español.propio.ventana;
import español.propio.ComponenteVisual;
import español.propio.*;

public class pruebaVentanaHangul implements TareaTareaEjecutable, ReceptorAcción {
    ventana Pantalla;
    etiqueta Guía;
    CampoTexto valorEntrada;
    public void ejecutarTarea() {
        Comprobaciones.exigir(ColaEvento.esDespachoEnCursoEvento(), "español Pantalla Tarea 큐");
        Pantalla = new ventana("español biblioteca ventana", 400, 280);
        Guía = ComponenteVisual.valorEtiquetaMarcador("한글로 Java 코딩", 20, 20, 340, 30);
        valorEntrada = ComponenteVisual.CampoTexto("nombre", 20, 65, 340, 30);
        Pantalla.añadirElemento(Guía);
        Pantalla.añadirElemento(valorEntrada);
        Pantalla.añadirElemento(ComponenteVisual.botón("saludar", 20, 110, 180, 32, this));
        Pantalla.mostrarVentana();
        Salida.escribirLínea("KOREAN SWING READY");
    }
    public void recibirAcción(NotificaciónAcción evento) {
        Comprobaciones.exigir(ColaEvento.esDespachoEnCursoEvento(), "español acción 되부름");
        Comprobaciones.exigir(evento.número() == 1001 && evento.fuenteEvento() instanceof botón, "español evento 객체와 valorOrigen");
        Comprobaciones.exigir(!((Object)evento.fuenteEvento() instanceof javax.swing.JButton), "표준 단추와 독립된 valorFormato");
        Comprobaciones.exigir(!((Object)evento instanceof java.awt.event.ActionEvent), "표준 사건과 독립된 valorFormato");
        Guía.escribirTexto("안녕하세요 " + valorEntrada.leerTexto());
        Salida.escribirLínea("KOREAN SWING CLICK " + valorEntrada.leerTexto());
    }
    public static void main(String[] argumentos) {
        ColaEvento.invocarPosterior(new pruebaVentanaHangul());
    }
}
