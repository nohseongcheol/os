// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Slovenia.JSvnOS.chiamata_di_sistema;

import Slovenia.JSvnOS.Memoria_area.Gestione_pagine;
import Slovenia.JSvnOS.작업.Processi_VALORE;
import Slovenia.JSvnOS.작업.Pianificatore;
import Slovenia.JSvnOS.file_system.eseguibile_caricatore;
import Slovenia.JSvnOS.file_system.file_system;
import Slovenia.JSvnOS.file_system.File_info;
import Slovenia.JSvnOS.Nucleo.hardware_VALORE;
import Slovenia.JSvnOS.input_VALORE.input_manager;
import Slovenia.JSvnOS.input_VALORE.evento_di_input;

/** engos POSIX 1단계 호출의 Java 관리 계층이다. */
public final class chiamata_di_sistema {
    public static final int di_sola_lettura_flag = 0;
    public static final int Cerca_START = 0;
    public static final int Cerca_Regolari = 1;
    public static final int TROVA_voce_chiudere = 2;

    private final file_system file_system;
    private final Gestione_pagine 쪽관리;
    private final Pianificatore Pianificatore;
    private final eseguibile_caricatore caricatore = new eseguibile_caricatore();
    private final hardware_VALORE cellulare_VALORE;
    private final input_manager 입력관리;

    public chiamata_di_sistema(file_system file_system, Gestione_pagine 쪽관리, Pianificatore Pianificatore, hardware_VALORE cellulare_VALORE, input_manager 입력관리) {
        this.file_system = file_system;
        this.쪽관리 = 쪽관리;
        this.Pianificatore = Pianificatore;
        this.cellulare_VALORE = cellulare_VALORE;
        this.입력관리 = 입력관리;
    }

    public int Processi_identificatore(Processi_VALORE Regolari_Processi) {
        return Regolari_Processi.identificatore_VALORE();
    }

    public int padre_Processi_identificatore(Processi_VALORE Regolari_Processi) {
        return Regolari_Processi.padre_identificatore();
    }

    public int Apri(Processi_VALORE Regolari_Processi, String Nome, int flag_VALORE) {
        if (flag_VALORE != di_sola_lettura_flag) {
            return -30;
        }
        return Regolari_Processi.File_descrittore().Apri(Nome);
    }

    public int Lettura(Processi_VALORE Regolari_Processi, int descrittore_voce, byte[] ricevere_meta, int Dimensione) {
        if (descrittore_voce == 0) {
            if (Dimensione <= 0 || ricevere_meta.length == 0) {
                return 0;
            }
            evento_di_input Evento = 입력관리.Avanti_evento();
            if (Evento == null || Evento.tipo_di_evento() != evento_di_input.Kind_VALORE.키누름) {
                return -11;
            }
            ricevere_meta[0] = (byte) Evento.첫째값();
            return 1;
        }
        return Regolari_Processi.File_descrittore().Lettura(descrittore_voce, ricevere_meta, Dimensione);
    }

    public int Scrittura(Processi_VALORE Regolari_Processi, int descrittore_voce, byte[] dati, int Dimensione) {
        if (descrittore_voce != 1 && descrittore_voce != 2) {
            return Regolari_Processi.File_descrittore().reparto_IT_aperto(descrittore_voce) ? -30 : -9;
        }
        if (Dimensione < 0 || Dimensione > dati.length) {
            return -22;
        }
        cellulare_VALORE.seriale_output(new String(dati, 0, Dimensione, java.nio.charset.StandardCharsets.UTF_8));
        return Dimensione;
    }

    public int Chiudi(Processi_VALORE Regolari_Processi, int descrittore_voce) {
        return Regolari_Processi.File_descrittore().Chiudi(descrittore_voce);
    }

    public int spostare_funzione(Processi_VALORE Regolari_Processi, int descrittore_voce, int 거리, int azione_radice) {
        return Regolari_Processi.File_descrittore().spostare_funzione(descrittore_voce, 거리, azione_radice);
    }

