// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Português.nativo;
/** nativo JVM과 커널의 Janela 관리 기능에 직접 연결되는 Janela. */
public final class Janela extends tela_elemento {
    public Janela(String janela_Título, int 폭, int altura_VALOR) {
        throw new Estado_exceção("nativo JVM의 Português Janela gerar 기능이 필요합니다.");
    }
    public native void Adicionar_elemento(tela_elemento elemento_VALOR);
    public native void mostrar_janela();
    public native void Fechar();
    public native boolean 보이는가();
}
