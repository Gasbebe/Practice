```c++
struct VS_INPUT{
    float4 Pos : POSITION;
    float4 normal : NORMAL;
    float2 UV : TEXCOORD0;
}

struct VS_OUTPUT{
    float4 Pos : SV_POSITION;
    float4 normal : NORMAL;
    float2 UV : TEXCOORD0;
}

VS_OUTPUT RenderSceneVS(VS_INPUT IN){
    VS_OUTPUT Output;
    
    Output.Pos = mul(IN.Pos, WorldViewProj);
    
    Output.UV = input.TextureUV;
    
    Ouput.normal = mul(IN.normal, (float3x3)World);
    
    return Output;
}
```

