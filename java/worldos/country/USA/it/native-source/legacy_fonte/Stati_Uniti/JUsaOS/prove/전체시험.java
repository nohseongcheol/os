// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Stati_Uniti.JUsaOS.prove;

import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import Stati_Uniti.JUsaOS.Memoria_area.Memoria_manager;
import Stati_Uniti.JUsaOS.Memoria_area.Gestione_pagine;
import Stati_Uniti.JUsaOS.input_VALORE.evento_di_input;
import Stati_Uniti.JUsaOS.작업.Processi_VALORE;
import Stati_Uniti.JUsaOS.chiamata_di_sistema.chiamata_di_sistema;
import Stati_Uniti.JUsaOS.file_system.eseguibile_caricatore;
import Stati_Uniti.JUsaOS.Nucleo.Nucleo;
import Stati_Uniti.JUsaOS.host.host_hardware;
import Stati_Uniti.JUsaOS.IRQ.IRQ_manager;
import Stati_Uniti.JUsaOS.descrittore_voce.tabella_dei_descrittori_globali;
import Stati_Uniti.JUsaOS.dispositivo_di_archiviazione.고급기술결합장치;
import Stati_Uniti.JUsaOS.cellulare_VALORE.accessorio_bus_manager;
import Stati_Uniti.JUsaOS.rete_Pila.rete_Strumenti;
import Stati_Uniti.JUsaOS.rete_Pila.livello_rete;
import Stati_Uniti.JUsaOS.cellulare_VALORE.clock;
import Stati_Uniti.JUsaOS.descrittore_voce.task_Stato_segmento;
import Stati_Uniti.JUsaOS.schermata.carattere_display;
import Stati_Uniti.JUsaOS.file_system.partizione_primaria_tabella;

public final class 전체시험 {
    private static int passare_CONTA_NUMERI;

    private 전체시험() {
    }

    public static void main(String[] parametro_argomento) {
        host_hardware cellulare_VALORE = new host_hardware();
        Nucleo kernel_VALORE = new Nucleo(cellulare_VALORE);
        kernel_VALORE.avvia();

        test_Memoria(kernel_VALORE);
        쪽관리시험(kernel_VALORE);
        파일과과정시험(kernel_VALORE);
        실행파일시험(kernel_VALORE);
        test_input(kernel_VALORE);
        test_hardware(cellulare_VALORE);
        개입중단과서술자시험();
        test_Memoria_E_Rete();
        test_schermata_E_clock();

        System.out.println("JUsaOS prove passare_VALORE: " + passare_CONTA_NUMERI);
    }

    private static void test_Memoria(Nucleo kernel_VALORE) {
        Memoria_manager manager_VALORE = kernel_VALORE.Memoria_area();
        int 첫주소 = manager_VALORE.정렬할당(100, 64);
        verificare((첫주소 & 63) == 0, "allineare_VALORE allocare_Memoria");
        manager_VALORE.scrivere_byte_VALORE(첫주소, (byte) 0x5a);
        verificare(manager_VALORE.바이트읽기(첫주소) == (byte) 0x5a, "물리 Memoria_area 읽고 Scrittura");
        int 사용전 = manager_VALORE.사용크기();
        manager_VALORE.release_Memoria(첫주소);
        verificare(manager_VALORE.사용크기() < 사용전, "Memoria_area release_Memoria");
    }

    private static void 쪽관리시험(Nucleo kernel_VALORE) {
        Gestione_pagine manager_VALORE = kernel_VALORE.쪽관리();
        Gestione_pagine.spazio_indirizzi padre_Space = manager_VALORE.새주소공간();
        manager_VALORE.MAP_pagina(padre_Space, 0x1000, true);
        manager_VALORE.scrivere_byte_VALORE(padre_Space, 0x1010, (byte) 7);
        Gestione_pagine.spazio_indirizzi figlio_Space = manager_VALORE.clone_copia_su_scrittura(padre_Space);
        manager_VALORE.scrivere_byte_VALORE(figlio_Space, 0x1010, (byte) 9);
        verificare(manager_VALORE.바이트읽기(padre_Space, 0x1010) == 7, "Scrittura 시 copiare_VALORE padre_VALORE 격리");
        verificare(manager_VALORE.바이트읽기(figlio_Space, 0x1010) == 9, "Scrittura 시 copiare_VALORE figlio_VALORE Scrittura");
    }

