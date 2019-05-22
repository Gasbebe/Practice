# Outlines Post processing(번역)

##### Summary

후처리를 통해 윤곽선 검출 방법,   외곽선을 계산할 방법은 렌더링 할 픽셀 주변의 여러 픽셀을 읽고 중심 픽셀의 깊이와 법선의 차이를 계산하는 것입니다. 그것들이 다를수록 윤곽이 강해집니다.

이웃하는 픽셀의 위치를 계산하기 위해 우리는 얼마나 큰 픽셀이 하나인지 알아야합니다. 다행히도 우리는 단순히 특정 이름의 변수를 추가 할 수 있으며, 단일성은 크기를 알려줍니다. 기술적으로 텍스쳐 픽셀을 다루기 때문에, **텍셀 화 (texelsize)**라고합니다.

어떤 텍스처에 대해서도 **texturename_TexelSize**라는 변수를 생성하고 크기를 구할 수 있습니다.

```c++
//깊이버퍼노말 노말텍스쳐
sampler2D _CameraDepthNormalsTexture;
//텍셀 화된 깊이버퍼노말 텍스쳐
float4 _CameraDepthNormalsTexture_TexelSize;
```

그런 다음 깊이와 법선에 액세스하는 코드를 복사하지만 이름을 변경하면 오른쪽으로 약간 텍스처에 액세스합니다.

```c++
//이웃한 픽셀값을 읽는다
float4 neighborDepthnormal = tex2D(_CameraDepthNormalsTexture, 
        uv + _CameraDepthNormalsTexture_TexelSize.xy * offset);
float3 neighborNormal;
float neighborDepth;
DecodeDepthNormal(neighborDepthnormal, neighborDepth, neighborNormal);
neighborDepth = neighborDepth * _ProjectionParams.z;
```

두개의 샘플의 차이를 계산하여 화면에 그릴수 있습니다

```c++
float difference = depth - neightborDepth;
return difference;
```

![img](https://www.ronja-tutorials.com/assets/images/posts/019/LeftWhite.png)

이 샘플을 통해 왼쪽의 오브젝트들의 윤곽선을 볼수 있습니다  이제 4방향을 구해야합니다



```c++
void Compare(float baseDepth, float2 uv, float2 offset){
    //read neighbor pixel
    float4 neighborDepthnormal = tex2D(_CameraDepthNormalsTexture, 
            uv + _CameraDepthNormalsTexture_TexelSize.xy * offset);
    float3 neighborNormal;
    float neighborDepth;
    DecodeDepthNormal(neighborDepthnormal, neighborDepth, neighborNormal);
    neighborDepth = neighborDepth * _ProjectionParams.z;

    return baseDepth - neighborDepth;
}
```

사용법

```c++
    float depthDifference = Compare(depth, i.uv, float2(1, 0));

    return depthDifference;
}
```

결과는 이전과 똑같이 보일 것입니다. 그러나 셰이더를 확장하여 샘플을 여러 방향으로 읽는 것이 더 쉽습니다. 따라서 픽셀을 샘플링하고 오른쪽에서 아래로 샘플링 한 다음 모든 샘플의 결과를 함께 추가합니다.

```c++
fixed4 frag(v2f i) : SV_TARGET{
    //read depthnormal
    float4 depthnormal = tex2D(_CameraDepthNormalsTexture, i.uv);

    //decode depthnormal
    float3 normal;
    float depth;
    DecodeDepthNormal(depthnormal, depth, normal);

    //get depth as distance from camera in units 
    depth = depth * _ProjectionParams.z;

    float depthDifference = Compare(depth, i.uv, float2(1, 0));
    depthDifference = depthDifference + Compare(depth, i.uv, float2(0, 1));
    depthDifference = depthDifference + Compare(depth, i.uv, float2(0, -1));
    depthDifference = depthDifference + Compare(depth, i.uv, float2(-1, 0));

    return depthDifference;
}
```

![img](https://www.ronja-tutorials.com/assets/images/posts/019/DepthOutlines.png)



법선에서 윤곽선을 생성

```c++
void Compare(inout float depthOutline, inout float normalOutline, 
    float baseDepth, float3 baseNormal, float2 uv, float2 offset){
```

```c++
void Compare(inout float depthOutline, inout float normalOutline, 
        float baseDepth, float3 baseNormal, float2 uv, float2 offset){
    //read neighbor pixel
    float4 neighborDepthnormal = tex2D(_CameraDepthNormalsTexture, 
            uv + _CameraDepthNormalsTexture_TexelSize.xy * offset);
    float3 neighborNormal;
    float neighborDepth;
    DecodeDepthNormal(neighborDepthnormal, neighborDepth, neighborNormal);
    neighborDepth = neighborDepth * _ProjectionParams.z;

    float depthDifference = baseDepth - neighborDepth;
    depthOutline = depthOutline + depthDifference;
}
```

```c++
float depthDifference = 0;
float normalDifference = 0;

Compare(depthDifference, normalDifference, depth, normal, i.uv, float2(1, 0));
Compare(depthDifference, normalDifference, depth, normal, i.uv, float2(0, 1));
Compare(depthDifference, normalDifference, depth, normal, i.uv, float2(0, -1));
Compare(depthDifference, normalDifference, depth, normal, i.uv, float2(-1, 0));

return depthDifference;
```



<https://www.ronja-tutorials.com/>

