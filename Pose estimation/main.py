# env tensorflow
import tensorflow as tf
import cv2
import time


import posenet


argModel = 101
cam_id = 0  # "rtsp://admin:MSAZYB@192.168.1.248/h264_stream"
cam_width = 1280
cam_height = 720
scale_factor = 0.7125

background = cv2.imread('images/bg.jpg')

R_arm = cv2.imread('images/R_arm.jpg')
L_arm = cv2.imread('images/L_arm.jpg')
D_arm = cv2.imread('images/D_arm.jpg')
U_arm = cv2.imread('images/U_arm.jpg')

imcollection = {'R_arm': R_arm, 'L_arm': L_arm, 'D_arm': D_arm, 'U_arm': U_arm}
background = cv2.imread('images/bg.jpg')


def main():
    with tf.Session() as sess:
        model_cfg, model_outputs = posenet.load_model(argModel, sess)
        output_stride = model_cfg['output_stride']
        cap = cv2.VideoCapture(cam_id)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        cap.set(3, cam_width)
        cap.set(4, cam_height)

        while True:
            input_image, display_image, output_scale = posenet.read_cap(
                cap, scale_factor=scale_factor, output_stride=output_stride)

            heatmaps_result, offsets_result, displacement_fwd_result, displacement_bwd_result = sess.run(
                model_outputs,
                feed_dict={'image:0': input_image}
            )

            pose_scores, keypoint_scores, keypoint_coords = posenet.decode_multi.decode_multiple_poses(
                heatmaps_result.squeeze(axis=0),
                offsets_result.squeeze(axis=0),
                displacement_fwd_result.squeeze(axis=0),
                displacement_bwd_result.squeeze(axis=0),
                output_stride=output_stride,
                max_pose_detections=10,
                min_pose_score=0.15)

            keypoint_coords *= output_scale

            overlay_image = posenet.draw_skel_and_kp(
                display_image, pose_scores, keypoint_scores, keypoint_coords,
                min_pose_score=0.15, min_part_score=0.1)

            leftHandHigh = False

            leftWrist_h = keypoint_coords[0, :, :][9][0]
            leftShoulder_h = keypoint_coords[0, :, :][5][0]
            if(leftWrist_h < leftShoulder_h):
                leftHandHigh = True

            rightHandHigh = False

            rightWrist_h = keypoint_coords[0, :, :][10][0]
            rightShoulder_h = keypoint_coords[0, :, :][6][0]
            if(rightWrist_h < rightShoulder_h):
                rightHandHigh = True

            if(rightHandHigh and leftHandHigh):
                pos = 'U_arm'
            elif(rightHandHigh):
                pos = 'R_arm'
            elif(leftHandHigh):
                pos = 'L_arm'
            else:
                pos = 'D_arm'
            background[200:200+346, 200: 200+240] = imcollection[pos]
            cv2.imshow('posenet', background)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


if __name__ == "__main__":
    main()
