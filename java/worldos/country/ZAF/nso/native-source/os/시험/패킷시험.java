// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.Arrays;

/** kgonthe_data Java taba_boleng 처리기를 JVM에서 호출해 경계와 손상된 입력을 빠르게 검사한다. */
public final class 패킷시험 {
    static int 횟수 = 0;
    static void kgonthiša(boolean boleng) { if (!boleng) throw new AssertionError("case " + 횟수); 횟수++; }
    static int 검사합(int[] boleng, int Diriša, int botelele_boleng, int 초기) {
        int 합 = 초기;
        for (int lokela = 0; lokela < botelele_boleng; lokela++) 합 += boleng[Diriša + lokela] << ((lokela & 1) == 0 ? 8 : 0);
        합 = (합 & 65535) + (합 >>> 16);
        합 = (합 & 65535) + (합 >>> 16);
        return ~합 & 65535;
    }
    static void Lokišetša(int botelele_boleng) {
        Netweke_kgoboko.과정정리();
        kgonthiša(Netweke_kgoboko.Bula(5000) == 3);
        int[] freime_lokela = Netweke_kgoboko.입력틀;
        Arrays.fill(freime_lokela, 0);
        for (int lokela = 0; lokela < 6; lokela++) freime_lokela[lokela] = Netweke_teraeba.sedirišwa_atrese[lokela];
        Netweke_kgoboko.넣기16(freime_lokela, 12, 0x0800);
        freime_lokela[14] = 0x45; freime_lokela[22] = 64; freime_lokela[23] = 17;
        Netweke_kgoboko.넣기16(freime_lokela, 16, 28 + botelele_boleng);
        Netweke_kgoboko.넣기32(freime_lokela, 26, 0x0a000202); Netweke_kgoboko.넣기32(freime_lokela, 30, Netweke_kgoboko.내주소);
        Netweke_kgoboko.넣기16(freime_lokela, 34, 4321); Netweke_kgoboko.넣기16(freime_lokela, 36, 5000); Netweke_kgoboko.넣기16(freime_lokela, 38, botelele_boleng + 8);
        for (int lokela = 0; lokela < botelele_boleng; lokela++) freime_lokela[42 + lokela] = lokela & 255;
        검사합넣기(botelele_boleng);
    }
    static void 검사합넣기(int botelele_boleng) {
        int[] freime_lokela = Netweke_kgoboko.입력틀;
        Netweke_kgoboko.넣기16(freime_lokela, 24, 0); Netweke_kgoboko.넣기16(freime_lokela, 40, 0);
        Netweke_kgoboko.넣기16(freime_lokela, 24, 검사합(freime_lokela, 14, 20, 0));
        int 초기 = Netweke_kgoboko.가상머리합(Netweke_kgoboko.palotlalo_32(freime_lokela, 26), Netweke_kgoboko.내주소, botelele_boleng + 8);
        int 합 = 검사합(freime_lokela, 34, botelele_boleng + 8, 초기);
        Netweke_kgoboko.넣기16(freime_lokela, 40, 합 == 0 ? 65535 : 합);
    }
    static void 거부(int botelele_boleng) { Netweke_kgoboko.tiragalo_freime(botelele_boleng); kgonthiša(Netweke_kgoboko.받은길이[0] == -1); }
    public static void main(String[] 인수) {
        for (int botelele_boleng : new int[]{0, 1, 2, 7, 1023, 1024}) {
            Lokišetša(botelele_boleng); Netweke_kgoboko.tiragalo_freime(botelele_boleng + 42);
            kgonthiša(Netweke_kgoboko.받은길이[0] == botelele_boleng);
            kgonthiša(Netweke_kgoboko.받은주소[0] == 0x0a000202 && Netweke_kgoboko.받은접속번호[0] == 4321);
            for (int lokela = 0; lokela < botelele_boleng; lokela++) kgonthiša(Netweke_kgoboko.받은자료[lokela] == (lokela & 255));
        }
        for (int botelele_boleng = 0; botelele_boleng < 42; botelele_boleng++) { Lokišetša(0); 거부(botelele_boleng); }
        Lokišetša(1025); 거부(1067);
        Lokišetša(2); Netweke_kgoboko.입력틀[24] ^= 1; 거부(44);
        Lokišetša(2); Netweke_kgoboko.입력틀[42] ^= 1; 거부(44);
        Lokišetša(2); Netweke_kgoboko.넣기16(Netweke_kgoboko.입력틀, 38, 7); 거부(44);
        Lokišetša(2); Netweke_kgoboko.넣기16(Netweke_kgoboko.입력틀, 38, 65535); 거부(44);
        Lokišetša(2); Netweke_kgoboko.입력틀[14] = 0x4f; 거부(44);
        Lokišetša(2); Netweke_kgoboko.입력틀[14] = 0x44; 거부(44);
        Lokišetša(2); Netweke_kgoboko.입력틀[20] = 0x20; 검사합넣기(2); 거부(44);
        Lokišetša(2); Netweke_kgoboko.입력틀[21] = 1; 검사합넣기(2); 거부(44);
        Lokišetša(2); Netweke_kgoboko.입력틀[33] = 99; 검사합넣기(2); 거부(44);
        Lokišetša(2); Netweke_kgoboko.입력틀[0] ^= 1; 거부(44);
        Lokišetša(2); Netweke_kgoboko.입력틀[23] = 6; 검사합넣기(2); 거부(44);
        Lokišetša(2); Netweke_kgoboko.넣기16(Netweke_kgoboko.입력틀, 40, 0); Netweke_kgoboko.tiragalo_freime(44); kgonthiša(Netweke_kgoboko.받은길이[0] == 2);
        int[] 결과 = new int[4];
        kgonthiša(Netweke_kgoboko.받기(3, 결과, 1, 0) == -90);
        kgonthiša(Netweke_kgoboko.받기(3, 결과, 4, 0) == -11);
        Lokišetša(2); Netweke_kgoboko.tiragalo_freime(44); int tloša_boleng = Netweke_kgoboko.폐기수;
        Netweke_kgoboko.tiragalo_freime(44); kgonthiša(Netweke_kgoboko.폐기수 == tloša_boleng + 1);
        Netweke_kgoboko.과정정리(); kgonthiša(Netweke_kgoboko.Bula(5000) == 3);
        kgonthiša(Netweke_kgoboko.Bula(5000) == -98); kgonthiša(Netweke_kgoboko.Bula(0) == 4);
        kgonthiša(Netweke_kgoboko.Bula(0) == 5); kgonthiša(Netweke_kgoboko.Bula(0) == 6); kgonthiša(Netweke_kgoboko.Bula(0) == -24);
        kgonthiša(Netweke_kgoboko.Tswalela(4) == 0); kgonthiša(Netweke_kgoboko.Tswalela(4) == -9);
        Netweke_kgoboko.찾은주소 = Netweke_kgoboko.tsela_ya_netweke_boleng;
        kgonthiša(Netweke_kgoboko.Romela(3, Netweke_kgoboko.tsela_ya_netweke_boleng, 4321, new int[]{1, 2, 3}, 3) == 3);
        int[] 보냄 = Netweke_teraeba.ya_bjale_boleng;
        kgonthiša(검사합(보냄, 14, 20, 0) == 0);
        kgonthiša(검사합(보냄, 34, 11, Netweke_kgoboko.가상머리합(Netweke_kgoboko.내주소, Netweke_kgoboko.tsela_ya_netweke_boleng, 11)) == 0);
        kgonthiša(보냄[42] == 1 && 보냄[44] == 3);
        System.out.println("PACKET TEST PASS: " + 횟수 + " assertions");
    }
}
