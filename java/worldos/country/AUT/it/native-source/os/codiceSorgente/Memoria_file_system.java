// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 세션 동안 유지되는 8개 file. 원본 Modifica_VALORE/compilare_fonte errore_VALORE 시 기존 파일을 보존한다. */
public final class Memoria_file_system {
    static final int 최대크기 = 16384;
    static int[] 이름들 = new int[8 * 64];
    static int[] ridimensionare_elenco = new int[8];
    static int[] aperto_CONTA_NUMERI = new int[8], 허가들 = new int[8];
    static int[] Nome = new int[64];
    static int[] Modifica_VALORE = new int[최대크기];
    static boolean 편집중 = false;
    static boolean overflow_VALORE = false;
    static int Modifica_ridimensionare = 0;

    static boolean assegno_nome(int[] carattere_VALORE, int durata_VALORE) {
        if (durata_VALORE < 1 || durata_VALORE > 63) return false;
        for (int numero = 0; numero < durata_VALORE; numero++) {
            int VALORE = carattere_VALORE[numero];
            if (!(VALORE >= 'a' && VALORE <= 'z') && !(VALORE >= 'A' && VALORE <= 'Z')
                && !(VALORE >= '0' && VALORE <= '9') && VALORE != '_' && VALORE != '-' && VALORE != '.') return false;
        }
        return carattere_VALORE[0] != '.';
    }

    static int TROVA_voce(int[] carattere_VALORE, int durata_VALORE) {
        if (!assegno_nome(carattere_VALORE, durata_VALORE)) return -22;
        for (int numero = 0; numero < 8; numero++) {
            boolean 같음 = 이름들[numero * 64 + durata_VALORE] == 0;
            for (int slot_voce = 0; slot_voce < durata_VALORE; slot_voce++) if (이름들[numero * 64 + slot_voce] != carattere_VALORE[slot_voce]) 같음 = false;
            if (같음) return numero;
        }
        return -2;
    }

    static int Store_VALORE(int[] carattere_VALORE, int durata_VALORE, int[] dati, int Dimensione) {
        if (!assegno_nome(carattere_VALORE, durata_VALORE) || Dimensione < 0 || Dimensione > dati.length) return -22;
        if (Dimensione > 최대크기) return -90;
        int INDICE = TROVA_voce(carattere_VALORE, durata_VALORE);
        if (INDICE == -2) {
            for (int numero = 0; numero < 8 && INDICE < 0; numero++) if (이름들[numero * 64] == 0 && aperto_CONTA_NUMERI[numero] == 0) INDICE = numero;
            if (INDICE >= 0) 허가들[INDICE] = 438;
        }
        if (INDICE < 0) return -28;
        int e_mail = cellulare_VALORE.File_Memoria() + INDICE * 최대크기;
        for (int numero = 0; numero < Dimensione; numero++) cellulare_VALORE.scrivere_Memoria(e_mail + numero, dati[numero]);
        for (int numero = 0; numero < 64; numero++) 이름들[INDICE * 64 + numero] = numero < durata_VALORE ? carattere_VALORE[numero] : 0;
        ridimensionare_elenco[INDICE] = Dimensione;
        return Dimensione;
    }

    static void voce_elenco() {
        for (int numero = 0; numero < 8; numero++) if (이름들[numero * 64] != 0) {
            for (int slot_voce = 0; slot_voce < 64 && 이름들[numero * 64 + slot_voce] != 0; slot_voce++) SMS_Terminale.문자(이름들[numero * 64 + slot_voce]);
            SMS_Terminale.Scrittura("  "); SMS_Terminale.scrivere_numero(ridimensionare_elenco[numero]); SMS_Terminale.Scrittura("byte_VALORE\n");
        }
        SMS_Terminale.Scrittura(dispositivo_di_archiviazione_connessione.reparto_IT_Disponibile ? "file 8칸, 파일당 16384바이트; sync로 Store_VALORE 장치에 보존\n"
            : "임시 file 8칸, 파일당 16384바이트; retry_VALORE 시작하면 사라짐\n");
    }

    static void comando(int[] input_VALORE, int avvia, int durata_VALORE, int Azione) {
        while (avvia < durata_VALORE && input_VALORE[avvia] == ' ') avvia++;
        int 끝 = durata_VALORE;
        while (끝 > avvia && input_VALORE[끝 - 1] == ' ') 끝--;
        int numero = 끝 - avvia;
        if (numero < 1 || numero > 63) { SMS_Terminale.Scrittura("올바르지 않은 file Nome\n"); return; }
        for (int slot_voce = 0; slot_voce < 64; slot_voce++) Nome[slot_voce] = slot_voce < numero ? input_VALORE[avvia + slot_voce] : 0;
        int INDICE = TROVA_voce(Nome, numero);
        if (INDICE == -22) { SMS_Terminale.Scrittura("올바르지 않은 file Nome\n"); return; }
        if (Azione == 0) {
            편집중 = true; Modifica_ridimensionare = 0; overflow_VALORE = false;
            SMS_Terminale.Scrittura("원문을 입력하세요. .save는 보존, .cancel은 취소합니다.\n");
        } else if (INDICE < 0) SMS_Terminale.Scrittura("파일을 찾을 numero 없습니다\n");
        else if (Azione == 1) {
            int e_mail = cellulare_VALORE.File_Memoria() + INDICE * 최대크기;
            for (int slot_voce = 0; slot_voce < ridimensionare_elenco[INDICE]; slot_voce++) SMS_Terminale.문자(cellulare_VALORE.기억읽기(e_mail + slot_voce));
            SMS_Terminale.문자(10);
        } else { 이름들[INDICE * 64] = 0; ridimensionare_elenco[INDICE] = 0; SMS_Terminale.Scrittura("파일을 지웠습니다\n"); }
    }

