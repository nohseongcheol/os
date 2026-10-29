// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** iarbhír_sonraí 부팅 후 호출되는 Java iontráil_pointe. JVM과 óstach 운영체제에 의존하지 않는다. */
public final class eithne {
    static int 합계(int 끝) {
        int SUM_VALUE = 0;
        for (int INDEX = 1; INDEX <= 끝; INDEX++) SUM_VALUE += INDEX;
        return SUM_VALUE;
    }

    static boolean 시험() {
        int[] 값들 = new int[4];
        값들[2] = 합계(10);
        int 음수 = -7;
        int 최소 = 0x80000000;
        int roinnt_tomhas = -1;
        int INDEX = 기억공간.leithdháil_Stóras();
        boolean seol_ar_aghaidh_VALUE = 값들[0] == 0 && 값들[2] == 55 && 값들.length == 4
            && 음수 / 3 == -2 && 음수 % 3 == -1 && 최소 / roinnt_tomhas == 최소
            && 최소 % roinnt_tomhas == 0 && "한글".length() == 2 && "한글".charAt(1) == '글'
            && INDEX >= 0 && 기억공간.return_tomhas(INDEX) && !기억공간.return_tomhas(INDEX);
        SMS_Teirminéal.Scríobh(seol_ar_aghaidh_VALUE ? "JAVA SELFTEST PASS\n" : "JAVA SELFTEST FAIL\n");
        return seol_ar_aghaidh_VALUE;
    }

    public static void Rith_2() {
        SMS_Teirminéal.Ullmhaigh();
        SMS_Teirminéal.Scríobh("JKOROS NATIVE JAVA\n");
        SMS_Teirminéal.Scríobh("자바 기계어 eithne_VALUE Rith_2\n");
        if (gléas_VALUE.부팅표식() != 0x2badb002) {
            SMS_Teirminéal.Scríobh("BAD MULTIBOOT MAGIC\n");
            gléas_VALUE.정지();
        }
        if (!시험()) gléas_VALUE.정지();
        if (기억공간.UPPER_Cuimhne_socraigh_méid() < 15360) {
            SMS_Teirminéal.Scríobh("At least 16 MiB RAM required\n");
            gléas_VALUE.정지();
        }
        gléas_VALUE.Ullmhaigh_úsáideoir_clár();
        SMS_Teirminéal.Scríobh("USER ELF: ring 3 / paging / int 0x80\n");
        Líonra_tiománaí.Ullmhaigh();
        Líonra_Cruach.CLEAN_Próiseas();
        Cuimhne_córas_comhad.Ullmhaigh();
        파일보존.Ullmhaigh();
        명령해석기.Rith_2();
    }
}
