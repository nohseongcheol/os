// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 mašīna 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class Panelis {
    public static native int 표시화소읽기(int 가로, int vertikāle_amats);
    public static native void rakstīšana_rādīt_attēla_elements(int 가로, int vertikāle_amats, int 색);
    public static native int attālā_vadība(int 종류, int Darbība);
    public static native void beigt_zvanu_attāls_komanda(int Statuss_VALUE);
    public static native void attāls_pagaidi(int Statuss_VALUE);
    public static native void 직렬쓰기(int VALUE);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int centrālais_procesors_atļauja_līmenis();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int vertikāle_amats, int 색);
    public static native void YIELD_apstrādātājs();
    public static native int atvērt_uzdevums(int INDEX);
    public static native int uzdevums_Statuss(int INDEX);
    public static native void Pārtraukt(int Statuss_VALUE);
    public static native int 씨플러스시험();
    public static native int virkne_lietotājs_programma(int INDEX);
    public static native int čeks_lietotājs_programma();
    public static native int 인수준비(int krājums_COUNT);
    public static native int Izpildīt_lietotājs_Fails();
    public static native int 리눅스파일실행();
    public static native int arg_byte(int INDEX, int Novietojums, int VALUE);
    public static native int Terminālis(int Darbība);
    public static native int vadība_lietotājs_programma(int Darbība);
    public static native void 입출력전환(int Darbība);
    public static native int faila_pārsūtīšana_serviss(int Darbība);
    public static native int tīkls_statuss(int ievade_VALUE, int INDEX);
    public static native int tīkls_Iestatījumi(int Darbība, int adrese, int maska_VALUE, int vārteja_VALUE);
    public static native int sūtīt_atbilde(int adrese, int secība_VALUE);
    public static native int 응답읽기(int ievade_VALUE);
    public static native int vaicāt_sistēma(int ievade_VALUE, int INDEX);
    public static native void 전원끄기();
}
