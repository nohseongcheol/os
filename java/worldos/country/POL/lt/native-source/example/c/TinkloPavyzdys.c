#include "예제규약.h"
#include <통신규약.h>
int main(int argumentas_COUNT,char **Argumentai) {
    if(argumentas_COUNT!=2)return Išvestis("사용법: ./네트워크 UDP창구번호\n");
    unsigned jungtis_VALUE=0;for(int numeris=0;Argumentai[1][numeris];numeris++) {
        if(Argumentai[1][numeris]<'0'||Argumentai[1][numeris]>'9')return 2;
        jungtis_VALUE=jungtis_VALUE*10+Argumentai[1][numeris]-'0';if(jungtis_VALUE>65535)return 2;
    }
    if(!jungtis_VALUE)return 2;
    int dalyvis=kurti_dalyvis(debesis_Šeima,paketų_maršruto_schemos_jungtis,paketų_kelio_schema_protokolas);if(dalyvis<0)return 3;
    struct 인터넷통신주소 ADDRESS={0};ADDRESS.ADDRESS_Šeima=debesis_Šeima;
    if(BIND_ADDRESS(dalyvis,(struct 통신주소 *)&ADDRESS,sizeof(ADDRESS))<0)return 4;
    ADDRESS.prievado_numeris=망차례짧은수(jungtis_VALUE);ADDRESS.interneto_adresas.ADDRESS_VALUE=tinklas_sveikasis_skaičius(0x0a000202);
    const char paketų_kelio_schema[]="C UDP lt";
    if(siųsti_paketų_kelio_schema_duomenys(dalyvis,paketų_kelio_schema,sizeof(paketų_kelio_schema)-1,0,(struct 통신주소 *)&ADDRESS,sizeof(ADDRESS))!=sizeof(paketų_kelio_schema)-1)return 5;
    char atsakyti[512];unsigned Paleisti=밀리초();int RECEIVED_COUNT;
    do {
        RECEIVED_COUNT=gauti_paketų_kelio_schema_duomenys(dalyvis,atsakyti,sizeof(atsakyti),0,0,0);
        if(RECEIVED_COUNT<0&&klaidos_numeris!=다시시도오류)return 6;
    } while(RECEIVED_COUNT<0&&(unsigned)(밀리초()-Paleisti)<700);
    Uždaryti_Failas(dalyvis);if(RECEIVED_COUNT!=sizeof(paketų_kelio_schema)-1)return 7;
    for(int numeris=0;numeris<RECEIVED_COUNT;numeris++)if(paketų_kelio_schema[numeris]!=atsakyti[numeris])return 8;
    return Išvestis("C 네트워크 patvirtinti: UDP lt\n");
}
