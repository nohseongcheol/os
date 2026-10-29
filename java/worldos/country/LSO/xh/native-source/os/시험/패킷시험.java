// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.Arrays;

/** eyona_yenzekileyo_iingcombolo Java isiganeko_ixabiso 처리기를 JVM에서 호출해 경계와 손상된 입력을 빠르게 검사한다. */
public final class 패킷시험 {
    static int 횟수 = 0;
    static void ngqinisisa(boolean ixabiso) { if (!ixabiso) throw new AssertionError("case " + 횟수); 횟수++; }
    static int 검사합(int[] ixabiso, int Phumeza, int ubude_ixabiso, int 초기) {
        int 합 = 초기;
        for (int indeksa = 0; indeksa < ubude_ixabiso; indeksa++) 합 += ixabiso[Phumeza + indeksa] << ((indeksa & 1) == 0 ? 8 : 0);
        합 = (합 & 65535) + (합 >>> 16);
        합 = (합 & 65535) + (합 >>> 16);
        return ~합 & 65535;
    }
    static void lungisa(int ubude_ixabiso) {
        Inethiwekhi_fumba.과정정리();
        ngqinisisa(Inethiwekhi_fumba.Vula(5000) == 3);
        int[] ifreyim_indeksa = Inethiwekhi_fumba.입력틀;
        Arrays.fill(ifreyim_indeksa, 0);
        for (int indeksa = 0; indeksa < 6; indeksa++) ifreyim_indeksa[indeksa] = Inethiwekhi_idrayiva.isixhobo_idilesi[indeksa];
        Inethiwekhi_fumba.넣기16(ifreyim_indeksa, 12, 0x0800);
        ifreyim_indeksa[14] = 0x45; ifreyim_indeksa[22] = 64; ifreyim_indeksa[23] = 17;
        Inethiwekhi_fumba.넣기16(ifreyim_indeksa, 16, 28 + ubude_ixabiso);
        Inethiwekhi_fumba.넣기32(ifreyim_indeksa, 26, 0x0a000202); Inethiwekhi_fumba.넣기32(ifreyim_indeksa, 30, Inethiwekhi_fumba.내주소);
        Inethiwekhi_fumba.넣기16(ifreyim_indeksa, 34, 4321); Inethiwekhi_fumba.넣기16(ifreyim_indeksa, 36, 5000); Inethiwekhi_fumba.넣기16(ifreyim_indeksa, 38, ubude_ixabiso + 8);
        for (int indeksa = 0; indeksa < ubude_ixabiso; indeksa++) ifreyim_indeksa[42 + indeksa] = indeksa & 255;
        검사합넣기(ubude_ixabiso);
    }
    static void 검사합넣기(int ubude_ixabiso) {
        int[] ifreyim_indeksa = Inethiwekhi_fumba.입력틀;
        Inethiwekhi_fumba.넣기16(ifreyim_indeksa, 24, 0); Inethiwekhi_fumba.넣기16(ifreyim_indeksa, 40, 0);
        Inethiwekhi_fumba.넣기16(ifreyim_indeksa, 24, 검사합(ifreyim_indeksa, 14, 20, 0));
        int 초기 = Inethiwekhi_fumba.가상머리합(Inethiwekhi_fumba.inani_elipheleleyo_32(ifreyim_indeksa, 26), Inethiwekhi_fumba.내주소, ubude_ixabiso + 8);
        int 합 = 검사합(ifreyim_indeksa, 34, ubude_ixabiso + 8, 초기);
        Inethiwekhi_fumba.넣기16(ifreyim_indeksa, 40, 합 == 0 ? 65535 : 합);
    }
    static void 거부(int ubude_ixabiso) { Inethiwekhi_fumba.Inkqubo_ifreyim(ubude_ixabiso); ngqinisisa(Inethiwekhi_fumba.받은길이[0] == -1); }
    public static void main(String[] 인수) {
        for (int ubude_ixabiso : new int[]{0, 1, 2, 7, 1023, 1024}) {
            lungisa(ubude_ixabiso); Inethiwekhi_fumba.Inkqubo_ifreyim(ubude_ixabiso + 42);
            ngqinisisa(Inethiwekhi_fumba.받은길이[0] == ubude_ixabiso);
            ngqinisisa(Inethiwekhi_fumba.받은주소[0] == 0x0a000202 && Inethiwekhi_fumba.받은접속번호[0] == 4321);
            for (int indeksa = 0; indeksa < ubude_ixabiso; indeksa++) ngqinisisa(Inethiwekhi_fumba.받은자료[indeksa] == (indeksa & 255));
        }
        for (int ubude_ixabiso = 0; ubude_ixabiso < 42; ubude_ixabiso++) { lungisa(0); 거부(ubude_ixabiso); }
        lungisa(1025); 거부(1067);
        lungisa(2); Inethiwekhi_fumba.입력틀[24] ^= 1; 거부(44);
        lungisa(2); Inethiwekhi_fumba.입력틀[42] ^= 1; 거부(44);
        lungisa(2); Inethiwekhi_fumba.넣기16(Inethiwekhi_fumba.입력틀, 38, 7); 거부(44);
        lungisa(2); Inethiwekhi_fumba.넣기16(Inethiwekhi_fumba.입력틀, 38, 65535); 거부(44);
        lungisa(2); Inethiwekhi_fumba.입력틀[14] = 0x4f; 거부(44);
        lungisa(2); Inethiwekhi_fumba.입력틀[14] = 0x44; 거부(44);
        lungisa(2); Inethiwekhi_fumba.입력틀[20] = 0x20; 검사합넣기(2); 거부(44);
        lungisa(2); Inethiwekhi_fumba.입력틀[21] = 1; 검사합넣기(2); 거부(44);
        lungisa(2); Inethiwekhi_fumba.입력틀[33] = 99; 검사합넣기(2); 거부(44);
        lungisa(2); Inethiwekhi_fumba.입력틀[0] ^= 1; 거부(44);
        lungisa(2); Inethiwekhi_fumba.입력틀[23] = 6; 검사합넣기(2); 거부(44);
        lungisa(2); Inethiwekhi_fumba.넣기16(Inethiwekhi_fumba.입력틀, 40, 0); Inethiwekhi_fumba.Inkqubo_ifreyim(44); ngqinisisa(Inethiwekhi_fumba.받은길이[0] == 2);
        int[] 결과 = new int[4];
        ngqinisisa(Inethiwekhi_fumba.받기(3, 결과, 1, 0) == -90);
        ngqinisisa(Inethiwekhi_fumba.받기(3, 결과, 4, 0) == -11);
        lungisa(2); Inethiwekhi_fumba.Inkqubo_ifreyim(44); int lahla_ixabiso = Inethiwekhi_fumba.폐기수;
        Inethiwekhi_fumba.Inkqubo_ifreyim(44); ngqinisisa(Inethiwekhi_fumba.폐기수 == lahla_ixabiso + 1);
        Inethiwekhi_fumba.과정정리(); ngqinisisa(Inethiwekhi_fumba.Vula(5000) == 3);
        ngqinisisa(Inethiwekhi_fumba.Vula(5000) == -98); ngqinisisa(Inethiwekhi_fumba.Vula(0) == 4);
        ngqinisisa(Inethiwekhi_fumba.Vula(0) == 5); ngqinisisa(Inethiwekhi_fumba.Vula(0) == 6); ngqinisisa(Inethiwekhi_fumba.Vula(0) == -24);
        ngqinisisa(Inethiwekhi_fumba.Vala(4) == 0); ngqinisisa(Inethiwekhi_fumba.Vala(4) == -9);
        Inethiwekhi_fumba.찾은주소 = Inethiwekhi_fumba.isango_lekhompyutha_ixabiso;
        ngqinisisa(Inethiwekhi_fumba.thumela(3, Inethiwekhi_fumba.isango_lekhompyutha_ixabiso, 4321, new int[]{1, 2, 3}, 3) == 3);
        int[] 보냄 = Inethiwekhi_idrayiva.kutshanje_ixabiso;
        ngqinisisa(검사합(보냄, 14, 20, 0) == 0);
        ngqinisisa(검사합(보냄, 34, 11, Inethiwekhi_fumba.가상머리합(Inethiwekhi_fumba.내주소, Inethiwekhi_fumba.isango_lekhompyutha_ixabiso, 11)) == 0);
        ngqinisisa(보냄[42] == 1 && 보냄[44] == 3);
        System.out.println("PACKET TEST PASS: " + 횟수 + " assertions");
    }
}
