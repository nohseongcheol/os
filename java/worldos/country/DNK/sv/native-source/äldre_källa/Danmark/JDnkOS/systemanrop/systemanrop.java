// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Danmark.JDnkOS.systemanrop;

import Danmark.JDnkOS.Minne_område.Sidhanteraren;
import Danmark.JDnkOS.작업.Process_värde;
import Danmark.JDnkOS.작업.Scheduler;
import Danmark.JDnkOS.filsystem.körbar_fil_inläsare;
import Danmark.JDnkOS.filsystem.filsystem;
import Danmark.JDnkOS.filsystem.fil_info;
import Danmark.JDnkOS.kärna.maskinvara_värde;
import Danmark.JDnkOS.indata_värde.indata_Ansvarig;
import Danmark.JDnkOS.indata_värde.inmatningshändelse;

/** engos POSIX 1단계 호출의 Java 관리 계층이다. */
public final class systemanrop {
    public static final int skrivskyddad_flagga = 0;
    public static final int SÖK_START = 0;
    public static final int SÖK_aktuellt = 1;
    public static final int Sök_post_avsluta = 2;

    private final filsystem filsystem;
    private final Sidhanteraren 쪽관리;
    private final Scheduler Scheduler;
    private final körbar_fil_inläsare inläsare = new körbar_fil_inläsare();
    private final maskinvara_värde enhet_värde;
    private final indata_Ansvarig 입력관리;

    public systemanrop(filsystem filsystem, Sidhanteraren 쪽관리, Scheduler Scheduler, maskinvara_värde enhet_värde, indata_Ansvarig 입력관리) {
        this.filsystem = filsystem;
        this.쪽관리 = 쪽관리;
        this.Scheduler = Scheduler;
        this.enhet_värde = enhet_värde;
        this.입력관리 = 입력관리;
    }

    public int Process_identifierare(Process_värde aktuellt_Process) {
        return aktuellt_Process.identifierare_värde();
    }

    public int överordnad_Process_identifierare(Process_värde aktuellt_Process) {
        return aktuellt_Process.överordnad_identifierare();
    }

    public int Öppna(Process_värde aktuellt_Process, String Namn, int flagga_värde) {
        if (flagga_värde != skrivskyddad_flagga) {
            return -30;
        }
        return aktuellt_Process.파일서술자().Öppna(Namn);
    }

    public int Läs(Process_värde aktuellt_Process, int 서술자, byte[] få_mål, int Storlek) {
        if (서술자 == 0) {
            if (Storlek <= 0 || få_mål.length == 0) {
                return 0;
            }
            inmatningshändelse Händelse = 입력관리.Nästa_händelse();
            if (Händelse == null || Händelse.händelsesort() != inmatningshändelse.variant_värde.Nyckel_ur_funktion) {
                return -11;
            }
            få_mål[0] = (byte) Händelse.첫째값();
            return 1;
        }
        return aktuellt_Process.파일서술자().Läs(서술자, få_mål, Storlek);
    }

    public int Skriv(Process_värde aktuellt_Process, int 서술자, byte[] data, int Storlek) {
        if (서술자 != 1 && 서술자 != 2) {
            return aktuellt_Process.파일서술자().informationsteknik_skapa(서술자) ? -30 : -9;
        }
        if (Storlek < 0 || Storlek > data.length) {
            return -22;
        }
        enhet_värde.직렬출력(new String(data, 0, Storlek, java.nio.charset.StandardCharsets.UTF_8));
        return Storlek;
    }

    public int Stäng(Process_värde aktuellt_Process, int 서술자) {
        return aktuellt_Process.파일서술자().Stäng(서술자);
    }

    public int flytta_placera(Process_värde aktuellt_Process, int 서술자, int 거리, int åtgärd_rot) {
        return aktuellt_Process.파일서술자().flytta_placera(서술자, 거리, åtgärd_rot);
    }

    public int 서술자복제(Process_värde aktuellt_Process, int 서술자) {
        return aktuellt_Process.파일서술자().복제서술자(서술자, 0);
    }

    public int 지정서술자복제(Process_värde aktuellt_Process, int 서술자, int 새서술자) {
        return aktuellt_Process.파일서술자().지정복제(서술자, 새서술자);
    }

    public int 접근가능(String Namn, int metod_läge) {
        fil_info msinfo32_exe = filsystem.msinfo32_exe(Namn);
        if (msinfo32_exe == null) {
            return -2;
        }
        if ((metod_läge & 1) != 0 && (msinfo32_exe.form_variant() & 0111) == 0) {
            return -13;
        }
        if ((metod_läge & 2) != 0) {
            return -30;
        }
        return 0;
    }

    public int byta_uppgiftslista(String Namn) {
        return "/".equals(Namn) ? 0 : -20;
    }

    public String aktuellt_uppgiftslista(int få_storlek) {
        return få_storlek >= 2 ? "/" : null;
    }

    public int UID() { return 0; }
    public int effektiv_UID() { return 0; }
    public int GID() { return 0; }
    public int effektiv_GID() { return 0; }

    public int synka_fil(Process_värde aktuellt_Process, int 서술자) {
        return aktuellt_Process.파일서술자().msinfo32_exe(서술자) == null ? -9 : 0;
    }

    public void 모두동기화() {
        // aktuellt_objekt 파일체계는 Läs 전용이어서 밀어낼 자료가 없다.
    }

    public boolean informationsteknik_Terminal(Process_värde aktuellt_Process, int 서술자) {
        fil_info msinfo32_exe = aktuellt_Process.파일서술자().msinfo32_exe(서술자);
        return msinfo32_exe != null && (msinfo32_exe.form_variant() & 0170000) == 0020000;
    }

