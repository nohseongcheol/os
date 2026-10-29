// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Svalbard_og_Jan_Mayen.JSjmOS.체계호출;

import Svalbard_og_Jan_Mayen.JSjmOS.Minne_område.Sidebehandling;
import Svalbard_og_Jan_Mayen.JSjmOS.작업.Prosess_VERDI;
import Svalbard_og_Jan_Mayen.JSjmOS.작업.Scheduler;
import Svalbard_og_Jan_Mayen.JSjmOS.filsystem.kjørbar_fil_laster;
import Svalbard_og_Jan_Mayen.JSjmOS.filsystem.filsystem;
import Svalbard_og_Jan_Mayen.JSjmOS.filsystem.Fil_info;
import Svalbard_og_Jan_Mayen.JSjmOS.kjerne.maskinvare_VERDI;
import Svalbard_og_Jan_Mayen.JSjmOS.inndata_VERDI.inndata_overordnet;
import Svalbard_og_Jan_Mayen.JSjmOS.inndata_VERDI.inndatahendelse;

/** engos POSIX 1단계 호출의 Java 관리 계층이다. */
public final class 체계호출 {
    public static final int skrivebeskyttet_flagg = 0;
    public static final int SØK_START = 0;
    public static final int SØK_betalt = 1;
    public static final int Søk_oppføring_avslutte_en_samtale = 2;

    private final filsystem filsystem;
    private final Sidebehandling 쪽관리;
    private final Scheduler Scheduler;
    private final kjørbar_fil_laster laster = new kjørbar_fil_laster();
    private final maskinvare_VERDI enhet_VERDI;
    private final inndata_overordnet 입력관리;

    public 체계호출(filsystem filsystem, Sidebehandling 쪽관리, Scheduler Scheduler, maskinvare_VERDI enhet_VERDI, inndata_overordnet 입력관리) {
        this.filsystem = filsystem;
        this.쪽관리 = 쪽관리;
        this.Scheduler = Scheduler;
        this.enhet_VERDI = enhet_VERDI;
        this.입력관리 = 입력관리;
    }

    public int Prosess_identifikator(Prosess_VERDI betalt_Prosess) {
        return betalt_Prosess.identifikator_VERDI();
    }

    public int overordnet_Prosess_identifikator(Prosess_VERDI betalt_Prosess) {
        return betalt_Prosess.overordnet_identifikator();
    }

    public int Åpne(Prosess_VERDI betalt_Prosess, String Navn, int flagg_VERDI) {
        if (flagg_VERDI != skrivebeskyttet_flagg) {
            return -30;
        }
        return betalt_Prosess.파일서술자().Åpne(Navn);
    }

    public int Les(Prosess_VERDI betalt_Prosess, int 서술자, byte[] motta_mål, int Størrelse) {
        if (서술자 == 0) {
            if (Størrelse <= 0 || motta_mål.length == 0) {
                return 0;
            }
            inndatahendelse Hendelse = 입력관리.Neste_hendelse();
            if (Hendelse == null || Hendelse.사건종류() != inndatahendelse.종류.키누름) {
                return -11;
            }
            motta_mål[0] = (byte) Hendelse.첫째값();
            return 1;
        }
        return betalt_Prosess.파일서술자().Les(서술자, motta_mål, Størrelse);
    }

    public int Skriv(Prosess_VERDI betalt_Prosess, int 서술자, byte[] data, int Størrelse) {
        if (서술자 != 1 && 서술자 != 2) {
            return betalt_Prosess.파일서술자().informasjonssystemer_åpen(서술자) ? -30 : -9;
        }
        if (Størrelse < 0 || Størrelse > data.length) {
            return -22;
        }
        enhet_VERDI.직렬출력(new String(data, 0, Størrelse, java.nio.charset.StandardCharsets.UTF_8));
        return Størrelse;
    }

    public int Lukk(Prosess_VERDI betalt_Prosess, int 서술자) {
        return betalt_Prosess.파일서술자().Lukk(서술자);
    }

