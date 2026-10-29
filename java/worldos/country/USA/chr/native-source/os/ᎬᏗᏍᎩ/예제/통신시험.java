// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 통신시험 {
    public static int ᎠᎢᏎᏍᏗ() {
        int 첫째 = ᎬᏗᏍᎩ.ᎯᏍᏚᎢ_ᏧᎾᏚᏓᎵ(45000);
        if (첫째 < 0) { ᎬᏗᏍᎩ.ᎪᏪᎶᏗ("NETWORK UNAVAILABLE\n"); return 3; }
        int[] ᎦᏟᏌᏅᎯ = new int[8];
        boolean 통과 = ᎬᏗᏍᎩ.ᎯᏍᏚᎢ_ᏧᎾᏚᏓᎵ(45000) == -98
            && ᎬᏗᏍᎩ.자료받기(첫째, ᎦᏟᏌᏅᎯ, 0) == -11
            && ᎬᏗᏍᎩ.자료받기(첫째, ᎦᏟᏌᏅᎯ, 50) == -110
            && ᎬᏗᏍᎩ.자료받기(첫째, ᎦᏟᏌᏅᎯ, 3000) == -22
            && ᎬᏗᏍᎩ.ᏫᎦᏅᏗ_ᎦᏟᏌᏅᎯ(첫째, 0x0a000202, 9, ᎦᏟᏌᏅᎯ, 9) == -90
            && ᎬᏗᏍᎩ.자료받기(첫째, null, 0) == -14
            && ᎬᏗᏍᎩ.ᎯᏍᏚᎲᎦ_ᏧᎾᏚᏓᎵ(첫째) == 0 && ᎬᏗᏍᎩ.ᎯᏍᏚᎲᎦ_ᏧᎾᏚᏓᎵ(첫째) == -9;
        ᎬᏗᏍᎩ.ᎪᏪᎶᏗ(통과 ? "UDP API CHECK PASS\n" : "UDP API CHECK FAIL\n");
        return 통과 ? 0 : 1;
    }
}
