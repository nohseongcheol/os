// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 화면 rezati_VALUE·띠 합성·kazalec 밑그림을 관리한다. dejanski_podatki 화면 pomnilnik_podatki 접근은 보드가 담당한다. */
public final class 화면합성 {
    static int 너비, višina_VALUE, 합성중, 왼경계, 위경계, 오른경계, 아래경계;
    static int kazalec_X, kazalec_Y, kazalec_oblika;
    static int 기록아래낱말, 기록위낱말;
    static int[] 완성그림 = new int[32 * 1920];
    static int[] kazalec_Ozadje = new int[21 * 21];
    static int[] 잘린범위 = new int[4];
    public static void Pripravi(int 폭, int 길이) {
        너비 = 폭; višina_VALUE = 길이; 합성중 = 0; kazalec_oblika = 0;
        기록아래낱말 = 0; 기록위낱말 = 0;
    }
    public static int 너비얻기() { return 너비; }
    public static int dobiti_višina() { return višina_VALUE; }
    public static int 기록아래얻기() { return 기록아래낱말; }
    public static int 기록위얻기() { return 기록위낱말; }
    public static int izrezek_VALUE(int 순번) { return 잘린범위[순번]; }
    static int 양의길이더하기(int Start_VALUE, int 길이) {
        if (Start_VALUE > 2147483647 - 길이) return 2147483647;
        return Start_VALUE + 길이;
    }
    public static int izrezek(int 가로, int Navpično_položaj, int 폭, int 길이) {
        if (너비 == 0 || 폭 <= 0 || 길이 <= 0) return 0;
        int RIGHT = 양의길이더하기(가로, 폭), 아래쪽 = 양의길이더하기(Navpično_položaj, 길이);
        int 왼쪽 = 합성중 != 0 ? 왼경계 : 0, 위쪽 = 합성중 != 0 ? 위경계 : 0;
        int 최대가로 = 합성중 != 0 ? 오른경계 : 너비, 최대세로 = 합성중 != 0 ? 아래경계 : višina_VALUE;
        if (가로 < 왼쪽) 가로 = 왼쪽;
        if (Navpično_položaj < 위쪽) Navpično_položaj = 위쪽;
        if (RIGHT > 최대가로) RIGHT = 최대가로;
        if (아래쪽 > 최대세로) 아래쪽 = 최대세로;
        if (RIGHT <= 가로 || 아래쪽 <= Navpično_položaj) return 0;
        잘린범위[0] = 가로; 잘린범위[1] = Navpično_položaj;
        잘린범위[2] = RIGHT - 가로; 잘린범위[3] = 아래쪽 - Navpično_položaj;
        return 1;
    }
    public static int Zaženi(int 가로, int Navpično_položaj, int 폭, int 길이) {
        if (합성중 != 0 || 길이 > 32 || izrezek(가로, Navpično_položaj, 폭, 길이) == 0) return 0;
        왼경계 = 잘린범위[0]; 위경계 = 잘린범위[1];
        오른경계 = 왼경계 + 잘린범위[2]; 아래경계 = 위경계 + 잘린범위[3];
        합성중 = 1; return 1;
    }
    static boolean kazalec_bit(int 가로, int Navpično_položaj, int oblika_VALUE_f1cd655a) {
        if (oblika_VALUE_f1cd655a == 1) return 가로 >= 0 && 가로 <= Navpično_položaj / 2 && Navpično_položaj < 16;
        if (oblika_VALUE_f1cd655a == 3) 가로 = 20 - 가로;
        int 차이 = 가로 - Navpično_položaj; if (차이 < 0) 차이 = -차이;
        return (차이 <= 1 && 가로 >= 3 && 가로 <= 17) ||
            (가로 >= 2 && 가로 <= 8 && Navpično_položaj >= 2 && Navpično_položaj <= 8 && (가로 <= 3 || Navpično_položaj <= 3)) ||
            (가로 >= 12 && 가로 <= 18 && Navpično_položaj >= 12 && Navpično_položaj <= 18 && (가로 >= 17 || Navpično_položaj >= 17));
    }
    static int kazalec_slikovna_pika(int 가로, int Navpično_položaj) {
        if (kazalec_bit(가로, Navpično_položaj, kazalec_oblika)) return 2;
        for (int Črtni = -1; Črtni <= 1; Črtni++) for (int 칸 = -1; 칸 <= 1; 칸++)
            if (kazalec_bit(가로 + 칸, Navpično_položaj + Črtni, kazalec_oblika)) return 1;
        return 0;
    }
    static void zaslon_slikovna_pika(int 가로, int Navpično_položaj, int 색) {
        int 칸 = 가로 - kazalec_X, Črtni = Navpično_položaj - kazalec_Y;
        if (kazalec_oblika != 0 && 칸 >= 0 && Črtni >= 0 && 칸 < 21 && Črtni < 21) {
            kazalec_Ozadje[Črtni * 21 + 칸] = 색;
            int p_VALUE = kazalec_slikovna_pika(칸, Črtni); if (p_VALUE != 0) 색 = p_VALUE == 2 ? 0xffffff : 0x101010;
        }
        if (Tabla.표시화소읽기(가로, Navpično_položaj) != 색) {
            Tabla.pisati_zaslon_slikovna_pika(가로, Navpično_položaj, 색);
            기록아래낱말++; if (기록아래낱말 == 0) 기록위낱말++;
        }
    }
    public static void konec() {
        if (합성중 == 0) return;
        for (int Črtni = 위경계; Črtni < 아래경계; Črtni++) for (int 칸 = 왼경계; 칸 < 오른경계; 칸++)
            zaslon_slikovna_pika(칸, Črtni, 완성그림[(Črtni - 위경계) * 1920 + 칸]);
        합성중 = 0;
    }
    public static int slikovna_pika(int 가로, int Navpično_položaj, int 색) {
        if (가로 < 0 || Navpično_položaj < 0 || 가로 >= 너비 || Navpično_položaj >= višina_VALUE) return 0;
        if (합성중 != 0) {
            if (가로 >= 왼경계 && 가로 < 오른경계 && Navpično_položaj >= 위경계 && Navpično_položaj < 아래경계)
                완성그림[(Navpično_položaj - 위경계) * 1920 + 가로] = 색;
        } else zaslon_slikovna_pika(가로, Navpično_položaj, 색);
        return 0;
    }
    public static void pravokotnik_polnilo(int 가로, int Navpično_položaj, int 폭, int 길이, int 색) {
        if (izrezek(가로, Navpično_položaj, 폭, 길이) == 0) return;
        가로 = 잘린범위[0]; Navpično_položaj = 잘린범위[1]; 폭 = 잘린범위[2]; 길이 = 잘린범위[3];
        for (int Črtni = Navpično_položaj; Črtni < Navpično_položaj + 길이; Črtni++) for (int 칸 = 가로; 칸 < 가로 + 폭; 칸++) {
            if (합성중 != 0) 완성그림[(Črtni - 위경계) * 1920 + 칸] = 색;
            else zaslon_slikovna_pika(칸, Črtni, 색);
        }
    }
    public static void kazalec(int 가로, int Navpično_položaj, int oblika_VALUE_f1cd655a) {
        if (너비 == 0) return;
        int 새가로 = 가로 - (oblika_VALUE_f1cd655a >= 2 ? 10 : 0), 새세로 = Navpično_položaj - (oblika_VALUE_f1cd655a >= 2 ? 10 : 0);
        if (kazalec_oblika == oblika_VALUE_f1cd655a && kazalec_X == 새가로 && kazalec_Y == 새세로) return;
        if (kazalec_oblika != 0) for (int Črtni = 0; Črtni < 21; Črtni++) for (int 칸 = 0; 칸 < 21; 칸++) {
            int 가 = kazalec_X + 칸, 세 = kazalec_Y + Črtni;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < višina_VALUE) Tabla.pisati_zaslon_slikovna_pika(가, 세, kazalec_Ozadje[Črtni * 21 + 칸]);
        }
        kazalec_oblika = oblika_VALUE_f1cd655a; kazalec_X = 새가로; kazalec_Y = 새세로;
        if (oblika_VALUE_f1cd655a != 0) for (int Črtni = 0; Črtni < 21; Črtni++) for (int 칸 = 0; 칸 < 21; 칸++) {
            int 가 = kazalec_X + 칸, 세 = kazalec_Y + Črtni;
            if (가 >= 0 && 세 >= 0 && 가 < 너비 && 세 < višina_VALUE) {
                kazalec_Ozadje[Črtni * 21 + 칸] = Tabla.표시화소읽기(가, 세);
                int p_VALUE = kazalec_slikovna_pika(칸, Črtni); if (p_VALUE != 0) Tabla.pisati_zaslon_slikovna_pika(가, 세, p_VALUE == 2 ? 0xffffff : 0x101010);
            }
        }
    }
}
