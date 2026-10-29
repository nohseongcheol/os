#include "../명명/기계연결이름.h"
/* Static Java 8 bytecode -> C -> TinyCC ARM64 code, entirely inside EL0.
 * This is not a complete JVM. Unsupported instructions/APIs stop compilation.
 */
#include "호출.h"
#include "grupo.h"
#include "stdio.h"
#include <stdarg.h>
#include <string.h>
#include <stdint.h>
static unsigned char dados[16384];static unsigned duração_VALOR,em_dia_cargo;static int TI_inválido;
static unsigned Rótulos_Lista[512],첫째값[512],SEGUNDO_VALOR[512],constante_pool,em_dia_aula;
static char texto[65536];static unsigned Tamanho_do_texto;
typedef struct {unsigned Configuração_BITS,Nome,descritor_dados,instrução_SEQUÊNCIA,Tamanho,지역변수들,memória_de_pilha;} método_entrada;
static método_entrada 메소드목록[64];static unsigned 메소드개수;
static unsigned nome_de_campo[64],Campo_descritor[64],Campo_constante[64],필드개수;
static unsigned PEGAR_VALOR(unsigned item_CONT_NÚM){if(em_dia_cargo>duração_VALOR||item_CONT_NÚM>duração_VALOR-em_dia_cargo){TI_inválido=1;return 0;}unsigned dados_cargo=em_dia_cargo;em_dia_cargo+=item_CONT_NÚM;return dados_cargo;}
static unsigned byte_dados(void){unsigned dados_cargo=PEGAR_VALOR(1);return TI_inválido?0:dados[dados_cargo];}
static unsigned 절반값(void){unsigned coordenada_X=byte_dados();return coordenada_X<<8|byte_dados();}
static uint32_t 가득참(void){uint32_t coordenada_X=절반값();return coordenada_X<<16|절반값();}
static int UNICODE_VALOR(unsigned 순번,const char*cadeia_dados){return 순번>0&&순번<constante_pool&&Rótulos_Lista[순번]==1&&strlen(cadeia_dados)==SEGUNDO_VALOR[순번]&&!memcmp(dados+첫째값[순번],cadeia_dados,SEGUNDO_VALOR[순번]);}
static int 같음(unsigned coordenada_X,unsigned Y_coordenada){return coordenada_X>0&&coordenada_X<constante_pool&&Y_coordenada>0&&Y_coordenada<constante_pool&&Rótulos_Lista[coordenada_X]==1&&Rótulos_Lista[Y_coordenada]==1&&SEGUNDO_VALOR[coordenada_X]==SEGUNDO_VALOR[Y_coordenada]&&!memcmp(dados+첫째값[coordenada_X],dados+첫째값[Y_coordenada],SEGUNDO_VALOR[coordenada_X]);}
static void 내보내기(const char*Arquivo_entrada,...){if(TI_inválido)return;va_list argumento_MATRIZ;va_start(argumento_MATRIZ,Arquivo_entrada);int item_CONT_NÚM=vsnprintf(texto+Tamanho_do_texto,sizeof(texto)-Tamanho_do_texto,Arquivo_entrada,argumento_MATRIZ);va_end(argumento_MATRIZ);if(item_CONT_NÚM<0||(unsigned)item_CONT_NÚM>=sizeof(texto)-Tamanho_do_texto){TI_inválido=1;return;}Tamanho_do_texto+=item_CONT_NÚM;}
static int descritor_entrada(unsigned identificador_VALOR,int*resultado){
    if(identificador_VALOR<1||identificador_VALOR>=constante_pool||Rótulos_Lista[identificador_VALOR]!=1)return -1;unsigned dados_cargo=첫째값[identificador_VALOR],encerrar_DESLOC=dados_cargo+SEGUNDO_VALOR[identificador_VALOR];if(dados_cargo>=encerrar_DESLOC||dados[dados_cargo++]!='(')return -1;int entrada_CONT_NÚM_8f7753a1=0;
    while(dados_cargo<encerrar_DESLOC&&dados[dados_cargo]!=')'){
        unsigned ponto_de_código=dados[dados_cargo++];while(ponto_de_código=='['&&dados_cargo<encerrar_DESLOC)ponto_de_código=dados[dados_cargo++];
        if(ponto_de_código=='L'){while(dados_cargo<encerrar_DESLOC&&dados[dados_cargo]!=';')dados_cargo++;if(dados_cargo==encerrar_DESLOC)return -1;dados_cargo++;}
        else if(ponto_de_código!='I'&&ponto_de_código!='Z'&&ponto_de_código!='B'&&ponto_de_código!='C'&&ponto_de_código!='S')return -1;
        if(++entrada_CONT_NÚM_8f7753a1>16)return -1;
    }
    if(dados_cargo+1>=encerrar_DESLOC||dados[dados_cargo++]!=')')return -1;*resultado=dados[dados_cargo]=='V'?0:1;
    if(dados[dados_cargo]=='J'||dados[dados_cargo]=='D'||dados[dados_cargo]=='F')return -1;return entrada_CONT_NÚM_8f7753a1;
}
static void características(void){unsigned item_CONT_NÚM=절반값();for(unsigned 순번=0;순번<item_CONT_NÚM&&!TI_inválido;순번++){절반값();unsigned Tamanho=가득참();PEGAR_VALOR(Tamanho);}}
static int analisar_entrada(void){
    if(가득참()!=0xcafebabe)return -1;unsigned versão_secundária=절반값(),número_de_versão=절반값();if(versão_secundária||número_de_versão<45||número_de_versão>52)return -1;
    constante_pool=절반값();if(constante_pool<1||constante_pool>512)return -1;
    for(unsigned 순번=1;순번<constante_pool&&!TI_inválido;순번++){
        Rótulos_Lista[순번]=byte_dados();switch(Rótulos_Lista[순번]){
        case 1:SEGUNDO_VALOR[순번]=절반값();첫째값[순번]=PEGAR_VALOR(SEGUNDO_VALOR[순번]);break;case 3:case 4:첫째값[순번]=가득참();break;
        case 5:case 6:PEGAR_VALOR(8);if(++순번>=constante_pool)return -1;break;
        case 7:case 8:case 16:첫째값[순번]=절반값();break;
        case 9:case 10:case 11:case 12:case 18:첫째값[순번]=절반값();SEGUNDO_VALOR[순번]=절반값();break;
        case 15:첫째값[순번]=byte_dados();SEGUNDO_VALOR[순번]=절반값();break;default:return -1;
        }
    }
    절반값();em_dia_aula=절반값();절반값();if(em_dia_aula<1||em_dia_aula>=constante_pool||Rótulos_Lista[em_dia_aula]!=7||첫째값[em_dia_aula]<1||첫째값[em_dia_aula]>=constante_pool||Rótulos_Lista[첫째값[em_dia_aula]]!=1)return -1;unsigned 인터페이스목록=절반값();PEGAR_VALOR(인터페이스목록*2);
    필드개수=절반값();if(필드개수>64)return -1;
    for(unsigned 순번=0;순번<필드개수&&!TI_inválido;순번++){
        unsigned Configuração_BITS=절반값();nome_de_campo[순번]=절반값();Campo_descritor[순번]=절반값();
        if(!(Configuração_BITS&8))return -1;
        unsigned entrada_CONT_NÚM_8f7753a1=절반값();for(unsigned 안쪽순번=0;안쪽순번<entrada_CONT_NÚM_8f7753a1&&!TI_inválido;안쪽순번++){
            unsigned Nome=절반값(),Tamanho=가득참();
            if(UNICODE_VALOR(Nome,"ConstantValue")){if(Tamanho!=2)return -1;Campo_constante[순번]=절반값();}
            else PEGAR_VALOR(Tamanho);
        }
    }
    메소드개수=절반값();if(메소드개수>64)return -1;
    for(unsigned 순번=0;순번<메소드개수&&!TI_inválido;순번++){
        método_entrada*Grupo_dimensionar=메소드목록+순번;Grupo_dimensionar->Configuração_BITS=절반값();Grupo_dimensionar->Nome=절반값();Grupo_dimensionar->descritor_dados=절반값();unsigned entrada_CONT_NÚM_8f7753a1=절반값();
        for(unsigned 안쪽순번=0;안쪽순번<entrada_CONT_NÚM_8f7753a1&&!TI_inválido;안쪽순번++){
            unsigned Nome=절반값(),Tamanho=가득참(),iniciar=em_dia_cargo;
            if(Tamanho>duração_VALOR-em_dia_cargo)return -1;
            if(UNICODE_VALOR(Nome,"Code")){
                Grupo_dimensionar->memória_de_pilha=절반값();Grupo_dimensionar->지역변수들=절반값();Grupo_dimensionar->Tamanho=가득참();Grupo_dimensionar->instrução_SEQUÊNCIA=PEGAR_VALOR(Grupo_dimensionar->Tamanho);
                if(Grupo_dimensionar->memória_de_pilha>128||Grupo_dimensionar->지역변수들>128||Grupo_dimensionar->Tamanho>8192||절반값())return -1;características();
            }else PEGAR_VALOR(Tamanho);
            if(em_dia_cargo!=iniciar+Tamanho)return -1;
        }
        if(!UNICODE_VALOR(Grupo_dimensionar->Nome,"<init>")&&(!(Grupo_dimensionar->Configuração_BITS&8)||(Grupo_dimensionar->Configuração_BITS&(0x100|0x20))||!Grupo_dimensionar->Tamanho))return -1;
    }
    características();return TI_inválido||em_dia_cargo!=duração_VALOR?-1:0;
}
static void constante_VALOR(unsigned identificador_VALOR){
    if(!identificador_VALOR||identificador_VALOR>=constante_pool){TI_inválido=1;return;}
    if(Rótulos_Lista[identificador_VALOR]==3)내보내기("P(%uU);",첫째값[identificador_VALOR]);
    else if(Rótulos_Lista[identificador_VALOR]==8)내보내기("P((W)k%u);",identificador_VALOR);else TI_inválido=1;
}
static void 호출(unsigned identificador_VALOR,int virtual_Ligar){
    if(identificador_VALOR<1||identificador_VALOR>=constante_pool||(Rótulos_Lista[identificador_VALOR]!=10&&Rótulos_Lista[identificador_VALOR]!=11)||첫째값[identificador_VALOR]<1||첫째값[identificador_VALOR]>=constante_pool||Rótulos_Lista[첫째값[identificador_VALOR]]!=7||SEGUNDO_VALOR[identificador_VALOR]<1||SEGUNDO_VALOR[identificador_VALOR]>=constante_pool||Rótulos_Lista[SEGUNDO_VALOR[identificador_VALOR]]!=12){TI_inválido=1;return;}
    unsigned proprietário_objeto=첫째값[첫째값[identificador_VALOR]],Nome=첫째값[SEGUNDO_VALOR[identificador_VALOR]],descritor_dados=SEGUNDO_VALOR[SEGUNDO_VALOR[identificador_VALOR]];int resultado=0,item_CONT_NÚM=descritor_entrada(descritor_dados,&resultado);if(item_CONT_NÚM<0){TI_inválido=1;return;}
    for(int 순번=item_CONT_NÚM;순번>0;순번--)내보내기("x[%d]=Q();",순번-1);if(virtual_Ligar)내보내기("Q();");
    if(!virtual_Ligar&&같음(proprietário_objeto,첫째값[em_dia_aula])){
        unsigned Grupo_dimensionar=0;for(;Grupo_dimensionar<메소드개수;Grupo_dimensionar++)if(같음(Nome,메소드목록[Grupo_dimensionar].Nome)&&같음(descritor_dados,메소드목록[Grupo_dimensionar].descritor_dados))break;
        if(Grupo_dimensionar==메소드개수||!(메소드목록[Grupo_dimensionar].Configuração_BITS&8)){TI_inválido=1;return;}
        if(resultado)내보내기("P(");내보내기("m%u(",Grupo_dimensionar);for(int 순번=0;순번<item_CONT_NÚM;순번++)내보내기(순번?",x[%d]":"x[%d]",순번);내보내기(resultado?"));":" );");return;
    }
    if((virtual_Ligar&&UNICODE_VALOR(proprietário_objeto,"java/io/PrintStream")&& (UNICODE_VALOR(Nome,"print")||UNICODE_VALOR(Nome,"println")))||(!virtual_Ligar&&UNICODE_VALOR(proprietário_objeto,"Português/nativo/saídaTexto"))){
        if(UNICODE_VALOR(descritor_dados,"(I)V")&&(UNICODE_VALOR(Nome,"print")||UNICODE_VALOR(Nome,"println")||UNICODE_VALOR(Nome,"gravar_número"))){내보내기("jprint(x[0],1,%d);",UNICODE_VALOR(Nome,"print")?0:1);return;}
        if(UNICODE_VALOR(descritor_dados,"(Ljava/lang/String;)V")&&(UNICODE_VALOR(Nome,"print")||UNICODE_VALOR(Nome,"println")||UNICODE_VALOR(Nome,"Escrita")||UNICODE_VALOR(Nome,"gravar_linha"))){내보내기("jprint(x[0],0,%d);",UNICODE_VALOR(Nome,"print")||UNICODE_VALOR(Nome,"Escrita")?0:1);return;}
        if(UNICODE_VALOR(descritor_dados,"()V")&&UNICODE_VALOR(Nome,"println")){내보내기("jprint((W)\"\",0,1);");return;}
    }
    if(!virtual_Ligar&&UNICODE_VALOR(proprietário_objeto,"Português/nativo/ficheiro")){
        if(UNICODE_VALOR(Nome,"Escrita")&&UNICODE_VALOR(descritor_dados,"(Ljava/lang/String;Ljava/lang/String;)V")){내보내기("jfwrite(x[0],x[1]);");return;}
        if(UNICODE_VALOR(Nome,"Leitura")&&UNICODE_VALOR(descritor_dados,"(Ljava/lang/String;)Ljava/lang/String;")){내보내기("P(jfread(x[0]));");return;}
    }
    TI_inválido=1;
}
static void compilar_método(unsigned PROC_ÍNDICE){
    método_entrada*Grupo_dimensionar=메소드목록+PROC_ÍNDICE;if(UNICODE_VALOR(Grupo_dimensionar->Nome,"<init>"))return;int resultado,item_CONT_NÚM=descritor_entrada(Grupo_dimensionar->descritor_dados,&resultado);if(item_CONT_NÚM<0){TI_inválido=1;return;}
    내보내기("static W m%u(",PROC_ÍNDICE);for(int 순번=0;순번<item_CONT_NÚM;순번++)내보내기(순번?",W a%d":"W a%d",순번);if(!item_CONT_NÚM)내보내기("void");
    if((unsigned)item_CONT_NÚM>Grupo_dimensionar->지역변수들){TI_inválido=1;return;}
    내보내기("){W v[%u]={0},s[128],x[16];int sp=0;W q,r;\n",Grupo_dimensionar->지역변수들?Grupo_dimensionar->지역변수들:1);for(int 순번=0;순번<item_CONT_NÚM;순번++)내보내기("v[%d]=a%d;",순번,순번);
    unsigned 저장값=duração_VALOR;duração_VALOR=Grupo_dimensionar->instrução_SEQUÊNCIA+Grupo_dimensionar->Tamanho;em_dia_cargo=Grupo_dimensionar->instrução_SEQUÊNCIA;
    while(em_dia_cargo<duração_VALOR&&!TI_inválido){unsigned comando_cargo=em_dia_cargo-Grupo_dimensionar->instrução_SEQUÊNCIA,cirurgia_VALOR=byte_dados();내보내기("L%u:;",comando_cargo);
        if(cirurgia_VALOR==0){}
        else if(cirurgia_VALOR==1)내보내기("P(0);");
        else if(cirurgia_VALOR>=2&&cirurgia_VALOR<=8)내보내기("P(%uU);",cirurgia_VALOR-3);
        else if(cirurgia_VALOR==16){int VALOR=(int8_t)byte_dados();내보내기("P(%uU);",(unsigned)VALOR);}
        else if(cirurgia_VALOR==17){int VALOR=(int16_t)절반값();내보내기("P(%uU);",(unsigned)VALOR);}
        else if(cirurgia_VALOR==18||cirurgia_VALOR==19)constante_VALOR(cirurgia_VALOR==18?byte_dados():절반값());
        else if(cirurgia_VALOR==21||cirurgia_VALOR==25){unsigned 순번=byte_dados();if(순번>=Grupo_dimensionar->지역변수들)TI_inválido=1;내보내기("P(v[%u]);",순번);}
        else if((cirurgia_VALOR>=26&&cirurgia_VALOR<=29)||(cirurgia_VALOR>=42&&cirurgia_VALOR<=45)){unsigned 순번=cirurgia_VALOR>=42?cirurgia_VALOR-42:cirurgia_VALOR-26;if(순번>=Grupo_dimensionar->지역변수들)TI_inválido=1;내보내기("P(v[%u]);",순번);}
        else if(cirurgia_VALOR==54||cirurgia_VALOR==58){unsigned 순번=byte_dados();if(순번>=Grupo_dimensionar->지역변수들)TI_inválido=1;내보내기("v[%u]=Q();",순번);}
        else if((cirurgia_VALOR>=59&&cirurgia_VALOR<=62)||(cirurgia_VALOR>=75&&cirurgia_VALOR<=78)){unsigned 순번=cirurgia_VALOR>=75?cirurgia_VALOR-75:cirurgia_VALOR-59;if(순번>=Grupo_dimensionar->지역변수들)TI_inválido=1;내보내기("v[%u]=Q();",순번);}
        else if(cirurgia_VALOR==46||cirurgia_VALOR==50||cirurgia_VALOR==51||cirurgia_VALOR==52||cirurgia_VALOR==53)내보내기("q=Q();r=Q();P(*jindex(r,(int)q));");
        else if(cirurgia_VALOR==79||cirurgia_VALOR==83||cirurgia_VALOR==84||cirurgia_VALOR==85||cirurgia_VALOR==86)내보내기("q=Q();r=Q();*jindex(Q(),(int)r)=%s;",cirurgia_VALOR==84?"(unsigned)(signed char)q":cirurgia_VALOR==85?"(unsigned short)q":cirurgia_VALOR==86?"(unsigned)(short)q":"q");
        else if(cirurgia_VALOR==87)내보내기("Q();");
        else if(cirurgia_VALOR==89)내보내기("q=Q();P(q);P(q);");
        else if(cirurgia_VALOR==90)내보내기("q=Q();r=Q();P(q);P(r);P(q);");
        else if(cirurgia_VALOR==95)내보내기("q=Q();r=Q();P(q);P(r);");
        else if(cirurgia_VALOR==96||cirurgia_VALOR==100||cirurgia_VALOR==104||cirurgia_VALOR==120||cirurgia_VALOR==124||cirurgia_VALOR==126||cirurgia_VALOR==128||cirurgia_VALOR==130){const char*Codificação_VALOR=cirurgia_VALOR==96?"+":cirurgia_VALOR==100?"-":cirurgia_VALOR==104?"*":cirurgia_VALOR==120?"<<":cirurgia_VALOR==124?">>":cirurgia_VALOR==126?"&":cirurgia_VALOR==128?"|":"^";내보내기("q=Q();r=Q();P((unsigned)r%s(unsigned)q%s);",Codificação_VALOR,cirurgia_VALOR==120||cirurgia_VALOR==124?"%32":"");}
        else if(cirurgia_VALOR==108||cirurgia_VALOR==112)내보내기("q=Q();r=Q();P((unsigned)jdivide((int)r,(int)q,%d));",cirurgia_VALOR==112);
        else if(cirurgia_VALOR==116)내보내기("P(0U-(unsigned)Q());");
        else if(cirurgia_VALOR==122)내보내기("q=Q();r=Q();P((unsigned)((int)r>>((unsigned)q&31)));");
        else if(cirurgia_VALOR==132){unsigned 순번=byte_dados();int 차이=(int8_t)byte_dados();if(순번>=Grupo_dimensionar->지역변수들)TI_inválido=1;내보내기("v[%u]=(unsigned)v[%u]+%uU;",순번,순번,(unsigned)차이);}
        else if(cirurgia_VALOR>=145&&cirurgia_VALOR<=147)내보내기("P((unsigned)(%s)Q());",cirurgia_VALOR==145?"signed char":cirurgia_VALOR==146?"unsigned short":"short");
        else if(cirurgia_VALOR>=153&&cirurgia_VALOR<=166){int meta=(int)comando_cargo+(int16_t)절반값();const char*Comparação_VALOR[]={"==","!=","<",">=",">","<="};if(meta<0||meta>=(int)Grupo_dimensionar->Tamanho){TI_inválido=1;break;}if(cirurgia_VALOR<159)내보내기("if((int)Q()%s0)goto L%d;",Comparação_VALOR[cirurgia_VALOR-153],meta);else if(cirurgia_VALOR<165)내보내기("q=Q();r=Q();if((int)r%s(int)q)goto L%d;",Comparação_VALOR[cirurgia_VALOR-159],meta);else 내보내기("q=Q();r=Q();if(r%sq)goto L%d;",cirurgia_VALOR==165?"==":"!=",meta);}
        else if(cirurgia_VALOR==167){int meta=(int)comando_cargo+(int16_t)절반값();if(meta<0||meta>=(int)Grupo_dimensionar->Tamanho)TI_inválido=1;내보내기("goto L%d;",meta);}
        else if(cirurgia_VALOR==172||cirurgia_VALOR==176)내보내기("return Q();");else if(cirurgia_VALOR==177)내보내기("return 0;");
        else if(cirurgia_VALOR==178||cirurgia_VALOR==179){unsigned identificador_VALOR=절반값();if(identificador_VALOR<1||identificador_VALOR>=constante_pool||Rótulos_Lista[identificador_VALOR]!=9||첫째값[identificador_VALOR]>=constante_pool||SEGUNDO_VALOR[identificador_VALOR]>=constante_pool||Rótulos_Lista[첫째값[identificador_VALOR]]!=7||Rótulos_Lista[SEGUNDO_VALOR[identificador_VALOR]]!=12){TI_inválido=1;break;}unsigned proprietário_objeto=첫째값[첫째값[identificador_VALOR]],Nome=첫째값[SEGUNDO_VALOR[identificador_VALOR]],descritor_dados=SEGUNDO_VALOR[SEGUNDO_VALOR[identificador_VALOR]];
            if(cirurgia_VALOR==178&&UNICODE_VALOR(proprietário_objeto,"java/lang/System")&&UNICODE_VALOR(Nome,"out")&&UNICODE_VALOR(descritor_dados,"Ljava/io/PrintStream;"))내보내기("P(1);");
            else {unsigned Arquivo_entrada=0;while(Arquivo_entrada<필드개수&&(!같음(Nome,nome_de_campo[Arquivo_entrada])||!같음(descritor_dados,Campo_descritor[Arquivo_entrada])))Arquivo_entrada++;if(!같음(proprietário_objeto,첫째값[em_dia_aula])||Arquivo_entrada==필드개수){TI_inválido=1;break;}내보내기(cirurgia_VALOR==178?"P(fields[%u]);":"fields[%u]=Q();",Arquivo_entrada);}}
        else if(cirurgia_VALOR==182||cirurgia_VALOR==184)호출(절반값(),cirurgia_VALOR==182);
        else if(cirurgia_VALOR==188){unsigned TIPO_área=byte_dados();if(TIPO_área!=4&&TIPO_área!=5&&TIPO_área!=8&&TIPO_área!=9&&TIPO_área!=10)TI_inválido=1;내보내기("P(jarray((int)Q()));");}
        else if(cirurgia_VALOR==190)내보내기("P(jlength(Q()));");
        else if(cirurgia_VALOR==198||cirurgia_VALOR==199){int meta=(int)comando_cargo+(int16_t)절반값();if(meta<0||meta>=(int)Grupo_dimensionar->Tamanho)TI_inválido=1;내보내기("if(Q()%s0)goto L%d;",cirurgia_VALOR==198?"==":"!=",meta);}
        else TI_inválido=1;
        if(TI_inválido)printf("jaot: method %u bytecode %u at %u unsupported or malformed\n",PROC_ÍNDICE,cirurgia_VALOR,comando_cargo);
        내보내기("\n");
    }
    duração_VALOR=저장값;내보내기("jfail();return 0;}\n");
}
static unsigned cadeia_lição(unsigned *dados_cargo,unsigned encerrar_DESLOC){
    if(*dados_cargo>=encerrar_DESLOC){TI_inválido=1;return 0;}unsigned ponto_de_código=dados[(*dados_cargo)++];
    if(ponto_de_código<128)return ponto_de_código;
    unsigned item_CONT_NÚM=ponto_de_código>=0xc0&&ponto_de_código<=0xdf?1:ponto_de_código>=0xe0&&ponto_de_código<=0xef?2:3;
    if(item_CONT_NÚM==3||item_CONT_NÚM>encerrar_DESLOC-*dados_cargo){TI_inválido=1;return 0;}unsigned VALOR=ponto_de_código&((1u<<(6-item_CONT_NÚM))-1);
    for(unsigned 순번=0;순번<item_CONT_NÚM;순번++){unsigned Avançar_item=dados[(*dados_cargo)++];if((Avançar_item&0xc0)!=0x80)TI_inválido=1;VALOR=VALOR<<6|(Avançar_item&63);}
    if((item_CONT_NÚM==1&&VALOR<128&&VALOR!=0)||(item_CONT_NÚM==2&&VALOR<2048))TI_inválido=1;return VALOR;
}
static void cadeia_constante(unsigned identificador_VALOR){
    unsigned 부호없는값=첫째값[identificador_VALOR];if(부호없는값<1||부호없는값>=constante_pool||Rótulos_Lista[부호없는값]!=1){TI_inválido=1;return;}내보내기("static const unsigned char k%u[]={",identificador_VALOR);
    unsigned dados_cargo=첫째값[부호없는값],encerrar_DESLOC=dados_cargo+SEGUNDO_VALOR[부호없는값];
    while(dados_cargo<encerrar_DESLOC&&!TI_inválido){unsigned ponto_de_código=cadeia_lição(&dados_cargo,encerrar_DESLOC);
        if(ponto_de_código>=0xd800&&ponto_de_código<=0xdbff){unsigned 낮은부분=cadeia_lição(&dados_cargo,encerrar_DESLOC);if(낮은부분<0xdc00||낮은부분>0xdfff){TI_inválido=1;break;}ponto_de_código=0x10000+((ponto_de_código-0xd800)<<10)+낮은부분-0xdc00;}
        else if(ponto_de_código>=0xdc00&&ponto_de_código<=0xdfff){TI_inválido=1;break;}
        if(!ponto_de_código){printf("jaot: embedded NUL string needs JVM mode\n");TI_inválido=1;break;}
        if(ponto_de_código<128)내보내기("%u,",ponto_de_código);
        else{unsigned item_CONT_NÚM=ponto_de_código<2048?2:ponto_de_código<65536?3:4;내보내기("%u,",(item_CONT_NÚM==2?0xc0:item_CONT_NÚM==3?0xe0:0xf0)|(ponto_de_código>>(6*(item_CONT_NÚM-1))));for(unsigned 순번=item_CONT_NÚM-1;순번;순번--)내보내기("%u,",0x80|((ponto_de_código>>(6*(순번-1)))&63));}
    }내보내기("0};\n");
}
const char *자바미리번역원문(const char*Nome){
    size_t item_CONT_NÚM=strlen(Nome);
    if(item_CONT_NÚM>4&&!strcmp(Nome+item_CONT_NÚM-4,".jar")){
        if(꾸러미열기(Nome)<0){printf("jaot: invalid JAR/Main-Class\n");return 0;}char caminho[256];const char*entrada_método=꾸러미진입클래스();item_CONT_NÚM=strlen(entrada_método);if(item_CONT_NÚM+6>=sizeof(caminho))return 0;
        for(unsigned 순번=0;순번<item_CONT_NÚM;순번++)caminho[순번]=entrada_método[순번]=='.'?'/':entrada_método[순번];strcpy(caminho+item_CONT_NÚM,".class");int entrada_CONT_NÚM_8f7753a1=꾸러미읽기(caminho,dados,sizeof(dados));if(entrada_CONT_NÚM_8f7753a1<0)return 0;duração_VALOR=entrada_CONT_NÚM_8f7753a1;
    }else{intptr_t identificador_de_arquivo=사용자호출(3,(uintptr_t)Nome,0,0,0,0,0);if(identificador_de_arquivo<0)return 0;intptr_t entrada_CONT_NÚM_8f7753a1=사용자호출(9,identificador_de_arquivo,0,0,0,0,0);if(entrada_CONT_NÚM_8f7753a1<0||entrada_CONT_NÚM_8f7753a1>sizeof(dados)){사용자호출(4,identificador_de_arquivo,0,0,0,0,0);return 0;}intptr_t RECEBER_CONT_NÚM=사용자호출(2,identificador_de_arquivo,(uintptr_t)dados,entrada_CONT_NÚM_8f7753a1,0,0,0);사용자호출(4,identificador_de_arquivo,0,0,0,0,0);if(RECEBER_CONT_NÚM!=entrada_CONT_NÚM_8f7753a1)return 0;duração_VALOR=entrada_CONT_NÚM_8f7753a1;}
    if(analisar_entrada()<0){printf("jaot: requires static Java 8 int/reference subset without exceptions\n");return 0;}
    내보내기("typedef unsigned long W; extern void jfail(void);extern void jpush(W*,int*,W);extern W jpop(W*,int*);extern W jarray(int);extern W*jindex(W,int);extern int jlength(W),jdivide(int,int,int);extern void jprint(W,int,int);extern W jfread(W),jfwrite(W,W);static W fields[64];\n#define P(x) jpush(s,&sp,(W)(x))\n#define Q() jpop(s,&sp)\n");
    for(unsigned 순번=1;순번<constante_pool&&!TI_inválido;순번++)if(Rótulos_Lista[순번]==8)cadeia_constante(순번);
    if(TI_inválido)return 0;
    int ponto_de_entrada=-1,초기값=-1;
    for(unsigned 순번=0;순번<메소드개수;순번++)if(!UNICODE_VALOR(메소드목록[순번].Nome,"<init>")){
        int resultado,entrada_CONT_NÚM_8f7753a1=descritor_entrada(메소드목록[순번].descritor_dados,&resultado);if(entrada_CONT_NÚM_8f7753a1<0)return 0;내보내기("static W m%u(",순번);for(int 안쪽순번=0;안쪽순번<entrada_CONT_NÚM_8f7753a1;안쪽순번++)내보내기(안쪽순번?",W":"W");if(!entrada_CONT_NÚM_8f7753a1)내보내기("void");내보내기(");\n");
        if(UNICODE_VALOR(메소드목록[순번].Nome,"main")&&UNICODE_VALOR(메소드목록[순번].descritor_dados,"([Ljava/lang/String;)V")&&(메소드목록[순번].Configuração_BITS&9)==9)ponto_de_entrada=순번;
        if(UNICODE_VALOR(메소드목록[순번].Nome,"<clinit>"))초기값=순번;
    }
    if(ponto_de_entrada<0)return 0;for(unsigned 순번=0;순번<메소드개수&&!TI_inválido;순번++)compilar_método(순번);
    내보내기("int main(int argc,char**argv){W a[9]={0};a[0]=argc>0?argc-1:0;for(int i=1;i<argc&&i<9;i++)a[i]=(W)argv[i];");
    for(unsigned 순번=0;순번<필드개수;순번++)if(Campo_constante[순번]){
        unsigned ponto_de_código=Campo_constante[순번];if(ponto_de_código>=constante_pool)return 0;
        if(Rótulos_Lista[ponto_de_código]==3)내보내기("fields[%u]=%uU;",순번,첫째값[ponto_de_código]);else if(Rótulos_Lista[ponto_de_código]==8)내보내기("fields[%u]=(W)k%u;",순번,ponto_de_código);else return 0;
    }
    if(초기값>=0)내보내기("m%d();",초기값);내보내기("m%d((W)a);return 0;}\n",ponto_de_entrada);
    return TI_inválido?0:texto;
}
