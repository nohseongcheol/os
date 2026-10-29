// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 빛 {
    public static void main(String[] argomenti) throws Exception {
        int SUM_VALORE = 0;
        int numero = 1;
        while (numero <= 10) {
            SUM_VALORE = SUM_VALORE + numero;
            numero = numero + 1;
        }
        Italiano.nativo.uscitaTesto.scrivere_numero(SUM_VALORE);
        Italiano.nativo.file.Scrittura("aot.txt", "한글 AOT file 😀");
        Italiano.nativo.uscitaTesto.scrivere_riga(Italiano.nativo.file.Lettura("aot.txt"));
    }
}
