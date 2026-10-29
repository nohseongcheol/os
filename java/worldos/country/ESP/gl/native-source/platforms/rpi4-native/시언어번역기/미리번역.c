#include "../명명/기계연결이름.h"
/* Static Java 8 bytecode -> C -> TinyCC ARM64 code, entirely inside EL0.
 * This is not a complete JVM. Unsupported instructions/APIs stop compilation.
 */
#include "호출.h"
#include "paquete.h"
#include "stdio.h"
#include <stdarg.h>
#include <string.h>
#include <stdint.h>
static unsigned char datos[16384];static unsigned duración_VALOR,ao_corrente_cargo;static int Tecnoloxía_da_información_TI_non_válido;
static unsigned Etiquetas_Lista[512],첫째값[512],SEGUNDO_VALOR[512],constante_grupo,ao_corrente_Clase;
static char Texto[65536];static unsigned Tamaño_de_texto;
typedef struct {unsigned configuración_Servizo_de_transferencia_intelixente_en_segundo_plano,Nome,서술값,instrución_SECUENCIA,Tamaño,지역변수들,Montón_Almacenamento;} 메소드;
static 메소드 메소드목록[64];static unsigned 메소드개수;
static unsigned nome_de_campo[64],필드서술[64],campo_constante[64],필드개수;
static unsigned COLLER_VALOR(unsigned elemento_CONTAR){if(ao_corrente_cargo>duración_VALOR||elemento_CONTAR>duración_VALOR-ao_corrente_cargo){Tecnoloxía_da_información_TI_non_válido=1;return 0;}unsigned datos_cargo=ao_corrente_cargo;ao_corrente_cargo+=elemento_CONTAR;return datos_cargo;}
static unsigned byte_datos(void){unsigned datos_cargo=COLLER_VALOR(1);return Tecnoloxía_da_información_TI_non_válido?0:datos[datos_cargo];}
static unsigned 절반값(void){unsigned X_coordenada=byte_datos();return X_coordenada<<8|byte_datos();}
static uint32_t 가득참(void){uint32_t X_coordenada=절반값();return X_coordenada<<16|절반값();}
static int UNICODE_VALOR(unsigned 순번,const char*cadea_datos){return 순번>0&&순번<constante_grupo&&Etiquetas_Lista[순번]==1&&strlen(cadea_datos)==SEGUNDO_VALOR[순번]&&!memcmp(datos+첫째값[순번],cadea_datos,SEGUNDO_VALOR[순번]);}
static int 같음(unsigned X_coordenada,unsigned Y_coordenada){return X_coordenada>0&&X_coordenada<constante_grupo&&Y_coordenada>0&&Y_coordenada<constante_grupo&&Etiquetas_Lista[X_coordenada]==1&&Etiquetas_Lista[Y_coordenada]==1&&SEGUNDO_VALOR[X_coordenada]==SEGUNDO_VALOR[Y_coordenada]&&!memcmp(datos+첫째값[X_coordenada],datos+첫째값[Y_coordenada],SEGUNDO_VALOR[X_coordenada]);}
static void 내보내기(const char*Ficheiro_introdución,...){if(Tecnoloxía_da_información_TI_non_válido)return;va_list argumento_MATRIZ;va_start(argumento_MATRIZ,Ficheiro_introdución);int elemento_CONTAR=vsnprintf(Texto+Tamaño_de_texto,sizeof(Texto)-Tamaño_de_texto,Ficheiro_introdución,argumento_MATRIZ);va_end(argumento_MATRIZ);if(elemento_CONTAR<0||(unsigned)elemento_CONTAR>=sizeof(Texto)-Tamaño_de_texto){Tecnoloxía_da_información_TI_non_válido=1;return;}Tamaño_de_texto+=elemento_CONTAR;}
static int 서술자(unsigned 식별자,int*RESULTANTE){
    if(식별자<1||식별자>=constante_grupo||Etiquetas_Lista[식별자]!=1)return -1;unsigned datos_cargo=첫째값[식별자],finalizar_DESPRAZAMENTO=datos_cargo+SEGUNDO_VALOR[식별자];if(datos_cargo>=finalizar_DESPRAZAMENTO||datos[datos_cargo++]!='(')return -1;int introdución_CONTAR=0;
    while(datos_cargo<finalizar_DESPRAZAMENTO&&datos[datos_cargo]!=')'){
        unsigned código_de_carácter=datos[datos_cargo++];while(código_de_carácter=='['&&datos_cargo<finalizar_DESPRAZAMENTO)código_de_carácter=datos[datos_cargo++];
        if(código_de_carácter=='L'){while(datos_cargo<finalizar_DESPRAZAMENTO&&datos[datos_cargo]!=';')datos_cargo++;if(datos_cargo==finalizar_DESPRAZAMENTO)return -1;datos_cargo++;}
        else if(código_de_carácter!='I'&&código_de_carácter!='Z'&&código_de_carácter!='B'&&código_de_carácter!='C'&&código_de_carácter!='S')return -1;
        if(++introdución_CONTAR>16)return -1;
    }
    if(datos_cargo+1>=finalizar_DESPRAZAMENTO||datos[datos_cargo++]!=')')return -1;*RESULTANTE=datos[datos_cargo]=='V'?0:1;
    if(datos[datos_cargo]=='J'||datos[datos_cargo]=='D'||datos[datos_cargo]=='F')return -1;return introdución_CONTAR;
}
static void atributos(void){unsigned elemento_CONTAR=절반값();for(unsigned 순번=0;순번<elemento_CONTAR&&!Tecnoloxía_da_información_TI_non_válido;순번++){절반값();unsigned Tamaño=가득참();COLLER_VALOR(Tamaño);}}
static int 해석하기(void){
    if(가득참()!=0xcafebabe)return -1;unsigned menor_versión=절반값(),판번호=절반값();if(menor_versión||판번호<45||판번호>52)return -1;
    constante_grupo=절반값();if(constante_grupo<1||constante_grupo>512)return -1;
    for(unsigned 순번=1;순번<constante_grupo&&!Tecnoloxía_da_información_TI_non_válido;순번++){
        Etiquetas_Lista[순번]=byte_datos();switch(Etiquetas_Lista[순번]){
        case 1:SEGUNDO_VALOR[순번]=절반값();첫째값[순번]=COLLER_VALOR(SEGUNDO_VALOR[순번]);break;case 3:case 4:첫째값[순번]=가득참();break;
        case 5:case 6:COLLER_VALOR(8);if(++순번>=constante_grupo)return -1;break;
        case 7:case 8:case 16:첫째값[순번]=절반값();break;
        case 9:case 10:case 11:case 12:case 18:첫째값[순번]=절반값();SEGUNDO_VALOR[순번]=절반값();break;
        case 15:첫째값[순번]=byte_datos();SEGUNDO_VALOR[순번]=절반값();break;default:return -1;
        }
    }
    절반값();ao_corrente_Clase=절반값();절반값();if(ao_corrente_Clase<1||ao_corrente_Clase>=constante_grupo||Etiquetas_Lista[ao_corrente_Clase]!=7||첫째값[ao_corrente_Clase]<1||첫째값[ao_corrente_Clase]>=constante_grupo||Etiquetas_Lista[첫째값[ao_corrente_Clase]]!=1)return -1;unsigned 인터페이스목록=절반값();COLLER_VALOR(인터페이스목록*2);
    필드개수=절반값();if(필드개수>64)return -1;
    for(unsigned 순번=0;순번<필드개수&&!Tecnoloxía_da_información_TI_non_válido;순번++){
        unsigned configuración_Servizo_de_transferencia_intelixente_en_segundo_plano=절반값();nome_de_campo[순번]=절반값();필드서술[순번]=절반값();
        if(!(configuración_Servizo_de_transferencia_intelixente_en_segundo_plano&8))return -1;
        unsigned introdución_CONTAR=절반값();for(unsigned 안쪽순번=0;안쪽순번<introdución_CONTAR&&!Tecnoloxía_da_información_TI_non_válido;안쪽순번++){
            unsigned Nome=절반값(),Tamaño=가득참();
            if(UNICODE_VALOR(Nome,"ConstantValue")){if(Tamaño!=2)return -1;campo_constante[순번]=절반값();}
            else COLLER_VALOR(Tamaño);
        }
    }
    메소드개수=절반값();if(메소드개수>64)return -1;
    for(unsigned 순번=0;순번<메소드개수&&!Tecnoloxía_da_información_TI_non_válido;순번++){
        메소드*묶음수=메소드목록+순번;묶음수->configuración_Servizo_de_transferencia_intelixente_en_segundo_plano=절반값();묶음수->Nome=절반값();묶음수->서술값=절반값();unsigned introdución_CONTAR=절반값();
        for(unsigned 안쪽순번=0;안쪽순번<introdución_CONTAR&&!Tecnoloxía_da_información_TI_non_válido;안쪽순번++){
            unsigned Nome=절반값(),Tamaño=가득참(),Executar_2=ao_corrente_cargo;
            if(Tamaño>duración_VALOR-ao_corrente_cargo)return -1;
            if(UNICODE_VALOR(Nome,"Code")){
                묶음수->Montón_Almacenamento=절반값();묶음수->지역변수들=절반값();묶음수->Tamaño=가득참();묶음수->instrución_SECUENCIA=COLLER_VALOR(묶음수->Tamaño);
                if(묶음수->Montón_Almacenamento>128||묶음수->지역변수들>128||묶음수->Tamaño>8192||절반값())return -1;atributos();
            }else COLLER_VALOR(Tamaño);
            if(ao_corrente_cargo!=Executar_2+Tamaño)return -1;
        }
        if(!UNICODE_VALOR(묶음수->Nome,"<init>")&&(!(묶음수->configuración_Servizo_de_transferencia_intelixente_en_segundo_plano&8)||(묶음수->configuración_Servizo_de_transferencia_intelixente_en_segundo_plano&(0x100|0x20))||!묶음수->Tamaño))return -1;
    }
    atributos();return Tecnoloxía_da_información_TI_non_válido||ao_corrente_cargo!=duración_VALOR?-1:0;
}
static void constante_VALOR(unsigned 식별자){
    if(!식별자||식별자>=constante_grupo){Tecnoloxía_da_información_TI_non_válido=1;return;}
    if(Etiquetas_Lista[식별자]==3)내보내기("P(%uU);",첫째값[식별자]);
    else if(Etiquetas_Lista[식별자]==8)내보내기("P((W)k%u);",식별자);else Tecnoloxía_da_información_TI_non_válido=1;
}
static void 호출(unsigned 식별자,int virtual_CHAMAR){
    if(식별자<1||식별자>=constante_grupo||(Etiquetas_Lista[식별자]!=10&&Etiquetas_Lista[식별자]!=11)||첫째값[식별자]<1||첫째값[식별자]>=constante_grupo||Etiquetas_Lista[첫째값[식별자]]!=7||SEGUNDO_VALOR[식별자]<1||SEGUNDO_VALOR[식별자]>=constante_grupo||Etiquetas_Lista[SEGUNDO_VALOR[식별자]]!=12){Tecnoloxía_da_información_TI_non_válido=1;return;}
    unsigned propietario_obxecto=첫째값[첫째값[식별자]],Nome=첫째값[SEGUNDO_VALOR[식별자]],서술값=SEGUNDO_VALOR[SEGUNDO_VALOR[식별자]];int RESULTANTE=0,elemento_CONTAR=서술자(서술값,&RESULTANTE);if(elemento_CONTAR<0){Tecnoloxía_da_información_TI_non_válido=1;return;}
    for(int 순번=elemento_CONTAR;순번>0;순번--)내보내기("x[%d]=Q();",순번-1);if(virtual_CHAMAR)내보내기("Q();");
    if(!virtual_CHAMAR&&같음(propietario_obxecto,첫째값[ao_corrente_Clase])){
        unsigned 묶음수=0;for(;묶음수<메소드개수;묶음수++)if(같음(Nome,메소드목록[묶음수].Nome)&&같음(서술값,메소드목록[묶음수].서술값))break;
        if(묶음수==메소드개수||!(메소드목록[묶음수].configuración_Servizo_de_transferencia_intelixente_en_segundo_plano&8)){Tecnoloxía_da_información_TI_non_válido=1;return;}
        if(RESULTANTE)내보내기("P(");내보내기("m%u(",묶음수);for(int 순번=0;순번<elemento_CONTAR;순번++)내보내기(순번?",x[%d]":"x[%d]",순번);내보내기(RESULTANTE?"));":" );");return;
    }
    if((virtual_CHAMAR&&UNICODE_VALOR(propietario_obxecto,"java/io/PrintStream")&& (UNICODE_VALOR(Nome,"print")||UNICODE_VALOR(Nome,"println")))||(!virtual_CHAMAR&&UNICODE_VALOR(propietario_obxecto,"Galego/자체/Saída"))){
        if(UNICODE_VALOR(서술값,"(I)V")&&(UNICODE_VALOR(Nome,"print")||UNICODE_VALOR(Nome,"println")||UNICODE_VALOR(Nome,"수쓰기"))){내보내기("jprint(x[0],1,%d);",UNICODE_VALOR(Nome,"print")?0:1);return;}
        if(UNICODE_VALOR(서술값,"(Ljava/lang/String;)V")&&(UNICODE_VALOR(Nome,"print")||UNICODE_VALOR(Nome,"println")||UNICODE_VALOR(Nome,"Escritura")||UNICODE_VALOR(Nome,"escribir_liña"))){내보내기("jprint(x[0],0,%d);",UNICODE_VALOR(Nome,"print")||UNICODE_VALOR(Nome,"Escritura")?0:1);return;}
        if(UNICODE_VALOR(서술값,"()V")&&UNICODE_VALOR(Nome,"println")){내보내기("jprint((W)\"\",0,1);");return;}
    }
    if(!virtual_CHAMAR&&UNICODE_VALOR(propietario_obxecto,"Galego/자체/Ficheiro")){
        if(UNICODE_VALOR(Nome,"Escritura")&&UNICODE_VALOR(서술값,"(Ljava/lang/String;Ljava/lang/String;)V")){내보내기("jfwrite(x[0],x[1]);");return;}
        if(UNICODE_VALOR(Nome,"Lectura")&&UNICODE_VALOR(서술값,"(Ljava/lang/String;)Ljava/lang/String;")){내보내기("P(jfread(x[0]));");return;}
    }
    Tecnoloxía_da_información_TI_non_válido=1;
}
static void 메소드번역(unsigned Busca_ÍNDICE){
    메소드*묶음수=메소드목록+Busca_ÍNDICE;if(UNICODE_VALOR(묶음수->Nome,"<init>"))return;int RESULTANTE,elemento_CONTAR=서술자(묶음수->서술값,&RESULTANTE);if(elemento_CONTAR<0){Tecnoloxía_da_información_TI_non_válido=1;return;}
    내보내기("static W m%u(",Busca_ÍNDICE);for(int 순번=0;순번<elemento_CONTAR;순번++)내보내기(순번?",W a%d":"W a%d",순번);if(!elemento_CONTAR)내보내기("void");
    if((unsigned)elemento_CONTAR>묶음수->지역변수들){Tecnoloxía_da_información_TI_non_válido=1;return;}
    내보내기("){W v[%u]={0},s[128],x[16];int sp=0;W q,r;\n",묶음수->지역변수들?묶음수->지역변수들:1);for(int 순번=0;순번<elemento_CONTAR;순번++)내보내기("v[%d]=a%d;",순번,순번);
    unsigned 저장값=duración_VALOR;duración_VALOR=묶음수->instrución_SECUENCIA+묶음수->Tamaño;ao_corrente_cargo=묶음수->instrución_SECUENCIA;
    while(ao_corrente_cargo<duración_VALOR&&!Tecnoloxía_da_información_TI_non_válido){unsigned comando_cargo=ao_corrente_cargo-묶음수->instrución_SECUENCIA,cirurxía_VALOR=byte_datos();내보내기("L%u:;",comando_cargo);
        if(cirurxía_VALOR==0){}
        else if(cirurxía_VALOR==1)내보내기("P(0);");
        else if(cirurxía_VALOR>=2&&cirurxía_VALOR<=8)내보내기("P(%uU);",cirurxía_VALOR-3);
        else if(cirurxía_VALOR==16){int VALOR=(int8_t)byte_datos();내보내기("P(%uU);",(unsigned)VALOR);}
        else if(cirurxía_VALOR==17){int VALOR=(int16_t)절반값();내보내기("P(%uU);",(unsigned)VALOR);}
        else if(cirurxía_VALOR==18||cirurxía_VALOR==19)constante_VALOR(cirurxía_VALOR==18?byte_datos():절반값());
        else if(cirurxía_VALOR==21||cirurxía_VALOR==25){unsigned 순번=byte_datos();if(순번>=묶음수->지역변수들)Tecnoloxía_da_información_TI_non_válido=1;내보내기("P(v[%u]);",순번);}
        else if((cirurxía_VALOR>=26&&cirurxía_VALOR<=29)||(cirurxía_VALOR>=42&&cirurxía_VALOR<=45)){unsigned 순번=cirurxía_VALOR>=42?cirurxía_VALOR-42:cirurxía_VALOR-26;if(순번>=묶음수->지역변수들)Tecnoloxía_da_información_TI_non_válido=1;내보내기("P(v[%u]);",순번);}
        else if(cirurxía_VALOR==54||cirurxía_VALOR==58){unsigned 순번=byte_datos();if(순번>=묶음수->지역변수들)Tecnoloxía_da_información_TI_non_válido=1;내보내기("v[%u]=Q();",순번);}
        else if((cirurxía_VALOR>=59&&cirurxía_VALOR<=62)||(cirurxía_VALOR>=75&&cirurxía_VALOR<=78)){unsigned 순번=cirurxía_VALOR>=75?cirurxía_VALOR-75:cirurxía_VALOR-59;if(순번>=묶음수->지역변수들)Tecnoloxía_da_información_TI_non_válido=1;내보내기("v[%u]=Q();",순번);}
        else if(cirurxía_VALOR==46||cirurxía_VALOR==50||cirurxía_VALOR==51||cirurxía_VALOR==52||cirurxía_VALOR==53)내보내기("q=Q();r=Q();P(*jindex(r,(int)q));");
        else if(cirurxía_VALOR==79||cirurxía_VALOR==83||cirurxía_VALOR==84||cirurxía_VALOR==85||cirurxía_VALOR==86)내보내기("q=Q();r=Q();*jindex(Q(),(int)r)=%s;",cirurxía_VALOR==84?"(unsigned)(signed char)q":cirurxía_VALOR==85?"(unsigned short)q":cirurxía_VALOR==86?"(unsigned)(short)q":"q");
        else if(cirurxía_VALOR==87)내보내기("Q();");
        else if(cirurxía_VALOR==89)내보내기("q=Q();P(q);P(q);");
        else if(cirurxía_VALOR==90)내보내기("q=Q();r=Q();P(q);P(r);P(q);");
        else if(cirurxía_VALOR==95)내보내기("q=Q();r=Q();P(q);P(r);");
        else if(cirurxía_VALOR==96||cirurxía_VALOR==100||cirurxía_VALOR==104||cirurxía_VALOR==120||cirurxía_VALOR==124||cirurxía_VALOR==126||cirurxía_VALOR==128||cirurxía_VALOR==130){const char*codificación_VALOR=cirurxía_VALOR==96?"+":cirurxía_VALOR==100?"-":cirurxía_VALOR==104?"*":cirurxía_VALOR==120?"<<":cirurxía_VALOR==124?">>":cirurxía_VALOR==126?"&":cirurxía_VALOR==128?"|":"^";내보내기("q=Q();r=Q();P((unsigned)r%s(unsigned)q%s);",codificación_VALOR,cirurxía_VALOR==120||cirurxía_VALOR==124?"%32":"");}
        else if(cirurxía_VALOR==108||cirurxía_VALOR==112)내보내기("q=Q();r=Q();P((unsigned)jdivide((int)r,(int)q,%d));",cirurxía_VALOR==112);
        else if(cirurxía_VALOR==116)내보내기("P(0U-(unsigned)Q());");
        else if(cirurxía_VALOR==122)내보내기("q=Q();r=Q();P((unsigned)((int)r>>((unsigned)q&31)));");
        else if(cirurxía_VALOR==132){unsigned 순번=byte_datos();int 차이=(int8_t)byte_datos();if(순번>=묶음수->지역변수들)Tecnoloxía_da_información_TI_non_válido=1;내보내기("v[%u]=(unsigned)v[%u]+%uU;",순번,순번,(unsigned)차이);}
        else if(cirurxía_VALOR>=145&&cirurxía_VALOR<=147)내보내기("P((unsigned)(%s)Q());",cirurxía_VALOR==145?"signed char":cirurxía_VALOR==146?"unsigned short":"short");
        else if(cirurxía_VALOR>=153&&cirurxía_VALOR<=166){int obxectivo_VALOR=(int)comando_cargo+(int16_t)절반값();const char*Comparación_VALOR[]={"==","!=","<",">=",">","<="};if(obxectivo_VALOR<0||obxectivo_VALOR>=(int)묶음수->Tamaño){Tecnoloxía_da_información_TI_non_válido=1;break;}if(cirurxía_VALOR<159)내보내기("if((int)Q()%s0)goto L%d;",Comparación_VALOR[cirurxía_VALOR-153],obxectivo_VALOR);else if(cirurxía_VALOR<165)내보내기("q=Q();r=Q();if((int)r%s(int)q)goto L%d;",Comparación_VALOR[cirurxía_VALOR-159],obxectivo_VALOR);else 내보내기("q=Q();r=Q();if(r%sq)goto L%d;",cirurxía_VALOR==165?"==":"!=",obxectivo_VALOR);}
        else if(cirurxía_VALOR==167){int obxectivo_VALOR=(int)comando_cargo+(int16_t)절반값();if(obxectivo_VALOR<0||obxectivo_VALOR>=(int)묶음수->Tamaño)Tecnoloxía_da_información_TI_non_válido=1;내보내기("goto L%d;",obxectivo_VALOR);}
        else if(cirurxía_VALOR==172||cirurxía_VALOR==176)내보내기("return Q();");else if(cirurxía_VALOR==177)내보내기("return 0;");
        else if(cirurxía_VALOR==178||cirurxía_VALOR==179){unsigned 식별자=절반값();if(식별자<1||식별자>=constante_grupo||Etiquetas_Lista[식별자]!=9||첫째값[식별자]>=constante_grupo||SEGUNDO_VALOR[식별자]>=constante_grupo||Etiquetas_Lista[첫째값[식별자]]!=7||Etiquetas_Lista[SEGUNDO_VALOR[식별자]]!=12){Tecnoloxía_da_información_TI_non_válido=1;break;}unsigned propietario_obxecto=첫째값[첫째값[식별자]],Nome=첫째값[SEGUNDO_VALOR[식별자]],서술값=SEGUNDO_VALOR[SEGUNDO_VALOR[식별자]];
            if(cirurxía_VALOR==178&&UNICODE_VALOR(propietario_obxecto,"java/lang/System")&&UNICODE_VALOR(Nome,"out")&&UNICODE_VALOR(서술값,"Ljava/io/PrintStream;"))내보내기("P(1);");
            else {unsigned Ficheiro_introdución=0;while(Ficheiro_introdución<필드개수&&(!같음(Nome,nome_de_campo[Ficheiro_introdución])||!같음(서술값,필드서술[Ficheiro_introdución])))Ficheiro_introdución++;if(!같음(propietario_obxecto,첫째값[ao_corrente_Clase])||Ficheiro_introdución==필드개수){Tecnoloxía_da_información_TI_non_válido=1;break;}내보내기(cirurxía_VALOR==178?"P(fields[%u]);":"fields[%u]=Q();",Ficheiro_introdución);}}
        else if(cirurxía_VALOR==182||cirurxía_VALOR==184)호출(절반값(),cirurxía_VALOR==182);
        else if(cirurxía_VALOR==188){unsigned TIPO_Categoría=byte_datos();if(TIPO_Categoría!=4&&TIPO_Categoría!=5&&TIPO_Categoría!=8&&TIPO_Categoría!=9&&TIPO_Categoría!=10)Tecnoloxía_da_información_TI_non_válido=1;내보내기("P(jarray((int)Q()));");}
        else if(cirurxía_VALOR==190)내보내기("P(jlength(Q()));");
        else if(cirurxía_VALOR==198||cirurxía_VALOR==199){int obxectivo_VALOR=(int)comando_cargo+(int16_t)절반값();if(obxectivo_VALOR<0||obxectivo_VALOR>=(int)묶음수->Tamaño)Tecnoloxía_da_información_TI_non_válido=1;내보내기("if(Q()%s0)goto L%d;",cirurxía_VALOR==198?"==":"!=",obxectivo_VALOR);}
        else Tecnoloxía_da_información_TI_non_válido=1;
        if(Tecnoloxía_da_información_TI_non_válido)printf("jaot: method %u bytecode %u at %u unsupported or malformed\n",Busca_ÍNDICE,cirurxía_VALOR,comando_cargo);
        내보내기("\n");
    }
    duración_VALOR=저장값;내보내기("jfail();return 0;}\n");
}
static unsigned cadea_lección(unsigned *datos_cargo,unsigned finalizar_DESPRAZAMENTO){
    if(*datos_cargo>=finalizar_DESPRAZAMENTO){Tecnoloxía_da_información_TI_non_válido=1;return 0;}unsigned código_de_carácter=datos[(*datos_cargo)++];
    if(código_de_carácter<128)return código_de_carácter;
    unsigned elemento_CONTAR=código_de_carácter>=0xc0&&código_de_carácter<=0xdf?1:código_de_carácter>=0xe0&&código_de_carácter<=0xef?2:3;
    if(elemento_CONTAR==3||elemento_CONTAR>finalizar_DESPRAZAMENTO-*datos_cargo){Tecnoloxía_da_información_TI_non_válido=1;return 0;}unsigned VALOR=código_de_carácter&((1u<<(6-elemento_CONTAR))-1);
    for(unsigned 순번=0;순번<elemento_CONTAR;순번++){unsigned Seguinte_elemento=datos[(*datos_cargo)++];if((Seguinte_elemento&0xc0)!=0x80)Tecnoloxía_da_información_TI_non_válido=1;VALOR=VALOR<<6|(Seguinte_elemento&63);}
    if((elemento_CONTAR==1&&VALOR<128&&VALOR!=0)||(elemento_CONTAR==2&&VALOR<2048))Tecnoloxía_da_información_TI_non_válido=1;return VALOR;
}
static void cadea_constante(unsigned 식별자){
    unsigned 부호없는값=첫째값[식별자];if(부호없는값<1||부호없는값>=constante_grupo||Etiquetas_Lista[부호없는값]!=1){Tecnoloxía_da_información_TI_non_válido=1;return;}내보내기("static const unsigned char k%u[]={",식별자);
    unsigned datos_cargo=첫째값[부호없는값],finalizar_DESPRAZAMENTO=datos_cargo+SEGUNDO_VALOR[부호없는값];
    while(datos_cargo<finalizar_DESPRAZAMENTO&&!Tecnoloxía_da_información_TI_non_válido){unsigned código_de_carácter=cadea_lección(&datos_cargo,finalizar_DESPRAZAMENTO);
        if(código_de_carácter>=0xd800&&código_de_carácter<=0xdbff){unsigned 낮은부분=cadea_lección(&datos_cargo,finalizar_DESPRAZAMENTO);if(낮은부분<0xdc00||낮은부분>0xdfff){Tecnoloxía_da_información_TI_non_válido=1;break;}código_de_carácter=0x10000+((código_de_carácter-0xd800)<<10)+낮은부분-0xdc00;}
        else if(código_de_carácter>=0xdc00&&código_de_carácter<=0xdfff){Tecnoloxía_da_información_TI_non_válido=1;break;}
        if(!código_de_carácter){printf("jaot: embedded NUL string needs JVM mode\n");Tecnoloxía_da_información_TI_non_válido=1;break;}
        if(código_de_carácter<128)내보내기("%u,",código_de_carácter);
        else{unsigned elemento_CONTAR=código_de_carácter<2048?2:código_de_carácter<65536?3:4;내보내기("%u,",(elemento_CONTAR==2?0xc0:elemento_CONTAR==3?0xe0:0xf0)|(código_de_carácter>>(6*(elemento_CONTAR-1))));for(unsigned 순번=elemento_CONTAR-1;순번;순번--)내보내기("%u,",0x80|((código_de_carácter>>(6*(순번-1)))&63));}
    }내보내기("0};\n");
}
const char *자바미리번역원문(const char*Nome){
    size_t elemento_CONTAR=strlen(Nome);
    if(elemento_CONTAR>4&&!strcmp(Nome+elemento_CONTAR-4,".jar")){
        if(꾸러미열기(Nome)<0){printf("jaot: invalid JAR/Main-Class\n");return 0;}char CAMIÑO[256];const char*진입함수=꾸러미진입클래스();elemento_CONTAR=strlen(진입함수);if(elemento_CONTAR+6>=sizeof(CAMIÑO))return 0;
        for(unsigned 순번=0;순번<elemento_CONTAR;순번++)CAMIÑO[순번]=진입함수[순번]=='.'?'/':진입함수[순번];strcpy(CAMIÑO+elemento_CONTAR,".class");int introdución_CONTAR=꾸러미읽기(CAMIÑO,datos,sizeof(datos));if(introdución_CONTAR<0)return 0;duración_VALOR=introdución_CONTAR;
    }else{intptr_t Ficheiro_agarradoira=사용자호출(3,(uintptr_t)Nome,0,0,0,0,0);if(Ficheiro_agarradoira<0)return 0;intptr_t introdución_CONTAR=사용자호출(9,Ficheiro_agarradoira,0,0,0,0,0);if(introdución_CONTAR<0||introdución_CONTAR>sizeof(datos)){사용자호출(4,Ficheiro_agarradoira,0,0,0,0,0);return 0;}intptr_t RECIBIDO_CONTAR=사용자호출(2,Ficheiro_agarradoira,(uintptr_t)datos,introdución_CONTAR,0,0,0);사용자호출(4,Ficheiro_agarradoira,0,0,0,0,0);if(RECIBIDO_CONTAR!=introdución_CONTAR)return 0;duración_VALOR=introdución_CONTAR;}
    if(해석하기()<0){printf("jaot: requires static Java 8 int/reference subset without exceptions\n");return 0;}
    내보내기("typedef unsigned long W; extern void jfail(void);extern void jpush(W*,int*,W);extern W jpop(W*,int*);extern W jarray(int);extern W*jindex(W,int);extern int jlength(W),jdivide(int,int,int);extern void jprint(W,int,int);extern W jfread(W),jfwrite(W,W);static W fields[64];\n#define P(x) jpush(s,&sp,(W)(x))\n#define Q() jpop(s,&sp)\n");
    for(unsigned 순번=1;순번<constante_grupo&&!Tecnoloxía_da_información_TI_non_válido;순번++)if(Etiquetas_Lista[순번]==8)cadea_constante(순번);
    if(Tecnoloxía_da_información_TI_non_válido)return 0;
    int introdución_p=-1,초기값=-1;
    for(unsigned 순번=0;순번<메소드개수;순번++)if(!UNICODE_VALOR(메소드목록[순번].Nome,"<init>")){
        int RESULTANTE,introdución_CONTAR=서술자(메소드목록[순번].서술값,&RESULTANTE);if(introdución_CONTAR<0)return 0;내보내기("static W m%u(",순번);for(int 안쪽순번=0;안쪽순번<introdución_CONTAR;안쪽순번++)내보내기(안쪽순번?",W":"W");if(!introdución_CONTAR)내보내기("void");내보내기(");\n");
        if(UNICODE_VALOR(메소드목록[순번].Nome,"main")&&UNICODE_VALOR(메소드목록[순번].서술값,"([Ljava/lang/String;)V")&&(메소드목록[순번].configuración_Servizo_de_transferencia_intelixente_en_segundo_plano&9)==9)introdución_p=순번;
        if(UNICODE_VALOR(메소드목록[순번].Nome,"<clinit>"))초기값=순번;
    }
    if(introdución_p<0)return 0;for(unsigned 순번=0;순번<메소드개수&&!Tecnoloxía_da_información_TI_non_válido;순번++)메소드번역(순번);
    내보내기("int main(int argc,char**argv){W a[9]={0};a[0]=argc>0?argc-1:0;for(int i=1;i<argc&&i<9;i++)a[i]=(W)argv[i];");
    for(unsigned 순번=0;순번<필드개수;순번++)if(campo_constante[순번]){
        unsigned código_de_carácter=campo_constante[순번];if(código_de_carácter>=constante_grupo)return 0;
        if(Etiquetas_Lista[código_de_carácter]==3)내보내기("fields[%u]=%uU;",순번,첫째값[código_de_carácter]);else if(Etiquetas_Lista[código_de_carácter]==8)내보내기("fields[%u]=(W)k%u;",순번,código_de_carácter);else return 0;
    }
    if(초기값>=0)내보내기("m%d();",초기값);내보내기("m%d((W)a);return 0;}\n",introdución_p);
    return Tecnoloxía_da_información_TI_non_válido?0:Texto;
}
