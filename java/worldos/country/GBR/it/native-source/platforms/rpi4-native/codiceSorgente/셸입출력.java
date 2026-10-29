// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 파이프는 16 KiB씩 순서대로 실행한다. 프로세스/동시 파이프를 흉내 내지 않는다. */
public final class 셸입출력 {
    static int[] input_dati = new int[16384], output_dati = new int[16384];
    static int input_durata, input_funzione, output_durata, file_di_input = -1, file_di_output = -1;
    static boolean pipe_input, pipe_output;
    static int errore_VALORE;
    static boolean Consenti_interattivo = true;
    public static int reparto_IT_interattivo() { return Consenti_interattivo && file_di_input < 3 && file_di_output < 3 && !pipe_input && !pipe_output ? 1 : 0; }
    public static int uscitaTesto(int Canale_VALORE, int VALORE) {
        if (Canale_VALORE != 1) return 0;
        if (file_di_output >= 3) { int 처리값 = FileMemoria.Scrittura(file_di_output, VALORE); if (처리값 < 0) errore_VALORE = 처리값; return 1; }
        if (!pipe_output) return 0;
        if (output_durata == output_dati.length) errore_VALORE = -28;
        else output_dati[output_durata++] = VALORE;
        return 1;
    }
    public static int input_VALORE() {
        if (file_di_input >= 3) { int 처리값 = FileMemoria.Lettura(file_di_input); return 처리값 == 256 ? -2 : 처리값; }
        if (pipe_input) return input_funzione < input_durata ? input_dati[input_funzione++] : -2;
        return -3; // UART로 Avanti_VALORE
    }
    static void avvia(boolean interlinea_pipe, boolean finale_pipe) {
        pipe_input = interlinea_pipe; pipe_output = finale_pipe;
        input_funzione = 0; output_durata = 0; file_di_input = -1; file_di_output = -1; errore_VALORE = 0;
    }
    static void 끝() {
        scheda.입출력전환(0);
        if (file_di_input >= 3) FileMemoria.Chiudi(file_di_input);
        if (file_di_output >= 3) FileMemoria.Chiudi(file_di_output);
        if (pipe_output) { input_durata = output_durata; for (int Loop_INDICE = 0; Loop_INDICE < output_durata; Loop_INDICE++) input_dati[Loop_INDICE] = output_dati[Loop_INDICE]; }
        file_di_input = -1; file_di_output = -1; pipe_input = false; pipe_output = false;
    }
}
