"""보존한 공개 CA 인증서로 BearSSL 신뢰 기준을 만들고 TLS 검증 시각을 기록한다."""
from pathlib import Path as 경로형
import time as 시각도구,re as 정규식
from cryptography import x509 as 인증서도구
from cryptography.hazmat.backends import default_backend as 기본연결
from cryptography.hazmat.primitives.asymmetric import rsa as 큰수키,ec as 곡선키
from cryptography.hazmat.primitives import serialization as 직렬화

def 인증준비(기준,결과,꾸러미=None):
 원본=(꾸러미 or 기준/'외부원문/웹인증서.pem').read_bytes();줄들=['/* Public CA keys; generated from preserved PEM. */'];항목들=[]
 def 배열(이름,값):줄들.append('static const unsigned char '+이름+'[] = {'+','.join(str(수) for 수 in 값)+'};');return '(unsigned char*)'+이름+','+str(len(값))
 def 범위(자료,시작):
  위치=시작+1;길이=자료[위치];위치+=1
  if 길이&128:
   수=길이&127;길이=int.from_bytes(자료[위치:위치+수],'big');위치+=수
  return 위치,위치+길이
 for 덩이 in 정규식.findall(b'-----BEGIN CERTIFICATE-----.*?-----END CERTIFICATE-----',원본,정규식.S):
  인증=인증서도구.load_pem_x509_certificate(덩이,기본연결());키=인증.public_key();번호=len(항목들);접두='신뢰'+str(번호)
  자료=인증.public_bytes(직렬화.Encoding.DER);위치,_=범위(자료,0);위치,_=범위(자료,위치)
  if 자료[위치]==160:_,위치=범위(자료,위치)
  for _ in range(4):_,위치=범위(자료,위치)
  _,끝=범위(자료,위치);주체=배열(접두+'이름',자료[위치:끝])
  if isinstance(키,큰수키.RSAPublicKey):
   값=키.public_numbers();수=값.n.to_bytes((값.n.bit_length()+7)//8,'big');지수=값.e.to_bytes((값.e.bit_length()+7)//8,'big');공개='{BR_KEYTYPE_RSA,{.rsa={'+배열(접두+'수',수)+','+배열(접두+'지수',지수)+'}}}'
  elif isinstance(키,곡선키.EllipticCurvePublicKey):
   곡선={'secp256r1':23,'secp384r1':24,'secp521r1':25}.get(키.curve.name)
   if not 곡선:continue
   값=키.public_numbers();폭=(키.key_size+7)//8;점=b'\x04'+값.x.to_bytes(폭,'big')+값.y.to_bytes(폭,'big');공개='{BR_KEYTYPE_EC,{.ec={'+str(곡선)+','+배열(접두+'점',점)+'}}}'
  else:continue
  항목들.append('{{'+주체+'},BR_X509_TA_CA,'+공개+'}')
 줄들+=['static const br_x509_trust_anchor 웹신뢰기준[] = {'+','.join(항목들)+'};','#define 웹신뢰수 '+str(len(항목들))]
 목적=결과/'웹인증.h';목적.parent.mkdir(parents=True,exist_ok=True);본문='\n'.join(줄들)+'\n'
 if not 목적.exists() or 목적.read_text()!=본문:목적.write_text(본문)
 # 이미지를 다시 만들 때 검증 시각이 갱신된다. 게스트 웹시각 명령으로도 보정할 수 있다.
 시각=결과/'웹시각.h';시각.write_text('#define 웹빌드시각 '+str(int(시각도구.time()))+'u\n')
 return 목적
