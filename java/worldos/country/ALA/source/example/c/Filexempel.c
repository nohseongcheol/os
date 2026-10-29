#include "예제규약.h"
int main(void) {
    const char data[]="C filnamn: Svenska 😀\n";
    int filnamn=skapa_fil("c.txt",läsa_skriva|없으면만들기|trimma_Innehåll,0600);
    if(filnamn<0)return 1;
    if(skriva_fil_data(filnamn,data,sizeof(data)-1)!=sizeof(data)-1)return 2;
    if(söka_fil(filnamn,0,처음기준)!=0)return 3;
    char läsa_SMS_värde[128]={0};int längd_värde=läsa_fil_data(filnamn,läsa_SMS_värde,sizeof(läsa_SMS_värde)-1);
    Stäng_fil(filnamn);
    if(längd_värde!=sizeof(data)-1)return 4;
    for(int nummer=0;nummer<längd_värde;nummer++)if(data[nummer]!=läsa_SMS_värde[nummer])return 5;
    return utmatningsposition(läsa_SMS_värde);
}
