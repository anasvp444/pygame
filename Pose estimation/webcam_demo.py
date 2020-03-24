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

# 0 nose, score = 0.997010, coord = [322.98469098 431.18965425]
# 1 leftEye, score = 0.992624, coord = [294.20422103 459.74505598]
# 2 rightEye, score = 0.999042, coord = [290.41523358 403.81453119]
# 3 leftEar, score = 0.926846, coord = [321.46881468 488.65419034]
# 4 rightEar, score = 0.952558, coord = [316.34406403 370.28198493]
# 5 leftShoulder, score = 0.119886, coord = [453.55154479 532.23512232]
# 6 rightShoulder, score = 0.247877, coord = [463.16843462 304.10356362]
# 7 leftElbow, score = 0.574630, coord = [571.58455929 679.38348348]
# 8 rightElbow, score = 0.388544, coord = [568.20483883 151.25195348]
# 9 leftWrist, score = 0.431772, coord = [718.33568025 608.29851696]
# 10 rightWrist, score = 0.058216, coord = [685.72080739 243.3757943 ]
# 11 leftHip, score = 0.060756, coord = [805.68614328 536.90733838]
# 12 rightHip, score = 0.474692, coord = [804.50692987 357.52342284]
# 13 leftKnee, score = 0.036079, coord = [1070.11860956  550.88002582]
# 14 rightKnee, score = 0.058909, coord = [1084.12532047  367.24259368]
# 15 leftAnkle, score = 0.000629, coord = [1348.3495266   617.98179314]
# 16 rightAnkle, score = 0.012292, coord = [1355.75351902  384.14320633]


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

            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(overlay_image, str(leftHandHigh) + str(rightHandHigh), (10, 450),
                        font, 1, (0, 255, 0), 1, cv2.LINE_AA)
            cv2.imshow('posenet', overlay_image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


if __name__ == "__main__":
    main()
