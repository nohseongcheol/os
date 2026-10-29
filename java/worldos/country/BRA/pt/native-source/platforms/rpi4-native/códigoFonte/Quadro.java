// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 computador limite_VALOR. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class Quadro {
    public static native int lerPíxelExibido(int 가로, int Vertical_cargo);
    public static native void escreverPíxelExibido(int 가로, int Vertical_cargo, int 색);
    public static native int sombreamento(int Tipo_VALOR, int Acção);
    public static native void encerrar_remoto_comando(int Estado_VALOR);
    public static native void remoto_aguarde(int Estado_VALOR);
    public static native void 직렬쓰기(int VALOR);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int CPU_permissão_nível();
    public static native int Preparar_tela();
    public static native int 화면너비();
    public static native int tela_altura();
    public static native void 화면점(int 가로, int Vertical_cargo, int 색);
    public static native void LUCRO_CPU();
    public static native int Criar_Tarefa(int ÍNDICE);
    public static native int Tarefa_Estado(int ÍNDICE);
    public static native void Parar(int Estado_VALOR);
    public static native int 씨플러스시험();
    public static native int executar_usuário_app(int ÍNDICE);
    public static native int cheque_usuário_app();
    public static native int 인수준비(int item_CONT_NÚM);
    public static native int Executar_usuário_Arquivo();
    public static native int 리눅스파일실행();
    public static native int argumento_byte(int ÍNDICE, int posição, int VALOR);
    public static native int terminal(int Acção);
    public static native int visual_usuário_app(int Acção);
    public static native void 입출력전환(int Acção);
    public static native int transferência_de_arquivo_serviço(int Acção);
    public static native int rede_Status(int entrada_VALOR_962f286b, int ÍNDICE);
    public static native int rede_Configurações(int Acção, int Endereço, int máscara_VALOR, int gateway_VALOR);
    public static native int enviar_réplica(int Endereço, int ordem_VALOR);
    public static native int leitura_réplica(int entrada_VALOR_962f286b);
    public static native int consulta_Sistema(int entrada_VALOR_962f286b, int ÍNDICE);
    public static native void 전원끄기();
}
