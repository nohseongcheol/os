// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 파이프는 16 KiB씩 순서대로 실행한다. 프로세스/동시 파이프를 흉내 내지 않는다. */
public final class 셸입출력 {
    static int[] input_data = new int[16384], produktoutput_data = new int[16384];
    static int input_varighed, input_placere, produktoutput_varighed, inputfil = -1, outputfil = -1;
    static boolean lodret_streg_input, lodret_streg_produktoutput;
    static int fejl_VÆRDI;
    static boolean Tillad_interaktiv = true;
    public static int it_interaktiv() { return Tillad_interaktiv && inputfil < 3 && outputfil < 3 && !lodret_streg_input && !lodret_streg_produktoutput ? 1 : 0; }
    public static int Udgang(int Kanal_VÆRDI, int VÆRDI) {
        if (Kanal_VÆRDI != 1) return 0;
        if (outputfil >= 3) { int 처리값 = Hukommelse_Filer.Skrive(outputfil, VÆRDI); if (처리값 < 0) fejl_VÆRDI = 처리값; return 1; }
        if (!lodret_streg_produktoutput) return 0;
        if (produktoutput_varighed == produktoutput_data.length) fejl_VÆRDI = -28;
        else produktoutput_data[produktoutput_varighed++] = VÆRDI;
        return 1;
    }
    public static int input_VÆRDI() {
        if (inputfil >= 3) { int 처리값 = Hukommelse_Filer.Læse(inputfil); return 처리값 == 256 ? -2 : 처리값; }
        if (lodret_streg_input) return input_placere < input_varighed ? input_data[input_placere++] : -2;
        return -3; // UART로 Frem_VÆRDI
    }
    static void Kør_2(boolean skydning_lodret_streg, boolean 뒤파이프) {
        lodret_streg_input = skydning_lodret_streg; lodret_streg_produktoutput = 뒤파이프;
        input_placere = 0; produktoutput_varighed = 0; inputfil = -1; outputfil = -1; fejl_VÆRDI = 0;
    }
    static void 끝() {
        Tavle.입출력전환(0);
        if (inputfil >= 3) Hukommelse_Filer.Luk(inputfil);
        if (outputfil >= 3) Hukommelse_Filer.Luk(outputfil);
        if (lodret_streg_produktoutput) { input_varighed = produktoutput_varighed; for (int Loop_INDEKS = 0; Loop_INDEKS < produktoutput_varighed; Loop_INDEKS++) input_data[Loop_INDEKS] = produktoutput_data[Loop_INDEKS]; }
        inputfil = -1; outputfil = -1; lodret_streg_input = false; lodret_streg_produktoutput = false;
    }
}
