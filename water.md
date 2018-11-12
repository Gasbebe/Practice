```c++
roperties {
		_Color ("Color", Color) = (1,1,1,1)
		_MainTex ("Albedo (RGB)", 2D) = "white" {}
        _Bumpmap ("BumpMap", 2D) = "bump" {}
        _Cube ("Cube", Cube) = ""{}
        _WaveH ("Wave Height", Range(0, 0.5)) = 0.1
        _WaveT ("WaveTimeing", Range(5, 20)) = 5
        _WaveL ("Wave Length", Range(0, 10)) = 1


        _SPColor ("Spec Color", color) = (1,1,1,1)
        _SPPower ("Spec Power", Range(50, 300)) = 150
        _SPMulti("Spec Multiply", Range(1,10)) = 3
		//_Metallic ("Metallic", Range(0,1)) = 0.0

        _Refract ("Refract Power", Range(0, 0.2)) = 0.1
	}
	SubShader {
		Tags { "RenderType"="Transparent" "Queue" = "Transparent" }      
        GrabPass{}

		CGPROGRAM      
		#pragma surface surf WaterSpecular vertex:vert alpha:fade
		#pragma target 3.0

		sampler2D _MainTex;
        sampler2D _Bumpmap;
        sampler2D _GrabTexture;
        samplerCUBE _Cube;
        float _WaveH;
        float _WaveT;
        float _WaveL;

        float4 _SPColor;
        float _SPPower;
        float _SPMulti;
        float _Refract;

        void vert(inout appdata_full v)
        {
            float movement;
            movement = sin(abs((v.texcoord.x * 2 - 1) * _WaveL) + _Time.y * _WaveT) * _WaveH;
            movement = sin(abs((v.texcoord.y * 2 - 1) * _WaveL) + _Time.y * _WaveT) * _WaveH;
            v.vertex.y += movement/2;
        } 

		struct Input {
			float2 uv_MainTex;
            float2 uv_Bumpmap;
            float3 worldRefl;
            float3 viewDir;
            float4 screenPos;
            INTERNAL_DATA
		};

		half _Glossiness;
		half _Metallic;
		fixed4 _Color;
      
		void surf (Input IN, inout SurfaceOutput o) {
            //
            float3 normal1 = UnpackNormal(tex2D(_Bumpmap, IN.uv_Bumpmap + _Time.x * 0.1));
            float3 normal2 = UnpackNormal(tex2D(_Bumpmap, IN.uv_Bumpmap + _Time.x * 0.1));
            o.Normal = (normal1 + normal2)/2;

            float3 refcolor = texCUBE(_Cube, WorldReflectionVector(IN, o.Normal));

            //
            //float3 screenUV = IN.screenPos.rgb / IN.screenPos.a;
            //float3 refraction = tex2D(_GrabTexture,(screenUV.xy + o.Normal.xy * _Refract));

            //rim term
            float rim = saturate(dot(o.Normal, IN.viewDir));
            rim = pow(1-rim, 1.5);

            o.Emission =  refcolor * rim * _Color + _Color;
            o.Alpha = saturate(rim * 0.5 + 0.2);

		}

        float4 LightingWaterSpecular(SurfaceOutput s, float3 lightDir, float3 viewDir, float atten){

            float3 H = normalize(lightDir + viewDir);
            float3 spec = saturate(dot(H, s.Normal));
            spec = pow(spec, _SPPower);

            float4 finalColor;
            finalColor.rgb = spec * _SPColor.rgb * _SPMulti;
            finalColor.a = s.Alpha + spec;

            return finalColor;

        }
		ENDCG
```