    private static void 파일과과정시험(Nucleo kernel_VALORE) {
        byte[] Contenuto_VALORE = "안녕하세요".getBytes(StandardCharsets.UTF_8);
        kernel_VALORE.file_system().Aggiunta_File("prove", Contenuto_VALORE);
        Processi_VALORE padre_VALORE = kernel_VALORE.첫과정();
        chiamata_di_sistema 호출 = kernel_VALORE.chiamata_di_sistema();
        int descrittore_voce = 호출.Apri(padre_VALORE, "/prove", chiamata_di_sistema.di_sola_lettura_flag);
        verificare(descrittore_voce >= 3, "file Apri");

        byte[] ricevere_meta = new byte[Contenuto_VALORE.length];
        verificare(호출.Lettura(padre_VALORE, descrittore_voce, ricevere_meta, ricevere_meta.length) == Contenuto_VALORE.length, "file Lettura");
        verificare(Arrays.equals(Contenuto_VALORE, ricevere_meta), "file Contenuto_VALORE");
        verificare(호출.spostare_funzione(padre_VALORE, descrittore_voce, 0, chiamata_di_sistema.Cerca_START) == 0, "file posizione spostare_VALORE");

        int 복제서술자 = 호출.Duplica_descrittore(padre_VALORE, descrittore_voce);
        verificare(복제서술자 >= 0, "descrittore_voce clone_VALORE");
        Processi_VALORE figlio_VALORE = 호출.clone_Processi(padre_VALORE);
        verificare(figlio_VALORE.identificatore_VALORE() != padre_VALORE.identificatore_VALORE(), "Processi_VALORE identificatore_VALORE 분리");
        verificare(figlio_VALORE.padre_identificatore() == padre_VALORE.identificatore_VALORE(), "padre_VALORE Processi_VALORE identificatore_VALORE");
        verificare(호출.Chiudi(figlio_VALORE, descrittore_voce) == 0 && padre_VALORE.File_descrittore().reparto_IT_aperto(descrittore_voce), "figlio_VALORE Chiudi 격리");

        int Indietro_chiudere = 호출.aumento_app_pausa(padre_VALORE, 8192);
        verificare(Indietro_chiudere == 0x06000000, "app_f5044b9b 끝 늘리기");
        verificare(padre_VALORE.app_pausa() == 0x06002000, "app_f5044b9b 끝 반영");
        verificare(figlio_VALORE.app_pausa() == 0x06000000, "과정별 app_f5044b9b 끝 격리");

        figlio_VALORE.Esci_app(7);
        verificare(호출.자식기다리기(padre_VALORE, figlio_VALORE.identificatore_VALORE(), false) == (7 << 8), "figlio_VALORE Esci_app 기다리기");
        verificare(호출.접근가능("prove", 1) == -13, "Esegui_comando privilegio_VALORE rifiutare_VALORE");
        verificare(호출.UID() == 0 && 호출.GID() == 0, "사용자와 무리 identificatore_VALORE");
        verificare("/".equals(호출.Regolari_Elenco_attività(2)) && 호출.SWITCH_Elenco_attività("/") == 0, "Regolari_articolo 작업 voce_elenco");
        verificare(호출.reparto_IT_Terminale(padre_VALORE, 1), "표준 uscitaTesto 단말");
        verificare("JUsaOS".equals(호출.Sistema_Dettagli().Sistema_nome()), "sistema_operativo_VALORE msinfo32_exe");
    }

