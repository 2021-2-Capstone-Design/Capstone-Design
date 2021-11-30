import sys
import math
import numpy as np
from django.shortcuts import render

dance_name = sys.argv[1]
coordinates_video_path = 'capstone/original_coordinate/' + dance_name + '.txt'
coordinates_user_path = 'capstone/user_coordinate/' + dance_name + '_record.txt'
result_path = 'capstone/results/result_' + dance_name + '.txt'

result_video = []
result_user = []

def load_score():
    global result_video
    global result_user
    global result_path
    file_video = open(coordinates_video_path, mode='rt', encoding='utf-8')
    file_user = open(coordinates_user_path, mode='rt', encoding='utf-8')

    # coordinates_video to numpy 'result_video'
    for line in file_video:
        temp_line = line
        ret = np.array([])
        # count값은 관절좌표를 쭉 훑으면서 첫 x좌표를 얻기 위해 설정
        count = 0

        parse_line = temp_line.split(' ')

        if(len(parse_line) < 36):
            # 관절 누락이 있다는 뜻
            print("There are missing joint coordinates")
        else:
            while True:
                for full_joint in range(len(parse_line)):
                    if(full_joint / 3 == count):
                        # 처음 count와 일치하는 곳부터 +2 인덱스까지가 x, y, z좌표 값임
                        temp_joint = np.array([parse_line[full_joint], parse_line[full_joint+1], parse_line[full_joint+2]], float)
                        ret = np.append(ret, temp_joint, axis = 0)
                        break
                count += 1
                # count == 33이면 모든 관절을 훑어본 것. 좌표 3개당 count 1씩 증가하므로 (한 줄에 총 99개 좌표)
                if(count == 33):
                    break

        # while True:
        #     if(temp_line is not None):
        #         if(len(temp_line.split(' ')) == 3):
        #             joint_x, joint_y, joint_z = temp_line.split(' ')
        #             temp_joint = np.array([joint_x, joint_y, joint_z], float)
        #             temp_line = ''
        #             ret = np.append(ret, temp_joint, axis=0)
        #             break
        #         elif(len(temp_line.split(' ')) == 4):
        #             joint_x, joint_y, joint_z, temp_line = temp_line.split(' ', maxsplit=3)
        #             temp_joint = np.array([joint_x, joint_y, joint_z], float)
        #             ret = np.append(ret, temp_joint, axis=0)
        #         else:
        #             break
        #     else:
        #         break

        result_video = np.append(result_video, ret, axis=0)


    # coordinates_user to numpy 'result_user'
    for line in file_user:
        temp_line = line
        ret = np.array([])
        # count값은 관절좌표를 쭉 훑으면서 첫 x좌표를 얻기 위해 설정
        count = 0

        parse_line = temp_line.split(' ')

        if(len(parse_line) < 36):
            # 관절 누락이 있다는 뜻
            print("There are missing joint coordinates")
        else:
            while True:
                for full_joint in range(len(parse_line)):
                    if(full_joint / 3 == count):
                        # 처음 count와 일치하는 곳부터 +2 인덱스까지가 x, y, z좌표 값임
                        temp_joint = np.array([parse_line[full_joint], parse_line[full_joint+1], parse_line[full_joint+2]], float)
                        ret = np.append(ret, temp_joint, axis = 0)
                        break
                count += 1
                # count == 33이면 모든 관절을 훑어본 것. 좌표 3개당 count 1씩 증가하므로 (한 줄에 총 99개 좌표)
                if(count == 33):
                    break

        # while True:
        #     if(temp_line is not None):
        #         if(len(temp_line.split(' ')) == 3):
        #             joint_x, joint_y, joint_z = temp_line.split(' ')
        #             temp_joint = np.array([joint_x, joint_y, joint_z], float)
        #             temp_line = ''
        #             ret = np.append(ret, temp_joint, axis=0)
        #             break
        #         elif(len(temp_line.split(' ')) == 4):
        #             joint_x, joint_y, joint_z, temp_line = temp_line.split(' ', maxsplit=3)
        #             temp_joint = np.array([joint_x, joint_y, joint_z], float)
        #             ret = np.append(ret, temp_joint, axis=0)
        #         else:
        #             break
        #     else:
        #         break

        result_user = np.append(result_user, ret, axis=0)


    # 1차원 배열로 모든 관절 좌표 쭉! (99개씩 4프레임 예시로 텍스트 저장해둠)
    print("\n*** Check result ***")
    print("video")
    print(result_video)
    print("user")
    print(result_user)
    print("\n")

    # 프레임 수 계산
    num_frame_video = result_video.shape[0]/(12*3)
    num_frame_user = result_user.shape[0]/(12*3)
    print("*** Check result ***")
    print("video")
    print(num_frame_video)
    print("user")
    print(num_frame_user)
    print("\n")

    # frame 수,  tracking좌표 수, xyz
    result_video = np.reshape(result_video,(int(num_frame_video),12,3))
    result_user = np.reshape(result_user,(int(num_frame_user),12,3))

    # 프레임별로 numpy 배열 출력해보기
    print("*** Check frame by frame ***")
    print("video")
    for i in range(int(num_frame_video)):
        print("frame" + str(i))
        print(result_video[i])
        print("\n")

    print("user")
    for i in range(int(num_frame_user)):
        print("frame" + str(i))
        print(result_user[i])
        print("\n")

    # 차원 확인 (numpy 배열 크기 확인)
    print("*** Check result dimension ***")
    print("video")
    print(result_video.shape)
    print("user")
    print(result_user.shape)
    print("\n")
    body_index = [
        [0, 2, 4],  # left arm
        [1, 3, 4],  # right arm
        [6, 8, 10],  # left leg
        [7, 9, 11],  # right leg

        [3, 1, 7],  # right shoulder
        [2, 0, 6],  # left shoulder
        [6, 7, 9],  # right pelvis
        [7, 6, 8],  # left pelvis
    ]

    # 프레임 수가 무조건 유저영상 > 안무영상 이므로 length는 안무영상 프레임수로
    length = len(result_video)
    length_user = len(result_user)
    print(length)

    # 뒤에서부터 비교하기
    a = length
    b = length_user

    # 영상 짧아도 무조건 b가 유저 영상
    # 대신 짧은 값(안무 영상 프레임 수)을 length로 가지고 있으니 그걸 가지고 하면 될 듯함

    # 타임스탬프 체크용 카운터
    time_counter = 0

    txt = open(result_path, 'w')

    total_point = 0  # 총 포인트

    joint_counter = np.zeros(8)  # 틀린 프레임 누적하면서 어느 부분이 많이 틀렸는지 카운트

    for n in range(b - 1, b - 1 - length, -1):
        #     print("new frame")

        frame_point = 0 # 프레임에서 체크한 포인트
        joint_index = 0

        for index in body_index:
            l1 = result_video[n + (a - b)][index[0]]
            l2 = result_video[n + (a - b)][index[1]]
            l3 = result_video[n + (a - b)][index[2]]

            ll1 = l1 - l2
            ll2 = l3 - l2

            innerREAL = np.dot(ll1, ll2)
            REAL = np.linalg.norm(ll1) * np.linalg.norm(ll2)
            angleREAL = np.arccos(innerREAL / REAL) / np.pi * 180
            # print(angleREAL/np.pi*180)

            u1 = result_user[n][index[0]]
            u2 = result_user[n][index[1]]
            u3 = result_user[n][index[2]]

            uu1 = u1 - u2
            uu2 = u3 - u2

            innerUSER = np.dot(uu1, uu2)
            USER = np.linalg.norm(uu1) * np.linalg.norm(uu2)
            angleUSER = np.arccos(innerUSER / USER) / np.pi * 180

            # 동영상 각도 / 유저 각도 체크해보는 print
            #         print(angleREAL)
            #         print(angleUSER)
            #         print()

            if angleUSER <= angleREAL + 40.0 and angleUSER >= angleREAL - 40.0:
                total_point += 1
                frame_point += 1
            elif (angleREAL + 40.0 < angleUSER and angleUSER <= angleREAL + 60.0) and (
                    angleUSER >= angleREAL - 60.0 and angleREAL - 40.0 > angleUSER):
                total_point += 0.5
                frame_point += 0.5
                joint_counter[joint_index] += 1
                #             print("0.5!")
            else:
                joint_counter[joint_index] += 1
                #             print("x")

            joint_index += 1

        if (frame_point == 8):
            # 정확도 측정 요소 8개 모두 맞았을 때

            if (time_counter >= 20):
                # 20 프레임 이상 연속해서 틀리다가 다시 맞게 추었을 때
                timestamp_min_frame_num = n

                # 두 영상의 fps를 맞춰서 같은 변수로 저장했으므로 그대로 사용해도 된다.(가정)

                # 방금까지 측정된 부분의 시간(시작점)
                timestamp_min_time_sec = (int)(timestamp_min_frame_num / fps)
                timestamp_min_time_msec = (float)((timestamp_min_frame_num % fps) / fps)
                timestamp_min_time = (float)(timestamp_min_time_sec) + timestamp_min_time_msec
                timestamp_min_time_floor = math.floor(timestamp_min_time * 2)

                # 방금까지 측정된 부분의 시간(종료지점)
                timestamp_max_time_sec = (int)(timestamp_max_frame_num / fps)
                timestamp_max_time_msec = (float)((timestamp_max_frame_num % fps) / fps)
                timestamp_max_time = (float)(timestamp_max_time_sec) + timestamp_max_time_msec
                timestamp_max_time_ceil = math.floor(timestamp_max_time * 2)

                # 관절 좌표 어느부분(2부위)이 많이 틀렸는지 체크해서 알려주기
                joint_counter_sort = np.sort(joint_counter)[::-1]
                jointstamp_temp = ""

                already_check = -1
                i = 0
                sorting_zero_check = 0

                while True:
                    if (sorting_zero_check == 1):
                        break
                    for j in range(0, 8):
                        if (joint_counter_sort[i] == 0):
                            sorting_zero_check = 1
                            break
                        if (joint_counter[j] == joint_counter_sort[i] and joint_counter[j] != 0):
                            if ((j == 0 or j == 5) and already_check != 0):
                                jointstamp_temp = "왼쪽 팔"
                                already_check = 0
                                joint_counter[j] == 0
                                break
                            elif ((j == 1 or j == 4) and already_check != 1):
                                jointstamp_temp = "오른쪽 팔"
                                already_check = 1
                                joint_counter[j] == 0
                                break
                            elif ((j == 2 or j == 7) and already_check != 2):
                                jointstamp_temp = "왼쪽 다리"
                                already_check = 2
                                joint_counter[j] == 0
                                break
                            elif ((j == 3 or j == 6) and already_check != 3):
                                jointstamp_temp = "오른쪽 다리"
                                already_check = 3
                                joint_counter[j] == 0
                                break
                        else:
                            continue

                    if (i == 0):
                        jointstamp = jointstamp_temp
                    if (i != 0 and jointstamp != jointstamp_temp):
                        jointstamp = jointstamp + ", " + jointstamp_temp
                        break
                    if (i == 7):
                        break

                    i += 1

                # 텍스트 파일에 틀린 시간 적어줌
                timestamp = "대략 " + str(timestamp_min_time_floor) + "초 ~ " + str(timestamp_max_time_ceil) + "초 : "
                comment = timestamp + jointstamp + " 부분을 잘 보세요."
                txt.write(comment)
                txt.write("\n")

                #             print("wrong -> correct min")
                #             print(n)

                # 초기화
                #         print("min")
                #         print(n)
            time_counter = 0
            joint_counter[:] = 0
        else:
            # 정확도 측정 요소 8개 중 하나라도 틀렸다면

            if (time_counter == 0):
                # 틀린 자세 처음 count
                timestamp_max_frame_num = n

                #             print("max")
                #             print(n)
            time_counter += 1

        if (n == b - length and time_counter >= 20):
            # 마지막 프레임이면서 20 프레임 이상 연속해서 틀리다가 다시 맞게 추었을 때
            timestamp_min_frame_num = n

            # 두 영상의 fps를 맞춰서 같은 변수로 저장했으므로 그대로 사용해도 된다.(가정)

            # 방금까지 측정된 부분의 시간(시작점)
            timestamp_min_time_sec = (int)(timestamp_min_frame_num / fps)
            timestamp_min_time_msec = (float)((timestamp_min_frame_num % fps) / fps)
            timestamp_min_time = (float)(timestamp_min_time_sec) + timestamp_min_time_msec
            timestamp_min_time_floor = math.floor(timestamp_min_time)

            # 방금까지 측정된 부분의 시간(종료지점)
            timestamp_max_time_sec = (int)(timestamp_max_frame_num / fps)
            timestamp_max_time_msec = (float)((timestamp_max_frame_num % fps) / fps)
            timestamp_max_time = (float)(timestamp_max_time_sec) + timestamp_max_time_msec
            timestamp_max_time_ceil = math.ceil(timestamp_max_time)

            # 관절 좌표 어느부분(2부위)이 많이 틀렸는지 체크해서 알려주기
            joint_counter_sort = np.sort(joint_counter)[::-1]
            jointstamp_temp = ""

            already_check = -1
            i = 0
            sorting_zero_check = 0

            while True:
                if (sorting_zero_check == 1):
                    break
                for j in range(0, 8):
                    if (joint_counter_sort[i] == 0):
                        sorting_zero_check = 1
                        break
                    if (joint_counter[j] == joint_counter_sort[i] and joint_counter[j] != 0):
                        if ((j == 0 or j == 5) and already_check != 0):
                            jointstamp_temp = "왼쪽 팔"
                            already_check = 0
                            joint_counter[j] == 0
                            break
                        elif ((j == 1 or j == 4) and already_check != 1):
                            jointstamp_temp = "오른쪽 팔"
                            already_check = 1
                            joint_counter[j] == 0
                            break
                        elif ((j == 2 or j == 7) and already_check != 2):
                            jointstamp_temp = "왼쪽 다리"
                            already_check = 2
                            joint_counter[j] == 0
                            break
                        elif ((j == 3 or j == 6) and already_check != 3):
                            jointstamp_temp = "오른쪽 다리"
                            already_check = 3
                            joint_counter[j] == 0
                            break
                    else:
                        continue

                if (i == 0):
                    jointstamp = jointstamp_temp
                if (i != 0 and jointstamp != jointstamp_temp):
                    jointstamp = jointstamp + ", " + jointstamp_temp
                    break
                if (i == 7):
                    break

                i += 1

            # 텍스트 파일에 틀린 시간 적어줌
            timestamp = "대략 " + str(timestamp_min_time_floor) + "초 ~ " + str(timestamp_max_time_ceil) + "초 : "
            comment = timestamp + jointstamp + " 부분을 잘 보세요."
            txt.write(comment)
            txt.write("\n")

    # print("wrong -> correct min")
    #         print(n)
    txt.write("total point : " + str(total_point / (8 * length) * 100))
    txt.close()

    def load_score_main(request):
        load_score()
        return render(request, 'capstone/practice.html')