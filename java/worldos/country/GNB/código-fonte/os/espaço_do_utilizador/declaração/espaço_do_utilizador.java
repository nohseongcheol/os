// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros espaço_do_utilizador ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class espaço_do_utilizador {
    public static native int abrir_Arquivo_descritor(int[] Arquivo_entrada_nome, int abrir_Configurações);
    public static native int 파일한바이트읽기(int Arquivo_descritor);
    public static native int 파일한바이트쓰기(int Arquivo_descritor, int byte_VALOR);
    public static native int Close_Arquivo_descritor(int Arquivo_descritor);
    public static native int commit_Arquivos(int Arquivo_descritor);
    public static native int leitura_Arquivo(int[] Nome, int[] dados);
    public static native int gravar_caractere_VALOR(int 문자);
    public static native int gravar_Arquivo(int[] Nome, int[] dados, int duração_VALOR);
    public static native int Escrita(String Conteúdo_VALOR);
    public static native int 인수개수();
    public static native String argumentos(int ÍNDICE);
    public static native int execução_Permissão();
    public static native int abrir_rede(int local_porta);
    public static native int enviar_dados(int alça_VALOR, int Endereço, int destino_porta, int[] dados, int duração_VALOR);
    public static native int receber_dados(int alça_VALOR, int[] dados, int 제한밀리초);
    public static native int Close_rede(int alça_VALOR);
    public static native int 내주소();
    public static native int 보낸주소(int alça_VALOR);
    public static native int 보낸창구(int alça_VALOR);
}
