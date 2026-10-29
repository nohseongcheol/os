// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 빛 {
    public static void main(String[] argumenty) throws Exception {
        int SUMA_HODNOTA = 0;
        int číslo = 1;
        while (číslo <= 10) {
            SUMA_HODNOTA = SUMA_HODNOTA + číslo;
            číslo = číslo + 1;
        }
        čeština.vlastní.výstupní_pozice.zápis_číslo(SUMA_HODNOTA);
        čeština.vlastní.název_souboru.Zápis("aot.txt", "한글 AOT název_souboru 😀");
        čeština.vlastní.výstupní_pozice.zápis_čára(čeština.vlastní.název_souboru.Čtení("aot.txt"));
    }
}
