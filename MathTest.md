---
layout: post
title: "선형대수학"
description: 선형대수학
image: '\images\bg.jpg'
category: 'Unity3D'
tag:
 - Unity3D
introduction: 쉽게 풀어쓴 선형대수학
---

##### Math

$$
\begin{bmatrix}
0 & 0 & 0 \\\
0 & 0 & 0 \\\
0 & 0 & 0
\end{bmatrix}
$$

##### scale

$$
\begin{bmatrix}
S_x & 0 & 0 \\\
0 & S_y & 0 \\\
0 & 0 & S_z
\end{bmatrix}
\begin{bmatrix}
x \\\
y \\\
z
\end{bmatrix}
$$



##### move

$$
\begin{bmatrix}
1 & 0 & 0 & d_x \\\
0 & 1 & 0 & d_y \\\
0 & 0 & 1 & d_z \\\
0 & 0 & 0 & 1
\end{bmatrix}

\begin{bmatrix}
x\\\
y\\\
z \\\
1
\end{bmatrix}
$$



##### rotation pitch(x axis), yaw(y axis),  roll(z axis)


$$
\begin{bmatrix}
1 & 0 & 0 & 0 \\\
0 & cos\theta & -sin\theta & 0 \\\
0 & sin\theta & cos\theta & 0 \\\
0 & 0 & 0 & 1
\end{bmatrix}

\begin{bmatrix}
cos\theta & 0 & sin\theta & 0 \\\
0 & 1 & 0 & 0 \\\
-sin\theta & 0 & cos\theta & 0 \\\
0 & 0 & 0 & 1
\end{bmatrix}

\begin{bmatrix}
cos\theta & -sin\theta & 0 & 0 \\\
sin\theta & cos\theta & 0 & 0 \\\
0 & 0 & 1 & 0 \\\
0 & 0 & 0 & 1
\end{bmatrix}
$$


------







 n = normal, l = light vector, h = half vector, v = view
$$
f(l.v) = {F(v,h)G(l,v,h)D(h)\over4(n \cdot l)(n \cdot v))}
$$



https://datastory1.blogspot.com/2017/11/r-markdown_2.html

숫자가 아닐떄 True, 

```c++
bool linesegment_vs_plane(float3 p0, float3 p1, float3 pn, out float lerp_val)
{
    float3 u = p1 - p0;
    float D = dot(pn, u);
    float N = -dot(pn, p0);
    
    lerp_val = N / D;
    return !(lerp_val != saturate(lerp_val));
}
```

D = Direction
$$
D = {ax_1 + by_1 + cz_1 + d \over \sqrt {a^2 + b^2 + c^2}}
$$
consider : 고려하다  considered : 깊이생각한
assignment : 할당
representation : 1. (특정한 방식으로의) 묘사, (어떤 것을) 나타낸 것   2. 대표자를 내세움, 대의권
intrinsic :본질적인, 고유한


$$
tan\theta = 기울기 \; 
\theta = arcsin\ y \; 
\theta = arccos \ y \; 
\theta = arctan\ y
$$







