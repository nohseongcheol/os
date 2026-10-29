// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int រត់() {
        អ្នកប្រើ.សរសេរ("Hello from a separate Java ELF!\n");
        អ្នកប្រើ.សរសេរ(អ្នកប្រើ.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int សន្ទស្សន៏ = 0; សន្ទស្សន៏ < អ្នកប្រើ.인수개수(); សន្ទស្សន៏++) {
            អ្នកប្រើ.សរសេរ("arg: "); អ្នកប្រើ.សរសេរ(អ្នកប្រើ.អាគុយម៉ង់(សន្ទស្សន៏)); អ្នកប្រើ.សរសេរ("\n");
        }
        return អ្នកប្រើ.실행권한() == 3 ? 0 : 1;
    }
}
