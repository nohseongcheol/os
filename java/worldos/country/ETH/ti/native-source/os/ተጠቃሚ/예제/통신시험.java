// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 통신시험 {
    public static int ኣኺድ() {
        int 첫째 = ተጠቃሚ.ክፈት_ማሕበራዊ_ኔትወርክ(45000);
        if (첫째 < 0) { ተጠቃሚ.ጸሓፍ("NETWORK UNAVAILABLE\n"); return 3; }
        int[] ሓበሬታ = new int[8];
        boolean 통과 = ተጠቃሚ.ክፈት_ማሕበራዊ_ኔትወርክ(45000) == -98
            && ተጠቃሚ.자료받기(첫째, ሓበሬታ, 0) == -11
            && ተጠቃሚ.자료받기(첫째, ሓበሬታ, 50) == -110
            && ተጠቃሚ.자료받기(첫째, ሓበሬታ, 3000) == -22
            && ተጠቃሚ.ለኣኽ_ሓበሬታ(첫째, 0x0a000202, 9, ሓበሬታ, 9) == -90
            && ተጠቃሚ.자료받기(첫째, null, 0) == -14
            && ተጠቃሚ.ዕጸው_ማሕበራዊ_ኔትወርክ(첫째) == 0 && ተጠቃሚ.ዕጸው_ማሕበራዊ_ኔትወርክ(첫째) == -9;
        ተጠቃሚ.ጸሓፍ(통과 ? "UDP API CHECK PASS\n" : "UDP API CHECK FAIL\n");
        return 통과 ? 0 : 1;
    }
}
