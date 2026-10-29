// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Português.nativo;
/** tela(畫面): arranque_da_máquina 때 선택한 크기의 nativo kernel_VALOR RGB32 프레임버퍼. */
public final class tela {
    private tela() {}
    public static int 너비() { int VALOR = kernel_VALOR.화면너비(); if (VALOR < 0) throw new Estado_exceção("프레임버퍼 없음"); return VALOR; }
    public static int altura_VALOR() { int VALOR = kernel_VALOR.tela_altura(); if (VALOR < 0) throw new Estado_exceção("프레임버퍼 없음"); return VALOR; }
    public static void retângulo(int 가로, int Vertical_cargo, int 폭, int altura_VALOR, int 색) {
        if (가로 < 0 || Vertical_cargo < 0 || 폭 < 0 || altura_VALOR < 0 || 가로 > 너비() || Vertical_cargo > altura_VALOR() || 폭 > 너비() - 가로 || altura_VALOR > altura_VALOR() - Vertical_cargo) throw new inválido_argumento_exceção("tela recortar");
        if (kernel_VALOR.retângulo(가로, Vertical_cargo, 폭, altura_VALOR, 색) < 0) throw new Estado_exceção("프레임버퍼 없음");
    }
    public static void apagar_entrada(int 색) { retângulo(0, 0, 너비(), altura_VALOR(), 색); }
    public static void 기다리기() { if (kernel_VALOR.그림대기() < 0) throw new Estado_exceção("interativo entrada_VALOR 필요"); }
}