    private static void 실행파일시험(Nucleo kernel_VALORE) {
        byte[] dati = new byte[92];
        dati[0] = 0x7f;
        dati[1] = 'E';
        dati[2] = 'L';
        dati[3] = 'F';
        dati[4] = 1;
        dati[5] = 1;
        scrivere_intero_VALORE(dati, 24, 0x04001000);
        scrivere_intero_VALORE(dati, 32, 52);
        짧은정수쓰기(dati, 46, 40);
        짧은정수쓰기(dati, 48, 1);
        scrivere_intero_VALORE(dati, 56, 8);
        scrivere_intero_VALORE(dati, 60, 2);
        scrivere_intero_VALORE(dati, 64, 0x04002000);
        scrivere_intero_VALORE(dati, 72, 64);

        eseguibile_caricatore.foto foto_VALORE = new eseguibile_caricatore().검사(dati);
        verificare(foto_VALORE.START_e_mail() == 0x04001000, "ELF avvia e_mail");
        verificare(foto_VALORE.구역들().size() == 1 && foto_VALORE.구역들().get(0).Kind_VALORE() == 8, "ELF 빈 dati sezione_VALORE");
        int descrittore_voce = kernel_VALORE.chiamata_di_sistema().Apri(kernel_VALORE.첫과정(), "prove", chiamata_di_sistema.di_sola_lettura_flag);
        verificare(kernel_VALORE.chiamata_di_sistema().controllo_file(kernel_VALORE.첫과정(), descrittore_voce, 2, 1) == 0, "Esegui_comando 시 Chiudi Impostazioni");
        verificare(kernel_VALORE.chiamata_di_sistema().Esegui_comando(kernel_VALORE.첫과정(), dati, new String[] {"prove", "값"}, new String[] {"Lingua=Italiano"}) == 0, "ELF Esegui_comando foto_VALORE 적재");
        verificare(kernel_VALORE.첫과정().esecuzione_START_e_mail() == 0x04001000, "Esegui_comando avvia e_mail 반영");
        verificare(kernel_VALORE.첫과정().esecuzione_argomento().length == 2 && kernel_VALORE.첫과정().ambiente_VALORE().length == 1, "Esegui_comando 인자와 ambiente");
        verificare(!kernel_VALORE.첫과정().File_descrittore().reparto_IT_aperto(descrittore_voce), "Esegui_comando 시 descrittore_voce Chiudi");
        verificare(kernel_VALORE.쪽관리().바이트읽기(kernel_VALORE.첫과정().spazio_indirizzi(), 0x04002000) == 0, "빈 dati sezione_VALORE zero_operando inizializza");
    }

    private static void test_input(Nucleo kernel_VALORE) {
        kernel_VALORE.입력관리().키누름('가');
        kernel_VALORE.입력관리().쥐이동(3, -2);
        evento_di_input 첫사건 = kernel_VALORE.입력관리().Avanti_evento();
        evento_di_input SECONDO_evento = kernel_VALORE.입력관리().Avanti_evento();
        verificare(첫사건.tipo_di_evento() == evento_di_input.Kind_VALORE.키누름, "자판 Evento");
        verificare(SECONDO_evento.첫째값() == 3 && SECONDO_evento.SECONDO_VALORE() == -2, "쥐 spostare_VALORE Evento");
    }

    private static void test_hardware(host_hardware cellulare_VALORE) {
        cellulare_VALORE.scrivere_porta_byte(0x3f8, 0xab);
        verificare(cellulare_VALORE.포트바이트읽기(0x3f8) == 0xab, "hardware_porta I_O limite_VALORE");
        verificare(cellulare_VALORE.seriale_LOG().contains("JUsaOS"), "seriale_VALORE LOG_riga");
    }

    private static void 개입중단과서술자시험() {
        IRQ_manager manager_VALORE = new IRQ_manager();
        manager_VALORE.registro_voce(0x21, Memoria_e_mail -> Memoria_e_mail + 4);
        manager_VALORE.abilitare();
        verificare(manager_VALORE.distribuire_VALORE(0x21, 100) == 104, "IRQ distribuire_VALORE");
        manager_VALORE.disattivare();
        verificare(manager_VALORE.distribuire_VALORE(0x21, 100) == 100, "IRQ disattivare");

        tabella_dei_descrittori_globali descrittore_tabella = new tabella_dei_descrittori_globali();
        descrittore_tabella.set_valore_predefinito();
        verificare(descrittore_tabella.조각들().size() == 5, "전역 descrittore_tabella");
        task_Stato_segmento task_Stato = new task_Stato_segmento();
        task_Stato.특권쌓임공간설정(0x10, 0x800000);
        verificare(task_Stato.Pila_zero_Blocca() == 0x10 && task_Stato.Pila_zero_e_mail() == 0x800000, "작업 Stato_VALORE sezione_VALORE");
    }

