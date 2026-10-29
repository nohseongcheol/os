// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Grønland.JGrlOS.체계호출;

import Grønland.JGrlOS.Hukommelse_område.Sidestyring;
import Grønland.JGrlOS.작업.Proces_VÆRDI;
import Grønland.JGrlOS.작업.Scheduler;
import Grønland.JGrlOS.filsystem.eksekverbar_fil_indlæsningsfunktion;
import Grønland.JGrlOS.filsystem.filsystem;
import Grønland.JGrlOS.filsystem.fil_info;
import Grønland.JGrlOS.kerne.hardware_VÆRDI;
import Grønland.JGrlOS.input_VÆRDI.input_Leder;
import Grønland.JGrlOS.input_VÆRDI.inputhændelse;

/** engos POSIX 1단계 호출의 Java 관리 계층이다. */
public final class 체계호출 {
    public static final int skrivebeskyttet_flag = 0;
    public static final int SØG_START = 0;
    public static final int SØG_aktuel = 1;
    public static final int Søg_post_afslutte_et_opkald = 2;

    private final filsystem filsystem;
    private final Sidestyring 쪽관리;
    private final Scheduler Scheduler;
    private final eksekverbar_fil_indlæsningsfunktion indlæsningsfunktion = new eksekverbar_fil_indlæsningsfunktion();
    private final hardware_VÆRDI enhed_VÆRDI;
    private final input_Leder 입력관리;

    public 체계호출(filsystem filsystem, Sidestyring 쪽관리, Scheduler Scheduler, hardware_VÆRDI enhed_VÆRDI, input_Leder 입력관리) {
        this.filsystem = filsystem;
        this.쪽관리 = 쪽관리;
        this.Scheduler = Scheduler;
        this.enhed_VÆRDI = enhed_VÆRDI;
        this.입력관리 = 입력관리;
    }

    public int Proces_identifikator(Proces_VÆRDI aktuel_Proces) {
        return aktuel_Proces.identifikator_VÆRDI();
    }

    public int overordnet_Proces_identifikator(Proces_VÆRDI aktuel_Proces) {
        return aktuel_Proces.overordnet_identifikator();
    }

    public int Åbn(Proces_VÆRDI aktuel_Proces, String Navn, int flag_VÆRDI) {
        if (flag_VÆRDI != skrivebeskyttet_flag) {
            return -30;
        }
        return aktuel_Proces.파일서술자().Åbn(Navn);
    }

    public int Læse(Proces_VÆRDI aktuel_Proces, int 서술자, byte[] modtage_destination, int Størrelse) {
        if (서술자 == 0) {
            if (Størrelse <= 0 || modtage_destination.length == 0) {
                return 0;
            }
            inputhændelse hændelse = 입력관리.Næste_hændelse();
            if (hændelse == null || hændelse.hændelsestype() != inputhændelse.종류.tast_nede) {
                return -11;
            }
            modtage_destination[0] = (byte) hændelse.첫째값();
            return 1;
        }
        return aktuel_Proces.파일서술자().Læse(서술자, modtage_destination, Størrelse);
    }

    public int Skrive(Proces_VÆRDI aktuel_Proces, int 서술자, byte[] data, int Størrelse) {
        if (서술자 != 1 && 서술자 != 2) {
            return aktuel_Proces.파일서술자().it_åben(서술자) ? -30 : -9;
        }
        if (Størrelse < 0 || Størrelse > data.length) {
            return -22;
        }
        enhed_VÆRDI.직렬출력(new String(data, 0, Størrelse, java.nio.charset.StandardCharsets.UTF_8));
        return Størrelse;
    }

    public int Luk(Proces_VÆRDI aktuel_Proces, int 서술자) {
        return aktuel_Proces.파일서술자().Luk(서술자);
    }

    public int flytte_placere(Proces_VÆRDI aktuel_Proces, int 서술자, int 거리, int To_do_rod) {
        return aktuel_Proces.파일서술자().flytte_placere(서술자, 거리, To_do_rod);
    }

