// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros usuario ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class usuario {
    public static native int 파일서술자열기(int[] Ficheiro_introdución_nome, int abrir_Configuración);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int byte_VALOR);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int 파일저장확정(int 파일서술자);
    public static native int 파일읽기(int[] Nome, int[] datos);
    public static native int escribir_carácter_VALOR(int 문자);
    public static native int escribir_Ficheiro(int[] Nome, int[] datos, int duración_VALOR);
    public static native int Escritura(String Contido_VALOR);
    public static native int 인수개수();
    public static native String Argumentos(int ÍNDICE);
    public static native int 실행권한();
    public static native int abrir_Rede(int local_porto);
    public static native int enviar_datos(int agarradoira_VALOR, int ENDEREZO, int destino_porto, int[] datos, int duración_VALOR);
    public static native int 자료받기(int agarradoira_VALOR, int[] datos, int 제한밀리초);
    public static native int peche_Rede(int agarradoira_VALOR);
    public static native int 내주소();
    public static native int 보낸주소(int agarradoira_VALOR);
    public static native int 보낸창구(int agarradoira_VALOR);
}
