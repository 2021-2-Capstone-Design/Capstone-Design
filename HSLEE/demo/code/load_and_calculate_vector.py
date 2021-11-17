import sys
import math
import numpy as np

arguments = sys.argv
if len(arguments) == 3:
    coordinates_video = arguments[1]
    coordinates_user = arguments[2]
else:
    print("You insert wrong number of arguments.\n")
    print("Please insert 'python load_and_calculate_vector.py [coordinates_video_file] [coordinates_webcam_file]'")
    sys.exit()

coordinates_video_path = './../coordinates/' + coordinates_video + '.txt'
coordinates_user_path = './../coordinates/' + coordinates_user + '.txt'

file_v = open(coordinates_video_path, mode='rt', encoding='utf-8')
file_u = open(coordinates_user_path, mode='rt', encoding='utf-8')

result_v = []
result_u = []

# coordinates_video to numpy 'result_v'
for line in file_v:
    temp_line = line
    ret = np.array([])
    # count값은 관절좌표를 쭉 훑으면서 첫 x좌표를 얻기 위해 설정
    count = 0

    parse_line = temp_line.split(' ')

    if(len(parse_line) != 99):
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

    result_v = np.append(result_v, ret, axis=0)


# coordinates_user to numpy 'result_u'
for line in file_u:
    temp_line = line
    ret = np.array([])
    # count값은 관절좌표를 쭉 훑으면서 첫 x좌표를 얻기 위해 설정
    count = 0

    parse_line = temp_line.split(' ')

    if(len(parse_line) != 99):
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

    result_u = np.append(result_u, ret, axis=0)

# 1차원 배열로 모든 관절 좌표 쭉! (99개씩 4프레임 예시로 텍스트 저장해둠)
print("\n*** Check result ***")
print("video")
print(result_v)
print("user")
print(result_u)
print("\n")

# 프레임 수 계산
num_frame_v = result_v.shape[0]/(33*3)
num_frame_u = result_u.shape[0]/(33*3)
print("*** Check result ***")
print("video")
print(num_frame_v)
print("user")
print(num_frame_u)
print("\n")

# frame 수,  tracking좌표 수, xyz
result_v = np.reshape(result_v,(int(num_frame_v),33,3))
result_u = np.reshape(result_u,(int(num_frame_u),33,3))

# 프레임별로 numpy 배열 출력해보기
print("*** Check frame by frame ***")
print("video")
for i in range(int(num_frame_v)):
    print("frame" + str(i))
    print(result_v[i])
    print("\n")

print("user")
for i in range(int(num_frame_u)):
    print("frame" + str(i))
    print(result_u[i])
    print("\n")

# 차원 확인 (numpy 배열 크기 확인)
print("*** Check result dimension ***")
print("video")
print(result_v.shape)
print("user")
print(result_u.shape)
print("\n")

