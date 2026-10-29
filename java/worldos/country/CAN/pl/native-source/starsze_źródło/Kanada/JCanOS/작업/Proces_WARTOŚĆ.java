// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Kanada.JCanOS.작업;

import Kanada.JCanOS.Pamięć_region.strona_Menedżer;
import Kanada.JCanOS.system_plików.Plik_deskryptor_tabela;

public final class Proces_WARTOŚĆ {
    private final int identyfikator_WARTOŚĆ;
    private final int nadrzędny_identyfikator;
    private final strona_Menedżer.przestrzeń_adresowa przestrzeń_adresowa;
    private final Plik_deskryptor_tabela Plik_deskryptor;
    private Proces_Stan Stan_WARTOŚĆ = Proces_Stan.Przygotuj;
    private int kod_zakończenia;
    private int program_przerwa = 0x06000000;
    private int wykonanie_START_ADRES;
    private String[] wykonanie_argument = new String[0];
    private String[] środowisko_WARTOŚĆ = new String[0];

    Proces_WARTOŚĆ(int identyfikator_WARTOŚĆ, int nadrzędny_identyfikator, strona_Menedżer.przestrzeń_adresowa przestrzeń_adresowa, Plik_deskryptor_tabela Plik_deskryptor) {
        this.identyfikator_WARTOŚĆ = identyfikator_WARTOŚĆ;
        this.nadrzędny_identyfikator = nadrzędny_identyfikator;
        this.przestrzeń_adresowa = przestrzeń_adresowa;
        this.Plik_deskryptor = Plik_deskryptor;
    }

    public int identyfikator_WARTOŚĆ() {
        return identyfikator_WARTOŚĆ;
    }

    public int nadrzędny_identyfikator() {
        return nadrzędny_identyfikator;
    }

    public strona_Menedżer.przestrzeń_adresowa przestrzeń_adresowa() {
        return przestrzeń_adresowa;
    }

    public Plik_deskryptor_tabela Plik_deskryptor() {
        return Plik_deskryptor;
    }

    public Proces_Stan Stan_WARTOŚĆ() {
        return Stan_WARTOŚĆ;
    }

    public void set_Stan(Proces_Stan 새상태) {
        Stan_WARTOŚĆ = 새상태;
    }

    public int kod_zakończenia() {
        return kod_zakończenia;
    }

    public void wyjść_program(int WARTOŚĆ) {
        kod_zakończenia = WARTOŚĆ & 0xff;
        Stan_WARTOŚĆ = Proces_Stan.wyjść_program;
    }

    public int program_przerwa() {
        return program_przerwa;
    }

    public void set_program_przerwa(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("program_f5044b9b 끝 범위를 벗어났습니다.");
        }
        program_przerwa = 새끝;
    }

    public void set_kontekst(int START_ADRES, String[] parametr_argument, String[] środowisko) {
        wykonanie_START_ADRES = START_ADRES;
        wykonanie_argument = parametr_argument.clone();
        środowisko_WARTOŚĆ = środowisko.clone();
    }

    public int wykonanie_START_ADRES() { return wykonanie_START_ADRES; }
    public String[] wykonanie_argument() { return wykonanie_argument.clone(); }
    public String[] środowisko_WARTOŚĆ() { return środowisko_WARTOŚĆ.clone(); }
}
