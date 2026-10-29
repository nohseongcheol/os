// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class testi_Verkot {
    public static int Suorita_2() {
        int 첫째 = käyttäjätila.avata_verkko(45000);
        if (첫째 < 0) { käyttäjätila.Kirjoitus("NETWORK UNAVAILABLE\n"); return 3; }
        int[] data = new int[8];
        boolean välittää_ARVO = käyttäjätila.avata_verkko(45000) == -98
            && käyttäjätila.saada_data(첫째, data, 0) == -11
            && käyttäjätila.saada_data(첫째, data, 50) == -110
            && käyttäjätila.saada_data(첫째, data, 3000) == -22
            && käyttäjätila.lähettää_data_5b5410b2(첫째, 0x0a000202, 9, data, 9) == -90
            && käyttäjätila.saada_data(첫째, null, 0) == -14
            && käyttäjätila.Sulje_verkko(첫째) == 0 && käyttäjätila.Sulje_verkko(첫째) == -9;
        käyttäjätila.Kirjoitus(välittää_ARVO ? "UDP API CHECK PASS\n" : "UDP API CHECK FAIL\n");
        return välittää_ARVO ? 0 : 1;
    }
}