    static boolean reparto_IT_IDENTICO(int[] input_VALORE, int durata_VALORE, String 문구) {
        if (durata_VALORE != 문구.length()) return false;
        for (int slot_voce = 0; slot_voce < durata_VALORE; slot_voce++) if (input_VALORE[slot_voce] != 문구.charAt(slot_voce)) return false;
        return true;
    }

    static void Modificati_riga(int[] input_VALORE, int durata_VALORE, boolean riga_overflow) {
        if (reparto_IT_IDENTICO(input_VALORE, durata_VALORE, ".cancel")) {
            편집중 = false; SMS_Terminale.Scrittura("취소했습니다. 원래 파일은 그대로입니다\n");
        } else if (reparto_IT_IDENTICO(input_VALORE, durata_VALORE, ".save")) {
            편집중 = false;
            if (overflow_VALORE) { SMS_Terminale.Scrittura("입력이 너무 깁니다. 원래 파일은 그대로입니다\n"); return; }
            int numero = 0;
            while (numero < 64 && Nome[numero] != 0) numero++;
            int risultato = Store_VALORE(Nome, numero, Modifica_VALORE, Modifica_ridimensionare);
            SMS_Terminale.Scrittura(risultato >= 0 ? "보존한 byte_VALORE numero: " : "보존 errore_VALORE: ");
            SMS_Terminale.scrivere_numero(risultato); SMS_Terminale.문자(10);
        } else if (riga_overflow || durata_VALORE + 1 > 최대크기 - Modifica_ridimensionare) overflow_VALORE = true;
        else {
            for (int numero = 0; numero < durata_VALORE; numero++) Modifica_VALORE[Modifica_ridimensionare++] = input_VALORE[numero];
            Modifica_VALORE[Modifica_ridimensionare++] = 10;
        }
    }

    static void 예제(String file, String Contenuto_VALORE) {
        for (int numero = 0; numero < 64; numero++) Nome[numero] = numero < file.length() ? file.charAt(numero) : 0;
        for (int numero = 0; numero < Contenuto_VALORE.length(); numero++) Modifica_VALORE[numero] = Contenuto_VALORE.charAt(numero);
        Store_VALORE(Nome, file.length(), Modifica_VALORE, Contenuto_VALORE.length());
    }

    static void Prepara() {
        예제("Hello.java", "public class Hello {\n public static void main(String[] args) {\n  System.out.println(\"Hello from jkoros JVM!\");\n  int sum = 0;\n  for (int i = 1; i <= 10; i++) { sum = sum + i; }\n  System.out.println(sum);\n }\n}\n");
        int gruppo_VALORE = cellulare_VALORE.자바파일묶음(), Dimensione = cellulare_VALORE.자바파일묶음크기();
        if (Dimensione < 8 || esecuzione_manager.numero(gruppo_VALORE) != 0x464a4b4a) { SMS_Terminale.Scrittura("올바르지 않은 Java file gruppo_VALORE\n"); return; }
        int articolo_CONTA_NUMERI = esecuzione_manager.numero(gruppo_VALORE + 4);
        if (articolo_CONTA_NUMERI < 0 || articolo_CONTA_NUMERI > 8 || articolo_CONTA_NUMERI > (Dimensione - 8) / 72) { SMS_Terminale.Scrittura("올바르지 않은 Java file voce_elenco\n"); return; }
        for (int numero = 0; numero < articolo_CONTA_NUMERI; numero++) {
            int voce_VALORE = gruppo_VALORE + 8 + numero * 72, durata_VALORE = 0;
            for (int slot_voce = 0; slot_voce < 64; slot_voce++) Nome[slot_voce] = cellulare_VALORE.기억읽기(voce_VALORE + slot_voce);
            while (durata_VALORE < 64 && Nome[durata_VALORE] != 0) durata_VALORE++;
            int posizione = esecuzione_manager.numero(voce_VALORE + 64), dimensioni_del_file = esecuzione_manager.numero(voce_VALORE + 68);
            if (!assegno_nome(Nome, durata_VALORE) || dimensioni_del_file < 0 || dimensioni_del_file > 최대크기 || posizione < 8 + articolo_CONTA_NUMERI * 72 || posizione > Dimensione - dimensioni_del_file) {
                SMS_Terminale.Scrittura("올바르지 않은 Java file voce_VALORE\n"); return;
            }
            for (int slot_voce = 0; slot_voce < dimensioni_del_file; slot_voce++) Modifica_VALORE[slot_voce] = cellulare_VALORE.기억읽기(gruppo_VALORE + posizione + slot_voce);
            if (Store_VALORE(Nome, durata_VALORE, Modifica_VALORE, dimensioni_del_file) < 0) { SMS_Terminale.Scrittura("Java 파일을 가져오지 못했습니다\n"); return; }
        }
    }
}