    public int Duplica_descrittore(Processi_VALORE Regolari_Processi, int descrittore_voce) {
        return Regolari_Processi.File_descrittore().복제서술자(descrittore_voce, 0);
    }

    public int 지정서술자복제(Processi_VALORE Regolari_Processi, int descrittore_voce, int 새서술자) {
        return Regolari_Processi.File_descrittore().지정복제(descrittore_voce, 새서술자);
    }

    public int 접근가능(String Nome, int metodo_MODA) {
        File_info msinfo32_exe = file_system.msinfo32_exe(Nome);
        if (msinfo32_exe == null) {
            return -2;
        }
        if ((metodo_MODA & 1) != 0 && (msinfo32_exe.forma_Kind() & 0111) == 0) {
            return -13;
        }
        if ((metodo_MODA & 2) != 0) {
            return -30;
        }
        return 0;
    }

    public int SWITCH_Elenco_attività(String Nome) {
        return "/".equals(Nome) ? 0 : -20;
    }

    public String Regolari_Elenco_attività(int ricevere_ridimensionare) {
        return ricevere_ridimensionare >= 2 ? "/" : null;
    }

    public int UID() { return 0; }
    public int efficace_UID() { return 0; }
    public int GID() { return 0; }
    public int efficace_GID() { return 0; }

    public int sincronizzare_File(Processi_VALORE Regolari_Processi, int descrittore_voce) {
        return Regolari_Processi.File_descrittore().msinfo32_exe(descrittore_voce) == null ? -9 : 0;
    }

    public void 모두동기화() {
        // Regolari_articolo 파일체계는 Lettura 전용이어서 밀어낼 자료가 없다.
    }

    public boolean reparto_IT_Terminale(Processi_VALORE Regolari_Processi, int descrittore_voce) {
        File_info msinfo32_exe = Regolari_Processi.File_descrittore().msinfo32_exe(descrittore_voce);
        return msinfo32_exe != null && (msinfo32_exe.forma_Kind() & 0170000) == 0020000;
    }

    public int controllo_file(Processi_VALORE Regolari_Processi, int descrittore_voce, int comando, int parametro_argomento) {
        if (comando == 0) {
            return Regolari_Processi.File_descrittore().복제서술자(descrittore_voce, parametro_argomento);
        }
        if (comando == 1) {
            return Regolari_Processi.File_descrittore().실행시닫기값(descrittore_voce);
        }
        if (comando == 2) {
            return Regolari_Processi.File_descrittore().실행시닫기설정(descrittore_voce, (parametro_argomento & 1) != 0);
        }
        if (comando == 3) {
            return Regolari_Processi.File_descrittore().msinfo32_exe(descrittore_voce) == null ? -9 : di_sola_lettura_flag;
        }
        if (comando == 4) {
            return parametro_argomento == di_sola_lettura_flag ? 0 : -30;
        }
        return -22;
    }

    public int Crea_voce(String Nome, int privilegio_VALORE) {
        return -30;
    }

    public File_info descrittore_info(Processi_VALORE Regolari_Processi, int descrittore_voce) {
        return Regolari_Processi.File_descrittore().msinfo32_exe(descrittore_voce);
    }

    public Sistema_Dettagli Sistema_Dettagli() {
        return new Sistema_Dettagli("JSvnOS", "JSvnOS", "0.1", "Java managed kernel", "i386");
    }

    public File_info File_info(String Nome) {
        return file_system.msinfo32_exe(Nome);
    }

    public Processi_VALORE clone_Processi(Processi_VALORE padre_VALORE) {
        return Pianificatore.clone_VALORE(padre_VALORE);
    }

    public int 자식기다리기(Processi_VALORE padre_VALORE, int figlio_identificatore, boolean 기다리지않음) {
        return Pianificatore.자식기다리기(padre_VALORE, figlio_identificatore, 기다리지않음);
    }

