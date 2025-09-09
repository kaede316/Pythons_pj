# -*- coding: utf-8 -*-
import cv2
from ultralytics import YOLO
import os
import sys


class YOLOv8Demo:
    def __init__(self, model_path='yolov8n.pt'):
        """
        初始化YOLOv8模型
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
        if not os.path.exists(image_path):
            print(f"错误：图像文件 '{image_path}' 不存在！")
            return False

        try:
            # 执行预测
            results = self.model.predict(source=image_path, conf=conf_threshold, save=False)
            # 获取带标注的结果图像
            annotated_frame = results[0].plot()
            # 保存结果图像
            cv2.imwrite(output_path, annotated_frame)
            print(f"✅ 图像检测完成！结果已保存至: {output_path}")

            # 显示结果图像
            cv2.imshow('YOLOv8 Image Detection', annotated_frame)
            print("按任意键关闭图像窗口...")
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            return True

        except Exception as e:
            print(f"❌ 图像检测失败: {e}")
            return False

    def detect_video(self, video_path, output_path='detected_video.avi', conf_threshold=0.5):
        """
        对视频文件进行目标检测
        """
        if not os.path.exists(video_path):
            print(f"❌ 错误：视频文件 '{video_path}' 不存在！")
            return False

        try:
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                print("❌ 无法打开视频文件。")
                return False

            # 获取视频信息
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

            print("🎥 开始视频检测，按 'q' 键可中断...")
            frame_count = 0

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
                frame_count += 1

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            cap.release()
            out.release()
            cv2.destroyAllWindows()
            print(f"✅ 视频检测完成！处理了 {frame_count} 帧，结果已保存至: {output_path}")
            return True

        except Exception as e:
            print(f"❌ 视频检测失败: {e}")
            return False

    def detect_camera(self, camera_id=0, conf_threshold=0.5):
        """
        使用摄像头进行实时目标检测
        """
        # 先测试摄像头是否可用
        if not self.test_camera(camera_id):
            print(f"❌ 摄像头 {camera_id} 不可用，尝试自动检测可用摄像头...")
            available_cam = self.find_available_camera()
            if available_cam is not None:
                print(f"🔍 发现可用摄像头: ID {available_cam}")
                camera_id = available_cam
            else:
                print("❌ 未找到任何可用的摄像头！")
                return False

        try:
            cap = cv2.VideoCapture(camera_id)
            if not cap.isOpened():
                print(f"❌ 无法打开摄像头 {camera_id}")
                return False

            print(f"📷 开始摄像头 {camera_id} 实时检测，按 'ESC' 键退出...")
            print("💡 提示：确保摄像头没有被其他程序占用")

            frame_count = 0
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    print("❌ 无法获取视频帧")
                    break

                # 推理当前帧
                results = self.model.predict(frame, conf=conf_threshold, verbose=False)
                annotated_frame = results[0].plot()

                # 显示帧率信息
                fps_text = f"FPS: {int(cap.get(cv2.CAP_PROP_FPS))} | Frame: {frame_count}"
                cv2.putText(annotated_frame, fps_text, (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                cv2.imshow(f'YOLOv8 Camera {camera_id}', annotated_frame)
                frame_count += 1

                # 按ESC键退出
                if cv2.waitKey(1) == 27:
                    break

            cap.release()
            cv2.destroyAllWindows()
            print(f"✅ 摄像头检测结束，共处理 {frame_count} 帧")
            return True

        except Exception as e:
            print(f"❌ 摄像头检测失败: {e}")
            return False

    def test_camera(self, camera_id):
        """测试摄像头是否可用"""
        cap = cv2.VideoCapture(camera_id)
        if cap.isOpened():
            ret, frame = cap.read()
            cap.release()
            return ret
        return False

    def find_available_camera(self):
        """自动检测可用的摄像头"""
        print("🔍 正在扫描可用摄像头...")
        for i in range(0, 5):  # 检查前5个摄像头设备
            if self.test_camera(i):
                print(f"  摄像头 {i}: ✅ 可用")
                return i
            else:
                print(f"  摄像头 {i}: ❌ 不可用")
        return None

    def list_available_cameras(self):
        """列出所有可用的摄像头"""
        print("📋 可用摄像头列表:")
        available_cams = []
        for i in range(0, 5):
            if self.test_camera(i):
                print(f"  📷 摄像头 ID {i}: ✅ 可用")
                available_cams.append(i)
            else:
                print(f"  📷 摄像头 ID {i}: ❌ 不可用")
        return available_cams


def create_test_image():
    """创建测试图像"""
    import numpy as np
    test_img = np.ones((400, 600, 3), dtype=np.uint8) * 255  # 白色背景

    # 添加一些测试图形
    cv2.rectangle(test_img, (100, 100), (200, 200), (255, 0, 0), -1)  # 蓝色矩形
    cv2.circle(test_img, (400, 200), 50, (0, 255, 0), -1)  # 绿色圆形
    cv2.putText(test_img, 'YOLOv8 Test Image', (150, 350),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imwrite('test_image.jpg', test_img)
    return 'test_image.jpg'


if __name__ == '__main__':
    # 初始化Demo
    demo = YOLOv8Demo(model_path='yolov8n.pt')

    # 创建测试图像
    test_image_path = create_test_image()
    print(f"📸 已创建测试图像: {test_image_path}")

    while True:
        print("\n" + "=" * 60)
        print("🎯 YOLOv8 Demo 功能菜单")
        print("=" * 60)
        print("1. 📷 图像检测 (使用测试图像)")
        print("2. 🎥 视频检测 (需要提供视频文件路径)")
        print("3. 📹 摄像头实时检测")
        print("4. 🔍 查看可用摄像头")
        print("5. ❌ 退出程序")
        print("=" * 60)

        choice = input("\n请输入选择 (1-5): ").strip()

        if choice == '1':
            # 图像检测
            demo.detect_image(image_path=test_image_path,
                              output_path='result_image.jpg',
                              conf_threshold=0.5)

        elif choice == '2':
            # 视频检测
            video_path = input("请输入视频文件路径 (或输入 'test' 使用示例视频): ").strip()
            if video_path.lower() == 'test':
                print("❌ 请提供您自己的视频文件路径")
                print("💡 提示：您可以从网上下载一个测试视频，或使用手机拍摄")
            else:
                demo.detect_video(video_path=video_path,
                                  output_path='result_video.avi',
                                  conf_threshold=0.5)

        elif choice == '3':
            # 摄像头检测
            demo.list_available_cameras()
            camera_input = input("请输入摄像头ID (直接回车使用自动检测): ").strip()

            if camera_input:
                try:
                    camera_id = int(camera_input)
                    demo.detect_camera(camera_id=camera_id, conf_threshold=0.5)
                except ValueError:
                    print("❌ 请输入有效的数字")
            else:
                demo.detect_camera(conf_threshold=0.5)

        elif choice == '4':
            # 查看可用摄像头
            demo.list_available_cameras()

        elif choice == '5':
            print("👋 程序退出，感谢使用！")
            break

        else:
            print("❌ 无效选择，请重新输入")

        # 暂停一下让用户看到结果
        input("\n按回车键继续...")

    # 清理临时文件
    if os.path.exists('test_image.jpg'):
        os.remove('test_image.jpg')
        print("🧹 已清理临时文件")