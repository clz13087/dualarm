import soundfile as sf
import numpy as np
from scipy.fft import rfft, irfft
import scipy.signal as sg
import pysofaconventions
from resampy import resample

# パラメータ
wav_name  = "input.wav"            # 読み込むWAVデータの名前
out_name  = "output.wav"           # 出力するWAVデータの名前
sofa_name = 'Subject1_HRIRs.sofa'  # SOFAの名前
elev = 0         # 仰角
N    = 2048      # HRTFの点数
chg_len = 128    # HRTFを変える間隔
omega   = 90     # 角速度 [deg/s]

# WAVファイルを読み込む
x, fs = sf.read(wav_name)
x_len = len(x)

# 方位角0°～355°のHRIRを読み込む
##  SOFAFileオブジェクトを読み込む
sofa = pysofaconventions.SOFAFile(sofa_name, 'r')

## サンプリング周波数を確認
sofa_fs = sofa.getVariableValue('Data.SamplingRate')

## WAVファイルをリサンプリング
x = resample(x, fs, sofa_fs[0])

## HRIR を抽出
hrir_all = sofa.getDataIR().data

## 仰角0度,距離0.76mのIRデータを抜き出す
sourcePositions = sofa.getVariableValue('SourcePosition')
hrir_l = np.zeros((72, N))
hrir_r = np.zeros((72, N))
for i, angle in enumerate(range(0,360,5)):
    index = np.where(np.logical_and(sourcePositions[:,0]==angle, sourcePositions[:,1] == elev, sourcePositions[:,2] == 0.76))[0]
    hrir = np.squeeze(hrir_all[index])
    hrir_l[i,:] = hrir[0]
    hrir_r[i,:] = hrir[1] 

# FFT をして HRTF 作成
HRTF_L = np.zeros((72, N+1), dtype=np.complex128)
HRTF_R = np.zeros((72, N+1), dtype=np.complex128)
for m in range(72):
    h = np.pad(hrir_l[m,:], [0,N], 'constant')  # 0埋め
    HRTF_L[m,:] = rfft(h)
    h = np.pad(hrir_r[m,:], [0,N], 'constant')  # 0埋め
    HRTF_R[m,:] = rfft(h)

# 変数を初期化
n_frame = len(x) // chg_len + 1  # フレーム数
x = np.pad(x, [0,2*N])
y = np.zeros((len(x), 2))

# フレームごとに異なるHRTFを掛ける
for i in range(n_frame):

    # 移動音源がどの角度にあるか計算
    theta = omega * i * chg_len / fs
    while int(theta) > 359:   # 0<theta<360にする
        theta = theta - 360

    # HRTFを線形2点補間するためのパラメータを求める
    m = theta / 5
    m1 = int(m)
    m2 = m1 + 1
    if m2 == 72:
        m2 = 0
    r2 = m - int(m)
    r1 = 1.0 - r2

    # 取り出した x を FFT する
    x_N = np.pad(x[i*chg_len:i*chg_len+N], [0,N], 'constant') # 0埋め
    X = rfft(x_N)

    # 補間したHRTF と X を掛ける
    YL = X * (r1*HRTF_L[m1,:]+r2*HRTF_L[m2,:])
    YR = X * (r1*HRTF_R[m1,:]+r2*HRTF_R[m2,:])

    # 逆FFT をして足し合わせる
    y[i*chg_len:i*chg_len+2*N, 0] += irfft(YL)
    y[i*chg_len:i*chg_len+2*N, 1] += irfft(YR)

# ファイルに書き込む
if np.max(np.abs(y)) > 1: 
    y = y/np.max(y)   # ノーマライズ
y = resample(y, sofa_fs[0], fs, axis=0)
sf.write(out_name, y[:x_len,:], fs, subtype="PCM_16")