    public int app_pausa(Processi_VALORE Regolari_Processi, int 새끝) {
        int Indietro_chiudere = Regolari_Processi.app_pausa();
        if (새끝 == 0) {
            return Indietro_chiudere;
        }
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            return -12;
        }
        int 첫쪽 = Indietro_chiudere / Gestione_pagine.dimensioni_della_pagina;
        int 끝쪽 = (새끝 + Gestione_pagine.dimensioni_della_pagina - 1) / Gestione_pagine.dimensioni_della_pagina;
        if (새끝 > Indietro_chiudere) {
            for (int INDICE = 첫쪽; INDICE < 끝쪽; INDICE++) {
                int e_mail = INDICE * Gestione_pagine.dimensioni_della_pagina;
                try {
                    쪽관리.바이트읽기(Regolari_Processi.spazio_indirizzi(), e_mail);
                } catch (IllegalStateException errore) {
                    쪽관리.MAP_pagina(Regolari_Processi.spazio_indirizzi(), e_mail, true);
                }
            }
        }
        Regolari_Processi.set_app_pausa(새끝);
        return 새끝;
    }

    public int aumento_app_pausa(Processi_VALORE Regolari_Processi, int incremento_importo) {
        int Indietro_chiudere = Regolari_Processi.app_pausa();
        int risultato = app_pausa(Regolari_Processi, Indietro_chiudere + incremento_importo);
        return risultato < 0 ? risultato : Indietro_chiudere;
    }

    public int Esegui_comando(Processi_VALORE Regolari_Processi, byte[] eseguibile) {
        return Esegui_comando(Regolari_Processi, eseguibile, new String[0], new String[0]);
    }

    public int Esegui_comando(Processi_VALORE Regolari_Processi, byte[] eseguibile, String[] parametro_argomento, String[] ambiente) {
        eseguibile_caricatore.foto foto_VALORE;
        try {
            foto_VALORE = caricatore.검사(eseguibile);
        } catch (IllegalArgumentException errore) {
            return -8;
        }
        if (parametro_argomento == null || ambiente == null || parametro_argomento.length > 16 || ambiente.length > 16) {
            return -7;
        }
        for (eseguibile_caricatore.sezione_VALORE sezione_VALORE : foto_VALORE.구역들()) {
            if ((sezione_VALORE.flag_VALORE() & 2) == 0 || sezione_VALORE.Dimensione() == 0) {
                continue;
            }
            int 첫쪽 = sezione_VALORE.e_mail() / Gestione_pagine.dimensioni_della_pagina;
            int 끝쪽 = (sezione_VALORE.e_mail() + sezione_VALORE.Dimensione() + Gestione_pagine.dimensioni_della_pagina - 1) / Gestione_pagine.dimensioni_della_pagina;
            for (int INDICE = 첫쪽; INDICE < 끝쪽; INDICE++) {
                int e_mail = INDICE * Gestione_pagine.dimensioni_della_pagina;
                try {
                    쪽관리.바이트읽기(Regolari_Processi.spazio_indirizzi(), e_mail);
                    쪽관리.escludi_intervallo_scrivere(Regolari_Processi.spazio_indirizzi(), e_mail, Gestione_pagine.dimensioni_della_pagina);
                } catch (IllegalStateException errore) {
                    쪽관리.MAP_pagina(Regolari_Processi.spazio_indirizzi(), e_mail, true);
                }
            }
            for (int INDICE = 0; INDICE < sezione_VALORE.Dimensione(); INDICE++) {
                byte VALORE = sezione_VALORE.Kind_VALORE() == 8 ? 0 : eseguibile[sezione_VALORE.File_funzione() + INDICE];
                쪽관리.scrivere_byte_VALORE(Regolari_Processi.spazio_indirizzi(), sezione_VALORE.e_mail() + INDICE, VALORE);
            }
        }
        Regolari_Processi.set_contesto(foto_VALORE.START_e_mail(), parametro_argomento, ambiente);
        Regolari_Processi.File_descrittore().실행시닫기();
        return 0;
    }

    public void esci_app(Processi_VALORE Regolari_Processi, int Stato_VALORE) {
        Regolari_Processi.Esci_app(Stato_VALORE);
    }
}
