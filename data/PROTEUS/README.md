# PROTEUS：兼容 Scherer 格式的 MAT 数据

源数据：`assets/PROTEUS/nm000290_v1.0.0`，PROTEUS BCI Bordeaux v1.0.0，
DOI `10.82901/nemar.nm000290`，CC BY 4.0。作者和原始数据集说明保存在
`conversion_manifest.json` 的 `dataset` 字段中。

## 文件与分组

- `P01.mat` 至 `P10.mat`：每名被试一个 MAT 文件。
- 顶层变量 `data` 是 MATLAB 的 `1 × N` cell，与 `data/Scherer_2015/A.mat` 的容器形式相同。
- **一个独立 EDF run 对应一个 cell**，不拼接不同记录。
- P04、P10 各有 24 个单元，其余被试各有 8 个，共 112 个单元；原始实验共 14 次。
- 排序依据：原始 session 数字、run 数字；两个 run-0 基线固定为睁眼 OE、闭眼 CE。
  原始 EDF 测量日期已匿名化，无法从日期判断两个基线的真实先后，因此此顺序只用于稳定编号。
- `session` 为每名被试内部从 1 开始的**处理单元编号**，不是原始 BIDS session。
  原始实验编号、run 编号、任务名分别保存在 `original_session`、`run`、`task`。
- `conversion_manifest.json` 逐条列出文件来源、MAT 索引、现有主流程生成的 Raw 字典键、试次数与填充区间。

## 与现有读取函数一致的六个字段

| 字段 | 保存形式与含义 |
| --- | --- |
| `X` | `采样点 × 41 通道`，float32，单位 **µV** |
| `y` | 每个任务提示对应一个类别编号；uint8 |
| `trial` | 任务提示的采样点，**从 1 开始**；int32 |
| `fs` | 500 Hz，保留原始采样率 |
| `classes` | `['HAND', 'SUB', 'WORD']`，依次对应 y=1、2、3 |
| `session` | 该被试内从 1 开始的处理单元编号 |

类别映射：`mi → 1/HAND`（非优势手动觉运动想象）、`sub → 2/SUB`（心算减法）、
`word → 3/WORD`（词语生成）。此数据只有三类，**不能直接套用 Scherer 的五类标签编号**。

`trial` 对齐 BIDS 事件表中 `mi` / `sub` / `word` 的 `sample + 1`，即任务提示开始，
不是 `start_trial`、注视十字或反馈开始。全部 2,655 个提示的标注时长均为 8 秒。
类别数分别为 HAND=885、SUB=886、WORD=884。

保留 AcquisitionGraz/BH、OnlineRawGraz/BH，以及 BaselineOE/CE 的全部记录。
基线没有这三类任务，因此它们的 `y` 和 `trial` 都是空数组；做有监督分类时应跳过这些单元。
部分任务 run 的试次数不足，保留实际数据，不补造、截齐或丢弃试次。

## 保留的原始信息

每个单元还包含：`ch_names`、`ch_types`、`units`、`original_session`、`run`、`task`、
`source_file`、`reference`、`ground`、`events` 和 `annotations`。

- `events` 保留 TSV 的所有事件类型与代码；其中 `sample` 同样转换为从 1 开始，
  `onset` 和 `duration` 保持原始秒数。源 TSV 的 sample 则从 0 开始。
- `annotations` 保留 EDF 注释，包括每个 run 最后不足 1 秒的 `BAD_ACQ_SKIP` 填充区。
  全部 EDF 采样点均保留，未把末尾填充误当作跨 run 缺口。
- 未做滤波、重采样、插值、重参考、裁剪、归一化或通道重排。
- MNE 按每个 EDF 的 physical/digital scaling 解码后，以 µV 保存；保留 M1 参考。
- float32 与现有 `_read_mat` 最终采用的精度一致；相对于 EDF 解码出的 float64 有一次 float32 舍入。
- **现有 `build_valid_raw` 只使用 X 和显式传入的通道/采样率/布局参数，
  不会自动把 MAT 中的 `annotations`、`events` 或参考信息加到 Raw.info。**
  这些信息保存在 MAT 中供后续需要时使用，原有读取代码无需更改。

## 在 Preprocessing.py 中使用

`preprocessing_config.py` 提供完整的 PROTEUS 参数。需要使用：

```python
subjects = ['P01', 'P02', 'P03', 'P04', 'P05', 'P06', 'P07', 'P08', 'P09', 'P10']
data_folder = Path('./data/PROTEUS')
sfreq = 500
ch_types = ['eeg'] * 41
montage_name = 'colin27_1005'
# ch_names 必须使用 preprocessing_config.py 中的原始 41 通道顺序。
```

保留现有 `_read_mat(..., convert_index=True, convert_shape=True, scale_factor=1e-6)`：
结果将是 `41 × 采样点`、单位 V，trial 从 0 开始。41 个通道均可匹配当前 `colin27_1005` 布局。
**不能继续使用 Scherer 的 30 个通道名或 256 Hz。**

可从项目根目录直接验证读取和建立 Raw：

```python
import runpy
from src.Preprocessing import _read_mat, build_valid_raw

cfg = runpy.run_path('data/PROTEUS/preprocessing_config.py')
data = _read_mat(
    data_folder=cfg['data_folder'],
    subjects=['P01'],  # 可换成 cfg['subjects'] 读取全部被试
    convert_index=True, convert_shape=True, scale_factor=1e-6,
)
raws = build_valid_raw(
    data_dic=data, ch_names=cfg['ch_names'], ch_types=cfg['ch_types'],
    sfreq=cfg['sfreq'], montage_name=cfg['montage_name'],
)
```

使用主流程时，将以上参数应用到主脚本对应设置，并为 PROTEUS 使用独立缓存与结果目录，
从 `is_load_cached_mat` 开始。主脚本仍保持原样，本次转换没有修改它。
Scherer 的人工坏道 JSON 和 ICA 索引不适用于 PROTEUS；选择自动坏道检测，
需要人工剔除 ICA 成分时应另建该数据的标注。

## 复现与校验

转换脚本：`assets/convert_proteus_to_mat.py`。

```powershell
.\.venv\Scripts\python.exe assets/convert_proteus_to_mat.py
```

为保护已有输出，文件存在时会停止；明确需要重做时添加 `--overwrite`。

`validation_report.json` 记录转换后的校验：112 个单元全部通过现有 `_read_mat` 读取；
核对形状、类型、通道、标签、trial 与事件索引；每条记录的开始/中间/末尾各 8 个采样点，
逐通道与源 EDF 解码值比较；每条记录取短片段通过现有 `build_valid_raw` 和 montage 建立。
未运行坏道检测或 ICA，也未改动已有预处理缓存。
