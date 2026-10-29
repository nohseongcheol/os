// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 Įrankiai 전용 SVC Prisijungti. 기존 x86 Įrankiai 원문을 함께 빌드한다. */
public final class naudotojas {
    public static native int 파일서술자열기(int[] Pavadinimas_2, int Nustatymai);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int VALUE);
    public static native int 파일서술자닫기(int 서술자);
    public static native int 파일읽기(int[] Pavadinimas_2, int[] duomenys);
    public static native int rašymas_Failas(int[] Pavadinimas_2, int[] duomenys, int 길이);
    public static native int Rašymas(String Tekstas);
    public static native int rašymas_simbolis_VALUE(int VALUE);
    public static native int 인수개수();
    public static native String Argumentai(int INDEX);
    public static native int įrankis_numeris();
    public static native int 화면연결(int Veiksmas, int INDEX, int 가, int SECOND_operandas, int 다, int 라);
    public static native int 화면글(int INDEX, int[] Tekstas, int 길이);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int Stream_valdymas(int Veiksmas, int 서술자, int VALUE);
    public static native int ryšys_Stream(int 서술자, int ADDRESS, int jungtis_VALUE);
    public static native int kurti_tinklas(int jungtis_VALUE);
    public static native int siųsti_tinklas(int 서술자, int ADDRESS, int jungtis_VALUE, int[] duomenys, int 길이);
    public static native int gauti_tinklas(int 서술자, int[] duomenys, int 길이);
    public static native int tinklas_jungtis(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int stačiakampis(int 가로, int segmentas_padėtis, int 폭, int 높이, int 색);
}
