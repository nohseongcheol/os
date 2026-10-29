// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 màquina 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class Tauler {
    public static native int tancar_mostrar_píxel(int 가로, int Vertical_càrrec);
    public static native void escriure_mostrar_píxel(int 가로, int Vertical_càrrec, int 색);
    public static native int vigilància(int 종류, int Acció);
    public static native void finalitzar_remot_ordre(int Estat_VALOR);
    public static native void remot_Espera(int Estat_VALOR);
    public static native void 직렬쓰기(int VALOR);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int CPU_permís_nivell();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int Vertical_càrrec, int 색);
    public static native void RENDTO_CPU();
    public static native int Crear_tasca(int INDEX);
    public static native int tasca_Estat(int INDEX);
    public static native void Atura(int Estat_VALOR);
    public static native int 씨플러스시험();
    public static native int execució_usuari_programa(int INDEX);
    public static native int xec_usuari_programa();
    public static native int 인수준비(int element_COMPT);
    public static native int Executa_usuari_arxiu();
    public static native int 리눅스파일실행();
    public static native int arg_byte(int INDEX, int Posició, int VALOR);
    public static native int Terminal(int Acció);
    public static native int control_usuari_programa(int Acció);
    public static native void 입출력전환(int Acció);
    public static native int transferència_de_fitxers_servei(int Acció);
    public static native int xarxa_estat(int introducció_VALOR, int INDEX);
    public static native int xarxa_Configuració(int Acció, int Adreça, int màscara_VALOR, int passarel_la_VALOR);
    public static native int enviar_resposta(int Adreça, int comanda_VALOR);
    public static native int tancar_resposta(int introducció_VALOR);
    public static native int cerca_sistema(int introducció_VALOR, int INDEX);
    public static native void 전원끄기();
}
