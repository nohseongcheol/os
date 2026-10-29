// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 máquina 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class Panel {
    public static native int 표시화소읽기(int 가로, int Vertical_cargo);
    public static native void escribir_mostrar_píxel(int 가로, int Vertical_cargo, int 색);
    public static native int vixilancia(int 종류, int Acción);
    public static native void finalizar_remoto_comando(int Estado_VALOR);
    public static native void remoto_agarda(int Estado_VALOR);
    public static native void 직렬쓰기(int VALOR);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int CPU_permiso_nivel();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int Vertical_cargo, int 색);
    public static native void suspender_CPU();
    public static native int crear_tarefa(int ÍNDICE);
    public static native int tarefa_Estado(int ÍNDICE);
    public static native void Deter(int Estado_VALOR);
    public static native int 씨플러스시험();
    public static native int executar_usuario_apl(int ÍNDICE);
    public static native int cheque_usuario_apl();
    public static native int 인수준비(int elemento_CONTAR);
    public static native int executar_usuario_Ficheiro();
    public static native int 리눅스파일실행();
    public static native int argumento_byte(int ÍNDICE, int Posición, int VALOR);
    public static native int Terminal(int Acción);
    public static native int control_usuario_apl(int Acción);
    public static native void 입출력전환(int Acción);
    public static native int transferencia_de_ficheiros_servizo(int Acción);
    public static native int Rede_estado(int introdución_VALOR, int ÍNDICE);
    public static native int Rede_Configuración(int Acción, int ENDEREZO, int máscara_VALOR, int pasarela_VALOR);
    public static native int enviar_resposta(int ENDEREZO, int orde_VALOR);
    public static native int 응답읽기(int introdución_VALOR);
    public static native int consulta_sistema(int introdución_VALOR, int ÍNDICE);
    public static native void 전원끄기();
}
