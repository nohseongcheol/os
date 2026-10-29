// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 ferramentas 전용 SVC Ligar. 기존 x86 ferramentas 원문을 함께 빌드한다. */
public final class espaço_do_utilizador {
    public static native int abrir_Arquivo_descritor(int[] Nome, int Definições);
    public static native int 파일한바이트읽기(int descritor_entrada);
    public static native int 파일한바이트쓰기(int descritor_entrada, int VALOR);
    public static native int Close_Arquivo_descritor(int descritor_entrada);
    public static native int leitura_Arquivo(int[] Nome, int[] dados);
    public static native int gravar_Arquivo(int[] Nome, int[] dados, int duração_VALOR);
    public static native int Escrita(String texto);
    public static native int gravar_caractere_VALOR(int VALOR);
    public static native int 인수개수();
    public static native String argumentos(int ÍNDICE);
    public static native int ferramenta_número();
    public static native int tela_conexão(int Acção, int ÍNDICE, int 가, int SEGUNDO_operando, int 다, int 라);
    public static native int tela_SMS(int ÍNDICE, int[] texto, int duração_VALOR);
    public static native int 화면너비();
    public static native int tela_altura();
    public static native int fluxo_visual(int Acção, int descritor_entrada, int VALOR);
    public static native int Conexão_fluxo(int descritor_entrada, int Endereço, int porta_VALOR);
    public static native int abrir_rede(int porta_VALOR);
    public static native int enviar_rede(int descritor_entrada, int Endereço, int porta_VALOR, int[] dados, int duração_VALOR);
    public static native int receber_rede(int descritor_entrada, int[] dados, int duração_VALOR);
    public static native int rede_porta(int descritor_entrada);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int retângulo(int 가로, int Vertical_cargo, int 폭, int altura_VALOR, int 색);
}