    public int 서술자복제(Proces_VÆRDI aktuel_Proces, int 서술자) {
        return aktuel_Proces.파일서술자().복제서술자(서술자, 0);
    }

    public int 지정서술자복제(Proces_VÆRDI aktuel_Proces, int 서술자, int 새서술자) {
        return aktuel_Proces.파일서술자().지정복제(서술자, 새서술자);
    }

    public int 접근가능(String Navn, int metode_HYPPIGST) {
        fil_info msinfo32_exe = filsystem.msinfo32_exe(Navn);
        if (msinfo32_exe == null) {
            return -2;
        }
        if ((metode_HYPPIGST & 1) != 0 && (msinfo32_exe.형태() & 0111) == 0) {
            return -13;
        }
        if ((metode_HYPPIGST & 2) != 0) {
            return -30;
        }
        return 0;
    }

    public int SKIFT_Opgaveliste(String Navn) {
        return "/".equals(Navn) ? 0 : -20;
    }

    public String aktuel_Opgaveliste(int modtage_tilpasse_størrelse) {
        return modtage_tilpasse_størrelse >= 2 ? "/" : null;
    }

    public int UID() { return 0; }
    public int effektiv_UID() { return 0; }
    public int gruppe_identifikator() { return 0; }
    public int effektiv_gruppe_identifikator() { return 0; }

    public int synkronisere_fil(Proces_VÆRDI aktuel_Proces, int 서술자) {
        return aktuel_Proces.파일서술자().msinfo32_exe(서술자) == null ? -9 : 0;
    }

    public void 모두동기화() {
        // aktuel_vare 파일체계는 Læse 전용이어서 밀어낼 자료가 없다.
    }

    public boolean it_Terminal(Proces_VÆRDI aktuel_Proces, int 서술자) {
        fil_info msinfo32_exe = aktuel_Proces.파일서술자().msinfo32_exe(서술자);
        return msinfo32_exe != null && (msinfo32_exe.형태() & 0170000) == 0020000;
    }

    public int fil_kontrol(Proces_VÆRDI aktuel_Proces, int 서술자, int Kommando, int parameter_argument) {
        if (Kommando == 0) {
            return aktuel_Proces.파일서술자().복제서술자(서술자, parameter_argument);
        }
        if (Kommando == 1) {
            return aktuel_Proces.파일서술자().실행시닫기값(서술자);
        }
        if (Kommando == 2) {
            return aktuel_Proces.파일서술자().실행시닫기설정(서술자, (parameter_argument & 1) != 0);
        }
        if (Kommando == 3) {
            return aktuel_Proces.파일서술자().msinfo32_exe(서술자) == null ? -9 : skrivebeskyttet_flag;
        }
        if (Kommando == 4) {
            return parameter_argument == skrivebeskyttet_flag ? 0 : -30;
        }
        return -22;
    }

    public int åbne_post_81b8d99b(String Navn, int rettighed_VÆRDI) {
        return -30;
    }

    public fil_info 서술자정보(Proces_VÆRDI aktuel_Proces, int 서술자) {
        return aktuel_Proces.파일서술자().msinfo32_exe(서술자);
    }

    public System_Detaljer System_Detaljer() {
        return new System_Detaljer("JGrlOS", "JGrlOS", "0.1", "Java managed kernel", "i386");
    }

    public fil_info fil_info(String Navn) {
        return filsystem.msinfo32_exe(Navn);
    }

    public Proces_VÆRDI klon_Proces(Proces_VÆRDI overordnet_VÆRDI) {
        return Scheduler.klon_VÆRDI(overordnet_VÆRDI);
    }

    public int 자식기다리기(Proces_VÆRDI overordnet_VÆRDI, int barn_identifikator, boolean 기다리지않음) {
        return Scheduler.자식기다리기(overordnet_VÆRDI, barn_identifikator, 기다리지않음);
    }

