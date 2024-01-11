import cv2
import mediapipe as mp
import sys
import pyautogui
import ctypes
import time

# 전역 변수 초기화
is_index_bent = False  # 검지 손가락이 구부러진 상태 여부를 나타내는 변수
is_click_performed = False  # 클릭 동작을 수행했는지 여부를 나타내는 변수
hand_x, hand_y = 0, 0  # 손 좌표 초기화

def initialize_webcam():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Webcam not found or not opened.")
        sys.exit()
    cap.set(3, 640)
    cap.set(4, 640)
    return cap

def process_hand(frame, hands):
    global is_index_bent, is_click_performed, hand_x, hand_y

    # 손 감지
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    # 화면에 손가락 감지 결과 표시
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # 검지 손가락 추적
            index_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.MIDDLE_FINGER_MCP]
            index_tip_2 = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP]

            # 검지 손가락의 좌표를 이용하여 커서 위치 업데이트
            hand_x, hand_y = int(index_tip.x * frame.shape[1]), int(index_tip.y * frame.shape[0])

            # 검지 손가락의 y 좌표를 이용하여 구부러진 상태 여부 확인
            is_index_bent = index_tip_2.y < hand_landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_DIP].y

            # 검지 손가락 구부러짐을 기준으로 클릭 동작 감지 및 수행
        if is_index_bent and not is_click_performed:
            # 클릭 동작 수행 (원하는 로직 추가)
            print("Left click performed!")
            is_click_performed = True

            # 손 좌표 업데이트
            pyautogui.click()
            #hand_x, hand_y = int(index_tip.x * frame.shape[1]), int(index_tip.y * frame.shape[0])
            print(hand_x, hand_y)
            
        elif not is_index_bent:
            # 클릭 동작 초기화
            is_click_performed = False


#-------------------------------------------------------------------------------




def main():

    global hand_x, hand_y
    pyautogui.FAILSAFE = False  # fail-safe 비활성화
    cap = initialize_webcam()
    image_path = 'Blank_Go_board.png'

    with mp.solutions.hands.Hands() as hands:
        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                continue

            process_hand(frame, hands)
            cv2.imshow('Webcam Feed', frame)

            # 현재 마우스 위치 확인
            current_x, current_y = pyautogui.position()

            # 마우스 위치가 변경되었을 때만 이동
            if current_x != hand_x or current_y != hand_y:
                pyautogui.moveTo(hand_x, hand_y)


                

            if cv2.waitKey(1) & 0xFF == 27:
                break

    cap.release()
    cv2.destroyAllWindows()



if __name__ == "__main__":
    main()