    public int flytte_plassere(Prosess_VERDI betalt_Prosess, int 서술자, int 거리, int speile_rot) {
        return betalt_Prosess.파일서술자().flytte_plassere(서술자, 거리, speile_rot);
    }

    public int 서술자복제(Prosess_VERDI betalt_Prosess, int 서술자) {
        return betalt_Prosess.파일서술자().복제서술자(서술자, 0);
    }

    public int 지정서술자복제(Prosess_VERDI betalt_Prosess, int 서술자, int 새서술자) {
        return betalt_Prosess.파일서술자().지정복제(서술자, 새서술자);
    }

    public int 접근가능(String Navn, int metode_MODUS) {
        Fil_info msinfo32_exe = filsystem.msinfo32_exe(Navn);
        if (msinfo32_exe == null) {
            return -2;
        }
        if ((metode_MODUS & 1) != 0 && (msinfo32_exe.형태() & 0111) == 0) {
            return -13;
        }
        if ((metode_MODUS & 2) != 0) {
            return -30;
        }
        return 0;
    }

    public int bytt_Oppgaveliste(String Navn) {
        return "/".equals(Navn) ? 0 : -20;
    }

    public String betalt_Oppgaveliste(int motta_skalere) {
        return motta_skalere >= 2 ? "/" : null;
    }

    public int UID() { return 0; }
    public int effektiv_UID() { return 0; }
    public int gruppe_identifikator() { return 0; }
    public int effektiv_gruppe_identifikator() { return 0; }

    public int synkronisere_Fil(Prosess_VERDI betalt_Prosess, int 서술자) {
        return betalt_Prosess.파일서술자().msinfo32_exe(서술자) == null ? -9 : 0;
    }

    public void 모두동기화() {
        // betalt_vare 파일체계는 Les 전용이어서 밀어낼 자료가 없다.
    }

    public boolean informasjonssystemer_Terminal(Prosess_VERDI betalt_Prosess, int 서술자) {
        Fil_info msinfo32_exe = betalt_Prosess.파일서술자().msinfo32_exe(서술자);
        return msinfo32_exe != null && (msinfo32_exe.형태() & 0170000) == 0020000;
    }

    public int Fil_kontroll(Prosess_VERDI betalt_Prosess, int 서술자, int Kommando, int parameter_argument) {
        if (Kommando == 0) {
            return betalt_Prosess.파일서술자().복제서술자(서술자, parameter_argument);
        }
        if (Kommando == 1) {
            return betalt_Prosess.파일서술자().실행시닫기값(서술자);
        }
        if (Kommando == 2) {
            return betalt_Prosess.파일서술자().실행시닫기설정(서술자, (parameter_argument & 1) != 0);
        }
        if (Kommando == 3) {
            return betalt_Prosess.파일서술자().msinfo32_exe(서술자) == null ? -9 : skrivebeskyttet_flagg;
        }
        if (Kommando == 4) {
            return parameter_argument == skrivebeskyttet_flagg ? 0 : -30;
        }
        return -22;
    }

    public int åpne_oppføring(String Navn, int tillatelse_VERDI) {
        return -30;
    }

    public Fil_info 서술자정보(Prosess_VERDI betalt_Prosess, int 서술자) {
        return betalt_Prosess.파일서술자().msinfo32_exe(서술자);
    }

    public System_Detaljer System_Detaljer() {
        return new System_Detaljer("JSjmOS", "JSjmOS", "0.1", "Java managed kernel", "i386");
    }

    public Fil_info Fil_info(String Navn) {
        return filsystem.msinfo32_exe(Navn);
    }

    public Prosess_VERDI klon_Prosess(Prosess_VERDI overordnet_VERDI_881a8172) {
        return Scheduler.klon_VERDI(overordnet_VERDI_881a8172);
    }

    public int 자식기다리기(Prosess_VERDI overordnet_VERDI_881a8172, int barn_identifikator, boolean 기다리지않음) {
        return Scheduler.자식기다리기(overordnet_VERDI_881a8172, barn_identifikator, 기다리지않음);
    }

