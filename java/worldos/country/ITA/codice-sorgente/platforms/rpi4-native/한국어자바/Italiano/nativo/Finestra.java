// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Italiano.nativo;
/** nativo JVM과 커널의 Finestra 관리 기능에 직접 연결되는 Finestra. */
public final class Finestra extends schermata_elemento {
    public Finestra(String finestra_titolo, int 폭, int altezza_VALORE) {
        throw new Stato_eccezione("nativo JVM의 Italiano Finestra generare 기능이 필요합니다.");
    }
    public native void Aggiungi_elemento(schermata_elemento elemento_VALORE);
    public native void mostrare_finestra();
    public native void Chiudi();
    public native boolean 보이는가();
}
