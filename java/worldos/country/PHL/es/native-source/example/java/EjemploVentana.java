// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import español.propio.ventana;
import español.propio.etiqueta;
import español.propio.CampoTexto;
import español.propio.botón;
import español.propio.ColaEvento;
import español.propio.Salida;
import español.propio.TareaTareaEjecutable;
import español.propio.ReceptorAcción;
import español.propio.NotificaciónAcción;

/** Ventana Swing en el núcleo autónomo: texto en español, acción del botón y actualización de la etiqueta. */
public class EjemploVentana implements TareaTareaEjecutable, ReceptorAcción {
    private ventana ventanaSaludo;
    private CampoTexto campoNombre;
    private etiqueta saludo;
    private int númeroElementosSaludo;

    public void abrirVentana() {
        ventanaSaludo = new ventana("es Swing", 460, 300);
        ventanaSaludo.añadirElemento(new etiqueta("Hola", 20, 20, 420, 28));
        campoNombre = new CampoTexto("es", 20, 64, 420, 30);
        saludo = new etiqueta("Hola", 20, 152, 420, 28);
        ventanaSaludo.añadirElemento(campoNombre);
        ventanaSaludo.añadirElemento(new botón("saludar", 20, 108, 180, 32, this));
        ventanaSaludo.añadirElemento(saludo);
        ventanaSaludo.añadirElemento(new etiqueta("F9 / Shift+Space | X", 20, 204, 420, 28));
        ventanaSaludo.mostrarVentana();
        Salida.escribirLínea("GUI Ejemplos preparar: EjemploVentana");
    }

    public void saludar() {
        númeroElementosSaludo++;
        saludo.escribirTexto("Hola, " + campoNombre.leerTexto() + "님! (" + númeroElementosSaludo + ")");
        Salida.escribirLínea("GUI Saludo: " + saludo.leerTexto());
    }

    public void ejecutarTarea() { abrirVentana(); }
    public void recibirAcción(NotificaciónAcción notificación) {
        Salida.escribirLínea("acción notificación: " + notificación.textoComando());
        saludar();
    }
    public static void ponerEnMarcha() {
        ColaEvento.invocarPosterior(new EjemploVentana());
    }
}
