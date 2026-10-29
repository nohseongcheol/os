// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Português.nativo;
/** nativo JVM tela 객체의 공통 계약. 표준 Swing 객체를 보관하지 않는다. */
public abstract class tela_elemento {
    public native String leitura_SMS();
    public native void gravar_SMS(String texto);
    public native void 자리정하기(int 가로, int Vertical_cargo, int 폭, int altura_VALOR);
}
