// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 strumenti 전용 SVC Connetti. 기존 x86 strumenti 원문을 함께 빌드한다. */
public final class spazio_utente {
    public static native int aperto_File_descrittore(int[] Nome, int Impostazioni);
    public static native int 파일한바이트읽기(int descrittore_voce);
    public static native int 파일한바이트쓰기(int descrittore_voce, int VALORE);
    public static native int Chiudi_File_descrittore(int descrittore_voce);
    public static native int 파일읽기(int[] Nome, int[] dati);
    public static native int scrivere_File(int[] Nome, int[] dati, int durata_VALORE);
    public static native int Scrittura(String testo);
    public static native int scrivere_carattere_VALORE(int VALORE);
    public static native int 인수개수();
    public static native String argomenti(int INDICE);
    public static native int strumento_numero();
    public static native int schermata_connessione(int Azione, int INDICE, int 가, int SECONDO_operando, int 다, int 라);
    public static native int schermata_SMS(int INDICE, int[] testo, int durata_VALORE);
    public static native int 화면너비();
    public static native int schermata_altezza();
    public static native int Stream_controllo(int Azione, int descrittore_voce, int VALORE);
    public static native int CONNETTI_Stream(int descrittore_voce, int e_mail, int porta_VALORE);
    public static native int aperto_rete(int porta_VALORE);
    public static native int inviare_rete(int descrittore_voce, int e_mail, int porta_VALORE, int[] dati, int durata_VALORE);
    public static native int ricevere_rete(int descrittore_voce, int[] dati, int durata_VALORE);
    public static native int rete_porta(int descrittore_voce);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int rettangolo(int 가로, int Verticale_funzione, int 폭, int altezza_VALORE, int 색);
}
