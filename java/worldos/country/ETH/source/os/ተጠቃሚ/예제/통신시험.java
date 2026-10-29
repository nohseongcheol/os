// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 통신시험 {
    public static int ማስኬጃ() {
        int 첫째 = ተጠቃሚ.ክፈት_መረብ(45000);
        if (첫째 < 0) { ተጠቃሚ.መጻፊያ("NETWORK UNAVAILABLE\n"); return 3; }
        int[] ውሂብ = new int[8];
        boolean አስተላልፍ_እሴት = ተጠቃሚ.ክፈት_መረብ(45000) == -98
            && ተጠቃሚ.자료받기(첫째, ውሂብ, 0) == -11
            && ተጠቃሚ.자료받기(첫째, ውሂብ, 50) == -110
            && ተጠቃሚ.자료받기(첫째, ውሂብ, 3000) == -22
            && ተጠቃሚ.ላክ_ውሂብ(첫째, 0x0a000202, 9, ውሂብ, 9) == -90
            && ተጠቃሚ.자료받기(첫째, null, 0) == -14
            && ተጠቃሚ.ዝጋ_መረብ(첫째) == 0 && ተጠቃሚ.ዝጋ_መረብ(첫째) == -9;
        ተጠቃሚ.መጻፊያ(አስተላልፍ_እሴት ? "UDP API CHECK PASS\n" : "UDP API CHECK FAIL\n");
        return አስተላልፍ_እሴት ? 0 : 1;
    }
}
