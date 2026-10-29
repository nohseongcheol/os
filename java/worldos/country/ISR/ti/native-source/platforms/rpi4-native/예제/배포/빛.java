// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 빛 {
    public static void main(String[] 인수) throws Exception {
        int 합 = 0;
        int 수 = 1;
        while (수 <= 10) {
            합 = 합 + 수;
            수 = 수 + 1;
        }
        ትግርኛ.자체.출력.수쓰기(합);
        ትግርኛ.자체.ፋይል.ጸሓፍ("aot.txt", "한글 AOT ፋይል 😀");
        ትግርኛ.자체.출력.ጸሓፍ_መስመር(ትግርኛ.자체.ፋይል.읽기("aot.txt"));
    }
}
