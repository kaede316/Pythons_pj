# -*- coding: utf-8 -*-
import cv2
from ultralytics import YOLO
import os


class YOLOv8Demo:
    def __init__(self, model_path='yolov8n.pt'):
        """
        初始化YOLOv8模型
        :param model_path: 模型文件路径。默认为'yolov8n.pt'，会自动下载（若不存在）。
        """
        # 检查模型文件是否存在，如果不存在会自动下载
        if not os.path.exists(model_path) and model_path in ['yolov8n.pt', 'yolov8s.pt', 'yolov8m.pt', 'yolov8l.pt',
                                                             'yolov8x.pt']:
            print(f"模型文件 '{model_path}' 不存在，将自动下载...")

        # 加载模型
        self.model = YOLO(model_path)
        print(f"模型 '{model_path}' 加载成功！")

    def detect_image(self, image_path, output_path='detected_image.jpg', conf_threshold=0.5):
        """
        对单张图像进行目标检测
        """
        # 检查图像文件是否存在
        if not os.path.exists(image_path):
            print(f"错误：图像文件 '{image_path}' 不存在！")
            print("请提供有效的图像文件路径，例如：")
            print("- 'test_image.jpg' (当前目录下的文件)")
            print("- '/Users/你的用户名/Desktop/myphoto.jpg' (绝对路径)")
            return

        # 执行预测
        results = self.model.predict(source=image_path, conf=conf_threshold, save=False)
        # 获取带标注的结果图像
        annotated_frame = results[0].plot()
        # 保存结果图像
        cv2.imwrite(output_path, annotated_frame)
        print(f"图像检测完成！结果已保存至: {output_path}")
        # 显示结果图像
        cv2.imshow('YOLOv8 Image Detection', annotated_frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def detect_video(self, video_path, output_path='detected_video.avi', conf_threshold=0.5):
        """
        对视频文件进行目标检测
        """
        # 检查视频文件是否存在
        if not os.path.exists(video_path):
            print(f"错误：视频文件 '{video_path}' 不存在！")
            return

        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print("Error: 无法打开视频文件。")
            return

        # 获取视频信息
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        print("开始视频检测，按 'q' 键可中断...")
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            # 对当前帧进行推理
            results = self.model.predict(frame, conf=conf_threshold, verbose=False)
            annotated_frame = results[0].plot()
            # 写入输出视频
            out.write(annotated_frame)
            # 实时显示当前帧
            cv2.imshow('YOLOv8 Video Detection', annotated_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        out.release()
        cv2.destroyAllWindows()
        print(f"视频检测完成！结果已保存至: {output_path}")

    def detect_camera(self, camera_id=0, conf_threshold=0.5):
        """
        使用摄像头进行实时目标检测
        """
        cap = cv2.VideoCapture(camera_id)
        if not cap.isOpened():
            print("Error: 无法打开摄像头。请检查摄像头连接。")
            print("可以尝试不同的 camera_id：0（默认）, 1（外接摄像头）等")
            return

        print("开始摄像头实时检测，按 'ESC' 键退出...")
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("无法获取帧。")
                break
            # 推理当前帧
            results = self.model.predict(frame, conf=conf_threshold, verbose=False)
            annotated_frame = results[0].plot()
            cv2.imshow('YOLOv8 Real-Time Camera Detection', annotated_frame)
            # 按ESC键退出
            if cv2.waitKey(1) == 27:
                break

        cap.release()
        cv2.destroyAllWindows()
        print("摄像头检测结束。")


if __name__ == '__main__':
    # 初始化Demo
    demo = YOLOv8Demo(model_path='yolov8n.pt')

    # 创建测试图像（如果没有现成的图像文件）
    test_image_created = False
    if not os.path.exists('/Users/kaede/PycharmProjects/Pythons_pj/yolo8/test.jpg'):
        # 创建一个简单的测试图像
        import numpy as np

        test_img = np.ones((300, 400, 3), dtype=np.uint8) * 255  # 白色背景
        cv2.putText(test_img, 'YOLOv8 Test Image', (50, 150),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.imwrite('test_image.jpg', test_img)
        test_image_created = True
        print("已创建测试图像 'test_image.jpg'")

    print("\n" + "=" * 50)
    print("YOLOv8 Demo 使用说明")
    print("=" * 50)
    print("请选择要运行的功能：")
    print("1. 图像检测 (使用测试图像)")
    print("2. 视频检测 (需要提供视频文件路径)")
    print("3. 摄像头实时检测")
    print("4. 退出")

    choice = input("\n请输入选择 (1-4): ").strip()

    if choice == '1':
        # 图像检测
        image_path = '/Users/kaede/PycharmProjects/Pythons_pj/yolo8/test.jpg'
        if test_image_created:
            print(f"使用自动创建的测试图像: {image_path}")
        else:
            print(f"使用现有图像: {image_path}")
        demo.detect_image(image_path=image_path,
                          output_path='result_image.jpg',
                          conf_threshold=0.5)

    elif choice == '2':
        # 视频检测
        video_path = input("请输入视频文件路径 (或按回车跳过): ").strip()
        if not video_path:
            print("视频检测已跳过。")
        elif not os.path.exists(video_path):
            print(f"错误：文件 '{video_path}' 不存在！")
        else:
            demo.detect_video(video_path=video_path,
                              output_path='result_video.avi',
                              conf_threshold=0.5)

    elif choice == '3':
        # 摄像头检测
        camera_id = input("请输入摄像头ID (默认0，按回车使用默认): ").strip()
        if not camera_id:
            camera_id = 0
        else:
            camera_id = int(camera_id)
        demo.detect_camera(camera_id=camera_id, conf_threshold=0.5)

    elif choice == '4':
        print("程序退出。")

    else:
        print("无效选择，程序退出。")