    public int filstyrning(Process_värde aktuellt_Process, int 서술자, int kommando, int parameter_argument) {
        if (kommando == 0) {
            return aktuellt_Process.파일서술자().복제서술자(서술자, parameter_argument);
        }
        if (kommando == 1) {
            return aktuellt_Process.파일서술자().실행시닫기값(서술자);
        }
        if (kommando == 2) {
            return aktuellt_Process.파일서술자().실행시닫기설정(서술자, (parameter_argument & 1) != 0);
        }
        if (kommando == 3) {
            return aktuellt_Process.파일서술자().msinfo32_exe(서술자) == null ? -9 : skrivskyddad_flagga;
        }
        if (kommando == 4) {
            return parameter_argument == skrivskyddad_flagga ? 0 : -30;
        }
        return -22;
    }

    public int Skapa_post(String Namn, int behörighet_värde) {
        return -30;
    }

    public fil_info 서술자정보(Process_värde aktuellt_Process, int 서술자) {
        return aktuellt_Process.파일서술자().msinfo32_exe(서술자);
    }

    public System_Detaljer System_Detaljer() {
        return new System_Detaljer("JDnkOS", "JDnkOS", "0.1", "Java managed kernel", "i386");
    }

    public fil_info fil_info(String Namn) {
        return filsystem.msinfo32_exe(Namn);
    }

    public Process_värde klon_Process(Process_värde överordnad_värde) {
        return Scheduler.klon_värde(överordnad_värde);
    }

    public int 자식기다리기(Process_värde överordnad_värde, int barn_identifierare, boolean 기다리지않음) {
        return Scheduler.자식기다리기(överordnad_värde, barn_identifierare, 기다리지않음);
    }

    public int app_rast(Process_värde aktuellt_Process, int 새끝) {
        int Föregående_avsluta = aktuellt_Process.app_rast();
        if (새끝 == 0) {
            return Föregående_avsluta;
        }
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            return -12;
        }
        int 첫쪽 = Föregående_avsluta / Sidhanteraren.sidstorlek;
        int 끝쪽 = (새끝 + Sidhanteraren.sidstorlek - 1) / Sidhanteraren.sidstorlek;
        if (새끝 > Föregående_avsluta) {
            for (int INDEX = 첫쪽; INDEX < 끝쪽; INDEX++) {
                int Adress = INDEX * Sidhanteraren.sidstorlek;
                try {
                    쪽관리.läsa_byte_värde(aktuellt_Process.adressutrymme(), Adress);
                } catch (IllegalStateException fel) {
                    쪽관리.MAP_page(aktuellt_Process.adressutrymme(), Adress, true);
                }
            }
        }
        aktuellt_Process.uppsättning_app_rast(새끝);
        return 새끝;
    }

    public int ökning_app_rast(Process_värde aktuellt_Process, int inkrement_belopp) {
        int Föregående_avsluta = aktuellt_Process.app_rast();
        int RESULTAT = app_rast(aktuellt_Process, Föregående_avsluta + inkrement_belopp);
        return RESULTAT < 0 ? RESULTAT : Föregående_avsluta;
    }

    public int köra_kommando(Process_värde aktuellt_Process, byte[] körbar_fil_fil) {
        return köra_kommando(aktuellt_Process, körbar_fil_fil, new String[0], new String[0]);
    }

    public int köra_kommando(Process_värde aktuellt_Process, byte[] körbar_fil_fil, String[] parameter_argument, String[] miljö) {
        körbar_fil_inläsare.BILD BILD_värde;
        try {
            BILD_värde = inläsare.검사(körbar_fil_fil);
        } catch (IllegalArgumentException fel) {
            return -8;
        }
        if (parameter_argument == null || miljö == null || parameter_argument.length > 16 || miljö.length > 16) {
            return -7;
        }
        for (körbar_fil_inläsare.avsnitt_värde avsnitt_värde : BILD_värde.구역들()) {
            if ((avsnitt_värde.flagga_värde() & 2) == 0 || avsnitt_värde.Storlek() == 0) {
                continue;
            }
            int 첫쪽 = avsnitt_värde.Adress() / Sidhanteraren.sidstorlek;
            int 끝쪽 = (avsnitt_värde.Adress() + avsnitt_värde.Storlek() + Sidhanteraren.sidstorlek - 1) / Sidhanteraren.sidstorlek;
            for (int INDEX = 첫쪽; INDEX < 끝쪽; INDEX++) {
                int Adress = INDEX * Sidhanteraren.sidstorlek;
                try {
                    쪽관리.läsa_byte_värde(aktuellt_Process.adressutrymme(), Adress);
                    쪽관리.Privat_område_skriva(aktuellt_Process.adressutrymme(), Adress, Sidhanteraren.sidstorlek);
                } catch (IllegalStateException fel) {
                    쪽관리.MAP_page(aktuellt_Process.adressutrymme(), Adress, true);
                }
            }
            for (int INDEX = 0; INDEX < avsnitt_värde.Storlek(); INDEX++) {
                byte värde = avsnitt_värde.variant_värde() == 8 ? 0 : körbar_fil_fil[avsnitt_värde.fil_placera() + INDEX];
                쪽관리.skriva_byte_värde(aktuellt_Process.adressutrymme(), avsnitt_värde.Adress() + INDEX, värde);
            }
        }
        aktuellt_Process.uppsättning_körning_sammanhang(BILD_värde.START_ADRESS(), parameter_argument, miljö);
        aktuellt_Process.파일서술자().실행시닫기();
        return 0;
    }

    public void avsluta_app(Process_värde aktuellt_Process, int status_värde) {
        aktuellt_Process.Utgång_app(status_värde);
    }
}
