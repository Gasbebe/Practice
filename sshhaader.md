# Surface Shader 정리

### 버텍스 컬러 받아오기

1. struct 데이터에 Color:COLOR;
2. surface 데이터에 IN.Color;



------



### 페러렉스 데이터

![img](https://lh6.googleusercontent.com/PvSUSr_d1wQX-_8lVmJ9AyVYwsmYR6E5PeQU70AVtBjtY1KyEjEtml1wgRkgeSGsFjAPgXeSOiHgsLvYJrnabfXhBolzXCCxtjprdSBn_0UAEuA7rUmCt4cvt8PT_S6XUfC8K3jk)

float2 offset = ParallaxOffset((h * 1 + 0.25), _Parallax, IN.viewDir);

fixed4 c = tex2D (_MainTex, IN.uv_MainTex + offset) * _Color;



------



### 리플렉션 프로브 데이터

![img](https://lh5.googleusercontent.com/qhL-Fx03cpzJ1HRAIqslGswqyk5TeiV4chWih_LO8t9S2cN4mGrYaAsKw_UfE5MR23B7qV1qBXzbyGFDhEd0azpW_cEHrujtSk5Z23eePbdOyb3n2kooaRyjyYZb90370bhL-dM-)![img](https://lh4.googleusercontent.com/F2ViE1tYuNuaNpO5McHN5__S2gLkTR8RvhOepFPBWh_ut9q0LsvUikwc2LphoZLauT9hVCaA87Bh0a0Z6_pZfXFVERyzNHyz3-piFLXwPajrtjPqsbj-q9eqh6toF63f_8TCyu3U)

```c++
Shader "Ageia/SimpleReflectionProbe" {

	Properties {

		_Color ("Color", Color) = (1,1,1,1)

		_MainTex ("Albedo (RGB)", 2D) = "white" {}

		[Normal]_Normal("Normal", 2D) = "bump"{}

		_NormalPow("NormalPow", Range(0, 3)) = 1

		_Metallic("Metallic", Range(0, 1)) = 1

	}

	SubShader {

		Tags { "RenderType"="Opaque" }

		LOD 200

		CGPROGRAM

		// Physically based Standard lighting model, and enable shadows on all light types

		#pragma surface surf CumstomLighing fullforwardshadows

		// Use shader model 3.0 target, to get nicer looking lighting

		#pragma target 3.0

		sampler2D _MainTex;

		sampler2D _Normal;

		struct Input {

			float2 uv_MainTex;

			half2 uv_Normal;

			half3 viewDir;

			half3 worldRefl; //WorldReflectionVector 데이터에 사용됩니다.

			INTERNAL_DATA

			//worldRefl 데이터를 가져오기 위해 해당 데이터 구조를 필요로 함.

		};

		fixed4 _Color;

		half _NormalPow;

		half _NormalPow2;

		half _Metallic;

		// Add instancing support for this shader. You need to check 'Enable Instancing' on materials that use the shader.

		// See https://docs.unity3d.com/Manual/GPUInstancing.html for more information about instancing.

		// #pragma instancing_options assumeuniformscaling

		UNITY_INSTANCING_BUFFER_START(Props)

			// put more per-instance properties here

		UNITY_INSTANCING_BUFFER_END(Props)

		void surf (Input IN, inout SurfaceOutput o) {

			half3 NormalTest = UnpackNormal(tex2D(_Normal, IN.uv_Normal));

			o.Normal = lerp(o.Normal, NormalTest, _NormalPow);

			//simpleReflectionMap

			half3 Reflection1 = UNITY_SAMPLE_TEXCUBE(unity_SpecCube0, WorldReflectionVector(IN, o.Normal)) * unity_SpecCube0_HDR.r;

			//unity_SpecCube0_HDR.r : 리플렉션 큐브의 Intensity값.

			half3 Reflection2 = UNITY_SAMPLE_TEXCUBE_SAMPLER(unity_SpecCube1, unity_SpecCube0, WorldReflectionVector(IN, o.Normal)) * unity_SpecCube0_HDR.r;

			//Reflection2는 다른 리플렉션 프로브와의 보간을 처리합니다. 필요없는 경우 제거 하십시오.

			half3 ReflectionFinal = lerp(Reflection2, Reflection1, unity_SpecCube0_BoxMax.w * unity_SpecCube0_BoxMin.w);

			//unity_SpecCube0_BoxMin.w : 두개의 리플렉션 프로브를 보간합니다.

			fixed4 c = tex2D (_MainTex, IN.uv_MainTex) * _Color;

			o.Albedo = lerp(c.rgb, 0, _Metallic);

			//o.Emission = pow(NdotV * 0.5 + 0.5, 20);

			o.Emission = lerp(0, ReflectionFinal, _Metallic);

			o.Alpha = c.a;

		}

		half4 LightingCumstomLighing(SurfaceOutput s, half3 lightDir, half atten)

		{

			half4 c;

			c.rgb = s.Albedo;

			c.a = s.Alpha;

			return c;

		}

		ENDCG

	}

	FallBack "Diffuse"

}



------



### 빌보드 쉐이더

Shader "Ageia/Bilboard" {

	Properties{

		_Color("Color", Color) = (1,1,1,1)

		_MainTex("Albedo (RGB)", 2D) = "white" {}

		_Glossiness("Smoothness", Range(0,1)) = 0.5

		_Metallic("Metallic", Range(0,1)) = 0.0

	}

		SubShader{

		Tags{ "Queue" = "Transparent" "RenderType" = "Transparent" "DisableBatching" = "True" }

		LOD 200

		CGPROGRAM

\#pragma surface surf Standard fullforwardshadows vertex:vert alpha:fade

		sampler2D _MainTex;

	struct Input {

		float2 uv_MainTex;

	};

	half _Glossiness;

	half _Metallic;

	fixed4 _Color;

	void vert(inout appdata_full v, out Input o)

	{

		UNITY_INITIALIZE_OUTPUT(Input, o);

		// apply object scale

		v.vertex.xy *= float2(length(unity_ObjectToWorld._m00_m10_m20), length(unity_ObjectToWorld._m01_m11_m21));

		// get the camera basis vectors

		float3 forward = -normalize(UNITY_MATRIX_V._m20_m21_m22);

		float3 up = normalize(UNITY_MATRIX_V._m10_m11_m12);

		float3 right = normalize(UNITY_MATRIX_V._m00_m01_m02);

		// rotate to face camera

		float4x4 rotationMatrix = float4x4(right, 0,

			up, 0,

			forward, 0,

			0, 0, 0, 1);

		v.vertex = mul(v.vertex, rotationMatrix);

		v.normal = mul(v.normal, rotationMatrix);

		// undo object to world transform surface shader will apply

		v.vertex.xyz = mul((float3x3)unity_WorldToObject, v.vertex.xyz);

		v.normal = mul(v.normal, (float3x3)unity_ObjectToWorld);

	}

	void surf(Input IN, inout SurfaceOutputStandard o) {

		// Albedo comes from a texture tinted by color

		fixed4 c = tex2D(_MainTex, IN.uv_MainTex) * _Color;

		o.Albedo = c.rgb;

		// Metallic and smoothness come from slider variables

		o.Metallic = _Metallic;

		o.Smoothness = _Glossiness;

		o.Alpha = c.a;

	}

	ENDCG

	}

		FallBack "Transparent/VertexLit"

}


```



------



### ReflectionCube Color

o.Albedo = UNITY_SAMPLE_TEXCUBE(unity_SpecCube0, o.Normal);

### 

### 쉐이더 전처리 사용

```c++
Shader "Custom/VariantsTest" {

	Properties{

		_Color("Color", Color) = (1,1,1,1)

		_MainTex("Albedo (RGB)", 2D) = "white" {}

		_Glossiness("Smoothness", Range(0,1)) = 0.5

		_Metallic("Metallic", Range(0,1)) = 0.0

		[KeywordEnum(Color, Red, Greed, Blue)]

		_CHANGECOLOR("ChangeColor", float) = 0

		[Header(Normal)]

		[Toggle]_USENORMAL("Use Normal?", float) = 0

		[Normal]_Normal("Normal", 2D) = "bump" {}

	}

		SubShader{

		Tags{ "RenderType" = "Opaque" }

		LOD 200

		CGPROGRAM

		// Physically based Standard lighting model, and enable shadows on all light types

		#pragma surface surf Standard fullforwardshadows

		#pragma multi_compile _CHANGECOLOR_COLOR _CHANGECOLOR_RED _CHANGECOLOR_GREEN _CHANGECOLOR_BLUE

		#pragma multi_compile _USENORMAL_OFF _USENORMAL_ON

		#pragma shader_feature _USENORMAL_OFF _USENORMAL_ON

		//multi_compile은 큰 단위로 빌드 할 때 사용하지 않는 데이터도 포함하여 빌드함.

		//shader_feature은 더 작은 단위로 빌드할 때 사용하지 않는 데이터를 포함하지 않음.

		// Use shader model 3.0 target, to get nicer looking lighting

		#pragma target 2.0

		sampler2D _MainTex;

		//노멀

		#if _USENORMAL_ON

		sampler2D _Normal;

		#endif

	struct Input {

		float2 uv_MainTex;

		//노멀

		#if _USENORMAL_ON

		fixed2 uv_Normal;

		#endif

	};

	half _Glossiness;

	half _Metallic;

	fixed4 _Color;

	// Add instancing support for this shader. You need to check 'Enable Instancing' on materials that use the shader.

	// See https://docs.unity3d.com/Manual/GPUInstancing.html for more information about instancing.

	// #pragma instancing_options assumeuniformscaling

	UNITY_INSTANCING_BUFFER_START(Props)

		// put more per-instance properties here

		UNITY_INSTANCING_BUFFER_END(Props)

		void surf(Input IN, inout SurfaceOutputStandard o) {

		fixed4 c = tex2D(_MainTex, IN.uv_MainTex) * _Color;

		#if _CHANGECOLOR_COLOR

		o.Albedo = _Color;

		#elif	_CHANGECOLOR_RED

		o.Albedo = fixed3(1, 0, 0);

		#elif	_CHANGECOLOR_GREEN

		o.Albedo = fixed3(0, 1, 0);

		#elif	_CHANGECOLOR_BLUE

		o.Albedo = fixed3(0, 0, 1);

		#endif

		//노멀맵 사용

\#if _USENORMAL_ON

		o.Normal = UnpackNormal(tex2D(_Normal, IN.uv_Normal));

\#endif

		o.Metallic = _Metallic;

		o.Smoothness = _Glossiness;

		o.Alpha = c.a;

	}

	ENDCG

	}

		FallBack "Diffuse"

}
```



### 

### 버텍스 로컬좌표 이동 (Vertex Move Local Position)

![img](https://lh3.googleusercontent.com/nW2QW3F5It-Mu5bTO2unOQrbV3ERLw2PPBOaB5ParO2540QLBXvMSoBq5cP4jxB8d64RjdMmqN5WcL2X-fOvy2QJJX_0VUt5wxHh4RuVE0XoFO4hhwnPGDVDC6dKOOpNZlo9qDA5)

// Upgrade NOTE: replaced 'mul(UNITY_MATRIX_MVP,*)' with 'UnityObjectToClipPos(*)'

```c++
Shader "Custom/LocalPosition" {

	Properties {

		_Color ("Color", Color) = (1,1,1,1)

		_MainTex ("Albedo (RGB)", 2D) = "white" {}

		_Glossiness ("Smoothness", Range(0,1)) = 0.5

		_Metallic ("Metallic", Range(0,1)) = 0.0

		_Amount("Amount", Range(0, 1)) = 0

		//_Amount2("Amount2", Range(0, 1)) = 0

		_VectorTest("VectorTest", Vector) = (0, 0, 0, 0)

		_NoiseTex("NoiseTex", 2D) = "white" {}

	}

	SubShader {

		Tags { "RenderType"="Opaque"}

		LOD 200

		CGPROGRAM

		// Physically based Standard lighting model, and enable shadows on all light types

		#pragma surface surf Standard vertex:vert

		// Use shader model 3.0 target, to get nicer looking lighting

		#pragma target 3.0

		sampler2D _MainTex;

		sampler2D _GrabTexture;

		sampler2D _NoiseTex;

		struct Input {

			float2 uv_MainTex;

		};

		half _Glossiness;

		half _Metallic;

		fixed4 _Color;

		fixed _Amount;

		//fixed _Amount2;

		fixed4 _VectorTest;

		// Add instancing support for this shader. You need to check 'Enable Instancing' on materials that use the shader.

		// See https://docs.unity3d.com/Manual/GPUInstancing.html for more information about instancing.

		// #pragma instancing_options assumeuniformscaling

		UNITY_INSTANCING_BUFFER_START(Props)

			// put more per-instance properties here

		UNITY_INSTANCING_BUFFER_END(Props)

		void vert(inout appdata_full v) {

			fixed3 Disp = tex2Dlod(_NoiseTex, fixed4(v.texcoord.xy * 2, 0, 0));

			fixed4 CamPosition = mul(unity_WorldToObject, _VectorTest.xyz);

			v.vertex = lerp(v.vertex, CamPosition, saturate((Disp.r < _Amount)));

		}

		void surf (Input IN, inout SurfaceOutputStandard o) {

			// Albedo comes from a texture tinted by color

			//fixed3 TestUV = IN.worldPos - mul(unity_ObjectToWorld, float4(0, 0, 0, 1)).xyz;

			fixed4 c = tex2D (_MainTex, IN.uv_MainTex) * _Color;

			o.Albedo = c;

			o.Emission = 0;

			o.Metallic = _Metallic;

			o.Smoothness = _Glossiness;

			o.Alpha = 1;

		}

		ENDCG

	}

	FallBack ""

}
```



------



### 카메라 각 맵에 대한 렌더링 데이터 가져오기

![img](https://lh5.googleusercontent.com/J78GY73wd5WKV3dLgaxfznnpeGeGz3p0OEczTk3q-JSYjq-8_8nqRHhe7AQm2mVZek8trPyzg251j_biEHRH4xV8E3RjEYILNkpqfm7Om0PyvVFXZHyGce-atOIkmweS73gzean5)

```c++
sampler2D _CameraGBufferTexture1;

fixed4 c = tex2D (_CameraGBufferTexture1, screenUV);
```



### 

### Local Object UV

![img](https://lh4.googleusercontent.com/dR_MdWiP_EEnTgRBbxqxKWjqTYm_SVs5F0-eTskk6KmYKbJGYvtSVBd2g37KxGdAL0gO4uJHe0LvwLjDuFIWTHubaHi3w6FWx_V1vTyZA7G_HOdcrp5fToylPO7CPh02GYLFo6Fg)

```c++
struct Input {

	fixed3 worldPos;

};

fixed3 TestUV = IN.worldPos - mul(unity_ObjectToWorld, float4(0, 0, 0, 1)).xyz;
```



------



### 원거리 왜곡 버텍스

![img](https://lh3.googleusercontent.com/3ROzkFNPcWzbI7yX4mlh0HkPDSQI0ld5LUWIPW_ycbuUnEsTIHLJcwRfAx73rKuTN3SJHxu4gB1OoeAUwtNY5vU_lfH9PNMer6ckW4Oa0sIXjAau6kYlkcFpunqeFxd4-dhP_QSq)

```c++
		void vert(inout appdata_full v) {

			float4 worldPosition = mul(unity_ObjectToWorld, v.vertex);

			// get world space position of vertex

			half2 wpToCam = _WorldSpaceCameraPos.xz - worldPosition.xz;

			// get vector to camera and dismiss vertical component

			half distance = dot(wpToCam, wpToCam);

			// distance squared from vertex to the camera, this power gives the curvature

			worldPosition.y -= distance * 0.01;

			// offset vertical position by factor and square of distance.

			// the default 0.01 would lower the position by 1cm at 1m distance, 1m at 10m and 100m at 100m

			fixed4 CamPosition = mul(unity_WorldToObject, worldPosition);

			v.vertex = lerp(v.vertex, CamPosition, _Amount);

			// reproject position into object space

		}


```



------



### 렌더 텍스처 생성 스크립트

C# 스크립트 생성 후 하단을 만든 뒤, 새로운 쉐이더를 만들어서 스크립트 안에 넣어준다.

가장하단의 _GrabBlurTexture 를 Sampler2D데이터로 가져오면 됨.

```c++
using UnityEngine;

using UnityEngine.Rendering;

using System.Collections.Generic;

// See _ReadMe.txt for an overview

[ExecuteInEditMode]

public class CommandBufferBlurRefraction : MonoBehaviour

{

	public Shader m_BlurShader;

	private Material m_Material;

	private Camera m_Cam;

	// We'll want to add a command buffer on any camera that renders us,

	// so have a dictionary of them.

	private Dictionary<Camera,CommandBuffer> m_Cameras = new Dictionary<Camera,CommandBuffer>();

	// Remove command buffers from all cameras we added into

	private void Cleanup()

	{

		foreach (var cam in m_Cameras)

		{

			if (cam.Key)

			{

				cam.Key.RemoveCommandBuffer (CameraEvent.AfterSkybox, cam.Value);

			}

		}

		m_Cameras.Clear();

		Object.DestroyImmediate (m_Material);

	}

	public void OnEnable()

	{

		Cleanup();

	}

	public void OnDisable()

	{

		Cleanup();

	}

	// Whenever any camera will render us, add a command buffer to do the work on it

	public void OnWillRenderObject()

	{

		var act = gameObject.activeInHierarchy && enabled;

		if (!act)

		{

			Cleanup();

			return;

		}

		

		var cam = Camera.current;

		if (!cam)

			return;

		CommandBuffer buf = null;

		// Did we already add the command buffer on this camera? Nothing to do then.

		if (m_Cameras.ContainsKey(cam))

			return;

		if (!m_Material)

		{

			m_Material = new Material(m_BlurShader);

			m_Material.hideFlags = HideFlags.HideAndDontSave;

		}

		buf = new CommandBuffer();

		buf.name = "Grab screen and blur";

		m_Cameras[cam] = buf;

        // copy screen into temporary RT 

        //Tramporaty RT에 텍스처를 복사한다.

		int screenCopyID = Shader.PropertyToID("_ScreenCopyTexture");

		buf.GetTemporaryRT (screenCopyID, -1, -1, 0, FilterMode.Bilinear);

		buf.Blit (BuiltinRenderTextureType.CurrentActive, screenCopyID);

		

		// get two smaller RTs

		//int blurredID = Shader.PropertyToID("_Temp1");

		//int blurredID2 = Shader.PropertyToID("_Temp2");

		//buf.GetTemporaryRT (blurredID, -2, -2, 0, FilterMode.Bilinear);

		//buf.GetTemporaryRT (blurredID2, -2, -2, 0, FilterMode.Bilinear);

		

		// downsample screen copy into smaller RT, release screen RT

		//buf.Blit (screenCopyID, blurredID);

		//buf.ReleaseTemporaryRT (screenCopyID); 

		

		//// horizontal blur

		//buf.SetGlobalVector("offsets", new Vector4(4.0f/Screen.width,0,0,0));

		//buf.Blit (blurredID, blurredID2, m_Material);

		//// vertical blur

		//buf.SetGlobalVector("offsets", new Vector4(0,4.0f/Screen.height,0,0));

		//buf.Blit (blurredID2, blurredID, m_Material);

		//// horizontal blur

		//buf.SetGlobalVector("offsets", new Vector4(8.0f/Screen.width,0,0,0));

		//buf.Blit (blurredID, blurredID2, m_Material);

		//// vertical blur

		//buf.SetGlobalVector("offsets", new Vector4(0,8.0f/Screen.height,0,0));

		//buf.Blit (blurredID2, blurredID, m_Material);

        

        //렌더링을 정의한다.

        buf.SetGlobalTexture("_GrabBlurTexture", screenCopyID);

        cam.AddCommandBuffer (CameraEvent.AfterSkybox, buf);

	}	

}
```



------



### GGX스펙큘러

![img](https://lh5.googleusercontent.com/m_YzeVRron-tjprZIdQxgUye3P-AUGmSzEE5rBGg7TDmwQKjPfuXwxIQ8gqp0WOpoyEQbSS4mcPViIV0dtVEfzLI0mlg1Lw177qGftKg94TqyKI0Sb3CyXFo0QSyOvFEv_2hBc3t)

```c++
fixed3 H = IN.viewDir; 

fixed NdotV = saturate(dot(o.Normal, H)); //내적 

float NdotV_2 = NdotV * NdotV; 

float a_2 = _a * _a; 

float FinalRender = a_2 / pow(NdotV_2 * (a_2 - 1.0) + 1.0, 2.0);
```



------



### 쉐이더 블렌딩, 컬링 뎁스 테스트, 스텐실 프로퍼티스 정리

(서페이스 쉐이더에서는 스텐실 사용할 때 Render Queue 확인할 것. 최소 2501이상에서만 작동함.)

![img](https://lh6.googleusercontent.com/HhPxqbnJsT52nsNF5b6SkVgt7BXDAi4QGLq18_xY8gqaqDycJtexM_-9U6pmSZAG8q8Un7bJjJB9-LTXxUaeBjxmDygdI-HLU8qE_VoLrJMmMRsUdrukM0WZtZ2yvbFZ_smiuWoa)

​	

```c++
Properties {

		[Header(Blend State)]

		[Enum(UnityEngine.Rendering.BlendMode)] _SrcBlend("SrcBlend", Float) = 1 //"One"

		[Enum(UnityEngine.Rendering.BlendMode)] _DstBlend("DestBlend", Float) = 0 //"Zero"

		[Header(CullDepthTest)]

		[Enum(UnityEngine.Rendering.CullMode)] _Cull("Cull", Float) = 2 //"Back"

		[Enum(UnityEngine.Rendering.CompareFunction)] _ZTest("ZTest", Float) = 4 //"LessEqual"

		[Enum(Off,0,On,1)] _ZWrite("ZWrite", Float) = 1.0 //"On"

		[Enum(UnityEngine.Rendering.ColorWriteMask)] _ColorWriteMask("ColorWriteMask", Float) = 15 //"All"

		[Header(Stencil)]

		[Stencil]

		_Ref("Ref", Float) = 0 //"All"

		[Enum(UnityEngine.Rendering.CompareFunction)] _Comp("Comp", Float) = 0 //"Back"

		[Enum(UnityEngine.Rendering.StencilOp)] _Pass("Pass", Float) = 0 //"Back"

	}

		Blend[_SrcBlend][_DstBlend] //현재소스 X _SrcBlend + 배경소스 X _DstBlend

		Cull[_Cull]

		ZTest[_ZTest]

		ZWrite[_ZWrite]

		ColorMask[_ColorWriteMask]

		Stencil{

		Ref[_Ref]

		Comp [_Comp]

		Pass [_Pass]

		}

		Pass{}



------



### Unity 기본Ui에서 스크롤 FadeOut처리 하는 쉐이더

Shader "Mobile/ScrollViewFadeMask" {

	Properties {

		_Color ("Color", Color) = (0.5,0.5,0.5,0.5)

		[HideInInspector]_MainTex ("Albedo (RGB)", 2D) = "white" {}

		_Stencil("Stencil ID", Float) = 0

		_Alpha("전체알파", Range(0, 1)) = 1

		_MaxLeft("왼쪽 Fade", Range(-1, 0)) = 0

		_MaxRight("오른쪽 Fade", Range(-1, 0)) = 0

		_MaxUp("위쪽 Fade", Range(-1, 0)) = 0

		_MaxDown("아래쪽 Fade", Range(-1, 0)) = 0

		_HorizontalLineMul("가로 경계선 강도", int) = 20

		_VerticalLineMul("세로 경계선 강도", int) = 20

	}

	SubShader {

		Tags { "RenderType"="Transparent" "Queue" = "Transparent"}

		LOD 200

			Lighting Off

			ZWrite Off

			ZTest Off

			Blend SrcAlpha OneMinusSrcAlpha

		Stencil{

			Ref 1

			Comp equal

			Pass keep

		}

		

		CGPROGRAM

		// Physically based Standard lighting model, and enable shadows on all light types

		#pragma surface surf NoLighting alpha:fade

		// Use shader model 3.0 target, to get nicer looking lighting

		#pragma target 2.0

		sampler2D _MainTex;

		struct Input {

			float2 uv_MainTex;

			fixed4 screenPos;

		};

		fixed4 _Color;

		fixed _Alpha;

		fixed _MaxLeft; //왼쪽 마스크

		fixed _MaxRight; //오른쪽 마스크

		fixed _MaxUp; //위쪽 마스크

		fixed _MaxDown; //밑쪽 마스크

		fixed _HorizontalLineMul; //가로 강도

		fixed _VerticalLineMul; //세로 강도

		// Add instancing support for this shader. You need to check 'Enable Instancing' on materials that use the shader.

		// See https://docs.unity3d.com/Manual/GPUInstancing.html for more information about instancing.

		// #pragma instancing_options assumeuniformscaling

		UNITY_INSTANCING_CBUFFER_START(Props)

			// put more per-instance properties here

		UNITY_INSTANCING_CBUFFER_END

		void surf (Input IN, inout SurfaceOutput o) {

			fixed3 ScreenUV = IN.screenPos.xyz / IN.screenPos.a; //화면 렌더링

			fixed LeftMask = saturate((ScreenUV.x + _MaxLeft) * _HorizontalLineMul); //왼쪽마스크

			fixed RightMask = saturate((1 - ScreenUV.x + _MaxRight) * _HorizontalLineMul); //오른쪽 마스크

			fixed UpMask = saturate((1 - ScreenUV.y + _MaxUp) * _VerticalLineMul); //위쪽 마스크

			fixed DownMask = saturate((ScreenUV.y + _MaxDown) * _VerticalLineMul); //아래쪽 마스크

			

			fixed4 c = tex2D (_MainTex, IN.uv_MainTex) * _Color;

			o.Albedo = c.rgb;

			o.Alpha = c.a * _Alpha * LeftMask * RightMask * DownMask * UpMask;

		}

		fixed4 LightingNoLighting(SurfaceOutput s, fixed3 lightDir, fixed atten)

		{

			fixed4 c;

			c.rgb = s.Albedo;

			c.a = s.Alpha;

			return c;

		}

		ENDCG

	}

	FallBack "Diffuse"

}
```



------



### 모바일에서 행렬 사용시 주의사항

mul(UNITY_MATRIX_MVP, *)  <== 이런 형태의 "행렬 * 벡터 연산"에서

행렬과 벡터길이가 맞지 않으면, PC 에선 적절히 변형해서 적용되지만

안드로이드, iOS 같은 모바일 기기에서 쉐이더 에러발생함. 

(쉐이더를 이용하는 모델링들이 분홍색으로 출력됨)

mul( (float3x3)UNITY_MATRIX_MVP, vector3 ) <== 이렇게 행렬과 벡터 크기를 정확히 맞춰줘야함.



------



### Unlit 쉐이더 만들기

```c++
#pragma surface surf NoLighting

- 

fixed4 LightingNoLighting(SurfaceOutput s, fixed3 lightDir, fixed atten)

 {

-  fixed4 c;
- c.rgb = s.Albedo;
- c.a = s.Alpha;
- return c;

}

- 


```

------



### 엠비언트 라이트 데이터 직접 갖다 쓰기

<https://docs.unity3d.com/kr/current/Manual/SL-UnityShaderVariables.html>

UNITY_LIGHTMODEL_AMBIENT



------



### Radial Blur

![img](https://lh5.googleusercontent.com/45-urO4n4nGGdiCMr8K5yBYS1lz7M1PGaEaac-FRS5KP-B-xHpraS0FAgiLLMoYvF8dKTeQVE13VwX28i2YcJbESc8-BYQYACG6lKpixWpKKGkgXut5hA9OzlN6MxV8zVM02Yry1)

```c++
Shader "ImageEffect/Shader_ImageBlender" {

	Properties {

		[HDR]_Color ("Color", Color) = (1,1,1,1)

		_MainTex ("Image(메인 이미지)", 2D) = "white" {}

		_BlurAmount("_BlurAmount", Range(0, 10)) = 1

		_MaskAmount("_MaskAmount", Range(0, 10)) = 1

	}

	SubShader {

		Tags { "RenderType"="Transparent" "Queue" = "Transparent"}

		LOD 200

		CGPROGRAM

		// Physically based Standard lighting model, and enable shadows on all light types

		#pragma surface surf Lambert alpha:fade noshadow noambient novertexlights nolightmap nodynlightmap nodirlightmap nofog nometa noforwardadd nolppv noshadowmask halfasview interpolateview

		// Use shader model 3.0 target, to get nicer looking lighting

		#pragma target 2.0

		sampler2D _MainTex;

		struct Input {

			fixed2 uv_MainTex;

		};

		fixed4 _Color;

		fixed _MaskAmount;

		fixed _BlurAmount;

		// Add instancing support for this shader. You need to check 'Enable Instancing' on materials that use the shader.

		// See https://docs.unity3d.com/Manual/GPUInstancing.html for more information about instancing.

		// #pragma instancing_options assumeuniformscaling

		UNITY_INSTANCING_BUFFER_START(Props)

			// put more per-instance properties here

		UNITY_INSTANCING_BUFFER_END(Props)

		void surf (Input IN, inout SurfaceOutput o) {

			fixed4 c = tex2D (_MainTex, IN.uv_MainTex);

			fixed2 UVMinus = IN.uv_MainTex - 0.5;

			fixed Flare = length(UVMinus);

			UVMinus /= Flare;

			fixed3 radial = c;

			float Addfloat[11] = { -0.08,-0.05,-0.03,-0.02,-0.01,0,0.01,0.02,0.03,0.05,0.08 };

			for (int i = 0; i < 10; ++i)

			{

				radial += tex2D(_MainTex, IN.uv_MainTex + (UVMinus * Addfloat[i] * _BlurAmount));

			}

			radial /= 11;

			fixed Mask = saturate(Flare * _MaskAmount);

			o.Emission = lerp(c, radial, Mask);

			o.Alpha = _Color.a;

		}

		ENDCG

	}

	FallBack "Legercy Shaders/Transparent/VertexLit"

}


```



------



### 파티클 시스템 커스텀 데이터 Vertex Stream

![img](https://lh6.googleusercontent.com/b5kZnoaGZaONPInLW1xx8u7kQ2qEiTm_IcVaofst3PNi8cnJoOmnYBCrUNkgeXyxvXdSYGWmDTXeZL82MM9G21BtMEmIHkn8r-xYGfZ9R2gbDp5LaZa9FNCmbE9QaNwfkFt5QDHd)

![img](https://lh4.googleusercontent.com/arFeGzPXKrdWBVn4pAPwkdzKstwd5AiWL-GEwkd3vDlsFD608FY0bILkPTgwzhMUdGE8hoNvZYEFOIeFdteQiGRexZLkuDUH0A7e4Tr4bjlFbtzQbz9lRNdoOgmR-Bt-0EQwusgo)

```c++
Shader "Particles/CustomData" {

	Properties{

		_Color("Color", Color) = (1,1,1,1)

		_MainTex("Albedo (RGB)", 2D) = "white" {}

		_Glossiness("Smoothness", Range(0,1)) = 0.5

		_Metallic("Metallic", Range(0,1)) = 0.0

	}

		SubShader{

		Tags{ "Queue" = "Transparent" "RenderType" = "Transparent" }

		Blend SrcAlpha OneMinusSrcAlpha

		ZWrite off

		LOD 200

		CGPROGRAM

		// Physically based Standard lighting model, and enable shadows on all light types

		#pragma surface surf Standard vertex:vert alpha

		// Use shader model 3.0 target, to get nicer looking lighting

		#pragma target 3.0

		//사용할 데이터

		sampler2D _MainTex;

		half _Glossiness;

		half _Metallic;

		fixed4 _Color;

	//#1 -> #2

	struct appdata_particles {

		//기본적으로 갖추고 있어야 할 데이터 구조체

		float4 vertex : POSITION;

		float3 normal : NORMAL;

		float4 color : COLOR;

		float4 texcoord : TEXCOORD0;

		//커스텀 데이터

		float4 CustomDataTest : TEXCOORD1;

		float4 CustomDataTest2 : TEXCOORD2;

	};

	//#3 -> #4

	struct Input { //Surface데이터로 넘겨줌

		float2 uv_MainTex; //기본 UV 표현을 위한 좌표1 (필수)

		float2 texcoord; //기본 UV 표현을 위한 좌표2 (필수)

		float4 CustomDataFinal; //첫번째 커스텀 데이터

		float4 CustomDataFinal2; //두번째 커스텀 데이터

		float4 color;

	};

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

	//#2 -> #3

	//struct Input으로 넘겨줌.

	void vert(inout appdata_particles v, out Input o) {

		o.uv_MainTex = v.texcoord.xy; //기본 UV 표현을 위한 좌표1 (필수)

		o.texcoord = v.texcoord.zw; //기본 UV 표현을 위한 좌표2 (필수)

		o.color = v.color;

		o.CustomDataFinal = v.CustomDataTest;

		o.CustomDataFinal2 = v.CustomDataTest2;

	}

	//#4 Final

	void surf(Input IN, inout SurfaceOutputStandard o) {

		fixed3 BaseColor = tex2D(_MainTex, IN.uv_MainTex) * _Color;

		fixed Alpha = IN.CustomDataFinal.a * IN.CustomDataFinal2.a;

		o.Albedo = BaseColor * (IN.CustomDataFinal.rgb + IN.CustomDataFinal2.rgb);

		o.Metallic = _Metallic;

		o.Smoothness = _Glossiness;

		o.Alpha = Alpha;

	}

	ENDCG

	}

		FallBack "Diffuse"

}
```



------



### 유니티 프로젝터를 지원하는 쉐이더

(유니티 에셋 스토어에 있는 ‘Standard assets’에서 Projector 폴더를 다운 받아야 함.)

![img](https://lh4.googleusercontent.com/HnW_RwCoAcYq3436IRCMKkd4y6Y_gnrxGm9Sp5RZkV7Ex6y-Ok0ZnRtdew-3kwFahpPkeSYAwXguz-nHxN78MBc2NTgMkbdgobEHi54-XLyiFm95sAz089vH8IgoVFbm0hCe_1ty)

```
// Upgrade NOTE: replaced '_Projector' with 'unity_Projector'

// Upgrade NOTE: replaced '_Projector' with 'unity_Projector'

Shader "Custom/ProjectorShader" {

	Properties {

		_Color ("Color", Color) = (1,1,1,1)

		_MainTex ("Albedo (RGB)", 2D) = "white" {}

	}

	SubShader {

		Tags { "Queue" = "Transparent"}

		LOD 200

		Blend SrcAlpha One

		CGPROGRAM

		// Physically based Standard lighting model, and enable shadows on all light types

		#pragma surface surf Lambert vertex:vert noshadow  noambient novertexlights nolightmap nodynlightmap nodirlightmap nofog nometa noforwardadd nolppv noshadowmask

		// Use shader model 3.0 target, to get nicer looking lighting

		#pragma target 2.0

		float4x4 unity_Projector; //유니티 프로젝트 매트릭스

		struct Input {

			float2 uv_MainTex;

			float4 posProj : TEXCOORD0; // 프로젝트 공간 좌표

		};

		void vert(inout appdata_full v, out Input o) {

			UNITY_INITIALIZE_OUTPUT(Input, o);

			o.posProj = mul(unity_Projector, v.vertex);

		}

		sampler2D _MainTex;

		fixed4 _Color;

		// Add instancing support for this shader. You need to check 'Enable Instancing' on materials that use the shader.

		// See https://docs.unity3d.com/Manual/GPUInstancing.html for more information about instancing.

		// #pragma instancing_options assumeuniformscaling

		UNITY_INSTANCING_BUFFER_START(Props)

			// put more per-instance properties here

		UNITY_INSTANCING_BUFFER_END(Props)

		void surf (Input IN, inout SurfaceOutput o) {

			// Albedo comes from a texture tinted by color

			//fixed4 c = tex2D (_MainTex, IN.uv_MainTex) * _Color;

			fixed4 ProRender = tex2Dproj(_MainTex, UNITY_PROJ_COORD(IN.posProj)) * _Color;

			o.Albedo = ProRender;

		}

		ENDCG

	}

	FallBack ""

}
```



------



### 외부에서 제어 가능한 쉐이더 데이터 만들기

<https://docs.unity3d.com/ScriptReference/Shader.SetGlobalVector.html>

1. 쉐이더 안에 들어가는 데이터의 앞에 uniform이라는 명령어를 붙인다.

(Properties 값을 주석 처리 해야 함.)

uniform fixed4 Global_Position;

\2. 다른 코드에서 SetGlobalVector로 접근한다.

```c#
public class Pointer : MonoBehaviour {

    public GameObject PointerObject;

	// Use this for initialization

	void Start () {

		

	}

	

	// Update is called once per frame

	void Update () {

        Vector4 pos = PointerObject.transform.position;

        Shader.SetGlobalVector("Global_Position", pos);

	}

}


```

------



### 월드 좌표를 쉐이더에 대입하기

![img](https://lh6.googleusercontent.com/WG7q1JthWF0eJx5wX7KEoNOqIGhbknXvLV9hSmBkysyteuqQRCWPr_GkOBtHIIzWt_7m7zcebU2wVoVT0rlAmrkUNA1lCJwp8R0r7KN6f_Togq2DEvp7Ov4NIpzJaiJTUa7EkIlU)

```c++
Shader "Custom/SpghericalMask" {

	Properties {

		_Color ("Color", Color) = (1,1,1,1)

		_MainTex ("Albedo (RGB)", 2D) = "white" {}

		_Glossiness ("Smoothness", Range(0,1)) = 0.5

		_Metallic ("Metallic", Range(0,1)) = 0.0

		_Position("_Position", Vector) = (0, 0, 0, 0)

		_Radius("_Radius", Range(0, 100)) = 0

		_Softness("_Softness", Range(0, 100)) = 0

	}

	SubShader {

		Tags { "RenderType"="Opaque" }

		LOD 200

		CGPROGRAM

		// Physically based Standard lighting model, and enable shadows on all light types

		#pragma surface surf Standard fullforwardshadows

		// Use shader model 3.0 target, to get nicer looking lighting

		#pragma target 3.0

		sampler2D _MainTex;

		struct Input {

			float2 uv_MainTex;

			fixed3 worldPos;

		};

		half _Glossiness;

		half _Metallic;

		fixed4 _Color;

		fixed4 _Position;

		fixed _Radius;

		fixed _Softness;

		// Add instancing support for this shader. You need to check 'Enable Instancing' on materials that use the shader.

		// See https://docs.unity3d.com/Manual/GPUInstancing.html for more information about instancing.

		// #pragma instancing_options assumeuniformscaling

		UNITY_INSTANCING_BUFFER_START(Props)

			// put more per-instance properties here

		UNITY_INSTANCING_BUFFER_END(Props)

		void surf (Input IN, inout SurfaceOutputStandard o) {

			//기본 컬러

			fixed4 c = tex2D (_MainTex, IN.uv_MainTex) * _Color;

			//흑백처리

			fixed3 GrayScale = (c.r + c.g + c.b) * 0.333;

			//위치 처리기

			fixed p2w = distance(_Position, IN.worldPos); //_Position의 좌표와 월드좌표의 거리를 알아냄.

			fixed p2wMask = saturate((p2w - _Radius) / - _Softness); //거리를 제대로 시각화 시키기 위한 처리

			fixed4 LerpColor = lerp(GrayScale.r, c, p2wMask);

			o.Albedo = LerpColor.rgb;

			// Metallic and smoothness come from slider variables

			o.Metallic = _Metallic;

			o.Smoothness = _Glossiness;

			o.Alpha = c.a;

		}

		ENDCG

	}

	FallBack "Diffuse"

}


```



------



### Vertex:vert를 텍스처 데이터로 컨트롤 하기

![img](https://lh4.googleusercontent.com/2BE1T0Zcom-MHwH4A9IHNZWVNnCEMB0AHfpERIbWvkxxM3hL70YQoe4nkFIKDdr8-ctKa0AlRf638011vY2Ji33kAGD7jVq-ikRixnprlFyMwlJqf8-hnj8DpGOoKkB9DHrXMyHb)

```c++
Shader "Custom/Test" {

	Properties {

		[HDR]_Color ("Color", Color) = (1,1,1,1)

		_MainTex ("Albedo (RGB)", 2D) = "white" {}

		_MetallicSmoothness("_MetallicSmoothness", 2D) = "black" {}

		[Normal]_Normal("_Normal", 2D) = "white" {}

		_HeightMap("_HeightMap", 2D) = "white" {}

		_MaskRange("_MaskRange", Range(0, 1)) = 0

		_Amount("_Amount", Range(0, 1)) = 0

		_NoiseTexture("_NoiseTexture", 2D) = "black" {}

	}

		SubShader{

			Tags { "RenderType" = "Opaque" }

			LOD 200

			CGPROGRAM

			// Physically based Standard lighting model, and enable shadows on all light types

			#pragma surface surf Standard fullforwardshadows vertex:vert

			// Use shader model 3.0 target, to get nicer looking lighting

			#pragma target 3.0

			//VertData

			fixed _Amount;

			sampler2D _MainTex;

			sampler2D _Normal;

			sampler2D _MetallicSmoothness;

			sampler2D _HeightMap;

			sampler2D _NoiseTexture;

			fixed4 _Color;

			fixed _MaskRange;

		void vert(inout appdata_full v) {

			float3 disp = tex2Dlod(_NoiseTexture, fixed4(v.texcoord.xy, 0, 0));

			v.vertex.xyz += v.normal * disp.r * _Amount;

			//해당 값을 더하거나, 곱하면 됨. (v.Normal에 개입하는 거라면 곱하기, 개별적인 좌표로 움직이고 싶으면 Add)

		}

		struct Input {

			float2 uv_MainTex;

		};

		// Add instancing support for this shader. You need to check 'Enable Instancing' on materials that use the shader.

		// See https://docs.unity3d.com/Manual/GPUInstancing.html for more information about instancing.

		// #pragma instancing_options assumeuniformscaling

		UNITY_INSTANCING_BUFFER_START(Props)

			// put more per-instance properties here

		UNITY_INSTANCING_BUFFER_END(Props)

		void surf (Input IN, inout SurfaceOutputStandard o) {

			fixed4 c = tex2D (_MainTex, IN.uv_MainTex);

			fixed MatellicFinal = tex2D(_MetallicSmoothness, IN.uv_MainTex);

			fixed4 SmoothnessFinal = tex2D(_MetallicSmoothness, IN.uv_MainTex);

			fixed3 NormalFinal = UnpackNormal(tex2D(_Normal, IN.uv_MainTex));

			fixed SandMask = tex2D(_HeightMap, IN.uv_MainTex);

			if (SandMask <= _MaskRange)

			{

				SandMask = 1;

			}

			else

			{

				SandMask = 0;

			}

			o.Albedo = lerp(c.rgb, _Color, SandMask);

			// Metallic and smoothness come from slider variables

			o.Metallic = MatellicFinal.r;

			o.Smoothness = SmoothnessFinal.a;

			o.Normal = NormalFinal;

			//o.Alpha = c.a;

		}

		ENDCG

	}

	FallBack "Diffuse"

}
```



------



### Vertex:vert로 변형된 버텍스까지 그림자 처리 하기

![img](https://lh5.googleusercontent.com/n8bNSMUXkSbrcGKd7c4J5IOWya3UZNULZAVQ4cR5HLd7KUXwli-aCN2gZURkwKZ7aE4GTRe7MeO595gD00NfXc8KoZ8lwa8Y5qi192s5_A2GbtbuNPnohOkiR9n6-G6JJyPnkucm)

```
#pragma surface surf Standard addshadow
```



------



### atan2 계산식을 통한 X축 로테이션 출력

### ![img](https://lh5.googleusercontent.com/UOg8UQ1yZJPXKfOYumRi63NRAUYaciqdmXZEMTEvLqhYNIvf-zRrlP7Nl1n2lks_UmswwD-5udfCOoahW2IdS897xQ5AmgFyx1JxnZx02O4cnV80u7wGfF8rF32V0IM5I8sKnevl)

```
fixed4 c = tex2D (_MainTex, fixed2(atan2((IN.uv_MainTex.x - 0.5) * 0.5, (IN.uv_MainTex.y - 0.5) * 0.5), 0)) ;

*lengh를 추가로 계산 하면 늘어나지 않고 원으로 말아줌.


```



------



### 버텍스 컬러값 받아오기

```c++
Shader "TestTest" {

	Properties {

		_Color ("Color", Color) = (1,1,1,1)

		_MainTex ("Albedo (RGB)", 2D) = "white" {}

		_Cutoff("Base Alpha cutoff", Range(0, 1)) = 0.5

		_Glossiness ("Smoothness", Range(0,1)) = 0.5

		_Metallic ("Metallic", Range(0,1)) = 0.0

		[Normal]_Normal("_Normal", 2D) = "bump" {}

	}

	SubShader {

			Tags{ "RenderType" = "TransparentCutout" "Queue" = "AlphaTest" }

		LOD 200

			Cull Off

		CGPROGRAM

		// Physically based Standard lighting model, and enable shadows on all light types

		#pragma surface surf Standard alphatest:_Cutoff

		// Use shader model 3.0 target, to get nicer looking lighting

		#pragma target 3.0

		sampler2D _MainTex;

		sampler2D _Normal;

		struct Input {

			float2 uv_MainTex;

			fixed3 vertexcolor : COLOR;

		};

		half _Glossiness;

		half _Metallic;

		fixed4 _Color;

		void surf (Input IN, inout SurfaceOutputStandard o) {

			// Albedo comes from a texture tinted by color

			fixed4 c = tex2D (_MainTex, IN.uv_MainTex) * _Color;

			fixed3 NormalFinal = UnpackNormal(tex2D(_Normal, IN.uv_MainTex));

			o.Albedo = c.rgb * IN.vertexcolor;

			// Metallic and smoothness come from slider variables

			o.Metallic = _Metallic;

			o.Smoothness = _Glossiness;

			o.Normal = NormalFinal;

			o.Alpha = c.a;

		}

		ENDCG

	}

	FallBack "Legacy Shaders/Transparent/Cutout/VertexLit"

}
```



------



### 텍스처 회전 쉐이더

![img](https://lh3.googleusercontent.com/D3bPeJ3_O4upmpXgT_eTmvXmwKbjRpETij47tbPtQwaXKrHsfgnVj1NjJNXgxu7nUSDbDuFtvbyHK01-REy4ImF_7gHY1aqjurnOdp5xfc-UpGS0GeJI1XXVb5rSXRfl4cPhXL2w)

// Upgrade NOTE: replaced 'mul(UNITY_MATRIX_MVP,*)' with 'UnityObjectToClipPos(*)'

```c++
Shader "Jinho/EarthSpellAlpha" {

	Properties {

		[HDR]_Color ("Color", Color) = (1,1,1,1)

		_MainTex ("Albedo (RGB)", 2D) = "white" {}

		_ViewAmount ("_ViewAmount", Range(0, 0.2)) = 0.2

		_RotationSpeed("_RotationSpeed (텍스처 회전속도)", Range(0, 10)) = 1

	}

	SubShader {

		Tags { "RenderType"="Transparent" "Queue" = "Transparent"}

		LOD 200

		CGPROGRAM

		// Physically based Standard lighting model, and enable shadows on all light types

		#pragma surface surf Lambert alpha:fade vertex:vert

		// Use shader model 3.0 target, to get nicer looking lighting

		#pragma target 2.0

		sampler2D _MainTex;

		//sampler2D _AlphaCircle; //알파맵

		struct Input {

			fixed2 uv_MainTex;

			//fixed2 uv_AlphaCircle; //알파맵UV

		};

		fixed4 _Color;

		fixed _ViewAmount; //보이는 정도

		float _RotationSpeed; //텍스처 회전 속도

		// Add instancing support for this shader. You need to check 'Enable Instancing' on materials that use the shader.

		// See https://docs.unity3d.com/Manual/GPUInstancing.html for more information about instancing.

		// #pragma instancing_options assumeuniformscaling

		UNITY_INSTANCING_BUFFER_START(Props)

			// put more per-instance properties here

		UNITY_INSTANCING_BUFFER_END(Props)

		void vert(inout appdata_base v) {

			//fivot

			float2 pivot = float2(0.5, 0.5); //텍스처 전체의 피봇을 0.5만큼 더함.

			//Angle

			float sinAngle = sin(_RotationSpeed);

			float cosAngle = cos(_RotationSpeed);

			float2x2 rotationMatrix = float2x2(cosAngle, -sinAngle, sinAngle, cosAngle);

			v.texcoord.xy = mul(rotationMatrix, v.texcoord.xy - pivot) + pivot; //회전 후 피봇 만큼 UV를 이동

		}

		////https://forum.unity.com/threads/rotation-of-texture-uvs-directly-from-a-shader.150482/

		////참고자료

		void surf (Input IN, inout SurfaceOutput o) {

			// Albedo comes from a texture tinted by color

			fixed4 c = tex2D (_MainTex, IN.uv_MainTex) * _Color;

			fixed4 ViewFinal = (1 - (((IN.uv_MainTex.x - 0.5) * (IN.uv_MainTex.x - 0.5)) + ((IN.uv_MainTex.y - 0.5) * (IN.uv_MainTex.y - 0.5)))) + _ViewAmount; //보여지는 량.

			//fixed _ViewAmount = frac(-_Time.y * _ViewSpeed); //이미지 나타나는 속도

			if (ViewFinal.r >= 1)

			{

				ViewFinal = 1;

			}

			else

			{

				ViewFinal = 0;

			}

			o.Emission = c * ViewFinal;

			o.Alpha = c.a * ViewFinal;

		}

		ENDCG

	}

	FallBack "Legercy Shaders/Transparent/VertexLit"

}


```



------



### 오브젝트 탄젠트에 대한 월드 노멀 가져오기.

(worldPos 와의 차이점 : worldPos는 좌표 내의  0~무한대의 수치를 출력함. WorldNormalVector는 현재 오브젝트와 월드 상에서의 노멀 방향에 대한 float값만을 출력함.)

```c++
struct [Input](http://unity3d.com/support/documentation/ScriptReference/30_search.html?q=Input) {

    float2 uv_MainTex;

    float2 uv_BumpMap;

    float3 worldNormal;

    INTERNAL_DATA

};

void surf ([Input](http://unity3d.com/support/documentation/ScriptReference/30_search.html?q=Input) IN, inout SurfaceOutput o) {

    o.Albedo = tex2D (_MainTex, IN.uv_MainTex).rgb * 0.5;

    o.Normal = UnpackNormal (tex2D (_BumpMap, IN.uv_BumpMap));

    float3 worldNormal = WorldNormalVector (IN, o.Normal);

}
```



------



World Uv Texturing

![img](https://lh5.googleusercontent.com/jgwGwcoS9RILGgjybGDmJ29heowPfxCYJ-mv4nVAHmaaVFJEe80EpJ7aPMwAx4oMD7WvOfU_n8PbW4ktRhZWGRTkaObER6g1hANSolcs6Pc_w8QijC-gdkPW18bB17668CxuTZl-)

```c++
Shader "Jinho/Evi_SnowShader" {

	Properties {

		_Color ("Color", Color) = (1,1,1,1)

		_MainTex ("Color(RGB)", 2D) = "white" {}

		_Smoothness ("Smoothness", Range(0,1)) = 0.5

		_Metallic ("Metallic", Range(0,1)) = 0.0

		[Header(SnowSetting)]

		[NoScaleOffset]_SnowColor("_SnowColor", 2D) = "black" {}

		_UVTiling("_UVTiling", Range(0, 0.1)) = 0.1

		[NoScaleOffset]_ViewNoise("_ViewNoise", 2D) = "black" {}

		_cut("_cut", Range(0, 1)) = 0

	}

	SubShader {

		Tags { "RenderType"="Opaque" }

		LOD 200

		CGPROGRAM

		// Physically based Standard lighting model, and enable shadows on all light types

		#pragma surface surf Standard

		// Use shader model 3.0 target, to get nicer looking lighting

		#pragma target 2.0

		sampler2D _MainTex;

		sampler2D _SnowColor;

		sampler2D _ViewNoise;

		struct Input {

			fixed2 uv_MainTex;

			fixed3 worldPos;

			fixed3 worldNormal;

		};

		fixed _Smoothness;

		fixed _Metallic;

		fixed4 _Color;

		fixed _UVTiling;

		fixed _cut; //눈 보이는 정도

		// Add instancing support for this shader. You need to check 'Enable Instancing' on materials that use the shader.

		// See https://docs.unity3d.com/Manual/GPUInstancing.html for more information about instancing.

		// #pragma instancing_options assumeuniformscaling

		UNITY_INSTANCING_BUFFER_START(Props)

			// put more per-instance properties here

		UNITY_INSTANCING_BUFFER_END(Props)

		void surf (Input IN, inout SurfaceOutputStandard o) {

			//기본 텍스처 처리

			fixed4 c = tex2D (_MainTex, IN.uv_MainTex) * _Color;

			//SnowTex

			//텍스처 처리용 월드 UV

			fixed2 UVtop = fixed2(IN.worldPos.x, IN.worldPos.z) * _UVTiling;

			fixed2 UVfront = fixed2(IN.worldPos.x, IN.worldPos.y) * _UVTiling;

			fixed2 UVside = fixed2(IN.worldPos.y, IN.worldPos.z) * _UVTiling;

			//방향에 따른 텍스쳐 출력

			fixed4 TexTop = tex2D(_SnowColor, UVtop); //윗면 렌더링

			fixed4 Texfront = tex2D(_SnowColor, UVfront); //정면 렌더링

			fixed4 Texside = tex2D(_SnowColor, UVside); //옆면 렌더링

			//텍스처 출력 마스크

			fixed MaskTop = abs(IN.worldNormal.y); //상단 마스크

			fixed MaskSide = abs(IN.worldNormal.x); //옆면 마스크

			//눈 효과 최종 렌더링

			fixed3 SnowFinal = lerp(Texfront, TexTop, abs(MaskTop));

			fixed3 SnowFinal2 = lerp(SnowFinal, Texside, abs(MaskSide));

			//스노우 마스크용 처리

			//방향에 따른 텍스쳐 출력

			fixed4 TexTop_SnowMask = tex2D(_ViewNoise, UVtop); //윗면 렌더링

			fixed4 Texfront_SnowMask = tex2D(_ViewNoise, UVfront); //정면 렌더링

			fixed4 Texside_SnowMask = tex2D(_ViewNoise, UVside); //옆면 렌더링

			fixed3 SnowMask = lerp(Texfront_SnowMask, TexTop_SnowMask, abs(MaskTop));

			fixed3 SnowMask2 = lerp(SnowMask, Texside_SnowMask, abs(MaskSide));

			if (SnowMask2.r >= _cut)

				SnowMask2.r = 0;

			else

				SnowMask2.r = 1;

			//최종 렌더링

			o.Albedo = lerp(c.rgb, SnowFinal2, SnowMask2.r);

			o.Metallic = _Metallic;

			o.Smoothness = _Smoothness;

			o.Alpha = c.a;

		}

		ENDCG

	}

	FallBack "Diffuse"

}
```



------



### Water Shader

![img](https://lh5.googleusercontent.com/Jq6nEoPYfkvEew4ATtTA5V7_nHYZ1uvzZjj6vRXB36N0a7SyZSZ4wlSKcRPrxb0OpyHxNdPPYQncOtr2ngjlwsFs1MO9p1RQEmGpO2v2b6RuEgZrqwn1rjhWGGUm5cq_k_M882YW)

```c++
Shader "Jinho/Water_1" {

	Properties {

		[NoScaleOffset]_CubeMap("_CubeMap", Cube) = ""{}

		_Normal("_Normal", 2D) = "bump" {}

		[Header(RimLight)]

		_RimMul("_RimMul", Range(0, 10)) = 5

		_RimPow("_RimPow", Range(0, 50)) = 10

		[Header(Specular)]

		_SPPow("_SPPow", Range(0, 1000)) = 80

		_SPMul("_SPMul", Range(0, 100)) = 20

		[Header(VertexMove)]

		_WaveH ("_WaveH", Range(0, 0.5)) = 0.1

		_WaveL ("_WaveL", Range(0, 30)) = 12

		_WaveTime ("_WaveTime", Range(0, 10)) = 1

		[Header(GrabTexture)]

		_GrabMul ("_GrabMul", Range(0.1, 5)) = 2

		_GrabPow("_GrabPow", Range(0.1, 5)) = 3.5

		[Header(MeshAttach)]

		_InvFade("_InvFade", Range(0, 1)) = 0.15

		_MeshAttachPower("_MeshAttachPower", Range(0, 1)) = 0.5

		_MeshAttachGradation("_MeshAttachGradation", 2D) = "white" {}

	}

		SubShader{

			Tags { "RenderType" = "Trasparent" "Queue" = "Transparent" }

			GrabPass{}

			CGPROGRAM

			// Physically based Standard lighting model, and enable shadows on all light types

			#pragma surface surf WaterSpecular alpha:fade vertex:vert 

		// Use shader model 3.0 target, to get nicer looking lighting

		#pragma target 4.0

		//sampler2D _MainTex;

		sampler2D _Normal;

		samplerCUBE _CubeMap; //큐브맵

		sampler2D _GrabTexture;

		

		//접촉면 출력

		sampler2D _CameraDepthTexture; //카메라 뎁스값

		fixed _InvFade; // 최종값에 곱하는 량

		sampler2D _MeshAttachGradation; //접촉면 색 그라데이션

		struct Input {

			//fixed2 uv_MainTex;

			fixed2 uv_Normal;

			fixed3 worldRefl;

			INTERNAL_DATA

			fixed3 viewDir; //카메라 각도

			fixed4 screenPos; //카메라 UV좌표

			fixed3 lightColor0; //라이트 컬러

			//닿은 표면적 인식

			fixed4 projPos; //4개의 값을 받아와야 함.

			fixed4 vertex;

			fixed2 uv_MeshAttachGradation;

		};

		fixed _RimMul;

		fixed _RimPow;

		fixed _SPPow;

		fixed _SPMul;

		fixed _WaveH;

		fixed _WaveL;

		fixed _WaveTime;

		fixed _GrabMul;

		fixed _GrabPow;

		fixed _MeshAttachPower;

		// Add instancing support for this shader. You need to check 'Enable Instancing' on materials that use the shader.

		// See https://docs.unity3d.com/Manual/GPUInstancing.html for more information about instancing.

		// #pragma instancing_options assumeuniformscaling

		UNITY_INSTANCING_BUFFER_START(Props)

			// put more per-instance properties here

		UNITY_INSTANCING_BUFFER_END(Props)

		void vert(inout appdata_full v, out Input o) {

			fixed VertexWave;

			VertexWㄹave = sin(abs(v.texcoord.x * 2 - 1) * _WaveL + _Time.y * _WaveTime) * _WaveH;

			VertexWave += sin(abs(v.texcoord.y * 2 - 1) * _WaveL + _Time.y * _WaveTime) * _WaveH;

			v.vertex.y += VertexWave * 0.5;

			//오브젝트 접촉면 출력을 위한 부분

			UNITY_INITIALIZE_OUTPUT(Input, o);

			o.vertex = UnityObjectToClipPos(v.vertex);

			o.projPos = ComputeScreenPos(o.vertex);

			COMPUTE_EYEDEPTH(o.projPos.z);

		}

		void surf (Input IN, inout SurfaceOutput o) {

			//기본컬러

			//fixed4 c = tex2D (_MainTex, IN.uv_MainTex) * _Color;

			//노멀 처리

			fixed3 Normal_1 = UnpackNormal(tex2D(_Normal, fixed2(IN.uv_Normal.x + _Time.x, IN.uv_Normal.y)));

			fixed3 Normal_2 = UnpackNormal(tex2D(_Normal, fixed2(IN.uv_Normal.x * 1.35 - _Time.x, IN.uv_Normal.y * 1.35 + _Time.x)));

			fixed3 NormalFinal = (Normal_1 + Normal_2) * 0.5;

			o.Normal = NormalFinal;

			//반사광처리

			fixed3 RefColor = texCUBE(_CubeMap, WorldReflectionVector(IN,o.Normal));

			//림라이트

			fixed3 LdotV = saturate(dot(o.Normal, IN.viewDir));

			fixed3 Lim = pow((1 - LdotV) * _RimMul, _RimPow);

			//오브젝트 접촉부분 출력

			fixed sceneZ = LinearEyeDepth(SAMPLE_DEPTH_TEXTURE_PROJ(_CameraDepthTexture, UNITY_PROJ_COORD(IN.projPos))); //카메라 뎁스

			fixed partZ = IN.projPos.z; //오브젝트 뎁스

			fixed MeshAttach = saturate(_InvFade * (sceneZ - partZ));//카메라 뎁스과 오브젝트 뎁스를 뺀 후 곱하고 잘라냄.

			fixed3 MeshAttachFinal = ((1 - MeshAttach));

			fixed3 MeshAttachFinal_2 = _MeshAttachPower * _LightColor0.rgb * (MeshAttachFinal * (tex2D(_MeshAttachGradation, fixed2(MeshAttachFinal.r, IN.uv_MeshAttachGradation.y))));

			//그랩패스 출력

			fixed3 screenUV = IN.screenPos.rgb / IN.screenPos.a;

			fixed3 GrabFinal = pow(tex2D(_GrabTexture, screenUV.xy + o.Normal * 0.05 + 0.03) * _GrabMul, _GrabPow);

			o.Emission = RefColor * GrabFinal * Lim + MeshAttachFinal_2;

			o.Alpha = 1;

		}

		fixed4 LightingWaterSpecular(SurfaceOutput s, fixed3 lightDir, fixed3 viewDir, fixed atten) {

			//스펙큘러

			fixed3 H = normalize(lightDir + viewDir);

			fixed Spec = saturate(dot(H, s.Normal));

			Spec = pow(Spec, _SPPow);

			//최종렌더

			fixed4 finalColor;

			//finalColor.rgb = (Spec * _SPColor.rgb) * _SPMul;

			finalColor.rgb = (Spec * _LightColor0.rgb) * _SPMul;

			finalColor.a = s.Alpha;

			return finalColor;

		}

		ENDCG

	}

	FallBack "Legacy Shaders/Trasparent/VertexLit"

}
```



------



### Circle Texture 만드는 계산식

```
pow((1 - (((IN.uv_MainTex.x - 0.5) * (IN.uv_MainTex.x - 0.5)) + ((IN.uv_MainTex.y - 0.5) * (IN.uv_MainTex.y - 0.5)))), 50);

또는

    float2 dir = texCo - 0.5 ; //원래 텍스처에서 0.5를 뺀다.

    float dist = length(dir);


```



------



### 라이트 컬러 값 가져오기

```c++
Shader "Jinho/UnLightDirShader" {

	Properties {

		_Color ("Color", Color) = (1,1,1,1)

		_MainTex ("Albedo (RGB)", 2D) = "white" {}

	}

	SubShader {

		Tags { "RenderType"="Opaque" }

		CGPROGRAM

		// Physically based Standard lighting model, and enable shadows on all light types

		#pragma surface surf Lambert noshadow  noambient novertexlights nolightmap nodynlightmap nodirlightmap nofog nometa noforwardadd nolppv noshadowmask halfasview

		// Use shader model 3.0 target, to get nicer looking lighting

		#pragma target 2.0

		sampler2D _MainTex;

		struct Input {

			float2 uv_MainTex;

			fixed4 _LightColor0; //라이트 컬러값 받아옴.

		};

		fixed4 _Color;

		// Add instancing support for this shader. You need to check 'Enable Instancing' on materials that use the shader.

		// See https://docs.unity3d.com/Manual/GPUInstancing.html for more information about instancing.

		// #pragma instancing_options assumeuniformscaling

		UNITY_INSTANCING_BUFFER_START(Props)

			// put more per-instance properties here

		UNITY_INSTANCING_BUFFER_END(Props)

		void surf (Input IN, inout SurfaceOutput o) {

			fixed4 c = tex2D (_MainTex, IN.uv_MainTex) * _Color;

			o.Albedo = _LightColor0.rgb; //라이트 컬러값 출력

			o.Alpha = c.a;

		}

		ENDCG

	}

	FallBack "Diffuse"

}


```



------



### 오브젝트의 Z값을 계산하는 쉐이더.

![img](https://lh4.googleusercontent.com/G7b-8ZGPMkqNFDJDiLaZX7OhEIvWVQyF1V6aBIJOhL2iWU2ToWo3bzOz1zgmRrK6JQ8SAwsARAOJzQYssaHhwHaFFQAc3EOwpkZerAPDGGIbr6CkJbhnArLzkoQzcDKr4Lrex-ji)

```c++
Shader "Jinho/OnltyObjectDepth" {

	Properties {

		_partZMul("partZMul", int) = 0.04 //꼭 0.04여야함. 차이가 굉장히 미세함.

		_partZPower("partZPower", int) = 5 //시각적으로 확실하게 보이기 위한 대비값.

	}

		SubShader{

			Tags { "RenderType" = "Opaque" }

			LOD 200

			CGPROGRAM

			// Physically based Standard lighting model, and enable shadows on all light types

			#pragma surface surf Lambert vertex:vert

			// Use shader model 3.0 target, to get nicer looking lighting

			#pragma target 2.0

		sampler2D _MainTex;

		struct Input {

			fixed2 uv_MainTex;

			fixed4 projPos;

		};

		fixed _partZMul;

		fixed _partZPower;

		// Add instancing support for this shader. You need to check 'Enable Instancing' on materials that use the shader.

		// See https://docs.unity3d.com/Manual/GPUInstancing.html for more information about instancing.

		// #pragma instancing_options assumeuniformscaling

		UNITY_INSTANCING_CBUFFER_START(Props)

			// put more per-instance properties here

		UNITY_INSTANCING_CBUFFER_END

			//유니티 내부에서 오브젝트의 Z값을 가져옴.

			void vert(inout appdata_full v, out Input o)

		{

			UNITY_INITIALIZE_OUTPUT(Input, o);

			COMPUTE_EYEDEPTH(o.projPos.z);

		}

		void surf (Input IN, inout SurfaceOutput o) {

			float partZ = IN.projPos.z; //오브젝트 Z값

			o.Emission = pow(saturate(partZ * _partZMul), _partZPower); 

			//시각적으로 확실하게 보여주기 위한 계산

		}

		ENDCG

	}

	FallBack "Diffuse"

}


```



------

오브젝트의 표면 계산하는 쉐이더



![img](https://lh3.googleusercontent.com/CsvxLEKr9cimSgh7KWtEeySpRTFS1zH1rRZU8K7slU61C9qXfH76QUNeBunlcweFfECDyvzu8uZm7-jJSHoA6jjHmXpIK7tNN34iUedpq0HDxK_x66ar6IaAHhTa7zj9QI4VdHQs)

```c++
Shader "Custom/SurfaceDepthTexture" {

	Properties{

		[HDR]_Color("Color", Color) = (1,1,1,1)

		_MainTex("Albedo (RGB)", 2D) = "white" {}

		_InvFade("Soft Factor", Range(0.01,3.0)) = 1.0

	}

		SubShader{

		Tags{ "Queue" = "Transparent" "RenderType" = "Transparent" }

		LOD 200

		cull off

		CGPROGRAM

		#pragma surface surf Lambert alpha:fade vertex:vert 

		//vertex:vert라는 void를 정의 한 후 그 안에서 유니티 내부 데이터를 불러옴.

		// Use shader model 3.0 target, to get nicer looking lighting

		#pragma target 4.0

		//pragma Target이 4.0 인지 확인할것. (지원이 많이 안되는 쉐이더는 3.0으로도 충분하나 복합적으로 기능이 들어갈 경우 4.0 이상을 설정해야 함.)

		struct Input

	{

		fixed4 vertex; //vertex값 들어와야 함.

		fixed4 projPos; //4개의 값을 받아와야 함.

		fixed2 uv_MainTex;

	};

// 유니티 내부에서 오브젝트의 뎁스 값을 불러옴.

	void vert(inout appdata_full v, out Input o)

	{

		UNITY_INITIALIZE_OUTPUT(Input,o);

		o.vertex = UnityObjectToClipPos(v.vertex);

		o.projPos = ComputeScreenPos(o.vertex);

		COMPUTE_EYEDEPTH(o.projPos.z);

	}

	sampler2D _MainTex;

	sampler2D _CameraDepthTexture; //카메라 뎁스값

	fixed _InvFade; // 최종값에 곱하는 량

	fixed3 _Color;

	fixed fade;

	void surf(Input IN, inout SurfaceOutput o)

	{

		fixed4 d = tex2D(_MainTex, IN.uv_MainTex);

float sceneZ = LinearEyeDepth(SAMPLE_DEPTH_TEXTURE_PROJ(_CameraDepthTexture, UNITY_PROJ_COORD(IN.projPos))); //카메라 뎁스

		float partZ = IN.projPos.z; //오브젝트 뎁스

		fade = saturate(_InvFade * (sceneZ - partZ)); //카메라 뎁스과 오브젝트 뎁스를 뺀 후 곱하고 잘라냄.

		o.Emission = saturate(1 - float3(fade, fade, fade)) * _Color + d.rgb; //오브젝트 닿는 면적 * 컬러 + 텍스처

		o.Alpha = saturate(0.7 + 1 - float3(fade, fade, fade)); //알파값 뺌.

	}

	ENDCG

	}

}
```



------



### 뎁스 텍스쳐 받아오기

(Forward 렌더링에서는 작동안함.)

```c++
sampler2D _CameraDepthTexture;

		struct Input {

			fixed4 screenPos;

		};

		void surf (Input IN, inout SurfaceOutput o) {

			fixed3 screenUV2 = IN.screenPos.rgb / IN.screenPos.a;

			fixed4 Depth = tex2D(_CameraDepthTexture, screenUV2);

		}

		ENDCG
```



------



버텍스 쉐이더

```c
vertex:vert

     float _Amount;
      void vert (inout appdata_full v) {
          v.vertex.xyz += v.normal * _Amount;
      }


```



------



큐브맵 컬러값 받아오기

![img](https://lh4.googleusercontent.com/n4RZOZR-ILwLp0h0_vDxMl_EA74Zj6Heo4hnRPRN4-vFvM7H6qmrX2im8HyydKcUazomRSaniKLHjOmN3Wp_LjFlJd04Xk8w1UciAGPhE90Z-3VhpMym9GZsIg659-wzxRGjln6q)

![img](https://lh3.googleusercontent.com/G-mV6yMKBjHfGSLbcZjUAeBTLtW85WuS605MJLQM6-5ikDRjEc7ktsymBTX9l0Ra1cziPQE0PPlRiFLGoYvdA8BasHoZjLxOi4fpYBT2iN8Aexl_jVbtNeAkZOEJNKxxnq75al5k)

![img](https://lh3.googleusercontent.com/gW2kY0Q3Kkp_RZmA2ixNkRNCMcAAaqn0giS1MdA1kBcERzGO2NJ9wuHNN-Kd-pTFsM6g53ZshwwN46S6R7sBP511Ljzap3i046CEeWsy5PrIP8lq6Zxwc6l_k_V8TBJ0KBpIwHA3)

### Cutout 쉐이더 작성

클립 계산식으로 제외하기.

clip(c.a - 0.7);

![img](https://lh6.googleusercontent.com/jMOEywnlSYpwH-1VP0wjyJC8H50u9qXrgYPWaLCS_twOKOKVTa2fJjCYB-TRIWpBpTqsXNV8ej6foFlceNoeKbv6BSD_vf1pUbD3Hpi-RFXiWWnLNk-tLXSGdjqcP28GGW27AbPn)

![img](https://lh4.googleusercontent.com/CjMtSqDcqWyFUrHIKVIUMHqzaiQp5GmkIVrsMloLVNEVqGwvWdprk2MdJ2x86IdQGK-e-23n9qi7EWLbH1IcLW2dZ7utoTeHkyFsa_fe4GI-gvya04FQSo_SecB-J6CFAN0NZJ94)

![img](https://lh5.googleusercontent.com/b60HuxD9GKFGD_I8gpSyza_UuDWVGg489plHytPd7BOvADDinV_3jesUnc8UpVh1BzYRmlG4tR3uspgYomre1TrXZ49qId8Nwa0yEXkEBuQk0Y2A3mnCGu2VlgGvXKU_xiVGEGOH)

```c++
Shader "Custom/Test" {

	Properties {

		_Color ("Color", Color) = (1,1,1,1)

		_MainTex ("Albedo (RGB)", 2D) = "white" {}

_Cutoff("Base Alpha cutoff", Range(0, 1)) = 0.5

		_Glossiness ("Smoothness", Range(0,1)) = 0.5

		_Metallic ("Metallic", Range(0,1)) = 0.0

	}

	SubShader {

		Tags { "RenderType"="TransparentCutout" "Queue" = "AlphaTest" }

		LOD 200

		CGPROGRAM

		// Physically based Standard lighting model, and enable shadows on all light types

		#pragma surface surf Standard fullforwardshadows alphatest:_Cutoff addshadow//잘린 그림자가 필요할 때.

		// Use shader model 3.0 target, to get nicer looking lighting

		#pragma target 3.0

		sampler2D _MainTex;

		struct Input {

			float2 uv_MainTex;

		};

		half _Glossiness;

		half _Metallic;

		fixed4 _Color;

		// Add instancing support for this shader. You need to check 'Enable Instancing' on materials that use the shader.

		// See https://docs.unity3d.com/Manual/GPUInstancing.html for more information about instancing.

		// #pragma instancing_options assumeuniformscaling

		UNITY_INSTANCING_BUFFER_START(Props)

			// put more per-instance properties here

		UNITY_INSTANCING_BUFFER_END(Props)

		void surf (Input IN, inout SurfaceOutputStandard o) {

			// Albedo comes from a texture tinted by color

			fixed4 c = tex2D (_MainTex, IN.uv_MainTex) * _Color;

			o.Albedo = c.rgb;

			// Metallic and smoothness come from slider variables

			o.Metallic = _Metallic;

			o.Smoothness = _Glossiness;

			o.Alpha = c.a;

		}

		ENDCG

	}

	FallBack "Legacy Shaders/Transparent/Cutout/VertexLit"

}
```



------



### 쉐도우 제거 하기 (그림자 제거하기)

FallBack "Legercy Shaders/Transparent/VertexLit"



------



### Surface Shader XRay효과

![img](https://lh6.googleusercontent.com/3Co_wcvwTOhlUtKm8Sclg6TVvuqRkXUe5t21lXzWbL-HCWo0qBNQSzP_sBLuxf0I6tRYb5k8VoQzTyrh6Ep-3-Qa12OdUb-e-0Mx_M1tkbeMhw_5tJ7y05joJz6gV1sxKKNZENSJ)

![img](https://lh3.googleusercontent.com/gZNHYmITkjRBQ1SIOxJTXjeC3Zroyx0ecVDYainTb53p0Ohq7Dm6xwYy27caOeJPRZ0YKZ2i1PpFICp23f_mXdxKWeVWSbWag12I_3QFaCjYhMahxcQglIlDhnbRq75Ui1eth20n)

주의사항 : “Queue”는 ALphaTest여야 함.

XRay처리할 쉐이더를 위쪽으로 작성해야 함.

정상 렌더링을 해야할 쉐이더는 아래쪽에 작성 해야 함.



------



### 화면 찍어내는 쉐이더. GrabPass

조건 : 

Tags 렌더링 타입 확인

Subshader 바로 아래에 GrabPass{} 확인

\#pragma surface alpha : fade 확인

sampler2D _GrabTexture;



------



### 모든 옵션 끄기

noshadow  noambient novertexlights nolightmap nodynlightmap nodirlightmap nofog nometa noforwardadd nolppv noshadowmask halfasview interpolateview exclud_path:deferred exclud_path:forward exclud_path:prepass

exclud_path:deferred exclud_path:forward exclud_path:prepass : 작성된 렌더링 패스를 제거합니다. 차례대로 디퍼드 셰이딩, 포워드 패스, 레거시 디퍼드 패스 (제거하고 싶은 패스를 적으면 됨.)

noshadow : 모든 그림자 받기를 비활성화 합니다. (shadow Receiving)

noambient : 엠비언트 라이팅 또는 라이트 프로브를 적용하지 않습니다.

novertexLights : Forward 렌더링에서 라이트 프로브 또는 버텍스 라이트를 적용하지 않습니다.

nolightmap : 실시간 동적 전역 조명 지원을 비활성화 합니다.

nodirlightmap : 디렉셔널 라이트맵 지원을 비활성화 합니다.

nofog : 유니티 내장 포그 기능을 지원하지 않습니다.

nometa : 메타 패스를 만들지 않습니다. (이 패스는 라이트맵 및 동적 전역 조명을 위해 표면 정보를 추출하는 패스입니다.)

noforwardadd :  포워드 렌더링 추가 패스를 비활성화 합니다. 그러면 쉐이더는 디렉셔널 라이트 하나만 지원하고, 다른 모든 라이트는 정점당/SH 계산됩니다. 쉐이더도 더 작아집니다.

![img](https://lh6.googleusercontent.com/6EGWC8NsxXJz7fqfz8nUWJvrqe9oluDc01MepMrKkGZQDJIIgDpSkVzQmsiMrLBZdcox_K8TxUsHDPaPNZBqVJvYjQJuTZl7ZUH1BMqznQEXuq0OSRLAY0g_PTxrmY1M5NoJWpdN)



------



렌더링 타입 태그

- Opaque  : 대부분의 쉐이더 (Normal](shader-NormalFamily.html), [Self Illuminated](https://docs.unity3d.com/kr/530/Manual/shader-SelfIllumFamily.html), [Reflective](https://docs.unity3d.com/kr/530/Manual/shader-ReflectiveFamily.html), Terrain 쉐이더).
- Transparent  : 대부분의 알파 블렌딩 쉐이더에서 사용 (([Transparent](https://docs.unity3d.com/kr/530/Manual/shader-TransparentFamily.html), 파티클, 글꼴, Terrain 추가 패스 쉐이더).
- TransparentCutout  : 알파 테스트 쉐이딩에서 사용. 마스킹 된 투명 쉐이더([Transparent Cutout](https://docs.unity3d.com/kr/530/Manual/shader-TransparentCutoutFamily.html), 2 패스 식물 쉐이더).
- Background  : Skybox 쉐이더.
- Overlay  : GUITexture, 후광(Halo), 플레어 쉐이더(Flare shaders).
- TreeOpaque  : Terrain 엔진 나무 껍질.
- TreeTransparentCutout  : Terrain 엔진 나뭇잎.
- TreeBillboard  : Terrain 엔진 빌보드 Tree.
- Grass : terrain 엔진의 grass.
- GrassBillboard  : Terrain 엔진 빌보드 Grass.

### 

### 렌더큐 태그 (ShaderLab: SubShader Tags)

서브 쉐이더는 태그를 사용하여 렌더링 엔진에 렌더링 할 방법과시기를 알려줍니다.

Syntax

Tags { "TagName1" = "Value1" "TagName2" = "Value2" }

TagName1에 Value1, TagName2에 Value2를 지정합니다. 원하는만큼 태그를 추가 할 수 있습니다.

세부

태그는 기본적으로 키 - 값 쌍입니다. SubShader 태그 안에는 렌더링 순서와 하위 셰이더의 다른 매개 변수를 결정하는 데 사용되는 태그가 있습니다. Unity가 인식하는 다음 태그는 Pass가 아닌 SubShader 섹션 안에 있어야합니다!

Unity가 인식하는 내장 태그 이외에, 자신의 태그를 사용하고 Material.GetTag 함수를 사용하여 태그를 쿼리 할 수 있습니다.

렌더링 순서 - 대기열 태그

Queue 태그를 사용하여 객체가 그려지는 순서를 결정할 수 있습니다. Shader는 객체가 속해있는 렌더링 대기열을 결정합니다. 이렇게하면 모든 투명한 셰이더가 모든 불투명 객체 뒤에 그려지는지 확인합니다.

사전 정의 된 렌더링 대기열은 4 개이지만 미리 정의 된 대기열 사이에 더 많은 대기열이있을 수 있습니다. 미리 정의 된 대기열은 다음과 같습니다.

Background -이 렌더링 대기열은 다른 것보다 먼저 렌더링됩니다. 일반적으로 배경에 있어야하는 것들을 위해 이것을 사용합니다.

Geometry (기본값) - 대부분의 객체에 사용됩니다. 불투명 기하학은이 대기열을 사용합니다.

AlphaTest  된 지오메트리는이 대기열을 사용합니다. 기하학 객체와 별도의 대기열입니다. 왜냐하면 모든 단색 객체가 그려진 후에 알파 테스트 객체를 렌더링하는 것이 더 효율적이기 때문입니다.

Transparent -이 렌더링 대기열은 기하학 및 AlphaTest 다음으로 앞뒤 순서로 렌더링됩니다. 알파 블렌딩 된 것 (깊이 버퍼에 쓰지 않는 셰이더)은 여기에 있어야합니다 (glass, particle effects).

Overlay  - 이 렌더링 대기열은 오버레이 효과를위한 것입니다. 마지막으로 렌더링 된 것은 모두 여기에 있어야합니다 (예 : 렌즈 플레어).

Shader "투명한 대기열 예제"

{

​     하위 쉐이더

​     {

​        태그 { "Queue"= "Transparent"}

​        패스

​        {

​            // 나머지 셰이더 바디 ...

​        }

​    }

}

투명 큐에서 무언가를 렌더링하는 방법을 보여주는 예제

특수한 중간 사용 대기열을 사용할 수 있습니다. 내부적으로 각 큐는 정수 인덱스로 표시됩니다. Background 은 1000, Geometry은 2000, AlphaTest는 2450, Transparent 은 3000, Overlay 는 4000입니다. 셰이더가 다음과 같은 큐를 사용하는 경우 :

태그 { "Queue"= "Geometry + 1"}

이렇게하면 모든 불투명 한 객체 뒤에 객체가 렌더링되지만 투명한 객체 앞에는 렌더링 대기열 인덱스가 2001 (형상 +1)이됩니다. 이 기능은 일부 개체가 다른 개체 집합간에 항상 그려지도록하려는 경우에 유용합니다. 예를 들어, 대부분의 경우 투명한 물은 불투명 한 물체 뒤에 투명한 물체 앞에 그려야합니다.

2500까지의 대기열 ( "기하 +500")은 "불투명"으로 간주되어 최상의 성능을 위해 객체의 그리기 순서를 최적화합니다. 더 높은 렌더링 대기열은 "투명한 오브젝트"로 간주되어 먼 거리에서 렌더링을 시작하고 가장 가까운 것에서 끝나는 오브젝트를 거리별로 정렬합니다. 스카이 박스는 모든 불투명 한 객체와 모든 투명한 객체 사이에 그려집니다.

RenderType 태그

RenderType 태그는 셰이더를 미리 정의 된 여러 그룹으로 분류합니다. Is는 불투명 한 셰이더 또는 알파 테스트를받은 셰이더 등입니다. 셰이더 대체 (Shader Replacement) 및 경우에 따라 카메라의 심도 텍스처를 생성하는 데 사용됩니다.

DisableBatching 태그

일부 셰이더 (주로 오브젝트 공간의 정점 변형을하는 셰이더)는 호출 일괄 처리를 사용할 때 작동하지 않습니다. 이는 일괄 처리가 모든 지오메트리를 월드 공간으로 변환하여 "오브젝트 공간"이 손실되기 때문입니다.

DisableBatching 태그를 사용하여이를 활성화 할 수 있습니다. "True"(이 셰이더의 배치를 항상 비활성화 함), "False"(배치를 비활성화하지 않음, 기본값 임) 및 "LODFading"(LOD 페이드가 활성화 된 경우 일괄 처리 사용 안 함, 주로 나무에서 사용됨)입니다.

ForceNoShadowCasting 태그

ForceNoShadowCasting 태그가 주어지고 값이 "True"이면이 하위 셰이더를 사용하여 렌더링 된 객체는 결코 그림자를 투영하지 않습니다. 이는 투명한 객체에서 셰이더 대체를 사용하고 있고 다른 하위 셰이더에서 섀도우 패스를 상속하지 않을 때 주로 유용합니다.

IgnoreProjector 태그

IgnoreProjector 태그가 지정되고 값이 "True"이면이 쉐이더를 사용하는 객체는 프로젝터의 영향을받지 않습니다. 영사기가 영향을 미칠 수있는 좋은 방법이 없기 때문에 이것은 대부분 반투명의 객체에 유용합니다.

CanUseSpriteAtlas 태그

셰이더가 스프라이트를위한 것이라면 CanUseSpriteAtlas 태그를 "False"로 설정하고, 아트 래스터에 채워질 때 작동하지 않게됩니다 (Sprite Packer 참조).

PreviewType 태그

PreviewType은 머티리얼 인스펙터 미리보기에서 머티리얼을 표시하는 방법을 나타냅니다. 기본적으로 재질은 구체로 표시되지만 PreviewType은 "평면"(2D로 표시됨) 또는 "Skybox"(스카이 박스로 표시됨)로 설정할 수도 있습니다.

“IgnoreProjector” = “True”

유니티 내장 프로젝터에 반응하지 않도록 한다. (동전 그림자 만들 때(?) 자주 사용됨.)



------



### 그랩패스 쉐이더, 그랩 텍스처

Shader "Custom/JinhoBlurTest" {

​	Properties {

​		_Color ("Color", Color) = (1,1,1,1)

​		_MainTex ("Albedo (RGB)", 2D) = "white" {}

​	}

​	SubShader {

​		Tags { "RenderType" = "Transparent"  "Queue" = "Transparent" }

​		

​		GrabPass{}

​		//화면을 찍어냄

​		CGPROGRAM

​		// Physically based Standard lighting model, and enable shadows on all light types

​		#pragma surface surf Lambert alpha : fade noshadow  noambient novertexlights nolightmap nodynlightmap nodirlightmap nofog nometa noforwardadd nolppv noshadowmask 

​		// Use shader model 3.0 target, to get nicer looking lighting

​		#pragma target 2.0

​		sampler2D _MainTex;

​		sampler2D _GrabTexture;

​		struct Input {

​			fixed2 uv_MainTex;

​			float4 screenPos;

​		};

​		fixed4 _Color;

​		// Add instancing support for this shader. You need to check 'Enable Instancing' on materials that use the shader.

​		// See https://docs.unity3d.com/Manual/GPUInstancing.html for more information about instancing.

​		// #pragma instancing_options assumeuniformscaling

​		UNITY_INSTANCING_CBUFFER_START(Props)

​			// put more per-instance properties here

​		UNITY_INSTANCING_CBUFFER_END

​		void surf (Input IN, inout SurfaceOutput o) {

​			// Albedo comes from a texture tinted by color

​			fixed4 c = tex2D (_MainTex, IN.uv_MainTex) * _Color;

​			//o.Albedo = c.rgb;

​			// Metallic and smoothness come from slider variables

​			float3 screenUV = IN.screenPos.rgb / IN.screenPos.a;

​			o.Emission = tex2D(_GrabTexture, screenUV.xy);

​			o.Alpha = c.a;

​		}

​		ENDCG

​	}

​	FallBack "Diffuse"

}

# 

### 모바일 쉐이더

/// 림라이트 컬러 적용하다가 말았음.

Shader "Jinho/MoblieShaderTest" {

​	Properties {

​		_Color ("Color", Color) = (1,1,1,1)

​		_MainTex ("Albedo (RGB)Smoothness(A)", 2D) = "white" {}

​		_NormalMap("Normal", 2D) = "bump"{}

​		[HDR]_SpecColor("SpecColor", Color) = (0,0,0,0)

​		_SpecPower("SpecPower", Range(0, 500)) = 1

​		[HDR]_RimLightColor("RimLightColor", Color) = (0,0,0,0)

​		_RimPower("RimPower", Range(0, 1)) = 1

​		_ReflectionMask("EmissionColor(RGB)ReflectionMask(A)", 2D) = "white" {}

​		_Reflection("Reflection Cube Map", Cube) = ""{}

​		_ReflextionPower("ReflextionPower", Range(0, 10)) = 1

​		[HDR]_EmissionColor("EmissionColor", Color) = (0,0,0,0)

​		_EmissionPower("_EmissionPower", Range(0, 10)) = 1

​	}

​	SubShader {

​		Tags { "RenderType"="Opaque" }

​		LOD 200

​		

​		CGPROGRAM

​		// Physically based Standard lighting model, and enable shadows on all light types

​		#pragma surface surf Lambert noambient novertexlights nolightmap nodynlightmap nodirlightmap nofog nometa noforwardadd nolppv noshadowmask 

​		// Use shader model 3.0 target, to get nicer looking lighting

​		#pragma target 2.0

​		sampler2D _MainTex;

​		sampler2D _NormalMap;

​		sampler2D _ReflectionMask;

​		uniform samplerCUBE _Reflection; // 큐브맵 불러오는 정보

​		struct Input {

​			fixed2 uv_MainTex;

​			fixed2 uv_NormalMap;

​			fixed3 viewDir; //카메라 방향

​			fixed3 _SpecColor; // 스펙큘러 컬러

​			fixed3 _ReflectionMask;

​		};

​		fixed4 _Color; //기본 컬러		

​		fixed _SpecPower; // 스펙큘러 넓이

​		fixed _RimPower; // 림라이트 넓이

​		fixed3 _RimLightColor; // 림라이트 컬러

​		fixed3 _EmissionColor; //에미션 컬러

​		fixed _EmissionPower; //에미션 파워

​		fixed _ReflextionPower; //리플렉션 파워

​		// Add instancing support for this shader. You need to check 'Enable Instancing' on materials that use the shader.

​		// See https://docs.unity3d.com/Manual/GPUInstancing.html for more information about instancing.

​		// #pragma instancing_options assumeuniformscaling

​		UNITY_INSTANCING_CBUFFER_START(Props)

​			// put more per-instance properties here

​		UNITY_INSTANCING_CBUFFER_END

​		void surf (Input IN, inout SurfaceOutput o) {

​			// Albedo comes from a texture tinted by color

​			fixed4 c = tex2D (_MainTex, IN.uv_MainTex) * _Color; // 디퓨즈 컬러 계산식

​			o.Normal = UnpackNormal(tex2D(_NormalMap, IN.uv_NormalMap)); // 노멀맵 계산

​			fixed3 e = texCUBE(_Reflection , IN.viewDir + o.Normal); // 큐브맵 반사시키는 계산

​			fixed3 eMul = e.rgb * _ReflextionPower; //큐브맵 반사 강도

​			fixed4 h = tex2D(_ReflectionMask, IN.uv_MainTex); // 반사 마스크 컬러

​			fixed3 d = dot(IN.viewDir, o.Normal); //카메라, 노멀내적

​			fixed3 f = pow(d.rgb, _SpecPower) * _SpecColor.rgb; //스펙큘러 카메라 정면 

​			fixed3 g = (1 - pow(d.rgb, _RimPower)) * _RimLightColor; // 림라이트 강도

​			fixed3 i = h.rgb * _EmissionColor.rgb * _EmissionPower; //에미시브 컬러 및 파워

​			o.Albedo = c.rgb;

​			//o.Emission = (f.rgb * c.a + (eMul * h.a)) * _LightColor0 + i.rgb + g.rgb;												//use Albedo_Pc Defferd

​			//o.Emission = (c.rgb * 0.3 + f.rgb * c.a + (eMul * h.a)) * _LightColor0 + i.rgb + g.rgb;								//use Albedo_Mobile forward //디렉셔널 라이팅에 영향을 받음.

​			o.Emission = (c.rgb * 0.3 + f.rgb * c.a + (eMul * h.a)) + i.rgb + g.rgb;												//Use Albedo_Mobile forward //디렉셔널 라이팅에 약간만 영향받음

​			//o.Emission = ( f.rgb * c.a + (e.rgb * (1 - (c.rgb * 0.8)) * h.a)) * _LightColor0 + i.rgb + g.rgb;

​			//o.Emission = (c.rgb + f.rgb * c.a + (e.rgb * h.a)) * _LightColor0 + i.rgb + g.rgb;  //No Albedo Shader

​			

​		}

​		ENDCG

​	}

​	FallBack "Diffuse"

}

///////////////////////////////////////////////////////////

/////////////////////////// 아무것도 계산없이 빨간색만 출력하는 쉐이더.

Shader "Custom/SceneDistortinoSHader" {

​	Properties {

​		_Color ("Color", Color) = (1,1,1,1)

​		_MainTex ("Albedo (RGB)", 2D) = "white" {}

​		_Glossiness ("Smoothness", Range(0,1)) = 0.5

​		_Metallic ("Metallic", Range(0,1)) = 0.0

​	}

​	SubShader {

​		Tags { "RenderType"="Opaque" }

​		LOD 200

​		

​		CGPROGRAM

​		// Physically based Standard lighting model, and enable shadows on all light types

​		#pragma surface surf nolight noambient

​		// Use shader model 3.0 target, to get nicer looking lighting

​		#pragma target 3.0

​		struct Input {

​			float4 color:COLOR;

​		};

​		// Add instancing support for this shader. You need to check 'Enable Instancing' on materials that use the shader.

​		// See https://docs.unity3d.com/Manual/GPUInstancing.html for more information about instancing.

​		// #pragma instancing_options assumeuniformscaling

​		UNITY_INSTANCING_CBUFFER_START(Props)

​			// put more per-instance properties here

​		UNITY_INSTANCING_CBUFFER_END

​		void surf (Input IN, inout SurfaceOutput o) {

​		}

​		float4 Lightingnolight(SurfaceOutput s, float3 lightDir, float atten) {

​			return float4(1, 0, 0, 1);

​		}

​		ENDCG

​	}

​	FallBack "LegarcyShader/Transparent/Vertexlit"

}



------



### 순수하게 씬을 그리는 디스토션만 하는 쉐이더

Shader "Custom/SceneDistortinoSHader" {

​	Properties {

​		_MainTex("Albedo (RGB)", 2D) = "white"{}

​		_RefStrength("_RefStrength", Range(0, 10)) = 1

​	}

​		SubShader{

​		Tags { "RenderType" = "Transparent"  "Queue" = "Transparent" }

​		LOD 200

​		zwrite off

​		GrabPass{}

​		//화면을 캡쳐한다.

​		CGPROGRAM

​		// Physically based Standard lighting model, and enable shadows on all light types

​		#pragma surface surf nolight noambient alpha : fade

​		// Use shader model 3.0 target, to get nicer looking lighting

​		#pragma target 3.0

​		sampler2D _MainTex;

​		sampler2D _GrabTexture;

​		//화면을 캡쳐하고 있는 텍스처 데이터

​		float _RefStrength;

​		struct Input {

​			float2 uv_MainTex;

​			float4 color:COLOR;

​			float4 screenPos; //화면 좌표계

​		};

​		// Add instancing support for this shader. You need to check 'Enable Instancing' on materials that use the shader.

​		// See https://docs.unity3d.com/Manual/GPUInstancing.html for more information about instancing.

​		// #pragma instancing_options assumeuniformscaling

​		UNITY_INSTANCING_CBUFFER_START(Props)

​			// put more per-instance properties here

​		UNITY_INSTANCING_CBUFFER_END

​		void surf (Input IN, inout SurfaceOutput o) {

​			float4 ref = tex2D(_MainTex, IN.uv_MainTex);

​			float3 screenUV = IN.screenPos.rgb / IN.screenPos.a; //어느 방향에서 봐도 같은 uv값으로 출력

​			o.Emission = tex2D(_GrabTexture, screenUV.xy + ref.x * _RefStrength);

​		

​		}

​		float4 Lightingnolight(SurfaceOutput s, float3 lightDir, float atten) {

​			return float4(0, 0, 0, 1);

​		}

​		ENDCG

​	}

​	FallBack "LegacyShader/Transparent/Vertexlit"

}

# 용어 정리

### UnityObjectToClipPos(IN.vertex);

유니티 내부의 공간 매트릭스를 공간에 할당한다.  "mul(UNITY_MATRIX_MVP, IN.vertex)" 와 같은 의미

### v2f

Vertex Shader to Fragment Shader Structure

### MVP

Model View Projection Matrix

![img](https://lh5.googleusercontent.com/aIi2W2MTNbNdv8t_IcuUxZvuyAq_q6rlU-wQunZwhjI42uE6kNUwNGDFxt4O_Xk0ckAWOWfTPFgpo3IZAyJfuYaFo-sv0QTYNQmPUuu5zBC-HFQhCYMJImEWC5I6pS0WR7seYzSo)

### SV

### System-Value (시스템 값)

### SV_Position

| SV_Position | SVPosition이 셰이더에 대한 입력으로 선언되면 linearNoPerspective 또는 linearNoPerspectiveCentroid의 두 가지 보간 모드 중 하나를 지정할 수 있습니다.이 모드에서는 멀티 샘플 앤티 앨리어싱을 수행 할 때 중심점 스냅 된 xyzw 값을 제공합니다. 셰이더에서 사용되는 경우 SV_Position은 픽셀 위치를 설명합니다. 모든 셰이더에서 사용 가능하여 0.5 오프셋의 픽셀 중심을 얻습니다. |
| ----------- | ------------------------------------------------------------ |
|             |                                                              |



------



\#pragma

\#pragma는 컴파일러 제조회사에서 컴파일러의 기능을 확장시킬 수 있도록 하는 지시자이다. 표준 컴파일러에 자신의 컴파일러 제작 기술이 허락하는 대로 최대한의 기능을 제공할 수 있도록 여지를 남겨놓은 것이다. 만약 다른 컴파일러에서 해석할 수 없는 pragma directive를 만나면 그냥 무시함으로써 소스간 호환성 문제도 해결하고 있다.

\1. #pragma once

컴파일러에게 해당 헤더 파일이 한번만 빌드되도록 알려주는 명령어이다.

 

\2. #pragma comment()

\#pragma comment()는 여러가지 명령어로 사용되는데 가장 대표적으로

| 1    | #pragma comment(lib, "*.lib") |
| ---- | ----------------------------- |
|      |                               |

을 많이 사용한다. 이 명령어는 해당 라이브러리를 링크시켜주는 기능을 한다.

 

eg) 아래 명령어는 프로젝트 설정에서 라이브러리를 링크하는 대신에 소스코드를 통해 cv.lib을 링크할 수 있도록 해준다.

| 1    | #pragma comment(lib, "cv.lib") |
| ---- | ------------------------------ |
|      |                                |

 

\3. #pragma warning

해당 지시자가 나타난 순간부터 특정 경고 메시지를 무시하는 명령어이다.

| 1    | #pragma warning(disable:4176) |
| ---- | ----------------------------- |
|      |                               |

MS컴파일러에서 경고 메시지는 자신의 고유번호를 갖고 있다.

소스파일에 적어놓으면 이 지시자가 나타난 순간부터 4176관련 경고 메시지를 출력하지 못하게한다.

 

\#ifndef와 #pragma once의 비교

\#ifndef 는 macro wrapper방식을 이용하여 include의 중복을 막을 때 사용한다. 매크로 처리기를 통해 특정 매크로가 선언되어 있으면 조건이 참이 아니므로 #endif 까지의 코드가 무효화된다.

| 12345 | userClass.h#ifndef _USERCLASS_H_#define _USERCLASS_H_....(userClass 선언)....#endif |
| ----- | ------------------------------------------------------------ |
|       |                                                              |

 

\#ifndef는 전처리기가 파일을 계속 읽어들여 해당 헤더파일을 발견할 때마다 계속 읽는다. 모든 컴파일러에서 동작을 하지만 매번 헤더 파일을 열어서 define여부를 확인 해야 하기 때문에 느린 면이 있다.

\#pragma once 의 경우 컴파일러 전처리기 지시자로 한번 인식한 후 다음부터 같은 파일의 경우 파일을 읽기조차 하지 않는다 . 시간이 단축된다는 장점이 있지만, 특정 컴파일러에서만 동작을 한다. (Visual C++ 5.0 이상에서만 동작을 한다.)

구형 컴파일러에서도 동작하고 좀 더 범용적인 소스를 작성해야 하는 경우라면 #ifndef..#define 방식을 사용하고, 그 외의 경우에는 #pragma once를 사용하는 것을 추천한다.



------



# 외부 쉐이더 샘플

### 잔디 움직임 쉐이더

![img](https://lh3.googleusercontent.com/C1yJUJEjlP93r7rvgKjBBCW48oKzB2oj_DdhQxmzDGWsy9P1ksoc2gFS1UkogHWP2lss5ZHXT-fk5bbe7Ax4QoNsqub8CSsSx3H9yGjH4W3auJWI2KhMAwcJeBX2er9LH46HYm7i)

###  포워드 렌더링에서 Emissive컬러만 가져오기

<https://forum.unity.com/threads/bloom-only-emissive-surfaces-in-forward-renderer.408645/>

### 토글 이름 정의하기

Shader "Custom/Example"
{
    Properties
    {
        [Toggle(RED)] _Invert("Red ?" , Float) = 0
    }

    SubShader
    {
        CGINCLUDE
        #include "UnityCG.cginc"

        fixed4 frag(v2f_img i) : SV_Target
        {
            fixed4 col = fixed4(1, 1, 1, 1);
            #ifdef RED
            col.y = 0;
            col.z = 0;
            #endif
            return col;
        }
        ENDCG

        Pass
        {
            CGPROGRAM
            #pragma vertex vert_img
            #pragma fragment frag
            #pragma multi_compile _ RED
            ENDCG
        }
    }
}



------



### 랜덤 타일링 마스크

![img](https://lh5.googleusercontent.com/bpuihq8svcgfN08BBadkVEcn6F5uau6V5vVmSohSMe-wtzqVCXWJRQyQkbTd78iGlpTl7iaAb5Vzs7IkhqKYf9CZN4VpehGjrctWYL0z5EvC8CBKVIKEtot5uec7hyYu26ZV23UN)

1. Shader "Custom/Test2" {
2. ​    Properties {
3. ​        _Tex1 ("Texture 1", 2D) = "white" {}
4. ​        _Mask ("Mask", 2D) = "white" {}
5. ​    }
6. ​    SubShader {
7. ​        Tags { "RenderType"="Opaque" }
8. ​        LOD 200
9. ​     
10. ​        CGPROGRAM
11. ​        \#pragma surface surf Lambert
12.  
13. ​        sampler2D _Tex1, _Mask;
14. ​       
15. ​        struct Input {
16. ​            float2 uv_Tex1;
17. ​            float2 uv_Mask;
18. ​        };
19.  
20. ​        void surf (Input IN, inout SurfaceOutput o) {
21. ​         
22. ​            half4 mask = tex2D(_Mask, IN.uv_Mask * 0.5);    
23. ​            half4 outTex;
24.  
25. ​            float2 uvTexRot = IN.uv_Tex1 - 0.5;
26.  
27. ​            if ( mask.r <= 0.3 ) {
28. ​                //rotated 90 degrees
29. ​                float2x2 rotationMatrix = float2x2(  0,  1, -1,  0); // 90 degrees
30. ​                uvTexRot = mul (uvTexRot, rotationMatrix);
31. ​                uvTexRot.xy += 0.5;
32. ​                outTex = tex2D (_Tex1, uvTexRot);
33. ​            } else if ( mask.r <= 0.6 ) {
34. ​                // rotated 180 degrees
35. ​                float2x2 rotationMatrix = float2x2( -1,  0,  0, -1); // 180 degrees
36. ​                uvTexRot = mul (uvTexRot, rotationMatrix);
37. ​                uvTexRot.xy += 0.5;
38. ​                outTex = tex2D (_Tex1, uvTexRot);
39. ​            } else if ( mask.r <= 0.8 ) {
40. ​                // rotated 270 degrees
41. ​                float2x2 rotationMatrix = float2x2(  0, -1,  1,  0); // 270 degrees
42. ​                uvTexRot = mul (uvTexRot, rotationMatrix);
43. ​                uvTexRot.xy += 0.5;
44. ​                outTex = tex2D (_Tex1, uvTexRot);
45. ​            } else {
46. ​                // rotated 0 degrees
47. ​                outTex = tex2D (_Tex1, IN.uv_Tex1);
48. ​            }
49. ​                     
50. ​            o.Albedo = outTex.rgb;
51. ​            o.Alpha = outTex.a;
52. ​        }
53. ​        ENDCG
54. ​    }
55. ​    FallBack "Diffuse"
56. }



------



### 비 떨어지는 효과

![img](https://lh4.googleusercontent.com/hgaCcMV0h-F3heQgbFLOUJwQ4rF9EpGDPk9wzsv5b6z9BMua3KQs6xShhR9k8Yafe1RZBwwLVb1edhE32DEFioaH8G2JFYNcrMxD45L1ztLX1tt21ZPwaypepE8u_v3BnOeJFepe)

<https://deepspacebanana.github.io/deepspacebanana.github.io/blog/shader/art/unreal%20engine/Rainy-Surface-Shader-Part-1>

유니티 데칼 쉐이더 (이 안에 블룸 들어있으므로 추적해볼 것.)

<https://docs.unity3d.com/Manual/GraphicsCommandBuffers.html>

![img](https://lh5.googleusercontent.com/0hh9h_q1aTS1IKvq9DR5LUpqxxJZ64EjnFdA58-mTOJFRvi--4h1L7kwk8V0CvTWNb0VfMeIryJW52_pu6pPH2O8Oa0UXrL6dvWzcngy85azLhzQcVnmAPupK3IEYwZMpy_VB2S1)

렌더 텍스처 포맷 데이터 

<https://docs.unity3d.com/ScriptReference/RenderTextureFormat.html>

### 버텍스 빨려들어가는 효과

<https://blog.csdn.net/wwlcsdn000/article/details/78895272>



------



### MotionVector

<http://www.klemenlozar.com/frame-blending-with-motion-vectors/>

<https://www.youtube.com/watch?v=zykKhdMUTwg>



------



### Seamless Outline

![img](https://lh6.googleusercontent.com/gA-_CSoghI3P8OaED8D9c6PrERmM7asPB_uLurgJuwE4CpL2NcaIeCBThH1V49trU6YCFKLEk3J36ZbyIrhGE4VtiuGu3Ufcywk9BC1-B4d_HEllM4KmQ9yGJiLQ8_s-aGBtlAH-)

<https://www.youtube.com/watch?v=e4bvwoSGD6k>



------



# 그래픽스 렌더 파이프라인

![img](https://lh6.googleusercontent.com/_1wVnBWflE75cd0FAWhRyQc42jpyUT_9OGasre01SpYrHYSQ9k13pMhiHikH_EWzl_lpqpkFNqY5f0qyV7DN4hOFju1PKorhkq8F8Qmd2MG8AegvUksyrpQkdbZMXpj_mQFgiaHj)



------



# 링크

### 빌트인 쉐이더 헬퍼

<https://docs.unity3d.com/Manual/SL-BuiltinFunctions.html>

### 빌트인 쉐이더 변수

<https://docs.unity3d.com/kr/current/Manual/SL-UnityShaderVariables.html>

### 유니티 Mathf

<https://docs.unity3d.com/kr/530/ScriptReference/Mathf.html>

### HLSL 내장함수

<http://egloos.zum.com/indra207/v/4856054>

### ShaderCod (유니티 내장 쉐이더 설명)

<http://wiki.unity3d.com/index.php?title=Shader_Code>

### 그래픽스 커맨드 버퍼

<https://docs.unity3d.com/kr/530/Manual/GraphicsCommandBuffers.html>

### 카메라 이벤트

<https://docs.unity3d.com/kr/530/ScriptReference/Rendering.CameraEvent.html>

### Dirext Function 라이브러리

<http://developer.download.nvidia.com/CgTutorial/cg_tutorial_appendix_e.html>

### 엔비디아 CG 라이브러리

<http://developer.download.nvidia.com/cg/index_stdlib.html>

### 여러 셰이더 프로그램 배리언트 만들기 (Making Multiple shader program variants)

<https://docs.unity3d.com/kr/current/Manual/SL-MultipleProgramVariants.html>

### 커맨드 버퍼 Bbuffer0~3사용하는 방법

<https://forum.unity.com/threads/solved-cannot-draw-with-the-command-buffers-on-the-background-empty-pixels.445260/>

### SSR문서

![img](https://lh5.googleusercontent.com/PpgH66hfwYh7GLxgo2PVnfWDcK7ja-xo9WRzCeTXM_ktUnnscG7_WIEbZYXqWyRS6c7r8KRxYZ-4IzdLqHk-0bqsqqPcoTSlJrcsRhdHaCn0S_Kz2VboT4GYrLv2slVs3j3HLbSB)

<http://www.kode80.com/blog/2015/03/11/screen-space-reflections-in-unity-5/>

### Material properties and the GI system

<https://docs.unity3d.com/kr/current/Manual/MetaPass.html>

### 흑백 쉐이더 만들기

<http://blog.naver.com/PostView.nhn?blogId=jinwish&logNo=220883717941&parentCategoryNo=&categoryNo=50&viewDate=&isShowPopularPosts=false&from=postView>



------



### RGB => AlphaTest 쉐이더

![img](https://lh6.googleusercontent.com/2XRxS2Ga4ANYOLhpjS594JyxTtK297MOMx6W90I8cfNwIi4EikDXzTeTAvaI_VlkE2HCCCvhcfH3GLpqxV0kVfziD4MT78w_pkh_BZn0zBX2uH7deSE032D8SNvblPJEJ8m0Q2lU)

<http://blog.naver.com/PostView.nhn?blogId=jinwish&logNo=220912099394&parentCategoryNo=&categoryNo=50&viewDate=&isShowPopularPosts=false&from=postView>

### 유니티 렌더링 튜토리얼

<https://catlikecoding.com/unity/tutorials/>

![img](https://lh5.googleusercontent.com/rSZNIeuP918nY6cqhAxt_67t8KOu8iLhEJv3LKabhYcw9MidIulgogFwMoNa4ogrW6orOJ5RIn3Mi7VrZDWcqohpzrJWJUhH_mzq4DWdPDUpmI9TGFv9akOcPjpA_s8KN4KJ-5Nj)



------



### Unity3D shader 저사양 굴절 표현하기

float3 viewD = viewDirection;

float2 viewDMnormalD = (viewD*normalDirection).xy;

float2 uv_01 = i.uv0;

float2backmove=(uv_01.xy+((1.0 - viewD.xy)*normalize(distance(objPos.xyz,_WorldSpaceCameraPos.xyz)))+(-1.0)+float2(((viewDMnormalD.x*_Distortion)+uv_01.x),((viewDMnormalD.y*_Distortion)+uv_01.y)));

 

<http://blog.naver.com/PostView.nhn?blogId=jinwish&logNo=220980994445&parentCategoryNo=&categoryNo=50&viewDate=&isShowPopularPosts=false&from=postView>

 



------



 

### Unity 후처리 모션블러 효과

 

float4 pix = tex2D(_MainTex, i.uv);

float2 dir = 0.5 - i.uv;

float dist = length(dir);

dir /= dist;

float4 sum = pix;

sum += tex2D(_MainTex, i.uv + dir * -0.08 * _SampleDist);

sum += tex2D(_MainTex, i.uv + dir * -0.05 * _SampleDist);

sum += tex2D(_MainTex, i.uv + dir * -0.03 * _SampleDist);

sum += tex2D(_MainTex, i.uv + dir * -0.02 * _SampleDist);

sum += tex2D(_MainTex, i.uv + dir * -0.01 * _SampleDist);

 

sum *= 1.0 / 6.0;

float t = saturate(dist * _SampleStrength);

pix = lerp(pix, sum, t);

return pix;

 

<http://blog.naver.com/PostView.nhn?blogId=jinwish&logNo=220981034563&parentCategoryNo=&categoryNo=50&viewDate=&isShowPopularPosts=false&from=postView>



------



### 유니티 쉐이더 알고리즘.

![img](https://lh5.googleusercontent.com/zTYmzb7FtVMB_UFy7L2-HD2EgC1c5Mukyo5Lh0PBGbtgavp7KlsXRU3xfnqkAPYHseRQiIWOHWJx3iVsErblmhnjWC4YtmvGDxopzvqQIt1xm0VtKHdV-k-QZ9d6AYCF4VDGuSIM)



------



# 렌더링 관련 이슈

###  

### 주요 셰이더 최적화 7가지

프레임 단위에서는 게임 코드보다 셰이더 코드가 수행하는 작업이 훨씬 더 많습니다. 다음의 최적화를 사용하여 성능/FPS 속도를 쾌적하게 유지할 수 있습니다.

1. 비상수 연산을 최소화하세요. 상수 또는 "dynamic uniforms"(예: x=4/33, x=4xsin(24))를 사용하세요.
2. 스칼라 값(float, int)을 벡터 값(float3, float4)보다 먼저 곱하세요.
3. 알파테스트의 경우를 포함하여 가급적 폐기 명령을 지양하세요(주로 모바일에 적용됨). 오버드로우에 유의하세요.
4. 가능한 한 버텍스 셰이더 내로 계산을 제한하세요.
5. 벡터 작동이 결과의 모든 구성요소를 사용하지 않는 경우, 가능한 한 벡터 작동에 대한 쓰기 마스크를 지정하세요.
6. 동적으로 설정된 값/non-uniforms(if-else, loops)에 기반하여 브랜칭을 수행하지 마세요.
7. 작동(예: discard(), floor() 등)이 렌더러 모델(OpenGL 2, OpenGL 3, OpenGL ES 등)과 하드웨어에 미치는 영향을 확인하세요.



------



### 텍스처 압축시 바이트 배분 순서

A > G > R = B



------



### 선형 렌더링에서 주의할점.

디퓨즈, Emission 컬러와 같이 두루뭉술 하면서 눈으로 보면서 해야 하는 것들은 SRGB를 사용.

(단 SRGB처리 했을 때 알파값은 감마보정으로 유지되기 때문에 후처리를 해줘야 함.)

후처리 계산식 : power(rgb, 1/2.2)??

![img](https://lh3.googleusercontent.com/qow8fEKGOO6mPVOy-rxPJoOwXsuW958r5WSxJq9B40R11iAJbyMNvbEWqip4eHqaa_YSI1ZZn-9Bu9cU13zm-8G_7sGcdsFHKD9arpE89lHzg6PmktWhn6Cg8_-H0xy0P5acZg6f)

툴로 인해서 정확하게 추출해야 하는 것들(노멀, 메탈릭, 스무스니스 등)은 RGB를 사용.

### 엠비언트 컬러 제어하기 

(모바일 최적화 할때 씀.)

fixed4 ambient = UNITY_LIGHTMODEL_AMBIENT;

//엠비언트 컬러를 직접적으로 사용.

<https://docs.unity3d.com/Manual/SL-UnityShaderVariables.html>

(참고링크)

Unity API의 RenderSettings.ambientLight로 Scene에 동적으로 제어가 가능함.

Toggle로 해당 항목한 필요한 상황에 활성화 해 사용할 수 있음.

다만 모든 Scene의 오브젝트가 이에 대한 처리가 되어 있어야 함.

<https://docs.unity3d.com/ScriptReference/RenderSettings-ambientLight.html>

(참고링크)



------



fixed 와 Half의 차이점.

또 플랫폼마다 다르게 동작하는 문제가 있다.

바로 shader에서 float 타입 변수를 선언할 때마다 결정하는 것이 정확도이다.

지금까지는 이걸 굳이 신경 안써도 잘 동작해서, 왜 이런게 존재하나 했었는데. 최근에 이 차이로 인한 문제를 경험했다.

 

Specular와 Overlight를 지원하는 shader를 구현하여 모바일 빌드를 했는데, Android와 iOS의 화면이 다르다.

Android에서는 정상적으로 출력되는데 iOS에서는 하얗게 타서 나오는 것이다.

원인을 찾아보니, spec과 glow를 처리하는 코드에서 fixed 타입 변수를 사용했는데, 이 타입 변수는 정확도 뿐만 아니라 표현할 수 있는 범위도 매우 제한적이어서, 정확한 계산이 안 되는 것이다.

그런데 이 문제는 iOS에서만 발생한다. 즉 각 플랫폼마다 또 동작이 다르다.. (이구~~~)

 

문서를 보면, fixed는 -2 ~ + 2까지만 표현되고, half는 2**-15 ~ 2**+15 까지 표현된다고 한다.

보통 spec과 glow는 큰 값이 들어오므로, 이들의 외부 parameter 선언을 half로 선언하니 문제가 해결되었다.