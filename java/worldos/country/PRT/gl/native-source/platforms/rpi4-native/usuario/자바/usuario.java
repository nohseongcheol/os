// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 Ferramentas 전용 SVC Conectar. 기존 x86 Ferramentas 원문을 함께 빌드한다. */
public final class usuario {
    public static native int 파일서술자열기(int[] Nome, int Configuración);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int VALOR);
    public static native int 파일서술자닫기(int 서술자);
    public static native int 파일읽기(int[] Nome, int[] datos);
    public static native int escribir_Ficheiro(int[] Nome, int[] datos, int duración_VALOR);
    public static native int Escritura(String Texto);
    public static native int escribir_carácter_VALOR(int VALOR);
    public static native int 인수개수();
    public static native String Argumentos(int ÍNDICE);
    public static native int 도구번호();
    public static native int 화면연결(int Acción, int ÍNDICE, int 가, int 나, int 다, int 라);
    public static native int 화면글(int ÍNDICE, int[] Texto, int duración_VALOR);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int fluxo_control(int Acción, int 서술자, int VALOR);
    public static native int CONECTAR_fluxo(int 서술자, int ENDEREZO, int porto_VALOR);
    public static native int abrir_Rede(int porto_VALOR);
    public static native int enviar_Rede(int 서술자, int ENDEREZO, int porto_VALOR, int[] datos, int duración_VALOR);
    public static native int 통신받기(int 서술자, int[] datos, int duración_VALOR);
    public static native int Rede_porto(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int 사각형(int 가로, int Vertical_cargo, int 폭, int 높이, int 색);
}
