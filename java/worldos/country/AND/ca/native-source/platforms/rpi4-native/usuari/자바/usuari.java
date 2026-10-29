// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 Eines 전용 SVC Connecta. 기존 x86 Eines 원문을 함께 빌드한다. */
public final class usuari {
    public static native int 파일서술자열기(int[] Nom, int Ajusts);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int VALOR);
    public static native int 파일서술자닫기(int 서술자);
    public static native int tancar_arxiu(int[] Nom, int[] dades);
    public static native int escriure_arxiu(int[] Nom, int[] dades, int durada_VALOR);
    public static native int Escriptura(String SMS);
    public static native int escriure_caràcter_VALOR(int VALOR);
    public static native int 인수개수();
    public static native String 인수(int INDEX);
    public static native int 도구번호();
    public static native int 화면연결(int Acció, int INDEX, int 가, int 나, int 다, int 라);
    public static native int 화면글(int INDEX, int[] SMS, int durada_VALOR);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int flux_control(int Acció, int 서술자, int VALOR);
    public static native int CONNECTA_flux(int 서술자, int Adreça, int port_VALOR);
    public static native int crear_xarxa(int port_VALOR);
    public static native int enviar_xarxa(int 서술자, int Adreça, int port_VALOR, int[] dades, int durada_VALOR);
    public static native int rebre_xarxa(int 서술자, int[] dades, int durada_VALOR);
    public static native int xarxa_port(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int 사각형(int 가로, int Vertical_càrrec, int 폭, int 높이, int 색);
}