    public int app_pause(Prosess_VERDI betalt_Prosess, int 새끝) {
        int Forrige_avslutte_en_samtale = betalt_Prosess.app_pause();
        if (새끝 == 0) {
            return Forrige_avslutte_en_samtale;
        }
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            return -12;
        }
        int 첫쪽 = Forrige_avslutte_en_samtale / Sidebehandling.sidestørrelse;
        int 끝쪽 = (새끝 + Sidebehandling.sidestørrelse - 1) / Sidebehandling.sidestørrelse;
        if (새끝 > Forrige_avslutte_en_samtale) {
            for (int INDEKS = 첫쪽; INDEKS < 끝쪽; INDEKS++) {
                int e_post = INDEKS * Sidebehandling.sidestørrelse;
                try {
                    쪽관리.바이트읽기(betalt_Prosess.adresseområde(), e_post);
                } catch (IllegalStateException feil) {
                    쪽관리.kart_page(betalt_Prosess.adresseområde(), e_post, true);
                }
            }
        }
        betalt_Prosess.sett_app_pause(새끝);
        return 새끝;
    }

    public int økning_app_pause(Prosess_VERDI betalt_Prosess, int øke_trinnvis_beløp) {
        int Forrige_avslutte_en_samtale = betalt_Prosess.app_pause();
        int KR = app_pause(betalt_Prosess, Forrige_avslutte_en_samtale + øke_trinnvis_beløp);
        return KR < 0 ? KR : Forrige_avslutte_en_samtale;
    }

    public int Utfør_kommando(Prosess_VERDI betalt_Prosess, byte[] kjørbar_fil) {
        return Utfør_kommando(betalt_Prosess, kjørbar_fil, new String[0], new String[0]);
    }

    public int Utfør_kommando(Prosess_VERDI betalt_Prosess, byte[] kjørbar_fil, String[] parameter_argument, String[] miljø) {
        kjørbar_fil_laster.BILDE BILDE_VERDI;
        try {
            BILDE_VERDI = laster.검사(kjørbar_fil);
        } catch (IllegalArgumentException feil) {
            return -8;
        }
        if (parameter_argument == null || miljø == null || parameter_argument.length > 16 || miljø.length > 16) {
            return -7;
        }
        for (kjørbar_fil_laster.inndeling_VERDI inndeling_VERDI : BILDE_VERDI.구역들()) {
            if ((inndeling_VERDI.flagg_VERDI() & 2) == 0 || inndeling_VERDI.Størrelse() == 0) {
                continue;
            }
            int 첫쪽 = inndeling_VERDI.e_post() / Sidebehandling.sidestørrelse;
            int 끝쪽 = (inndeling_VERDI.e_post() + inndeling_VERDI.Størrelse() + Sidebehandling.sidestørrelse - 1) / Sidebehandling.sidestørrelse;
            for (int INDEKS = 첫쪽; INDEKS < 끝쪽; INDEKS++) {
                int e_post = INDEKS * Sidebehandling.sidestørrelse;
                try {
                    쪽관리.바이트읽기(betalt_Prosess.adresseområde(), e_post);
                    쪽관리.privat_område_skrive(betalt_Prosess.adresseområde(), e_post, Sidebehandling.sidestørrelse);
                } catch (IllegalStateException feil) {
                    쪽관리.kart_page(betalt_Prosess.adresseområde(), e_post, true);
                }
            }
            for (int INDEKS = 0; INDEKS < inndeling_VERDI.Størrelse(); INDEKS++) {
                byte VERDI = inndeling_VERDI.종류() == 8 ? 0 : kjørbar_fil[inndeling_VERDI.Fil_plassere() + INDEKS];
                쪽관리.skrive_byte_VERDI(betalt_Prosess.adresseområde(), inndeling_VERDI.e_post() + INDEKS, VERDI);
            }
        }
        betalt_Prosess.sett_kjøring_kontekst(BILDE_VERDI.START_e_post(), parameter_argument, miljø);
        betalt_Prosess.파일서술자().실행시닫기();
        return 0;
    }

    public void avslutt_app(Prosess_VERDI betalt_Prosess, int status_VERDI) {
        betalt_Prosess.Utgang_app(status_VERDI);
    }
}
