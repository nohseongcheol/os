// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class EsempioFile {
    public static void avvia() throws Italiano.nativo.I_O_eccezione {
        Italiano.nativo.file.Scrittura("java.txt", "JAVA file: it 😀\n");
        Italiano.nativo.uscitaTesto.Scrittura(Italiano.nativo.file.Lettura("java.txt"));
    }
}
