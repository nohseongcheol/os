// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Canada.JCanOS.Nucleo;

import Canada.JCanOS.Memoria_area.Memoria_manager;
import Canada.JCanOS.Memoria_area.Gestione_pagine;
import Canada.JCanOS.input_VALORE.input_manager;
import Canada.JCanOS.작업.Processi_VALORE;
import Canada.JCanOS.작업.Pianificatore;
import Canada.JCanOS.chiamata_di_sistema.chiamata_di_sistema;
import Canada.JCanOS.file_system.File_descrittore_tabella;
import Canada.JCanOS.file_system.file_system;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class Nucleo {
    private final hardware_VALORE cellulare_VALORE;
    private final Memoria_manager Memoria_area = new Memoria_manager(32 * 1024 * 1024);
    private final Gestione_pagine 쪽관리 = new Gestione_pagine();
    private final file_system file_system = new file_system();
    private final Pianificatore Pianificatore = new Pianificatore(쪽관리);
    private final input_manager 입력관리 = new input_manager(256);
    private final Processi_VALORE 첫과정;
    private final chiamata_di_sistema chiamata_di_sistema;

    public Nucleo(hardware_VALORE cellulare_VALORE) {
        this.cellulare_VALORE = cellulare_VALORE;
        첫과정 = Pianificatore.첫과정(new File_descrittore_tabella(file_system));
        chiamata_di_sistema = new chiamata_di_sistema(file_system, 쪽관리, Pianificatore, cellulare_VALORE, 입력관리);
    }

    public void avvia() {
        cellulare_VALORE.seriale_output("=== JCanOS 관리 kernel_VALORE ===\n");
    }

    public void Esegui_passaggio() {
        cellulare_VALORE.중앙처리장치멈춤();
    }

    public Memoria_manager Memoria_area() {
        return Memoria_area;
    }

    public Gestione_pagine 쪽관리() {
        return 쪽관리;
    }

    public file_system file_system() {
        return file_system;
    }

    public Pianificatore Pianificatore() {
        return Pianificatore;
    }

    public input_manager 입력관리() {
        return 입력관리;
    }

    public Processi_VALORE 첫과정() {
        return 첫과정;
    }

    public chiamata_di_sistema chiamata_di_sistema() {
        return chiamata_di_sistema;
    }
}
