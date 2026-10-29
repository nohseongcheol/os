// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Português.자바;

import javax.swing.*;

public final class tela {
    private tela() {}
    public static void 나중에(Runnable Acção) { SwingUtilities.invokeLater(Acção); }
    /** Swing 이벤트 Processo_VALOR_entrada 가닥에서 호출한다. */
    public static JFrame Janela(String janela_Título, JComponent Conteúdo_VALOR, int 너비, int altura_VALOR) {
        if (!SwingUtilities.isEventDispatchThread())
            throw new IllegalStateException("tela.나중에 안에서 창을 만드세요");
        JFrame Janela = new JFrame(janela_Título);
        Janela.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Janela.setContentPane(Conteúdo_VALOR);
        Janela.setSize(너비, altura_VALOR);
        Janela.setLocationByPlatform(true);
        Janela.setVisible(true);
        return Janela;
    }
}
