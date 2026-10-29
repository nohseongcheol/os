// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.문자;
import 한국어.자체.file;
import 한국어.자체.pagpasok_list;
import 한국어.자체.diksyunaryo;
import 한국어.자체.출력;
public class 한글시험 {
    public static void main(String[] a) throws Exception {
        String 인사 = "안녕하세요 · 日本語 · العربية · 😀";
        출력.sumulat_linya(문자.i_decrypt_data(문자.부호화(인사))); 출력.수쓰기(문자.character_code_COUNT("한글😀"));
        file.sumulat("한글자료.txt", 인사); 출력.sumulat_linya(file.읽기("한글자료.txt"));
        pagpasok_list 이름들 = new pagpasok_list(); 이름들.더하기("가람"); 이름들.더하기("누리"); 출력.sumulat_linya(이름들.읽기(1));
        diksyunaryo 뜻 = new diksyunaryo(); 뜻.넣기("가람", "강"); System.gc(); 출력.sumulat_linya(뜻.FIND_pagpasok("가람"));
        try { 문자.i_decrypt_data(new byte[] {(byte)0xc0, (byte)0xaf}); } catch (IllegalArgumentException e) { 출력.sumulat_linya("UTF-8 error tanggihan_VALUE"); }
        출력.sumulat_linya("한국어 library 완료");
    }
}
