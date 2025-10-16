print("Hello world!")

# 문제 1번 및 2번


# new라는 새로운 브랜치 생성, 동시에 해당 브랜치로 이동하는 것

print("git checkout -b new")

# 현재 브랜치를 직전 커밋으로 되돌리고, 되돌린 커밋의 변경사항을 staging 상태로 유지하기

print("git reset --soft HEAD^")

# 진행중인 merge 작업 취소하고, 시작 전 상태로 되돌림

print("git merge --abort")

#원격 저장소의 최신 변경 사항을 로컬로 가져오되, 현재 작업 브랜치에는 병합하지 않음

print("git fetch")

# 현재 체크아웃된 로컬 브랜치의 upstream을 origin/new-feature로 설정하기

print("git branch -u origin/new-feature")

#가장 퇴근에 작성한 커밋을 수정하는 명령어

print("git commit --amend")

#문제 3번

#1. 로그를 읽어서 전체 로그 원문 출력하기
#2. 원본 리스트 출력 [(timestamp, message)] 형식의 tuple list를 그대로 print()
## event column: antl / 파싱(parting)시 line.split(',', 2) 처럼 최대 2번만 분리해서, message 내 콤마 보존
## 문자열 표기: ("")가 출력되도록 list/tuple 자체를 프린트함
##3. 시간 역순(내림차순)정렬 리스트 출력. 2)의 리스트를 timestamp 기준 내림차순으로 정렬 후 그대로 *print()
##4. Dict로 변환하여 출력: 정렬 리스트를 {timestamp: message} 형태의 딕셔너리로 변환하여 그대로 출력
## ㄴ> key: timestamp(string) | value: message(string)
## 정렬 기준 timestamp: = "%Y-%m-%d %H:%M:%S" 형식으로 할 것
##

def read_log(path='mission_computer_main.log'): #log 파일을 읽어오는 함수
    try:
        with open(path, 'r', encoding='utf-8') as f: #해당 'path'의 파일을 'r'(read)모드, utf-8 인코딩으로 open한다.
            return f.read() #f.read 메소드 결과값을 반환
    except FileNotFoundError: #log 파일이 없을 때 예외
        raise
    except UnicodeDecodeError: #유니코드 디코딩이 불가했을 때 예외
        raise
    except Exception: # 그 외 예외 상황에 예외처리
        raise

def log2tuple(log): #log을 (timestamp, message) 형태의 tuple 값으로 반환하는 함수
    lines = log.strip().split('\n') #log를 받아와서 띄워쓰기를 제거하고, 줄바꿈 (\n) 기준으로 나눠준다 (= lines)
    pairs = []                      #pairs라는 빈 list를 정의한다.
    if lines[0] != 'timestamp,event,message': #만약 첫 줄이 'timestamp,event,message' 형태가 아니라면
        raise ValueError                        #ValueError 띄움
    for line in lines[1:]: #1번째(0부터 시작하니까 자료값 2번째 줄) 줄부터 반복적으로
        if not line.strip(): #내용이 없다고 하면 제끼고
            continue
        parts = line.split(',',2) #'timestamp,event,message' 형태의 각 줄을 앞에서 두번째까지의 콤마로 나눠서 parts에 저장한다
        if len(parts) != 3 or len(parts[0]) != 19: #parts의 원소가 3개가 아니거나(빈 자료), timestamp가 형식에 안 맞다면
            raise ValueError                       # ValueError을 띄운다.
        pairs.append((parts[0], parts[2])) # ('timestamp', 'message')형태로 된 tuple을 pairs 라는 list에 붙인다
    return pairs
        
def main():
    try:
        log = read_log() #log를 그대로 읽어서 log라는 이름의 객체로 저장
        print(log) #출력
        pairs = log2tuple(log) #log를 pairs라는 tuple로 바꿔서
        print(pairs) # 출력
        spairs = sorted(pairs, key= lambda x: x[0], reverse=True) # 시간 (x[0]) 역순으로 (reverse=True)바꿔준 뒤에
        print(spairs) #출력
        ldict = dict(spairs) #바로 dictionary 형태로 바꿔준 뒤에
        print(ldict) #출력.
    except FileNotFoundError: #파일이 없는 경우 예외
        print('file open error.')
    except UnicodeDecodeError: #유니코드 오류 예외처리
        print('decoding error.')
    except ValueError: #값이 안 맞을 경우 예외처리
        print('Invalid log format')
    except Exception: #그외의 경우 예외처리
        print('Processing error.')

if __name__=="__main__":
    main()



# 문제 4번

import math     #math 라이브러리를 불러온다
densities = {'유리':2.4,'알루미늄':2.7, '탄소강':7.85} #재료별 densities를 dictionary 형태로 저장해 둔다

