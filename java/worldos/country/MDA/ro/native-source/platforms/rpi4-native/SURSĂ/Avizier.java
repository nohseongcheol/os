// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 mașină 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class Avizier {
    public static native int 표시화소읽기(int 가로, int Verticală_poziție);
    public static native void scriere_afișa_element_imagine(int 가로, int Verticală_poziție, int 색);
    public static native int control_la_distanță(int 종류, int Acțiuni);
    public static native void termina_un_apel_la_distanță_comandă(int Stare_VALUE);
    public static native void 원격대기(int Stare_VALUE);
    public static native void 직렬쓰기(int VALUE);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int CPU_permisiune_nivel();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int Verticală_poziție, int 색);
    public static native void YIELD_CPU();
    public static native int crea_sarcină(int INDEX);
    public static native int sarcină_Stare(int INDEX);
    public static native void Oprește(int Stare_VALUE);
    public static native int 씨플러스시험();
    public static native int rula_utilizator_program(int INDEX);
    public static native int verifica_utilizator_program();
    public static native int 인수준비(int element_COUNT);
    public static native int executa_utilizator_Fișier();
    public static native int 리눅스파일실행();
    public static native int argument_byte(int INDEX, int Poziție, int VALUE);
    public static native int Terminal(int Acțiuni);
    public static native int control_utilizator_program(int Acțiuni);
    public static native void 입출력전환(int Acțiuni);
    public static native int transfer_de_fișiere_serviciu(int Acțiuni);
    public static native int rețea_stare(int intrare_VALUE, int INDEX);
    public static native int rețea_Setări(int Acțiuni, int adresa, int mască_VALUE, int gateway_VALUE);
    public static native int trimite_răspuns(int adresa, int ordine_VALUE);
    public static native int 응답읽기(int intrare_VALUE);
    public static native int interoga_sistem(int intrare_VALUE, int INDEX);
    public static native void 전원끄기();
}
