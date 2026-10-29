// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Italiano.nativo;
/** schermata(畫面): avvio_macchina 때 선택한 크기의 nativo kernel_VALORE RGB32 프레임버퍼. */
public final class schermata {
    private schermata() {}
    public static int 너비() { int VALORE = kernel_VALORE.화면너비(); if (VALORE < 0) throw new Stato_eccezione("프레임버퍼 없음"); return VALORE; }
    public static int altezza_VALORE() { int VALORE = kernel_VALORE.schermata_altezza(); if (VALORE < 0) throw new Stato_eccezione("프레임버퍼 없음"); return VALORE; }
    public static void rettangolo(int 가로, int Verticale_funzione, int 폭, int altezza_VALORE, int 색) {
        if (가로 < 0 || Verticale_funzione < 0 || 폭 < 0 || altezza_VALORE < 0 || 가로 > 너비() || Verticale_funzione > altezza_VALORE() || 폭 > 너비() - 가로 || altezza_VALORE > altezza_VALORE() - Verticale_funzione) throw new non_valida_argomento_eccezione("schermata ritagliare");
        if (kernel_VALORE.rettangolo(가로, Verticale_funzione, 폭, altezza_VALORE, 색) < 0) throw new Stato_eccezione("프레임버퍼 없음");
    }
    public static void cancellare_voce(int 색) { rettangolo(0, 0, 너비(), altezza_VALORE(), 색); }
    public static void 기다리기() { if (kernel_VALORE.그림대기() < 0) throw new Stato_eccezione("interattivo input_VALORE 필요"); }
}
