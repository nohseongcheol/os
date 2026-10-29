// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PC/AT PS/2 ແປພາສາ_ແຫຼ່ງທີ່ມາ 집합 1 폴링 입력. ຄ່າທີ່ກໍານົດໄວ້ແລ້ວ 미국식 자판, Shift, Backspace, Enter. */
public final class ແປ້ນພິມ {
    static boolean 왼올림 = false;
    static boolean 오른올림 = false;
    static boolean ສ່ວນຂະຫຍາຍ_ຄ່າ = false;
    static String ຄ່າທີ່ກໍານົດໄວ້ແລ້ວ = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String 올림 = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int 읽기() {
        int ສະຖານະ_ຄ່າ = ມືຖື_ຄ່າ.입출력바이트읽기(0x64);
        if ((ສະຖານະ_ຄ່າ & 1) == 0) return -1;
        int ຄ່າ = ມືຖື_ຄ່າ.입출력바이트읽기(0x60);
        if ((ສະຖານະ_ຄ່າ & 0x20) != 0) return -1;
        if (ຄ່າ == 0xe0 || ຄ່າ == 0xe1) { ສ່ວນຂະຫຍາຍ_ຄ່າ = true; return -1; }
        if (ສ່ວນຂະຫຍາຍ_ຄ່າ) { ສ່ວນຂະຫຍາຍ_ຄ່າ = false; return -1; }
        if (ຄ່າ == 42 || ຄ່າ == 170) { 왼올림 = ຄ່າ == 42; return -1; }
        if (ຄ່າ == 54 || ຄ່າ == 182) { 오른올림 = ຄ່າ == 54; return -1; }
        if (ຄ່າ >= ຄ່າທີ່ກໍານົດໄວ້ແລ້ວ.length()) return -1;
        int 문자 = (왼올림 || 오른올림) ? 올림.charAt(ຄ່າ) : ຄ່າທີ່ກໍານົດໄວ້ແລ້ວ.charAt(ຄ່າ);
        return 문자 == 0 ? -1 : 문자;
    }
}
