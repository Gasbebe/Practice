### Test Dissolve

```c++
Shader "Custom/NoiseTest" {
	Properties {
		_Color ("Color", Color) = (1,1,1,1)
		_MainTex ("Albedo (RGB)", 2D) = "white" {}
		_NoiseTex("Noise", 2D) = "white" {}
		_FlowTex("flow Tex", 2D) = "white" {}
		_Glossiness ("Smoothness", Range(0,1)) = 0.5
		_Metallic ("Metallic", Range(0,1)) = 0.0
		_value("value", Range(0,1)) = 0.0

	}
	SubShader {
		Tags { "RenderType"="Opaque" }
		LOD 200

		CGPROGRAM
		
		#pragma surface surf Standard fullforwardshadows alpha:blend

		#pragma target 3.0

		sampler2D _MainTex;
		sampler2D _NoiseTex;
		sampler2D _FlowTex;

		struct Input {
			float2 uv_MainTex;
			float2 uv_NoiseTex;
			float2 uv_FlowTex;
		};
		half _value;
		half _Glossiness;
		half _Metallic;
		fixed4 _Color;

		UNITY_INSTANCING_BUFFER_START(Props)
			// put more per-instance properties here
		UNITY_INSTANCING_BUFFER_END(Props)

		void surf (Input IN, inout SurfaceOutputStandard o) {
			
			fixed4 c = tex2D (_MainTex, IN.uv_MainTex) * _Color;
			fixed4 f = tex2D(_FlowTex, float2(IN.uv_FlowTex.x + _Time.y, IN.uv_FlowTex.y + _Time.x));
			fixed4 n = tex2D(_NoiseTex, IN.uv_NoiseTex + f.xx);
			fixed final = n.r + f.g;
			clip(final - _value);
			o.Albedo = c.rgb;
			o.Metallic = _Metallic;
			o.Smoothness = _Glossiness;
			o.Alpha = c.a;
		}
		ENDCG
	}
	FallBack "Diffuse"
}
```

