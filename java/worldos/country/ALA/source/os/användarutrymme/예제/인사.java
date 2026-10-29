// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int Kör() {
        användarutrymme.Skriv("Hello from a separate Java ELF!\n");
        användarutrymme.Skriv(användarutrymme.körning_behörighet() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int INDEX = 0; INDEX < användarutrymme.인수개수(); INDEX++) {
            användarutrymme.Skriv("arg: "); användarutrymme.Skriv(användarutrymme.argument(INDEX)); användarutrymme.Skriv("\n");
        }
        return användarutrymme.körning_behörighet() == 3 ? 0 : 1;
    }
}