    public int app_pause(Proces_VÆRDI aktuel_Proces, int 새끝) {
        int Forrige_afslutte_et_opkald = aktuel_Proces.app_pause();
        if (새끝 == 0) {
            return Forrige_afslutte_et_opkald;
        }
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            return -12;
        }
        int 첫쪽 = Forrige_afslutte_et_opkald / Sidestyring.sidestørrelse;
        int 끝쪽 = (새끝 + Sidestyring.sidestørrelse - 1) / Sidestyring.sidestørrelse;
        if (새끝 > Forrige_afslutte_et_opkald) {
            for (int INDEKS = 첫쪽; INDEKS < 끝쪽; INDEKS++) {
                int mail = INDEKS * Sidestyring.sidestørrelse;
                try {
                    쪽관리.바이트읽기(aktuel_Proces.adresseinterval(), mail);
                } catch (IllegalStateException fejl) {
                    쪽관리.MAP_side(aktuel_Proces.adresseinterval(), mail, true);
                }
            }
        }
        aktuel_Proces.sæt_app_pause(새끝);
        return 새끝;
    }

    public int forøgelse_app_pause(Proces_VÆRDI aktuel_Proces, int gradvis_forøgelse_sum) {
        int Forrige_afslutte_et_opkald = aktuel_Proces.app_pause();
        int KR = app_pause(aktuel_Proces, Forrige_afslutte_et_opkald + gradvis_forøgelse_sum);
        return KR < 0 ? KR : Forrige_afslutte_et_opkald;
    }

    public int Udfør_kommando(Proces_VÆRDI aktuel_Proces, byte[] eksekverbar_fil) {
        return Udfør_kommando(aktuel_Proces, eksekverbar_fil, new String[0], new String[0]);
    }

    public int Udfør_kommando(Proces_VÆRDI aktuel_Proces, byte[] eksekverbar_fil, String[] parameter_argument, String[] miljø) {
        eksekverbar_fil_indlæsningsfunktion.Image Image_VÆRDI;
        try {
            Image_VÆRDI = indlæsningsfunktion.검사(eksekverbar_fil);
        } catch (IllegalArgumentException fejl) {
            return -8;
        }
        if (parameter_argument == null || miljø == null || parameter_argument.length > 16 || miljø.length > 16) {
            return -7;
        }
        for (eksekverbar_fil_indlæsningsfunktion.sektion_VÆRDI sektion_VÆRDI : Image_VÆRDI.구역들()) {
            if ((sektion_VÆRDI.flag_VÆRDI() & 2) == 0 || sektion_VÆRDI.Størrelse() == 0) {
                continue;
            }
            int 첫쪽 = sektion_VÆRDI.mail() / Sidestyring.sidestørrelse;
            int 끝쪽 = (sektion_VÆRDI.mail() + sektion_VÆRDI.Størrelse() + Sidestyring.sidestørrelse - 1) / Sidestyring.sidestørrelse;
            for (int INDEKS = 첫쪽; INDEKS < 끝쪽; INDEKS++) {
                int mail = INDEKS * Sidestyring.sidestørrelse;
                try {
                    쪽관리.바이트읽기(aktuel_Proces.adresseinterval(), mail);
                    쪽관리.privat_område_skrive(aktuel_Proces.adresseinterval(), mail, Sidestyring.sidestørrelse);
                } catch (IllegalStateException fejl) {
                    쪽관리.MAP_side(aktuel_Proces.adresseinterval(), mail, true);
                }
            }
            for (int INDEKS = 0; INDEKS < sektion_VÆRDI.Størrelse(); INDEKS++) {
                byte VÆRDI = sektion_VÆRDI.종류() == 8 ? 0 : eksekverbar_fil[sektion_VÆRDI.fil_placere() + INDEKS];
                쪽관리.skrive_byte_VÆRDI(aktuel_Proces.adresseinterval(), sektion_VÆRDI.mail() + INDEKS, VÆRDI);
            }
        }
        aktuel_Proces.sæt_udførelse_kontekst(Image_VÆRDI.START_mail(), parameter_argument, miljø);
        aktuel_Proces.파일서술자().실행시닫기();
        return 0;
    }

    public void afslut_app(Proces_VÆRDI aktuel_Proces, int status_VÆRDI) {
        aktuel_Proces.Afslut_app(status_VÆRDI);
    }
}
