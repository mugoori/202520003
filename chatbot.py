# 이 코드는 레벤슈타인 거리 알고리즘을 사용하여
# 사용자의 질문과 가장 유사한 질문을 찾고
# 그에 맞는 답변을 제공하는 간단한 챗봇입니다.

# pandas 라이브러리를 불러옵니다. 데이터를 표 형태로 쉽게 다룰 수 있게 해줍니다.
import pandas as pd

# 레벤슈타인 거리를 계산하는 함수입니다.
# 두 문자열의 유사도를 숫자로 나타냅니다.
# 예: "안녕"과 "안녕하세요"는 3의 거리를 가집니다.
def levenshtein_distance(s1, s2):
    # 두 문자열의 길이를 저장합니다.
    len_s1, len_s2 = len(s1), len(s2)

    # 동적 프로그래밍을 위한 2차원 배열을 생성합니다.
    # 이 배열은 문자열을 변환하는데 필요한 최소 편집 횟수를 저장합니다.
    dp = [[0] * (len_s2 + 1) for _ in range(len_s1 + 1)]

    # 첫 번째 문자열을 빈 문자열로 만들기 위한 초기값 설정
    for i in range(len_s1 + 1):
        dp[i][0] = i

    # 두 번째 문자열을 만들기 위한 초기값 설정
    for j in range(len_s2 + 1):
        dp[0][j] = j

    # 두 문자열을 비교하며 최소 편집 거리를 계산합니다.
    for i in range(1, len_s1 + 1):
        for j in range(1, len_s2 + 1):
            # 현재 비교하는 문자가 같으면 비용은 0, 다르면 1
            cost = 0 if s1[i - 1] == s2[j - 1] else 1

            # 세 가지 연산 중 최소값을 선택합니다:
            # 1. 문자 삭제
            # 2. 문자 삽입
            # 3. 문자 교체
            dp[i][j] = min(
                dp[i - 1][j] + 1,       # 삭제
                dp[i][j - 1] + 1,       # 삽입
                dp[i - 1][j - 1] + cost # 교체
            )

    # 최종 편집 거리를 반환합니다.
    return dp[len_s1][len_s2]

# 챗봇의 학습 데이터를 CSV 파일에서 불러옵니다.
# Q 열은 질문, A 열은 답변을 포함합니다.
data = pd.read_csv("ChatbotData.csv")

# 사용자로부터 질문을 입력받습니다.
user_input = input("질문을 입력하세요: ")

# 입력된 질문과 모든 학습 데이터의 질문들 간의 거리를 계산합니다.
distances = []
for q in data['Q']:
    distance = levenshtein_distance(user_input, q)
    distances.append(distance)

# 가장 유사한 질문의 인덱스를 찾습니다.
min_index = distances.index(min(distances))

# 가장 유사한 질문에 대한 답변을 출력합니다.
print("챗봇의 답변:", data['A'][min_index])
