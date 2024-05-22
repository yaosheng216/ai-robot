import torch
import numpy as np

scaler = torch.tensor(7)
print(scaler)

randon_tensor = torch.rand(size = (3, 4))

# 创建一个0到10的张量
zero_to_ten = torch.arange(start=0, end=10, step=1)
# 创建一个零张量，与另一个张量的形状一样
ten_zeros = torch.zeros_like(input=zero_to_ten)

tensor = torch.tensor([1, 2, 3, 4, 5])
tensor.shape
# 逐元素矩阵乘法
tensor * tensor
# 矩阵乘法
torch.matmul(tensor, tensor)


array = np.arange(1.0, 8.0)
tensor = torch.from_numpy(array)
array, tensor
