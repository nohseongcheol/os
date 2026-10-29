// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package español.Java;

import javax.swing.*;

public final class Pantalla {
    private Pantalla() {}
    public static void valorPosterior(Runnable acción) { SwingUtilities.invokeLater(acción); }
    /** Invocar en el hilo de distribución de eventos de Swing. */
    public static JFrame ventana(String títuloVentana, JComponent valorContenidoValor, int valorAnchura, int valorAltura) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("Pantalla.valorPosterior 안에서 창을 만드세요");
        JFrame ventana = new JFrame(títuloVentana);
        ventana.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        ventana.setContentPane(valorContenidoValor);
        ventana.setSize(valorAnchura, valorAltura);
        ventana.setLocationByPlatform(true);
        ventana.setVisible(true);
        return ventana;
    }
}
