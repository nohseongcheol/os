// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 빛 {
    public static void main(String[] argumentit) throws Exception {
        int SUM_ARVO = 0;
        int numero = 1;
        while (numero <= 10) {
            SUM_ARVO = SUM_ARVO + numero;
            numero = numero + 1;
        }
        suomi.oma.tulostuspaikka.kirjoitus_numero(SUM_ARVO);
        suomi.oma.tiedoston_nimi.Kirjoitus("aot.txt", "한글 AOT tiedoston_nimi 😀");
        suomi.oma.tulostuspaikka.kirjoitus_rivi(suomi.oma.tiedoston_nimi.Luku("aot.txt"));
    }
}