    private static void test_Memoria_E_Rete() {
        고급기술결합장치 dispositivo_di_archiviazione = new 고급기술결합장치(4, false);
        byte[] 쓸자료 = new byte[고급기술결합장치.sezione_ridimensionare];
        byte[] 읽은자료 = new byte[고급기술결합장치.sezione_ridimensionare];
        쓸자료[17] = 42;
        dispositivo_di_archiviazione.Scrittura(2, 쓸자료);
        dispositivo_di_archiviazione.Lettura(2, 읽은자료);
        verificare(읽은자료[17] == 42, "ATA sezione_VALORE 읽고 Scrittura");

        accessorio_bus_manager accessorio = new accessorio_bus_manager();
        accessorio.발견(new accessorio_bus_manager.cellulare_VALORE(0x1022, 0x2000, 0xc000, 11));
        verificare(accessorio.TROVA_voce(0x1022, 0x2000) != null, "주변 cellulare_VALORE TROVA_voce");

        byte[] Ethernet_frame = new byte[34];
        Ethernet_frame[12] = 0x08;
        Ethernet_frame[13] = 0x00;
        Ethernet_frame[14] = 0x45;
        verificare(rete_Strumenti.Ethernet_MAIUSC_protocollo(Ethernet_frame) == 0x0800, "이더넷 상위 valore_di_contratto");
        verificare(rete_Strumenti.reparto_IT_IPV_4_protocollo(Ethernet_frame, 14), "상호통신망규약 4판");
        verificare(rete_Strumenti.cloud_checksum(new byte[] {0, 0}, 0, 2) == 0xffff, "인터넷 checksum");

        byte[] 첫구역 = new byte[512];
        첫구역[510] = 0x55;
        첫구역[511] = (byte) 0xaa;
        첫구역[450] = 0x0b;
        scrivere_intero_VALORE(첫구역, 454, 63);
        scrivere_intero_VALORE(첫구역, 458, 1024);
        verificare(new partizione_primaria_tabella().Lettura(첫구역).size() == 1, "valore_predefinito 분할 영역표");

        livello_rete layer_VALORE = new livello_rete();
        int[] RICEV_SCAD_CONTA_NUMERI = new int[1];
        layer_VALORE.registro_USER_dati_unità(7, (dati, avvia, durata_VALORE) -> RICEV_SCAD_CONTA_NUMERI[0]++);
        byte[] frame_INDICE = new byte[14 + 20 + 8];
        frame_INDICE[12] = 0x08;
        frame_INDICE[13] = 0x00;
        frame_INDICE[14] = 0x45;
        frame_INDICE[16] = 0;
        frame_INDICE[17] = 28;
        frame_INDICE[23] = 17;
        frame_INDICE[36] = 0;
        frame_INDICE[37] = 7;
        verificare(layer_VALORE.ricevere_Ethernet(frame_INDICE) && RICEV_SCAD_CONTA_NUMERI[0] == 1, "spazio_utente dati unità_VALORE distribuire_VALORE");
    }

    private static void test_schermata_E_clock() {
        carattere_display schermata = new carattere_display();
        schermata.uscitaTesto("가나\n다");
        verificare(schermata.문자(0, 0) == '가' && schermata.문자(0, 1) == '다', "문자 schermata uscitaTesto");
        clock clock = new clock(100);
        for (int INDICE = 0; INDICE < 10; INDICE++) {
            clock.tick_VALORE();
        }
        verificare(clock.지난밀리초() == 100, "clock tick_VALORE CONVERTI_VALORE");
    }

    private static void scrivere_intero_VALORE(byte[] dati, int posizione, int VALORE) {
        dati[posizione] = (byte) VALORE;
        dati[posizione + 1] = (byte) (VALORE >>> 8);
        dati[posizione + 2] = (byte) (VALORE >>> 16);
        dati[posizione + 3] = (byte) (VALORE >>> 24);
    }

    private static void 짧은정수쓰기(byte[] dati, int posizione, int VALORE) {
        dati[posizione] = (byte) VALORE;
        dati[posizione + 1] = (byte) (VALORE >>> 8);
    }

    private static void verificare(boolean condizione, String Nome) {
        if (!condizione) {
            throw new AssertionError("errore_VALORE: " + Nome);
        }
        passare_CONTA_NUMERI++;
        System.out.println("passare_VALORE: " + Nome);
    }
}
