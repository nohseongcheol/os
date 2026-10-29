// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PCI RTL8139 (10ec:8139), 단일 inviare_VALORE 버퍼와 8KiB ricevere_VALORE Loop_VALORE. 인터럽트 대신 폴링한다. */
public final class rete_driver {
    static int 입출력기준주소 = 0;
    static int ricevere_funzione = 0, trasmettere_slot = 0;
    static int[] cellulare_e_mail = new int[6];
    static int trasmettere_CONTA_NUMERI = 0, ricevere_CONTA_NUMERI = 0, errore_CONTA_NUMERI = 0;

    static int 설정읽기(int cellulare_numero, int posizione) {
        cellulare_VALORE.입출력정수쓰기(0xcf8, 0x80000000 | (cellulare_numero << 11) | posizione);
        return cellulare_VALORE.입출력정수읽기(0xcfc);
    }

    static boolean Prepara() {
        int cellulare_numero = -1;
        for (int INDICE = 0; INDICE < 32; INDICE++) {
            if (설정읽기(INDICE, 0) == 0x813910ec) { cellulare_numero = INDICE; break; }
        }
        if (cellulare_numero < 0) return false;
        int valore_predefinito = 설정읽기(cellulare_numero, 0x10);
        if ((valore_predefinito & 1) == 0 || (valore_predefinito & 0xfffffffc) < 0x100 || (valore_predefinito & 0xfffffffc) > 65535) return false;
        입출력기준주소 = valore_predefinito & 0xfffc;
        int comando = 설정읽기(cellulare_numero, 4);
        cellulare_VALORE.입출력정수쓰기(0xcf8, 0x80000004 | (cellulare_numero << 11));
        cellulare_VALORE.입출력짧은수쓰기(0xcfc, comando | 5); // I/O 및 bus master Consenti_VALORE, PCI Stato_VALORE 비트는 건드리지 않음
        cellulare_VALORE.입출력바이트쓰기(입출력기준주소 + 0x52, 0);
        if (!ripristina_VALORE()) { 입출력기준주소 = 0; return false; }
        for (int INDICE = 0; INDICE < 6; INDICE++) cellulare_e_mail[INDICE] = cellulare_VALORE.입출력바이트읽기(입출력기준주소 + INDICE);
        return true;
    }

    static boolean ripristina_VALORE() {
        cellulare_VALORE.입출력바이트쓰기(입출력기준주소 + 0x37, 0x10);
        int avvia = cellulare_VALORE.밀리초();
        while ((cellulare_VALORE.입출력바이트읽기(입출력기준주소 + 0x37) & 0x10) != 0)
            if (cellulare_VALORE.밀리초() - avvia > 100) return false;
        ricevere_funzione = 0; trasmettere_slot = 0;
        cellulare_VALORE.입출력정수쓰기(입출력기준주소 + 0x30, cellulare_VALORE.rete_Memoria());
        for (int INDICE = 0; INDICE < 4; INDICE++) cellulare_VALORE.입출력정수쓰기(입출력기준주소 + 0x20 + INDICE * 4, cellulare_VALORE.rete_Memoria() + 12288);
        cellulare_VALORE.입출력짧은수쓰기(입출력기준주소 + 0x3c, 0);
        cellulare_VALORE.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0xffff);
        cellulare_VALORE.입출력바이트쓰기(입출력기준주소 + 0x37, 0x0c);
        cellulare_VALORE.입출력정수쓰기(입출력기준주소 + 0x44, 0x0000e78a); // 자기주소/trasmesso_VALORE, wrap 연속 Store_VALORE, 8KiB
        cellulare_VALORE.입출력정수쓰기(입출력기준주소 + 0x40, 0x03000600);
        return true;
    }

    static int inviare(int[] dati, int durata_VALORE) {
        if (입출력기준주소 == 0) return -19;
        if (durata_VALORE < 14 || durata_VALORE > 1514) return -90;
        int stato_porta = 입출력기준주소 + 0x10 + trasmettere_slot * 4;
        int avvia = cellulare_VALORE.밀리초();
        while ((cellulare_VALORE.입출력정수읽기(stato_porta) & 0x2000) == 0)
            if (cellulare_VALORE.밀리초() - avvia > 100) return -110;
        int Dimensione = durata_VALORE < 60 ? 60 : durata_VALORE;
        for (int INDICE = 0; INDICE < Dimensione; INDICE++)
            cellulare_VALORE.scrivere_Memoria(cellulare_VALORE.rete_Memoria() + 12288 + INDICE, INDICE < durata_VALORE ? dati[INDICE] : 0);
        cellulare_VALORE.입출력정수쓰기(stato_porta, Dimensione | 0x00080000);
        avvia = cellulare_VALORE.밀리초();
        while ((cellulare_VALORE.입출력정수읽기(stato_porta) & 0xe0008000) == 0)
            if (cellulare_VALORE.밀리초() - avvia > 100) return -110;
        if ((cellulare_VALORE.입출력정수읽기(stato_porta) & 0x8000) == 0) { errore_CONTA_NUMERI++; return -5; }
        trasmettere_slot = (trasmettere_slot + 1) & 3;
        trasmettere_CONTA_NUMERI++;
        return durata_VALORE;
    }

    static int ricevere(int[] dati) {
        if (입출력기준주소 == 0) return 0;
        if ((cellulare_VALORE.입출력바이트읽기(입출력기준주소 + 0x3e) & 0x50) != 0) {
            errore_CONTA_NUMERI++;
            if (!ripristina_VALORE()) 입출력기준주소 = 0;
            return 0;
        }
        if ((cellulare_VALORE.입출력바이트읽기(입출력기준주소 + 0x37) & 1) != 0) return 0;
        int intestazione_VALORE = cellulare_VALORE.rete_Memoria() + ricevere_funzione;
        int Stato_VALORE = esecuzione_manager.짧은수(intestazione_VALORE), Dimensione = esecuzione_manager.짧은수(intestazione_VALORE + 2);
        if (Dimensione == 0xfff0) return 0; // DMA 진행 중
        if (Dimensione < 4 || Dimensione > 1518) {
            errore_CONTA_NUMERI++;
            if (!ripristina_VALORE()) 입출력기준주소 = 0;
            return 0;
        }
        int durata_VALORE = Dimensione - 4;
        if ((Stato_VALORE & 1) != 0) {
            for (int INDICE = 0; INDICE < durata_VALORE; INDICE++) dati[INDICE] = cellulare_VALORE.기억읽기(intestazione_VALORE + 4 + INDICE);
            ricevere_CONTA_NUMERI++;
        } else { durata_VALORE = 0; errore_CONTA_NUMERI++; }
        ricevere_funzione = (ricevere_funzione + Dimensione + 4 + 3) & ~3;
        ricevere_funzione &= 8191;
        cellulare_VALORE.입출력짧은수쓰기(입출력기준주소 + 0x38, (ricevere_funzione - 16) & 65535);
        cellulare_VALORE.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0x000f);
        return durata_VALORE;
    }
}
