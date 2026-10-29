#include "../명명/기계연결이름.h"
/* Static Java 8 bytecode -> C -> TinyCC ARM64 code, entirely inside EL0.
 * This is not a complete JVM. Unsupported instructions/APIs stop compilation.
 */
#include "호출.h"
#include "bundle.h"
#include "stdio.h"
#include <stdarg.h>
#include <string.h>
#include <stdint.h>
static unsigned char data[16384];static unsigned haba_VALUE,현재위치;static int information_technology_hindi_tama;
static unsigned Mga_Tag_list[512],첫째값[512],SECOND_VALUE[512],상수모음,현재클래스;
static char SMS[65536];static unsigned laki_ng_text;
typedef struct {unsigned kompigurasyon_Background_Intelligent_Transfer_Service,pangalan,서술값,instruksiyon_SEQUENCE,sukat_82232621,지역변수들,Stack_Storage;} pamamaraan_pagpasok;
static pamamaraan_pagpasok 메소드목록[64];static unsigned 메소드개수;
static unsigned pangalan_ng_field[64],필드서술[64],field_constant[64],필드개수;
static unsigned TAKE_VALUE(unsigned item_COUNT){if(현재위치>haba_VALUE||item_COUNT>haba_VALUE-현재위치){information_technology_hindi_tama=1;return 0;}unsigned data_posisyon=현재위치;현재위치+=item_COUNT;return data_posisyon;}
static unsigned byte_data(void){unsigned data_posisyon=TAKE_VALUE(1);return information_technology_hindi_tama?0:data[data_posisyon];}
static unsigned 절반값(void){unsigned x_coordinate=byte_data();return x_coordinate<<8|byte_data();}
static uint32_t 가득참(void){uint32_t x_coordinate=절반값();return x_coordinate<<16|절반값();}
static int UNICODE_VALUE(unsigned 순번,const char*string_data){return 순번>0&&순번<상수모음&&Mga_Tag_list[순번]==1&&strlen(string_data)==SECOND_VALUE[순번]&&!memcmp(data+첫째값[순번],string_data,SECOND_VALUE[순번]);}
static int 같음(unsigned x_coordinate,unsigned Y_button_coordinate){return x_coordinate>0&&x_coordinate<상수모음&&Y_button_coordinate>0&&Y_button_coordinate<상수모음&&Mga_Tag_list[x_coordinate]==1&&Mga_Tag_list[Y_button_coordinate]==1&&SECOND_VALUE[x_coordinate]==SECOND_VALUE[Y_button_coordinate]&&!memcmp(data+첫째값[x_coordinate],data+첫째값[Y_button_coordinate],SECOND_VALUE[x_coordinate]);}
static void 내보내기(const char*file_pagpasok,...){if(information_technology_hindi_tama)return;va_list argumento_ARRAY;va_start(argumento_ARRAY,file_pagpasok);int item_COUNT=vsnprintf(SMS+laki_ng_text,sizeof(SMS)-laki_ng_text,file_pagpasok,argumento_ARRAY);va_end(argumento_ARRAY);if(item_COUNT<0||(unsigned)item_COUNT>=sizeof(SMS)-laki_ng_text){information_technology_hindi_tama=1;return;}laki_ng_text+=item_COUNT;}
static int 서술자(unsigned tagakilala_VALUE,int*sukat){
    if(tagakilala_VALUE<1||tagakilala_VALUE>=상수모음||Mga_Tag_list[tagakilala_VALUE]!=1)return -1;unsigned data_posisyon=첫째값[tagakilala_VALUE],tapusin_OFFSET=data_posisyon+SECOND_VALUE[tagakilala_VALUE];if(data_posisyon>=tapusin_OFFSET||data[data_posisyon++]!='(')return -1;int pagpasok_COUNT=0;
    while(data_posisyon<tapusin_OFFSET&&data[data_posisyon]!=')'){
        unsigned character_code=data[data_posisyon++];while(character_code=='['&&data_posisyon<tapusin_OFFSET)character_code=data[data_posisyon++];
        if(character_code=='L'){while(data_posisyon<tapusin_OFFSET&&data[data_posisyon]!=';')data_posisyon++;if(data_posisyon==tapusin_OFFSET)return -1;data_posisyon++;}
        else if(character_code!='I'&&character_code!='Z'&&character_code!='B'&&character_code!='C'&&character_code!='S')return -1;
        if(++pagpasok_COUNT>16)return -1;
    }
    if(data_posisyon+1>=tapusin_OFFSET||data[data_posisyon++]!=')')return -1;*sukat=data[data_posisyon]=='V'?0:1;
    if(data[data_posisyon]=='J'||data[data_posisyon]=='D'||data[data_posisyon]=='F')return -1;return pagpasok_COUNT;
}
static void 속성들(void){unsigned item_COUNT=절반값();for(unsigned 순번=0;순번<item_COUNT&&!information_technology_hindi_tama;순번++){절반값();unsigned sukat_82232621=가득참();TAKE_VALUE(sukat_82232621);}}
static int 해석하기(void){
    if(가득참()!=0xcafebabe)return -1;unsigned menor_de_edad_bersyon=절반값(),판번호=절반값();if(menor_de_edad_bersyon||판번호<45||판번호>52)return -1;
    상수모음=절반값();if(상수모음<1||상수모음>512)return -1;
    for(unsigned 순번=1;순번<상수모음&&!information_technology_hindi_tama;순번++){
        Mga_Tag_list[순번]=byte_data();switch(Mga_Tag_list[순번]){
        case 1:SECOND_VALUE[순번]=절반값();첫째값[순번]=TAKE_VALUE(SECOND_VALUE[순번]);break;case 3:case 4:첫째값[순번]=가득참();break;
        case 5:case 6:TAKE_VALUE(8);if(++순번>=상수모음)return -1;break;
        case 7:case 8:case 16:첫째값[순번]=절반값();break;
        case 9:case 10:case 11:case 12:case 18:첫째값[순번]=절반값();SECOND_VALUE[순번]=절반값();break;
        case 15:첫째값[순번]=byte_data();SECOND_VALUE[순번]=절반값();break;default:return -1;
        }
    }
    절반값();현재클래스=절반값();절반값();if(현재클래스<1||현재클래스>=상수모음||Mga_Tag_list[현재클래스]!=7||첫째값[현재클래스]<1||첫째값[현재클래스]>=상수모음||Mga_Tag_list[첫째값[현재클래스]]!=1)return -1;unsigned 인터페이스목록=절반값();TAKE_VALUE(인터페이스목록*2);
    필드개수=절반값();if(필드개수>64)return -1;
    for(unsigned 순번=0;순번<필드개수&&!information_technology_hindi_tama;순번++){
        unsigned kompigurasyon_Background_Intelligent_Transfer_Service=절반값();pangalan_ng_field[순번]=절반값();필드서술[순번]=절반값();
        if(!(kompigurasyon_Background_Intelligent_Transfer_Service&8))return -1;
        unsigned pagpasok_COUNT=절반값();for(unsigned 안쪽순번=0;안쪽순번<pagpasok_COUNT&&!information_technology_hindi_tama;안쪽순번++){
            unsigned pangalan=절반값(),sukat_82232621=가득참();
            if(UNICODE_VALUE(pangalan,"ConstantValue")){if(sukat_82232621!=2)return -1;field_constant[순번]=절반값();}
            else TAKE_VALUE(sukat_82232621);
        }
    }
    메소드개수=절반값();if(메소드개수>64)return -1;
    for(unsigned 순번=0;순번<메소드개수&&!information_technology_hindi_tama;순번++){
        pamamaraan_pagpasok*Grupo_sukat=메소드목록+순번;Grupo_sukat->kompigurasyon_Background_Intelligent_Transfer_Service=절반값();Grupo_sukat->pangalan=절반값();Grupo_sukat->서술값=절반값();unsigned pagpasok_COUNT=절반값();
        for(unsigned 안쪽순번=0;안쪽순번<pagpasok_COUNT&&!information_technology_hindi_tama;안쪽순번++){
            unsigned pangalan=절반값(),sukat_82232621=가득참(),run=현재위치;
            if(sukat_82232621>haba_VALUE-현재위치)return -1;
            if(UNICODE_VALUE(pangalan,"Code")){
                Grupo_sukat->Stack_Storage=절반값();Grupo_sukat->지역변수들=절반값();Grupo_sukat->sukat_82232621=가득참();Grupo_sukat->instruksiyon_SEQUENCE=TAKE_VALUE(Grupo_sukat->sukat_82232621);
                if(Grupo_sukat->Stack_Storage>128||Grupo_sukat->지역변수들>128||Grupo_sukat->sukat_82232621>8192||절반값())return -1;속성들();
            }else TAKE_VALUE(sukat_82232621);
            if(현재위치!=run+sukat_82232621)return -1;
        }
        if(!UNICODE_VALUE(Grupo_sukat->pangalan,"<init>")&&(!(Grupo_sukat->kompigurasyon_Background_Intelligent_Transfer_Service&8)||(Grupo_sukat->kompigurasyon_Background_Intelligent_Transfer_Service&(0x100|0x20))||!Grupo_sukat->sukat_82232621))return -1;
    }
    속성들();return information_technology_hindi_tama||현재위치!=haba_VALUE?-1:0;
}
static void constant_VALUE(unsigned tagakilala_VALUE){
    if(!tagakilala_VALUE||tagakilala_VALUE>=상수모음){information_technology_hindi_tama=1;return;}
    if(Mga_Tag_list[tagakilala_VALUE]==3)내보내기("P(%uU);",첫째값[tagakilala_VALUE]);
    else if(Mga_Tag_list[tagakilala_VALUE]==8)내보내기("P((W)k%u);",tagakilala_VALUE);else information_technology_hindi_tama=1;
}
static void 호출(unsigned tagakilala_VALUE,int virtual_CALL){
    if(tagakilala_VALUE<1||tagakilala_VALUE>=상수모음||(Mga_Tag_list[tagakilala_VALUE]!=10&&Mga_Tag_list[tagakilala_VALUE]!=11)||첫째값[tagakilala_VALUE]<1||첫째값[tagakilala_VALUE]>=상수모음||Mga_Tag_list[첫째값[tagakilala_VALUE]]!=7||SECOND_VALUE[tagakilala_VALUE]<1||SECOND_VALUE[tagakilala_VALUE]>=상수모음||Mga_Tag_list[SECOND_VALUE[tagakilala_VALUE]]!=12){information_technology_hindi_tama=1;return;}
    unsigned may_ari_bagay=첫째값[첫째값[tagakilala_VALUE]],pangalan=첫째값[SECOND_VALUE[tagakilala_VALUE]],서술값=SECOND_VALUE[SECOND_VALUE[tagakilala_VALUE]];int sukat=0,item_COUNT=서술자(서술값,&sukat);if(item_COUNT<0){information_technology_hindi_tama=1;return;}
    for(int 순번=item_COUNT;순번>0;순번--)내보내기("x[%d]=Q();",순번-1);if(virtual_CALL)내보내기("Q();");
    if(!virtual_CALL&&같음(may_ari_bagay,첫째값[현재클래스])){
        unsigned Grupo_sukat=0;for(;Grupo_sukat<메소드개수;Grupo_sukat++)if(같음(pangalan,메소드목록[Grupo_sukat].pangalan)&&같음(서술값,메소드목록[Grupo_sukat].서술값))break;
        if(Grupo_sukat==메소드개수||!(메소드목록[Grupo_sukat].kompigurasyon_Background_Intelligent_Transfer_Service&8)){information_technology_hindi_tama=1;return;}
        if(sukat)내보내기("P(");내보내기("m%u(",Grupo_sukat);for(int 순번=0;순번<item_COUNT;순번++)내보내기(순번?",x[%d]":"x[%d]",순번);내보내기(sukat?"));":" );");return;
    }
    if((virtual_CALL&&UNICODE_VALUE(may_ari_bagay,"java/io/PrintStream")&& (UNICODE_VALUE(pangalan,"print")||UNICODE_VALUE(pangalan,"println")))||(!virtual_CALL&&UNICODE_VALUE(may_ari_bagay,"한국어/자체/출력"))){
        if(UNICODE_VALUE(서술값,"(I)V")&&(UNICODE_VALUE(pangalan,"print")||UNICODE_VALUE(pangalan,"println")||UNICODE_VALUE(pangalan,"수쓰기"))){내보내기("jprint(x[0],1,%d);",UNICODE_VALUE(pangalan,"print")?0:1);return;}
        if(UNICODE_VALUE(서술값,"(Ljava/lang/String;)V")&&(UNICODE_VALUE(pangalan,"print")||UNICODE_VALUE(pangalan,"println")||UNICODE_VALUE(pangalan,"sumulat")||UNICODE_VALUE(pangalan,"sumulat_linya"))){내보내기("jprint(x[0],0,%d);",UNICODE_VALUE(pangalan,"print")||UNICODE_VALUE(pangalan,"sumulat")?0:1);return;}
        if(UNICODE_VALUE(서술값,"()V")&&UNICODE_VALUE(pangalan,"println")){내보내기("jprint((W)\"\",0,1);");return;}
    }
    if(!virtual_CALL&&UNICODE_VALUE(may_ari_bagay,"한국어/자체/file")){
        if(UNICODE_VALUE(pangalan,"sumulat")&&UNICODE_VALUE(서술값,"(Ljava/lang/String;Ljava/lang/String;)V")){내보내기("jfwrite(x[0],x[1]);");return;}
        if(UNICODE_VALUE(pangalan,"읽기")&&UNICODE_VALUE(서술값,"(Ljava/lang/String;)Ljava/lang/String;")){내보내기("P(jfread(x[0]));");return;}
    }
    information_technology_hindi_tama=1;
}
static void bumuo_pamamaraan(unsigned LOOKUP_INDEX){
    pamamaraan_pagpasok*Grupo_sukat=메소드목록+LOOKUP_INDEX;if(UNICODE_VALUE(Grupo_sukat->pangalan,"<init>"))return;int sukat,item_COUNT=서술자(Grupo_sukat->서술값,&sukat);if(item_COUNT<0){information_technology_hindi_tama=1;return;}
    내보내기("static W m%u(",LOOKUP_INDEX);for(int 순번=0;순번<item_COUNT;순번++)내보내기(순번?",W a%d":"W a%d",순번);if(!item_COUNT)내보내기("void");
    if((unsigned)item_COUNT>Grupo_sukat->지역변수들){information_technology_hindi_tama=1;return;}
    내보내기("){W v[%u]={0},s[128],x[16];int sp=0;W q,r;\n",Grupo_sukat->지역변수들?Grupo_sukat->지역변수들:1);for(int 순번=0;순번<item_COUNT;순번++)내보내기("v[%d]=a%d;",순번,순번);
    unsigned 저장값=haba_VALUE;haba_VALUE=Grupo_sukat->instruksiyon_SEQUENCE+Grupo_sukat->sukat_82232621;현재위치=Grupo_sukat->instruksiyon_SEQUENCE;
    while(현재위치<haba_VALUE&&!information_technology_hindi_tama){unsigned utos_posisyon=현재위치-Grupo_sukat->instruksiyon_SEQUENCE,operasyon_VALUE=byte_data();내보내기("L%u:;",utos_posisyon);
        if(operasyon_VALUE==0){}
        else if(operasyon_VALUE==1)내보내기("P(0);");
        else if(operasyon_VALUE>=2&&operasyon_VALUE<=8)내보내기("P(%uU);",operasyon_VALUE-3);
        else if(operasyon_VALUE==16){int VALUE=(int8_t)byte_data();내보내기("P(%uU);",(unsigned)VALUE);}
        else if(operasyon_VALUE==17){int VALUE=(int16_t)절반값();내보내기("P(%uU);",(unsigned)VALUE);}
        else if(operasyon_VALUE==18||operasyon_VALUE==19)constant_VALUE(operasyon_VALUE==18?byte_data():절반값());
        else if(operasyon_VALUE==21||operasyon_VALUE==25){unsigned 순번=byte_data();if(순번>=Grupo_sukat->지역변수들)information_technology_hindi_tama=1;내보내기("P(v[%u]);",순번);}
        else if((operasyon_VALUE>=26&&operasyon_VALUE<=29)||(operasyon_VALUE>=42&&operasyon_VALUE<=45)){unsigned 순번=operasyon_VALUE>=42?operasyon_VALUE-42:operasyon_VALUE-26;if(순번>=Grupo_sukat->지역변수들)information_technology_hindi_tama=1;내보내기("P(v[%u]);",순번);}
        else if(operasyon_VALUE==54||operasyon_VALUE==58){unsigned 순번=byte_data();if(순번>=Grupo_sukat->지역변수들)information_technology_hindi_tama=1;내보내기("v[%u]=Q();",순번);}
        else if((operasyon_VALUE>=59&&operasyon_VALUE<=62)||(operasyon_VALUE>=75&&operasyon_VALUE<=78)){unsigned 순번=operasyon_VALUE>=75?operasyon_VALUE-75:operasyon_VALUE-59;if(순번>=Grupo_sukat->지역변수들)information_technology_hindi_tama=1;내보내기("v[%u]=Q();",순번);}
        else if(operasyon_VALUE==46||operasyon_VALUE==50||operasyon_VALUE==51||operasyon_VALUE==52||operasyon_VALUE==53)내보내기("q=Q();r=Q();P(*jindex(r,(int)q));");
        else if(operasyon_VALUE==79||operasyon_VALUE==83||operasyon_VALUE==84||operasyon_VALUE==85||operasyon_VALUE==86)내보내기("q=Q();r=Q();*jindex(Q(),(int)r)=%s;",operasyon_VALUE==84?"(unsigned)(signed char)q":operasyon_VALUE==85?"(unsigned short)q":operasyon_VALUE==86?"(unsigned)(short)q":"q");
        else if(operasyon_VALUE==87)내보내기("Q();");
        else if(operasyon_VALUE==89)내보내기("q=Q();P(q);P(q);");
        else if(operasyon_VALUE==90)내보내기("q=Q();r=Q();P(q);P(r);P(q);");
        else if(operasyon_VALUE==95)내보내기("q=Q();r=Q();P(q);P(r);");
        else if(operasyon_VALUE==96||operasyon_VALUE==100||operasyon_VALUE==104||operasyon_VALUE==120||operasyon_VALUE==124||operasyon_VALUE==126||operasyon_VALUE==128||operasyon_VALUE==130){const char*pag_encode_VALUE=operasyon_VALUE==96?"+":operasyon_VALUE==100?"-":operasyon_VALUE==104?"*":operasyon_VALUE==120?"<<":operasyon_VALUE==124?">>":operasyon_VALUE==126?"&":operasyon_VALUE==128?"|":"^";내보내기("q=Q();r=Q();P((unsigned)r%s(unsigned)q%s);",pag_encode_VALUE,operasyon_VALUE==120||operasyon_VALUE==124?"%32":"");}
        else if(operasyon_VALUE==108||operasyon_VALUE==112)내보내기("q=Q();r=Q();P((unsigned)jdivide((int)r,(int)q,%d));",operasyon_VALUE==112);
        else if(operasyon_VALUE==116)내보내기("P(0U-(unsigned)Q());");
        else if(operasyon_VALUE==122)내보내기("q=Q();r=Q();P((unsigned)((int)r>>((unsigned)q&31)));");
        else if(operasyon_VALUE==132){unsigned 순번=byte_data();int 차이=(int8_t)byte_data();if(순번>=Grupo_sukat->지역변수들)information_technology_hindi_tama=1;내보내기("v[%u]=(unsigned)v[%u]+%uU;",순번,순번,(unsigned)차이);}
        else if(operasyon_VALUE>=145&&operasyon_VALUE<=147)내보내기("P((unsigned)(%s)Q());",operasyon_VALUE==145?"signed char":operasyon_VALUE==146?"unsigned short":"short");
        else if(operasyon_VALUE>=153&&operasyon_VALUE<=166){int layunin=(int)utos_posisyon+(int16_t)절반값();const char*Paghahambing_VALUE[]={"==","!=","<",">=",">","<="};if(layunin<0||layunin>=(int)Grupo_sukat->sukat_82232621){information_technology_hindi_tama=1;break;}if(operasyon_VALUE<159)내보내기("if((int)Q()%s0)goto L%d;",Paghahambing_VALUE[operasyon_VALUE-153],layunin);else if(operasyon_VALUE<165)내보내기("q=Q();r=Q();if((int)r%s(int)q)goto L%d;",Paghahambing_VALUE[operasyon_VALUE-159],layunin);else 내보내기("q=Q();r=Q();if(r%sq)goto L%d;",operasyon_VALUE==165?"==":"!=",layunin);}
        else if(operasyon_VALUE==167){int layunin=(int)utos_posisyon+(int16_t)절반값();if(layunin<0||layunin>=(int)Grupo_sukat->sukat_82232621)information_technology_hindi_tama=1;내보내기("goto L%d;",layunin);}
        else if(operasyon_VALUE==172||operasyon_VALUE==176)내보내기("return Q();");else if(operasyon_VALUE==177)내보내기("return 0;");
        else if(operasyon_VALUE==178||operasyon_VALUE==179){unsigned tagakilala_VALUE=절반값();if(tagakilala_VALUE<1||tagakilala_VALUE>=상수모음||Mga_Tag_list[tagakilala_VALUE]!=9||첫째값[tagakilala_VALUE]>=상수모음||SECOND_VALUE[tagakilala_VALUE]>=상수모음||Mga_Tag_list[첫째값[tagakilala_VALUE]]!=7||Mga_Tag_list[SECOND_VALUE[tagakilala_VALUE]]!=12){information_technology_hindi_tama=1;break;}unsigned may_ari_bagay=첫째값[첫째값[tagakilala_VALUE]],pangalan=첫째값[SECOND_VALUE[tagakilala_VALUE]],서술값=SECOND_VALUE[SECOND_VALUE[tagakilala_VALUE]];
            if(operasyon_VALUE==178&&UNICODE_VALUE(may_ari_bagay,"java/lang/System")&&UNICODE_VALUE(pangalan,"out")&&UNICODE_VALUE(서술값,"Ljava/io/PrintStream;"))내보내기("P(1);");
            else {unsigned file_pagpasok=0;while(file_pagpasok<필드개수&&(!같음(pangalan,pangalan_ng_field[file_pagpasok])||!같음(서술값,필드서술[file_pagpasok])))file_pagpasok++;if(!같음(may_ari_bagay,첫째값[현재클래스])||file_pagpasok==필드개수){information_technology_hindi_tama=1;break;}내보내기(operasyon_VALUE==178?"P(fields[%u]);":"fields[%u]=Q();",file_pagpasok);}}
        else if(operasyon_VALUE==182||operasyon_VALUE==184)호출(절반값(),operasyon_VALUE==182);
        else if(operasyon_VALUE==188){unsigned TYPE_kategorya=byte_data();if(TYPE_kategorya!=4&&TYPE_kategorya!=5&&TYPE_kategorya!=8&&TYPE_kategorya!=9&&TYPE_kategorya!=10)information_technology_hindi_tama=1;내보내기("P(jarray((int)Q()));");}
        else if(operasyon_VALUE==190)내보내기("P(jlength(Q()));");
        else if(operasyon_VALUE==198||operasyon_VALUE==199){int layunin=(int)utos_posisyon+(int16_t)절반값();if(layunin<0||layunin>=(int)Grupo_sukat->sukat_82232621)information_technology_hindi_tama=1;내보내기("if(Q()%s0)goto L%d;",operasyon_VALUE==198?"==":"!=",layunin);}
        else information_technology_hindi_tama=1;
        if(information_technology_hindi_tama)printf("jaot: method %u bytecode %u at %u unsupported or malformed\n",LOOKUP_INDEX,operasyon_VALUE,utos_posisyon);
        내보내기("\n");
    }
    haba_VALUE=저장값;내보내기("jfail();return 0;}\n");
}
static unsigned string_aralin(unsigned *data_posisyon,unsigned tapusin_OFFSET){
    if(*data_posisyon>=tapusin_OFFSET){information_technology_hindi_tama=1;return 0;}unsigned character_code=data[(*data_posisyon)++];
    if(character_code<128)return character_code;
    unsigned item_COUNT=character_code>=0xc0&&character_code<=0xdf?1:character_code>=0xe0&&character_code<=0xef?2:3;
    if(item_COUNT==3||item_COUNT>tapusin_OFFSET-*data_posisyon){information_technology_hindi_tama=1;return 0;}unsigned VALUE=character_code&((1u<<(6-item_COUNT))-1);
    for(unsigned 순번=0;순번<item_COUNT;순번++){unsigned Susunod_item=data[(*data_posisyon)++];if((Susunod_item&0xc0)!=0x80)information_technology_hindi_tama=1;VALUE=VALUE<<6|(Susunod_item&63);}
    if((item_COUNT==1&&VALUE<128&&VALUE!=0)||(item_COUNT==2&&VALUE<2048))information_technology_hindi_tama=1;return VALUE;
}
static void string_constant(unsigned tagakilala_VALUE){
    unsigned 부호없는값=첫째값[tagakilala_VALUE];if(부호없는값<1||부호없는값>=상수모음||Mga_Tag_list[부호없는값]!=1){information_technology_hindi_tama=1;return;}내보내기("static const unsigned char k%u[]={",tagakilala_VALUE);
    unsigned data_posisyon=첫째값[부호없는값],tapusin_OFFSET=data_posisyon+SECOND_VALUE[부호없는값];
    while(data_posisyon<tapusin_OFFSET&&!information_technology_hindi_tama){unsigned character_code=string_aralin(&data_posisyon,tapusin_OFFSET);
        if(character_code>=0xd800&&character_code<=0xdbff){unsigned 낮은부분=string_aralin(&data_posisyon,tapusin_OFFSET);if(낮은부분<0xdc00||낮은부분>0xdfff){information_technology_hindi_tama=1;break;}character_code=0x10000+((character_code-0xd800)<<10)+낮은부분-0xdc00;}
        else if(character_code>=0xdc00&&character_code<=0xdfff){information_technology_hindi_tama=1;break;}
        if(!character_code){printf("jaot: embedded NUL string needs JVM mode\n");information_technology_hindi_tama=1;break;}
        if(character_code<128)내보내기("%u,",character_code);
        else{unsigned item_COUNT=character_code<2048?2:character_code<65536?3:4;내보내기("%u,",(item_COUNT==2?0xc0:item_COUNT==3?0xe0:0xf0)|(character_code>>(6*(item_COUNT-1))));for(unsigned 순번=item_COUNT-1;순번;순번--)내보내기("%u,",0x80|((character_code>>(6*(순번-1)))&63));}
    }내보내기("0};\n");
}
const char *자바미리번역원문(const char*pangalan){
    size_t item_COUNT=strlen(pangalan);
    if(item_COUNT>4&&!strcmp(pangalan+item_COUNT-4,".jar")){
        if(꾸러미열기(pangalan)<0){printf("jaot: invalid JAR/Main-Class\n");return 0;}char path[256];const char*pagpasok_pamamaraan=꾸러미진입클래스();item_COUNT=strlen(pagpasok_pamamaraan);if(item_COUNT+6>=sizeof(path))return 0;
        for(unsigned 순번=0;순번<item_COUNT;순번++)path[순번]=pagpasok_pamamaraan[순번]=='.'?'/':pagpasok_pamamaraan[순번];strcpy(path+item_COUNT,".class");int pagpasok_COUNT=꾸러미읽기(path,data,sizeof(data));if(pagpasok_COUNT<0)return 0;haba_VALUE=pagpasok_COUNT;
    }else{intptr_t file_hawakán=사용자호출(3,(uintptr_t)pangalan,0,0,0,0,0);if(file_hawakán<0)return 0;intptr_t pagpasok_COUNT=사용자호출(9,file_hawakán,0,0,0,0,0);if(pagpasok_COUNT<0||pagpasok_COUNT>sizeof(data)){사용자호출(4,file_hawakán,0,0,0,0,0);return 0;}intptr_t RECEIVED_COUNT=사용자호출(2,file_hawakán,(uintptr_t)data,pagpasok_COUNT,0,0,0);사용자호출(4,file_hawakán,0,0,0,0,0);if(RECEIVED_COUNT!=pagpasok_COUNT)return 0;haba_VALUE=pagpasok_COUNT;}
    if(해석하기()<0){printf("jaot: requires static Java 8 int/reference subset without exceptions\n");return 0;}
    내보내기("typedef unsigned long W; extern void jfail(void);extern void jpush(W*,int*,W);extern W jpop(W*,int*);extern W jarray(int);extern W*jindex(W,int);extern int jlength(W),jdivide(int,int,int);extern void jprint(W,int,int);extern W jfread(W),jfwrite(W,W);static W fields[64];\n#define P(x) jpush(s,&sp,(W)(x))\n#define Q() jpop(s,&sp)\n");
    for(unsigned 순번=1;순번<상수모음&&!information_technology_hindi_tama;순번++)if(Mga_Tag_list[순번]==8)string_constant(순번);
    if(information_technology_hindi_tama)return 0;
    int pagpasok_point=-1,초기값=-1;
    for(unsigned 순번=0;순번<메소드개수;순번++)if(!UNICODE_VALUE(메소드목록[순번].pangalan,"<init>")){
        int sukat,pagpasok_COUNT=서술자(메소드목록[순번].서술값,&sukat);if(pagpasok_COUNT<0)return 0;내보내기("static W m%u(",순번);for(int 안쪽순번=0;안쪽순번<pagpasok_COUNT;안쪽순번++)내보내기(안쪽순번?",W":"W");if(!pagpasok_COUNT)내보내기("void");내보내기(");\n");
        if(UNICODE_VALUE(메소드목록[순번].pangalan,"main")&&UNICODE_VALUE(메소드목록[순번].서술값,"([Ljava/lang/String;)V")&&(메소드목록[순번].kompigurasyon_Background_Intelligent_Transfer_Service&9)==9)pagpasok_point=순번;
        if(UNICODE_VALUE(메소드목록[순번].pangalan,"<clinit>"))초기값=순번;
    }
    if(pagpasok_point<0)return 0;for(unsigned 순번=0;순번<메소드개수&&!information_technology_hindi_tama;순번++)bumuo_pamamaraan(순번);
    내보내기("int main(int argc,char**argv){W a[9]={0};a[0]=argc>0?argc-1:0;for(int i=1;i<argc&&i<9;i++)a[i]=(W)argv[i];");
    for(unsigned 순번=0;순번<필드개수;순번++)if(field_constant[순번]){
        unsigned character_code=field_constant[순번];if(character_code>=상수모음)return 0;
        if(Mga_Tag_list[character_code]==3)내보내기("fields[%u]=%uU;",순번,첫째값[character_code]);else if(Mga_Tag_list[character_code]==8)내보내기("fields[%u]=(W)k%u;",순번,character_code);else return 0;
    }
    if(초기값>=0)내보내기("m%d();",초기값);내보내기("m%d((W)a);return 0;}\n",pagpasok_point);
    return information_technology_hindi_tama?0:SMS;
}
