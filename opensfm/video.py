from subprocess import Popen, PIPE

def video_orientation(video_file):
    # Rotation
    rotation = Popen(['exiftool', '-Rotation', '-b', video_file], stdout=PIPE).stdout.read()
    if rotation:
        rotation = float(rotation)
        if rotation == 0:
            orientation = 1
        elif rotation == 90:
            orientation = 6
        elif rotation == 180:
            orientation = 3
        elif rotation == 270:
            orientation = 8
    else:
        orientation = 1
    return orientation

    cap = cv2.VideoCapture(video_file)
    image_files = []
    for p in key_points:
        dt = (p[0] - video_start_time).total_seconds()
        if dt > 0:
            CAP_PROP_POS_MSEC = cv2.CAP_PROP_POS_MSEC if context.OPENCV3 else cv2.cv.CV_CAP_PROP_POS_MSEC
            cap.set(CAP_PROP_POS_MSEC, int(dt * 1000))
            ret, frame = cap.read()
            if ret:
                print('Grabbing frame for time {}'.format(p[0]))
                filepath = os.path.join(output_path, p[0].strftime("%Y_%m_%d_%H_%M_%S_%f")[:-3] + '.jpg')
                cv2.imwrite(filepath, frame)
                geotag_from_gpx.add_exif_using_timestamp(filepath, points, timestamp=p[0], orientation=orientation)

                # Display the resulting frame
                if visual:
                    # Display the resulting frame
                    max_display_size = 800
                    resize_ratio = float(max_display_size) / max(frame.shape[0], frame.shape[1])
                    frame = cv2.resize(frame, dsize=(0, 0), fx=resize_ratio, fy=resize_ratio)
                    cv2.imshow('frame', frame)
                    if cv2.waitKey(1) & 0xFF == 27:
                        break
                image_files.append(filepath)
    # When everything done, release the capture
    cap.release()
    if visual:
        cv2.destroyAllWindows()
    return image_files