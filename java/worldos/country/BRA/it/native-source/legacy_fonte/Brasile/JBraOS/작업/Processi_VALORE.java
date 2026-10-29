// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Brasile.JBraOS.작업;

import Brasile.JBraOS.Memoria_area.Gestione_pagine;
import Brasile.JBraOS.file_system.File_descrittore_tabella;

public final class Processi_VALORE {
    private final int identificatore_VALORE;
    private final int padre_identificatore;
    private final Gestione_pagine.spazio_indirizzi spazio_indirizzi;
    private final File_descrittore_tabella File_descrittore;
    private Processi_Stato Stato_VALORE = Processi_Stato.Prepara;
    private int codice_di_uscita;
    private int app_pausa = 0x06000000;
    private int esecuzione_START_e_mail;
    private String[] esecuzione_argomento = new String[0];
    private String[] ambiente_VALORE = new String[0];

    Processi_VALORE(int identificatore_VALORE, int padre_identificatore, Gestione_pagine.spazio_indirizzi spazio_indirizzi, File_descrittore_tabella File_descrittore) {
        this.identificatore_VALORE = identificatore_VALORE;
        this.padre_identificatore = padre_identificatore;
        this.spazio_indirizzi = spazio_indirizzi;
        this.File_descrittore = File_descrittore;
    }

    public int identificatore_VALORE() {
        return identificatore_VALORE;
    }

    public int padre_identificatore() {
        return padre_identificatore;
    }

    public Gestione_pagine.spazio_indirizzi spazio_indirizzi() {
        return spazio_indirizzi;
    }

    public File_descrittore_tabella File_descrittore() {
        return File_descrittore;
    }

    public Processi_Stato Stato_VALORE() {
        return Stato_VALORE;
    }

    public void set_Stato(Processi_Stato 새상태) {
        Stato_VALORE = 새상태;
    }

    public int codice_di_uscita() {
        return codice_di_uscita;
    }

    public void Esci_app(int VALORE) {
        codice_di_uscita = VALORE & 0xff;
        Stato_VALORE = Processi_Stato.Esci_app;
    }

    public int app_pausa() {
        return app_pausa;
    }

    public void set_app_pausa(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("app_f5044b9b 끝 범위를 벗어났습니다.");
        }
        app_pausa = 새끝;
    }

    public void set_contesto(int START_e_mail, String[] parametro_argomento, String[] ambiente) {
        esecuzione_START_e_mail = START_e_mail;
        esecuzione_argomento = parametro_argomento.clone();
        ambiente_VALORE = ambiente.clone();
    }

    public int esecuzione_START_e_mail() { return esecuzione_START_e_mail; }
    public String[] esecuzione_argomento() { return esecuzione_argomento.clone(); }
    public String[] ambiente_VALORE() { return ambiente_VALORE.clone(); }
}