def sphere_area(diameter: float, material: str, thickness: float = 1.0): #구의 표면적을 계산하는 함수
    if not math.isfinite(diameter) or not math.isfinite(thickness) or \ 
        diameter <= 0 or thickness <= 0 or material not in densities: #구의 지름, 두께가 너무 크거나 0이거나 음수거나/dictionary에 재료가 없는 경우
        raise ValueError                                              # ValueError 예외처리를 해 둔다.
    area_m2 = math.pi * diameter * diameter  # pi * (radius * 2) * (radius * 2) -> 4*PI*r^2 (구의 표면적 공식)
    area_cm2 = area_m2 * 1e4                 # m^2 -> cm^2 로 변환 (100 * 100을 곱함)
    volume_cm3 = area_cm2 * thickness        # 구가 충분히 크다 가정하고, 표면적에 두께를 그냥 곱한 값을 부피로 정의
    mass_kg = densities[material] * volume_cm3 / 1e3 # density가 g/cm^3로 되어있으므로, kg로 변환을 위해서 1e3 (1,000)으로 나눠줌
    mars_weight_kg = mass_kg * .38 # 화성 중력계수 0.38을 곱해줌
    return area_m2, mars_weight_kg # 구의 표면적 및 화성에서의 무게를 반환한다.
def main():
    try: #예외처리!
        d_raw = input("지름(m)을 입력하세요:").strip() #공백을 제거한 채로 input을 받음
        if not d_raw: #아무것도 입력 안 하고 enter 눌렀을 때 예외처리
            raise ValueError
        try:
            d = float(d_raw) #d_raw 를 float로 변환해줌. 값이 float로 변환 불가능할 때 예외처리
        except ValueError:
            raise
        if d <= 0: #지름이 음수일 때 예외처리
            raise ValueError
        mat = input("재질(유리/알루미늄/탄소강)을 입력하세요:").strip() #재질을 받음
        if mat not in densities: #densities안에 입력한 재질이 없을 경우 예외처리
            raise ValueError
        th_raw = input("두께(cm)을 입력하세요:").strip() #두께(cm) 입력 요청
        if not th_raw: #입력값이 없는 경우에는
            th_raw = 1.0 # 1로 자동 설정
        try:
            th = float(th_raw) #th_raw를 flost로 변환, 안될 시 예외처리
        except ValueError:
            raise
        if th <= 0: #th가 음수일 겨우 예외처리
            raise ValueError
        A, W = sphere_area(d, mat, th) # 지름, 재질, 두께를 매개변수로 sphere_area 함수에 넣어줌. 결과값은 A(Area)와 W(Weight)로 받아온다.
        print(f"재질 : {mat},지름: {d:g}, 두께: {th:g},면적 : {A:.3f}, 무게: {W:.3f} kg") # 이제 필요한 모든 것들을 출력 / .3f로 소숫점 셋째자리 체크
    except ValueError: #뭔가 없다면 에러
        print("Invalid input.")
    except Exception: #그 외 다른 예외라도 error
        print("Processing Error.")
if __name__=="__main__":
    main()




# 문제 5 번


CIPHER = "gdkkn vnqkc"  #CIPHER(암호문)이 무엇인지 처음에 선언

def caesar_cipher_decode(text): # 카이사르 암호를 푸는 함수 정의. 매개변수로 text를 받아옴.
    res = []                    # result라는 빈 list를 정의함
    for shift in range(26):     # 알파벳은 26개니까 배열을 바꾸는 방법도 26가지
        tmp = ""                # for 문에서 사용될 임시 변수 tmp(문자열)을 선언함
        for ch in text:         # text(문자열)의 각 문자(char)를 차례대로 읽어옴
            if ch.islower():    # 해당 문자가 소문자라면
                tmp += chr((ord(ch) - 97 - shift) % 26 + 97) #ASCII에서 해당 문자 순서(ord(ch)) - 97(알파벳 a의 순서) - shift(변환숫자) 값을
                                                                #26으로 나눈 나머지(알파벳 순서)에다 97을 더하고(다시 ASCII 순서) 그걸 chr로 재변환함
            else:               # else: 해당문자가 소문자가 아닐 경우 -> 해당 문자가 대문자라면
                tmp += ch       # 임시 문자열에 그냥 그 문자를 더한다 (여기서는 구두점, 공백 문자 등을 연계시키는 역할)
        res.append(tmp)         # 이제 완성된 문자열(tmp)을 res.append(tmp)로 뒤에 붙인다 (shift별로)
    return res                  #res 값을 반환한다.
def main():                     #main 함수 선언
    try:                        #예외처리를 위한 try-except 구문
        decode_text = caesar_cipher_decode(CIPHER) #우리가 할 일 (decode 함수에 CIPHER(암호문) 넣기)
        for i, text in enumerate(decode_text): # decode_text는 문자열로 구성된 list이므로 (1, '변환문') 형식이 되도록 index를 줌
            print(f"{i}: {text}") # 그렇게 print(f  )로 (0: '원래글자) (1:'변환문' ) (2: '변환문') ... 이런식으로 줄줄이 출력
        res = int(input())  #출력된 값 중에서 말이 되는 건 무엇일지 1~25 사이에 input을 받음.
        if not 0 <= res <= 25: #26개의 알파벳 사이클에서 벗어나는 입력값은
            raise ValueError   #ValueError 처리를 해줌 (예외)
        print(f"Result: {decode_text[res]}") #
    except ValueError:  #CIPHER가 잘못된 형식인 경우
        print(f"invalid input.")
    except Exception: #그 외의 그러한 그런 것들
        print(f"error")

if __name__ == '__main__': #직접 실행시만
    main()                 # main 함수를 실행할 것.