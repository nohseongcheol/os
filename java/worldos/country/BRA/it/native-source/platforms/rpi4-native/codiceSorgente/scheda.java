// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 computer limite_VALORE. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class scheda {
    public static native int 표시화소읽기(int 가로, int Verticale_funzione);
    public static native void scrivere_display_pixel(int 가로, int Verticale_funzione, int 색);
    public static native int shadowing(int Kind_VALORE, int Azione);
    public static native void chiudere_remoto_comando(int Stato_VALORE);
    public static native void remoto_aspetta(int Stato_VALORE);
    public static native void scrivere_seriale(int VALORE);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int CPU_privilegio_livello();
    public static native int Prepara_schermata();
    public static native int 화면너비();
    public static native int schermata_altezza();
    public static native void 화면점(int 가로, int Verticale_funzione, int 색);
    public static native void REND_CPU();
    public static native int Crea_task(int INDICE);
    public static native int task_Stato(int INDICE);
    public static native void Ferma(int Stato_VALORE);
    public static native int 씨플러스시험();
    public static native int eseguire_USER_app(int INDICE);
    public static native int assegno_USER_app();
    public static native int 인수준비(int articolo_CONTA_NUMERI);
    public static native int Esegui_USER_File();
    public static native int 리눅스파일실행();
    public static native int argomento_byte(int INDICE, int posizione, int VALORE);
    public static native int terminale(int Azione);
    public static native int controllo_USER_app(int Azione);
    public static native void 입출력전환(int Azione);
    public static native int trasferimento_di_file_servizio(int Azione);
    public static native int rete_stato(int voce_VALORE, int INDICE);
    public static native int rete_Impostazioni(int Azione, int e_mail, int maschera_VALORE, int gateway_VALORE);
    public static native int inviare_risposta(int e_mail, int ordine_VALORE);
    public static native int 응답읽기(int voce_VALORE);
    public static native int query_Sistema(int voce_VALORE, int INDICE);
    public static native void 전원끄기();
}
