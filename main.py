import cv2
import pandas as pd

import tkinter as tk
from PIL import Image, ImageTk
import argparse
import os


DATASET_PATH = 'dataset/image'
LABEL_PATH = 'dataset/label'



def create_gaze_point(canvas, x, y):
    radius = 10
    return canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill='red')

def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--personID','-P', required=True, type=int, help='撮影する人のID')
    args = parser.parse_args()
    
    
    personID = args.personID
    
    output_path = f'{DATASET_PATH}/p{personID}'
    if not os.path.exists(output_path):
        os.makedirs(output_path)
        print(f"Created directory: {output_path}")
    
    
    
    
    
    
    window = tk.Tk()
    window.attributes('-fullscreen', True)  # フルスクリーンモード

    # キャンバスの作成
    canvas = tk.Canvas(window, bg='black')
    canvas.pack(fill=tk.BOTH, expand=True)
    
    
    # カメラの設定
    cap = cv2.VideoCapture(2)
    cap15 = cv2.VideoCapture(0)

    # 注視点の座標
    gaze_points = [(100, 150), (200, 150), (150, 100), (150, 200)]
    # データセットのリスト
    dataset = []
    dataset15 = []


    for idx, point in enumerate(gaze_points):
        create_gaze_point(canvas, *point)
        input("Press Enter to capture when looking at point {}: ".format(point))
        ret, frame = cap.read()
        if not ret:
            break
        else:
            filename = f'image_{idx}.png'
            cv2.imwrite(f'{output_path}/{filename}', frame)
            dataset.append({'image': filename, 'gaze_point': point})

        ret15, frame15 = cap15.read()
        if not ret15:
            break
        else:
            filename15 = f'image_{idx}_15.png'
            cv2.imwrite(f'{output_path}/{filename15}', frame15)
            dataset15.append({'image': filename15, 'gaze_point': point})
        

        # # 'q'キーでプログラムを終了
        # window.bind('<q>', lambda e: window.destroy())

        # window.mainloop()
        
    # データセットをDataFrameにしてCSVで保存
    df = pd.DataFrame(dataset)
    df.to_csv(f'{LABEL_PATH}/p{personID}_label.csv', index=False)

    # カメラのリリース
    cap.release()

if __name__ == '__main__':
    main()




