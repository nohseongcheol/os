// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros usuari ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class usuari {
    public static native int 파일서술자열기(int[] arxiu_introducció_nom, int crear_Configuració);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int byte_VALOR);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int 파일저장확정(int 파일서술자);
    public static native int tancar_arxiu(int[] Nom, int[] dades);
    public static native int escriure_caràcter_VALOR(int 문자);
    public static native int escriure_arxiu(int[] Nom, int[] dades, int durada_VALOR);
    public static native int Escriptura(String contingut_VALOR);
    public static native int 인수개수();
    public static native String 인수(int INDEX);
    public static native int 실행권한();
    public static native int crear_xarxa(int local_port);
    public static native int enviar_dades(int control_VALOR_f011887b, int Adreça, int destinació_port, int[] dades, int durada_VALOR);
    public static native int rebre_dades(int control_VALOR_f011887b, int[] dades, int 제한밀리초);
    public static native int Tanca_xarxa(int control_VALOR_f011887b);
    public static native int 내주소();
    public static native int 보낸주소(int control_VALOR_f011887b);
    public static native int 보낸창구(int control_VALOR_f011887b);
}
