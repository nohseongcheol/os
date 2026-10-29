// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Niemcy.JDeuOS.host;

import Niemcy.JDeuOS.jądro.jądro;

public final class host_uruchomienie {
    private host_uruchomienie() {
    }

    public static void main(String[] parametr_argument) {
        jądro jądro_WARTOŚĆ = new jądro(new host_sprzęt());
        jądro_WARTOŚĆ.Uruchom_2();
        jądro_WARTOŚĆ.Wykonaj_krok();
    }
}

