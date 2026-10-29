// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros spazio_utente ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class spazio_utente {
    public static native int aperto_File_descrittore(int[] File_voce_nome, int aperto_Impostazioni);
    public static native int 파일한바이트읽기(int File_descrittore);
    public static native int 파일한바이트쓰기(int File_descrittore, int byte_VALORE);
    public static native int Chiudi_File_descrittore(int File_descrittore);
    public static native int commit_File(int File_descrittore);
    public static native int 파일읽기(int[] Nome, int[] dati);
    public static native int scrivere_carattere_VALORE(int 문자);
    public static native int scrivere_File(int[] Nome, int[] dati, int durata_VALORE);
    public static native int Scrittura(String Contenuto_VALORE);
    public static native int 인수개수();
    public static native String argomenti(int INDICE);
    public static native int esecuzione_privilegio();
    public static native int aperto_rete(int locale_porta);
    public static native int inviare_dati(int handle_VALORE, int e_mail, int meta_porta, int[] dati, int durata_VALORE);
    public static native int ricevere_dati(int handle_VALORE, int[] dati, int 제한밀리초);
    public static native int Chiudi_rete(int handle_VALORE);
    public static native int 내주소();
    public static native int 보낸주소(int handle_VALORE);
    public static native int 보낸창구(int handle_VALORE);
}
